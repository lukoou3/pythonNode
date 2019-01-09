## Request objects
Request 部分源码：
```python
# 部分代码
class Request(object_ref):

    def __init__(self, url, callback=None, method='GET', headers=None, body=None, 
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None):

        self._encoding = encoding  # this one has to be set first
        self.method = str(method).upper()
        self._set_url(url)
        self._set_body(body)
        assert isinstance(priority, int), "Request priority not an integer: %r" % priority
        self.priority = priority

        assert callback or not errback, "Cannot use errback without a callback"
        self.callback = callback
        self.errback = errback

        self.cookies = cookies or {}
        self.headers = Headers(headers or {}, encoding=encoding)
        self.dont_filter = dont_filter

        self._meta = dict(meta) if meta else None

    @property
    def meta(self):
        if self._meta is None:
            self._meta = {}
        return self._meta
```

#### Request比较常用的参数：  
* **url（string）**:  
此请求的url
* **callback（callable）**：  
此请求响应的回调函数。如果请求未指定回调，则将使用spider的 parse方法。请注意，如果在处理期间引发异常，则会调用errback回调。
* **method（string）**:   
请求方法，默认为GET方法，可设置为"GET"、"POST"、"PUT"等，且保证字符串大写。
* **headers（dict）**:   
请求头信息。dict值可以是字符串（对于单值标头）或列表（对于多值标头）。如果 None作为值传递，则不会发送HTTP头。
* **cookies（dict或list）**:   
cookies，可以使用使dict和list形式：
    ```python
    #使用dict
    request_with_cookies = Request(url="http://www.example.com",
                                   cookies={'currency': 'USD', 'country': 'UY'})
    #使用列表
    request_with_cookies = Request(url="http://www.example.com",
                                       cookies=[{'name': 'currency',
                                                'value': 'USD',
                                                'domain': 'example.com',
                                                'path': '/currency'}])
    ```
    后一种形式允许定制 cookie的属性domain和path属性。这只有在保存Cookie用于以后的请求时才有用。  
    当某些网站返回Cookie（在响应中）时，这些Cookie会存储在该域的Cookie中，并在将来的请求中再次发送。这是任何常规网络浏览器的典型行为。但是，如果由于某种原因，您想要避免与现有Cookie合并，您可以通过将dont_merge_cookies关键字设置为True 来指示Scrapy如此操作 Request.meta。  
    不合并Cookie的请求示例：  
    ```python
    equest_with_cookies = Request(url="http://www.example.com",
                                   cookies={'currency': 'USD', 'country': 'UY'},
                                   meta={'dont_merge_cookies': True})
    ```
    有关详细信息，请参阅[CookiesMiddleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#cookies-mw "CookiesMiddleware")  。

* **meta（dict）**:  
比较常用，在不同的请求之间传递数据使用的，字典dict型。the initial values for the Request.meta attribute. If given, the dict passed in this parameter will be shallow copied.
* **encoding（string）**:  
使用默认的'utf-8'就行。
* **dont_filter（boolean）**:  
表明该请求不由调度器过滤，默认为False。小心使用它，也许你会进入爬行循环。
* **errback（callable）**:  
指定错误处理函数, 这包括404 HTTP错误等失败的页面。

#### Request.meta
Request.meata在不同请求之间传递数据使用的。  
Request.meta属性可以包含任意的数据，但是Scrapy和它的内置扩展可以识别一些特殊的键。  
* **dont_rediect**:不重定向
* dont_retry:不重试
* handle_httpstatus_list
* **dont_merge_cookies**:不合并cookie
* cookiejar:使用cookiejar
* rediect_urls:重定向连接
* bindaddress：绑定ip地址
* dont_obey_robotstxt:不遵循反爬虫协议
* **download_timeout**:下载超时
* **download_maxsize**:下载文件最大大小

#### 使用Request.meta在不同请求之间传递数据
```python
def parse_page1(self, response):
    item = MyItem()
    item['main_url'] = response.url
    yield scrapy.Request("http://www.example.com/some_page.html",
                             meta={'item':item}
                             callback=self.parse_page2)

def parse_page2(self, response):
    item = response.meta['item']
    item['other_url'] = response.url
    yield item
```

## Request的子类FormRequest
FormRequest是Request的子类，一般用作表单数据提交,提交post请求，FormRequest通过formdata参数传递post参数 。 
```python
class FormRequest(Request):

    def __init__(self, *args, **kwargs):
        formdata = kwargs.pop('formdata', None)
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        super(FormRequest, self).__init__(*args, **kwargs)

        if formdata:
            items = formdata.items() if isinstance(formdata, dict) else formdata
            querystr = _urlencode(items, self.encoding)
            if self.method == 'POST':
                self.headers.setdefault(b'Content-Type', b'application/x-www-form-urlencoded')
                self._set_body(querystr)
            else:
                self._set_url(self.url + ('&' if '?' in self.url else '?') + querystr)

    @classmethod
    def from_response(cls, response, formname=None, formid=None, formnumber=0, formdata=None,
                      clickdata=None, dont_click=False, formxpath=None, formcss=None, **kwargs):

        kwargs.setdefault('encoding', response.encoding)

        if formcss is not None:
            from parsel.csstranslator import HTMLTranslator
            formxpath = HTMLTranslator().css_to_xpath(formcss)

        form = _get_form(response, formname, formid, formnumber, formxpath)
        formdata = _get_inputs(form, formdata, dont_click, clickdata, response)
        url = _get_form_url(form, kwargs.pop('url', None))
        method = kwargs.pop('method', form.method)
        return cls(url=url, method=method, formdata=formdata, **kwargs)
```
**FormRequest与Request相比多了一个formdata构造参数和一个from_response类方法**
#### from_response类方法
从一个response返回一个新FormRequest对象，其表单字段值预先填充在响应中form中的元素的值。  
该策略是在任何可查看的表单控件上默认自动模拟点击，如a 。即使这是相当方便，并且经常想要的行为，有时它可能导致难以调试的问题。  
```python
def from_response(cls, response, formname=None, formid=None, formnumber=0, formdata=None,clickdata=None, dont_click=False, formxpath=None, formcss=None, **kwargs)
```

* response:是指包含HTML表单的Response对象，该表单将用于预填充表单字段。
* formname:如果给定，将使用form表单的name属性为该值的name属性的表单。
* formid:如果给定，将使用form表单的id属性为该值的name属性的表单
* formnumber:当响应包含多个表单时，要使用的表单的数量。 formnumber默认是0，表示使用第一个。
* formdata:字段来覆盖表单数据。如果一个字段已经存在于响应<form>元素中，那么它的值被在这个参数中传递的值覆盖。
* formxpath：如果给定，将使用与XPath匹配的第一个表单。
* clickdata:查找单击控件的属性。如果没有给出，表单数据将被提交模拟点击第一个可点击的元素。
* dont_click:如果为True，表单数据将被提交而不需要单击任何元素。
* 此类方法的其他参数将直接传递给 FormRequest构造函数。

#### FormRequest事例
###### 使用FormRequest通过HTTP POST发送数据 
可以使用 yield scrapy.FormRequest(url, formdata, callback)方法发送POST请求。  
如果希望程序执行一开始就发送POST请求，可以重写Spider类的start_requests(self) 方法，并且不再调用start_urls里的url。
```python
class mySpider(scrapy.Spider):
    # start_urls = ["http://www.example.com/"]
 
    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
 
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url = url,
            formdata = {"email" : "xxx", "password" : "xxxxx"},
            callback = self.parse_page
        )
    def parse_page(self, response):
        # do something
```

###### 使用FormRequest.from_response（）来模拟用户登录
通常网站通过 实现对某些表单字段（如数据或是登录界面中的认证令牌等）的预填充  
使用Scrapy抓取网页时，如果想要预填充或重写像用户名、用户密码这些表单字段， 可以使用 FormRequest.from_response() 方法实现。
```python
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
```

## Response(scrapy.http.response.Response)
Response 部分源码：
```python
# 部分代码
from six.moves.urllib.parse import urljoin

from scrapy.http.request import Request
from scrapy.http.headers import Headers
from scrapy.link import Link
from scrapy.exceptions import NotSupported
class Response(object_ref):

    def __init__(self, url, status=200, headers=None, body=b'', flags=None, request=None):
        self.headers = Headers(headers or {})
        self.status = int(status)
        self._set_body(body)
        self._set_url(url)
        self.request = request
        self.flags = [] if flags is None else list(flags)

    @property
    def meta(self):
        try:
            return self.request.meta
        except AttributeError:
            raise AttributeError(
                "Response.meta not available, this response "
                "is not tied to any request"
            )

    body = property(_get_body, obsolete_setter(_set_body, 'body'))

    def urljoin(self, url):
        """Join this Response's url with a possible relative url to form an
        absolute interpretation of the latter."""
        return urljoin(self.url, url)

    @property
    def text(self):
        """For subclasses of TextResponse, this will return the body
        as text (unicode object in Python 2 and str in Python 3)
        """
        raise AttributeError("Response content isn't text")

    def css(self, *a, **kw):
        """Shortcut method implemented only by responses whose content
        is text (subclasses of TextResponse).
        """
        raise NotSupported("Response content isn't text")

    def xpath(self, *a, **kw):
        """Shortcut method implemented only by responses whose content
        is text (subclasses of TextResponse).
        """
        raise NotSupported("Response content isn't text")

    def follow(self, url, callback=None, method='GET', headers=None, body=None,
               cookies=None, meta=None, encoding='utf-8', priority=0,
               dont_filter=False, errback=None):
        # type: (...) -> Request
        """
        Return a :class:`~.Request` instance to follow a link ``url``.
        It accepts the same arguments as ``Request.__init__`` method,
        but ``url`` can be a relative URL or a ``scrapy.link.Link`` object,
        not only an absolute URL.
        
        :class:`~.TextResponse` provides a :meth:`~.TextResponse.follow` 
        method which supports selectors in addition to absolute/relative URLs
        and Link objects.
        """
        if isinstance(url, Link):
            url = url.url
        url = self.urljoin(url)
        return Request(url, callback,
                       method=method,
                       headers=headers,
                       body=body,
                       cookies=cookies,
                       meta=meta,
                       encoding=encoding,
                       priority=priority,
                       dont_filter=dont_filter,
                       errback=errback)
```
Response Parameters:  
* **url (string)** – the URL of this response
* **status (integer)** – the HTTP status of the response. Defaults to 200.
* headers (dict) – the headers of this response. The dict values can be strings (for single valued headers) or lists (for multi-valued headers).
* **body (bytes)** – the response body. To access the decoded text as str (unicode in Python 2) you can use * response.text from an encoding-aware Response subclass, such as TextResponse.
* flags (list) – is a list containing the initial values for the Response.flags attribute. If given, the list will be shallow copied.
* **request** (Request object) – the initial value of the Response.request attribute. This represents the Request that generated this response.

**`url`**   
``` 
A string containing the URL of the response.
This attribute is read-only. To change the URL of a Response use replace()
```
**`status`**   
``` 
An integer representing the HTTP status of the response. Example: 200, 404.
```
**`headers`**   
``` 
A dictionary-like object which contains the response headers. Values can be accessed using get() to return the first header value with the specified name or getlist() to return all header values with the specified name. For example, this call will give you all cookies in the headers:   
response.headers.getlist('Set-Cookie')
```
**`body`**   
``` 
The body of this Response. Keep in mind that Response.body is always a bytes object. If you want the unicode version use TextResponse.text (only available in TextResponse and subclasses).

This attribute is read-only. To change the body of a Response use replace().
```
**`request`**   
``` 
The Request object that generated this response. This attribute is assigned in the Scrapy engine, after the response and the request have passed through all Downloader Middlewares. In particular, this means that:  
HTTP redirections will cause the original request (to the URL before redirection) to be assigned to the redirected response (with the final URL after redirection).    
Response.request.url doesn’t always equal Response.url    
This attribute is only available in the spider code, and in the Spider Middlewares, but not in Downloader Middlewares (although you have the Request available there by other means) and handlers of the response_downloaded signal.
```
**`meta`**   
``` 
A shortcut to the Request.meta attribute of the Response.request object (ie. self.request.meta).  
Unlike the Response.request attribute, the Response.meta attribute is propagated along redirects and retries, so you will get the original Request.meta sent from your spider.
```
**`flags`**   
```
A list that contains flags for this response. Flags are labels used for tagging Responses. For example: ‘cached’, ‘redirected’, etc. And they’re shown on the string representation of the Response (__str__ method) which is used by the engine for logging.
```
**`urljoin(url)`**   
Constructs an absolute url by combining the Response’s url with a possible relative url.

This is a wrapper over urlparse.urljoin, it’s merely an alias for making this call:

urlparse.urljoin(response.url, url)
**`follow(url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding='utf-8', priority=0, dont_filter=False, errback=None)`**   
``` 
Return a Request instance to follow a link url. It accepts the same arguments as Request.__init__ method, but url can be a relative URL or a scrapy.link.Link object, not only an absolute URL.

TextResponse provides a follow() method which supports selectors in addition to absolute/relative URLs and Link objects.
```

## Response的子类(Response subclasses)
Here is the list of available built-in Response subclasses. You can also subclass the Response class to implement your own functionality.(这里是可用的内置Response子类的列表。您还可以将Response类子类化以实现您自己的功能。)    

#### Response的继承关系
```
Response
    TextResponse
        HtmlResponse
        XmlResponse
```

#### TextResponse
TextResponse在Response基础增加了编码能力    
TextResponse对象除了标准的Response对象外，还支持以下属性和方法：
* **encoding**:  
与此响应编码的字符串。 通过尝试以下机制来解决编码问题：  
在构造函数编码参数中传递的编码  
在Content-Type HTTP头中声明的编码。如果这种编码是无效的（即未知的），它将被忽略，并尝试下一个解析机制。  
在响应正文中声明的编码。TextResponse类不提供任何特殊的功能。但是，HtmlResponse和XmlResponse类可以。  
通过查看响应主体来推断编码。 这是更脆弱的方法，但也是最后一个尝试。  
* **selector**:  
使用响应作为目标的选择器实例
* **xpath(query)**:   
xpath解析
    ```python
    textresponse.selector.css('p')
    #也可以简写为：
    textresponse.css('p')
    ```
* **css(query)**:   
css解析，相当于BeautifulSoup4解析
    ```python
    textresponse.selector.css('p')
    #也可以简写为：
    textresponse.css('p')
    ```
* body_as_unicode():    
与text相同，但可作为方法使用。保留此方法是为了向后兼容。

#### HtmlResponse
HtmlResponse类是TextResponse的一个子类，它通过查看HTML meta http-equiv属性来添加编码自动发现支持。

#### XmlResponse
XmlResponse类是TextResponse的一个子类，它通过查看XML声明行来添加编码自动发现支持。

## Github爬虫案例参考
```python
from scrapy import Spider, Request, FormRequest

class GithubLoginSpider(Spider):
    name = "github"
    allow_domains = ['github.com']

    #post登入必须的头字段
    post_headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "Referer" : "https://github.com",
        "Origin" : 'https://github.com',
        "Host":'github.com'
    }

    def start_requests(self):
        """
            执行spider请求
            ：return 返回一个Request对象，请求登陆的页面
        """
        return [Request(url="https://github.com/login", meta={"cookiejar":1}, callback = self.post_login, headers = self.post_headers)]

    def post_login(self, response):
        """
            登陆的页面请求成功后，解析响应的页面，获取登陆需要的<input>标签信息
            :param response :登陆接口返回的页面
        """

        #github登陆上传必要的字段
        utf8 = response.xpath('//form//input[@name="utf8"]/@value').extract()[0]
        authenticity_token = response.xpath('//form//input[@name="authenticity_token"]/@value').extract()[0]
        login = "xxxx@qq.com"
        password = "xxxxxx"
        commit = response.xpath('//form//input[@name="commit"]/@value').extract()[0]

        #发送FormRequest表单请求
        return FormRequest.from_response(response=response, meta={"cookiejar":response.meta['cookiejar']},
            formdata = {
                "utf8" : utf8,
                "authenticity_token" :authenticity_token,
                "login" : login,
                "password" : password,
                "commit" : commit
            },
            callback = self.after_login,
            headers = self.post_headers
            )

    def after_login(self, response):
        """
            form表单请求成功后，请求登陆我的页面
            ：param response
            :return:返回一个响应
        """
        print(response.body)
        if response.status == 200:
            with open("my_github.html", "wb") as f:
                f.write(response.body)
```


https://www.jianshu.com/p/60caee137a25
https://blog.csdn.net/weixin_37947156/article/details/74974208

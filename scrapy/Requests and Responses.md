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
指定错误处理函数

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
https://www.jianshu.com/p/60caee137a25
https://blog.csdn.net/weixin_37947156/article/details/74974208

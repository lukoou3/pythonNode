## 下载器中间件(Downloader Middleware)
下载器中间件是介于Scrapy的request/response处理的钩子框架。 是用于全局修改Scrapy request和response的一个轻量、底层的系统。

## 激活Downloader Middleware
要激活下载器中间件组件，将其加入到 DOWNLOADER_MIDDLEWARES 设置中。 该设置是一个字典(dict)，键为中间件类的路径，值为其中间件的顺序(order)。

这里是一个例子:
```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
}
```
DOWNLOADER_MIDDLEWARES 设置会与Scrapy定义的 DOWNLOADER_MIDDLEWARES_BASE 设置合并(但不是覆盖)， 而后根据顺序(order)进行排序，最后得到启用中间件的有序列表: 第一个中间件是最靠近引擎的，最后一个中间件是最靠近下载器的。DownloaderMiddleware的process_request与process_response方法的处理顺序与web程序中的filter处理类似。

关于如何分配中间件的顺序请查看 DOWNLOADER_MIDDLEWARES_BASE 设置，而后根据您想要放置中间件的位置选择一个值。 由于每个中间件执行不同的动作，您的中间件可能会依赖于之前(或者之后)执行的中间件，因此顺序是很重要的。

如果您想禁止内置的(在 DOWNLOADER_MIDDLEWARES_BASE 中设置并默认启用的)中间件， 您必须在项目的 DOWNLOADER_MIDDLEWARES 设置中定义该中间件，并将其值赋为 None 。 例如，如果您想要关闭user-agent中间件:
```python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
```
最后，请注意，有些中间件需要通过特定的设置来启用。更多内容请查看相关中间件文档。

## 自定义Downloader Middleware
编写下载器中间件十分简单。每个中间件组件是一个定义了以下一个或多个方法的Python类:

#### process_request(request, spider)
参数:  
* request(Request 对象)–处理的request  
* spider(Spider 对象)–该request对应的spider  

当每个request通过下载中间件时，该方法被调用。  
process_request() 必须返回其中之一: 返回 None 、返回一个 Response 对象、返回一个 Request 对象或raise IgnoreRequest 。

* 如果其返回 None ，Scrapy将继续处理该request，执行其他的中间件的相应方法，直到合适的下载器处理函数(download handler)被调用， 该request被执行(其response被下载)。

* 如果其返回 Response 对象，Scrapy将不会调用 任何 其他的 process_request() 或 process_exception() 方法，或相应地下载函数； 其将返回该response。 已安装的中间件的 process_response() 方法则会在每个response返回时被调用。

* 如果其返回 Request 对象，Scrapy则停止调用 process_request方法并重新调度返回的request。当新返回的request被执行后， 相应地中间件链将会根据下载的response被调用。

* 如果其raise一个 IgnoreRequest 异常，则安装的下载中间件的 process_exception() 方法会被调用。如果没有任何一个方法处理该异常， 则request的errback(Request.errback)方法会被调用。如果没有代码处理抛出的异常， 则该异常被忽略且不记录(不同于其他异常那样)。

#### process_response(request, response, spider)
参数:  
* request (Request 对象) – response所对应的request  
* response (Response 对象) – 被处理的response  
* spider (Spider 对象) – response所对应的spider  

process_request() 必须返回以下之一: 返回一个 Response 对象、 返回一个 Request 对象或raise一个 IgnoreRequest 异常。

* 如果其返回一个 Response (可以与传入的response相同，也可以是全新的对象)， 该response会被在链中的其他中间件的 process_response() 方法处理。   
* 如果其返回一个 Request 对象，则中间件链停止， 返回的request会被重新调度下载。处理类似于 process_request() 返回request所做的那样。   
* 如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。   

#### process_exception(request, exception, spider)
参数:  
* request (是 Request 对象) – 产生异常的request  
* exception (Exception 对象) – 抛出的异常  
* spider (Spider 对象) – request对应的spider  

当下载处理器(download handler)或 process_request() (下载中间件)抛出异常(包括IgnoreRequest异常)时，Scrapy调用 process_exception() 。

process_exception() 应该返回以下之一: 返回 None 、 一个 Response 对象、或者一个 Request 对象。

* 如果其返回 None ，Scrapy将会继续处理该异常，接着调用已安装的其他中间件的 process_exception() 方法，直到所有中间件都被调用完毕，则调用默认的异常处理。  
* 如果其返回一个 Response 对象，则已安装的中间件链的 process_response() 方法被调用。Scrapy将不会调用任何其他中间件的 process_exception() 方法。  
* 如果其返回一个 Request 对象， 则返回的request将会被重新调用下载。这将停止中间件的 process_exception() 方法执行，就如返回一个response的那样。  

## 内置Downloader Middleware介绍
关于默认启用的中间件列表(及其顺序)请参考 [DOWNLOADER_MIDDLEWARES_BASE](http://blog.csdn.net/guodongxiaren "DOWNLOADER_MIDDLEWARES_BASE") 设置。  

#### CookiesMiddleware
```python
class scrapy.downloadermiddlewares.cookies.CookiesMiddleware
```
该中间件使得爬取需要cookie(例如使用session)的网站成为了可能。 其追踪了web server发送的cookie，并在之后的request中发送回去， 就如浏览器所做的那样。

##### 以下设置可以用来配置cookie中间件:
COOKIES_ENABLED默认为True。是否启用cookies middleware。如果关闭，cookies将不会发送给web server。  
COOKIES_DEBUG默认为False。如果启用，Scrapy将记录所有在request(Cookie 请求头)发送的cookies及response接收到的cookies(Set-Cookie 接收头)。  

如果 Request.meta['dont_merge_cookies'] 设置为True，cookie将不会发送到Web服务器，并且收到的cookie Response将 不会与现有cookie合并。

##### 单spider多cookie session    
Scrapy通过使用 cookiejar Request meta key来支持单spider追踪多cookie session。 默认情况下其使用一个cookie jar(session)，不过您可以传递一个标示符来使用多个。  
例如:
```python
for i, url in enumerate(urls):
    yield scrapy.Request("http://www.example.com", meta={'cookiejar': i},
        callback=self.parse_page)

#需要注意的是 cookiejar meta key不是”黏性的(sticky)”。 您需要在之后的request请求中接着传递。例如:

def parse_page(self, response):
    # do some processing
    return scrapy.Request("http://www.example.com/otherpage",
        meta={'cookiejar': response.meta['cookiejar']},
        callback=self.parse_other_page)
```
#### DefaultHeadersMiddleware
```python
class scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware
```
该中间件设置 DEFAULT_REQUEST_HEADERS 指定的默认request header。

#### DownloadTimeoutMiddleware
```python
class scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware
```
该中间件设置 DOWNLOAD_TIMEOUT 指定的request下载超时时间。
```
注意
您还可以使用Request.meta的download_timeout键设置每个请求的下载超时 ; 即使禁用DownloadTimeoutMiddleware，也支持此功能。
```

#### scrapy内置Downloader Middleware代码参考
DefaultHeadersMiddleware源码：
```python
from scrapy.utils.python import without_none_values

class DefaultHeadersMiddleware(object):

    def __init__(self, headers):
        self._headers = headers

    @classmethod
    def from_crawler(cls, crawler):
        headers = without_none_values(crawler.settings['DEFAULT_REQUEST_HEADERS'])
        return cls(headers.items())

    def process_request(self, request, spider):
        for k, v in self._headers:
            request.headers.setdefault(k, v)
```

DownloadTimeoutMiddleware源码：
```python
from scrapy import signals

class DownloadTimeoutMiddleware(object):

    def __init__(self, timeout=180):
        self._timeout = timeout

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings.getfloat('DOWNLOAD_TIMEOUT'))
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self._timeout = getattr(spider, 'download_timeout', self._timeout)

    def process_request(self, request, spider):
        if self._timeout:
            request.meta.setdefault('download_timeout', self._timeout)
```

CookiesMiddleware部分源码：
```python
class CookiesMiddleware(object):
    """This middleware enables working with sites that need cookies"""

    def __init__(self, debug=False):
        self.jars = defaultdict(CookieJar)
        self.debug = debug

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('COOKIES_ENABLED'):
            raise NotConfigured
        return cls(crawler.settings.getbool('COOKIES_DEBUG'))

    def process_request(self, request, spider):
        if request.meta.get('dont_merge_cookies', False):
            return

        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        cookies = self._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)

        # set Cookie header
        request.headers.pop('Cookie', None)
        jar.add_cookie_header(request)
        self._debug_cookie(request, spider)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_merge_cookies', False):
            return response

        # extract cookies from Set-Cookie and drop invalid/expired cookies
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        jar.extract_cookies(response, request)
        self._debug_set_cookie(response, spider)

        return response
```

## 使用案例
#### a、Scrapy代理IP、User-Agent切换案例
##### 1.创建middlewares.py文件
Scrapy代理IP、User-Agent的切换都是通过DOWNLOADER_MIDDLEWARES进行控制，我们在settings.py同级的目录下创建middlewares.py文件，包装所有请求。
```python
# middlewares.py

# -*- coding:utf-8 -*-

import random
import base64

from settings import USER_AGENTS
from settings import PROXIES

# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)

        request.headers.setdefault("User-Agent", useragent)

class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)

        if proxy['user_passwd'] is None:
            # 没有代理账户验证的代理使用方式
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            # 对账户密码进行base64编码转换
            base64_userpasswd = base64.b64encode(proxy['user_passwd'])
            # 对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
            request.meta['proxy'] = "http://" + proxy['ip_port']
```

为什么HTTP代理要使用base64编码：  
HTTP代理的原理很简单，就是通过HTTP协议与代理服务器建立连接，协议信令中包含有连接到的远程主机的IP和端口号，如果有需要身份验证的话还需要加上授权信息，服务器收到信令后首先进行身份验证，通过后便于远程主机建立连接，连接成功之后会返回给客户端200，表示验证通过，就这么简单。下面是具体的信令格式：
```python
CONNECT 59.64.128.198:21 HTTP/1.1
Host: 59.64.128.198:21
Proxy-Authorization: Basic bGV2I1TU5OTIz
User-Agent: OpenFetion
```
OK,客户端收到后面的信令后表示成功建立连接，接下来要发送给远程主机的数据就可以发送给代理服务器了，代理服务器建立连接后会根据IP地址和端口号对应的连接放入缓存，收到信令后再根据IP地址和端口号从缓存中找到对应的连接，将数据通过该连接转发出去。

##### 2.修改settings.py配置USER-AGENTS和PROXIES
* 添加USER_AGENTS：  
```python
USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
```

* 添加代理IP设置PROXIES：  

免费代理IP可以网上搜索，或者付费购买一些可用的私密代理IP：
```python
PROXIES = [
    {'ip_port': '111.8.60.9:8123', 'user_passwd': 'user1:pass1'},
    {'ip_port': '101.71.27.120:80', 'user_passwd': 'user2:pass2'},
    {'ip_port': '122.96.59.104:80', 'user_passwd': 'user3:pass3'},
    {'ip_port': '122.224.249.122:8088', 'user_passwd': 'user4:pass4'},
]
```

* 除非特殊需要，禁用cookies,防止某些网站根据Cookie来封锁爬虫。  
```python
COOKIES_ENABLED = False
```

* 设置下载延迟  
```python
DOWNLOAD_DELAY = 3
```

* 最后设置setting.py里的DOWNLOADER_MIDDLEWARES，添加自己编写的下载中间件类。  
```python
DOWNLOADER_MIDDLEWARES = {
    #'mySpider.middlewares.MyCustomDownloaderMiddleware': 543,
    'mySpider.middlewares.RandomUserAgent': 1,
    'mySpider.middlewares.ProxyMiddleware': 100
}
```
## scrapy框架数据流
Scrapy中的数据流由执行引擎控制，其过程如下：

1. 引擎从Spiders中获取到的最初的要爬取的请求(Requests)。
2. 引擎安排请求(Requests)到调度器中，并向调度器请求下一个要爬取的请求(Requests)。
3. 调度器返回下一个要爬取的请求(Request)给请求。
4. 引擎从上步中得到的请求(Requests)通过下载器中间件(Downloader Middlewares)发送给下载器(Downloader),这个过程中下载器中间件(Downloader Middlerwares)中的process_request()函数就会被调用。
5. 一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(Downloader Middlewares)中的process_response()函数，最后返回给引擎
6. 引擎从下载器中得到上步中的Response并通过Spider中间件(Spider Middewares)发送给Spider处理，这个过程中Spider中间件(Spider Middlewares)中的process_spider_input()函数会被调用到。
7. Spider处理Response并通过Spider中间件(Spider Middlewares)返回爬取到的Item及(跟进的)新的Request给引擎，这个过程中Spider中间件(Spider Middlewares)的process_spider_output()函数会被调用到。
8. 引擎将上步中Spider处理的及其爬取到的Item给Item管道(Piplline),将Spider处理的Requests发送给调度器，并向调度器请求可能存在的下一个要爬取的请求(Requests)
9. (从第二步)重复知道调度器中没有更多的请求(Requests)。

## Spider中间件(Spider Middleware)
Spider中间件是介入到Scrapy中的spider处理机制的钩子框架，可以插入自定义功能来处理发送给Spiders的response,以及spider产生的item和request。

## 激活Spider中间件(Spider Middleware)
要启用spider中间件，您可以将其加入到 SPIDER_MIDDLEWARES 设置中。 该设置是一个字典，键位中间件的路径，值为中间件的顺序(order)。

样例:
```python
SPIDER_MIDDLEWARES = {
    'myproject.middlewares.CustomSpiderMiddleware': 543,
}
```
SPIDER_MIDDLEWARES 设置会与Scrapy定义的 SPIDER_MIDDLEWARES_BASE 设置合并(但不是覆盖)， 而后根据顺序(order)进行排序，最后得到启用中间件的有序列表: 第一个中间件是最靠近引擎的，最后一个中间件是最靠近spider的。换句话说，process_spider_input() 将以增加的中间件顺序（100,200,300，...）process_spider_output()调用每个中间件的方法，并且将按递减顺序调用每个中间件的 方法。

关于如何分配中间件的顺序请查看 SPIDER_MIDDLEWARES_BASE 设置，而后根据您想要放置中间件的位置选择一个值。 由于每个中间件执行不同的动作，您的中间件可能会依赖于之前(或者之后)执行的中间件，因此顺序是很重要的。

如果您想禁止内置的(在 SPIDER_MIDDLEWARES_BASE 中设置并默认启用的)中间件， 您必须在项目的 SPIDER_MIDDLEWARES 设置中定义该中间件，并将其值赋为 None 。 例如，如果您想要关闭off-site中间件:
```python
SPIDER_MIDDLEWARES = {
    'myproject.middlewares.CustomSpiderMiddleware': 543,
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}
```
最后，请注意，有些中间件需要通过特定的设置来启用。更多内容请查看相关中间件文档。

## 自定义Spider Middleware
编写中间件十分简单，每个中间件组件是一个定义了以下一个或多个方法的Python类：

#### process_spider_input(response, spider)
参数:	
* response (Response 对象) – 被处理的response
* spider (Spider 对象) – 该response对应的spider

这个方法在将response发往spider的过程中被调用，处理该response。  
process_spider_input() 应该返回 None 或者抛出一个异常。

* 如果其返回None，Scrapy将会继续处理该response，调用所有其他中间件直到spider处理该response。  
* 如果其抛出一个异常(exception),Scrapy将不会调用任何其他中间件的process_spider_input()方法，并调用request的errback。errback的输出将会以另一个方向被输入到中间链中，使用process_spider_output()方法来处理，当其抛出异常时则带调用process_spider_exception()。  

#### process_spider_output(response, result, spider)
参数:	
* response (Response 对象) – 生成该输出的response  
* result (包含 Request 或 Item 或 dict 对象的可迭代对象(iterable)) – 由这个spider返回的结果  
* spider (Spider 对象) – 其结果被处理的spider  

当Spider处理response返回result时，该方法被调用。  
process_spider_output() 必须返回包含 Request 或 Item 或 dict 对象的可迭代对象(iterable)。

#### process_spider_exception(response, exception, spider)
参数:	
* response(Response对象) - 异常被抛出时被处理的response  
* exception(Exception对象) - 被抛出的异常  
* spider(Spider对象) - 抛出异常的spider  

当spider或(其他spider中间件的) process_spider_input() 跑出异常时， 该方法被调用。   
process_spider_exception() 必须要么返回 None ， 要么返回一个包含 Response 或 Item 或 dict  对象的可迭代对象(iterable)。

* 如果其返回 None ，Scrapy将继续处理该异常，调用中间件链中的其他中间件的 process_spider_exception() 方法，直到所有中间件都被调用，该异常到达引擎(异常将被记录并被忽略)。  
* process_start_requests(start_requests, spider)如果其返回一个可迭代对象，则中间件链的 process_spider_output() 方法被调用， 其他的 process_spider_exception() 将不会被调用。  

#### process_start_requests(start_requests, spider)
参数:	   
* start_requests (包含 Request 的可迭代对象) – start requests
* spider (Spider 对象) – start requests所属的spider

该方法以spider 启动的request为参数被调用，执行的过程类似于 process_spider_output() ，只不过其没有相关联的response并且必须返回request(不是item)。

其接受一个可迭代的对象(start_requests 参数)且必须返回另一个包含 Request 对象的可迭代对象。

#### from_crawler（cls，crawler ）
如果给出，这个类方法将会被调用从Crawler创建一个SpiderMiddleware实例，它必须返回一个SpiderMiddleware的新的实例，Crawler对象提供了调用scrapy所有的核心组件的权限，比如你可以调用settings里面的设置项。

## 内置Spider Middleware介绍
关于默认启用的中间件列表(及其顺序)请参考 SPIDER_MIDDLEWARES_BASE 设置。

#### DepthMiddleware 
```python
class scrapy.spidermiddlewares.depth.DepthMiddleware
```
DepthMiddleware是一个用于追踪每个Request在被爬取的网站的深度的中间件。 其可以用来限制爬取深度的最大深度或类似的事情。  

##### DepthMiddleware 可以通过下列设置进行配置(更多内容请参考设置文档):  
* DEPTH_LIMIT - 爬取所允许的最大深度，如果为0，则没有限制。  
* DEPTH_STATS - 是否收集爬取状态。  
* DEPTH_PRIORITY - 是否根据其深度对requet安排优先级  

#### HttpErrorMiddleware 
```python
class scrapy.spidermiddlewares.httperror.HttpErrorMiddleware
```
DepthMiddleware是一个用于追踪每个Request在被爬取的网站的深度的中间件。 其可以用来限制爬取深度的最大深度或类似的事情。    
过滤出所有失败(错误)的HTTP response，因此spider不需要处理这些request。 处理这些request意味着消耗更多资源，并且使得spider逻辑更为复杂。

根据 HTTP标准 ，返回值为200-300之间的值为成功的resonse。

如果您想处理在这个范围之外的response，您可以通过 spider的 handle_httpstatus_list 属性或 HTTPERROR_ALLOWED_CODES 设置来指定spider能处理的response返回值。  
例如，如果您想要处理返回值为404的response您可以这么做:
```python
class MySpider(CrawlSpider):
    handle_httpstatus_list = [404]
```
Request.meta 中的 handle_httpstatus_list 键也可以用来指定每个request所允许的response code。  
不过请记住，除非您知道您在做什么，否则处理非200返回一般来说是个糟糕的决定。

##### HttpErrorMiddleware settings
* HTTPERROR_ALLOWED_CODES  
默认: []  
忽略该列表中所有非200状态码的response。  

#### scrapy内置Spider Middleware代码参考
DepthMiddleware源码：
```python
class DepthMiddleware(object):

    def __init__(self, maxdepth, stats=None, verbose_stats=False, prio=1):
        self.maxdepth = maxdepth
        self.stats = stats
        self.verbose_stats = verbose_stats
        self.prio = prio

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        maxdepth = settings.getint('DEPTH_LIMIT')
        verbose = settings.getbool('DEPTH_STATS_VERBOSE')
        prio = settings.getint('DEPTH_PRIORITY')
        return cls(maxdepth, crawler.stats, verbose, prio)

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                depth = response.meta['depth'] + 1
                request.meta['depth'] = depth
                if self.prio:
                    request.priority -= depth * self.prio
                if self.maxdepth and depth > self.maxdepth:
                    logger.debug(
                        "Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
                        {'maxdepth': self.maxdepth, 'requrl': request.url},
                        extra={'spider': spider}
                    )
                    return False
                elif self.stats:
                    if self.verbose_stats:
                        self.stats.inc_value('request_depth_count/%s' % depth,
                                             spider=spider)
                    self.stats.max_value('request_depth_max', depth,
                                         spider=spider)
            return True

        # base case (depth=0)
        if self.stats and 'depth' not in response.meta:
            response.meta['depth'] = 0
            if self.verbose_stats:
                self.stats.inc_value('request_depth_count/0', spider=spider)

        return (r for r in result or () if _filter(r))
```

HttpErrorMiddleware源码：
```python
import logging

from scrapy.exceptions import IgnoreRequest

logger = logging.getLogger(__name__)


class HttpError(IgnoreRequest):
    """A non-200 response was filtered"""

    def __init__(self, response, *args, **kwargs):
        self.response = response
        super(HttpError, self).__init__(*args, **kwargs)


class HttpErrorMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.handle_httpstatus_all = settings.getbool('HTTPERROR_ALLOW_ALL')
        self.handle_httpstatus_list = settings.getlist('HTTPERROR_ALLOWED_CODES')

    def process_spider_input(self, response, spider):
        if 200 <= response.status < 300:  # common case
            return
        meta = response.meta
        if 'handle_httpstatus_all' in meta:
            return
        if 'handle_httpstatus_list' in meta:
            allowed_statuses = meta['handle_httpstatus_list']
        elif self.handle_httpstatus_all:
            return
        else:
            allowed_statuses = getattr(spider, 'handle_httpstatus_list', self.handle_httpstatus_list)
        if response.status in allowed_statuses:
            return
        raise HttpError(response, 'Ignoring non-200 response')

    def process_spider_exception(self, response, exception, spider):
        if isinstance(exception, HttpError):
            spider.crawler.stats.inc_value('httperror/response_ignored_count')
            spider.crawler.stats.inc_value(
                'httperror/response_ignored_status_count/%s' % response.status
            )
            logger.info(
                "Ignoring response %(response)r: HTTP status code is not handled or not allowed",
                {'response': response}, extra={'spider': spider},
            )
            return []
```
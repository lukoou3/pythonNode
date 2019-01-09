## settings
The Scrapy settings allows you to customize the behaviour of all Scrapy components, including the core, extensions, pipelines and spiders themselves.  
The infrastructure of the settings provides a global namespace of key-value mappings that the code can use to pull configuration values from. The settings can be populated through different mechanisms, which are described below.   
Scrapy设定(settings)提供了定制Scrapy组件的方法。你可以控制包括核心(core)，插件(extension)，pipeline及spider组件。设定为代码提供了提取以key-value映射的配置值的的全局命名空间(namespace)。

## Populating the settings
Settings can be populated using different mechanisms, each of which having a different precedence. Here is the list of them in decreasing order of precedence:
* Command line options (most precedence)
* Settings per-spider
* Project settings module
* Default settings per-command
* Default global settings (less precedence)

```
* 命令行选项（最高优先级）
* 每个爬虫的设置
* 项目设置模块
* 每命令的默认设置
* 默认全局设置（优先级较低）
```

#### 1.命令行选项
命令行提供的参数是最优先的参数，覆盖任何其他选项。您可以使用-s（或--set）命令行选项显式覆盖一个（或多个）设置。
```python
scrapy crawl myspider -s LOG_FILE=scrapy.log
```

#### 2.每个爬虫的设置
爬虫可以定义自己的设置，这些设置将优先并覆盖项目设置。他们可以通过设置custom_settings属性来实现：
```python
class MySpider(scrapy.Spider):
    name = 'myspider'
    custom_settings = {
        'SOME_SETTING': 'some value',
    }
```

#### 3.项目设置模块
项目设置模块是Scrapy项目的标准配置文件，它将填充大多数自定义设置。对于标准的Scrapy项目，这意味着您将添加或更改settings.py为您的项目创建的文件中的设置。

#### 4.每个命令的默认设置
每个Scrapy工具命令都可以有自己的默认设置，覆盖全局默认设置。这些自定义命令设置default_settings在命令类的属性中指定。

#### 5.默认全局设置
全局默认值位于scrapy.settings.default_settings 模块中，并记录在内置设置参考部分中。


## 如何访问设置(How to access settings)
In a spider, the settings are available through self.settings:
```python
class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['http://example.com']

    def parse(self, response):
        print("Existing settings: %s" % self.settings.attributes.keys())
```

## settings默认设置
##### ROBOTSTXT_OBEY
是否遵循robots协议，一定要要设置为False，不设白不设。
```python
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```
##### DEFAULT_REQUEST_HEADERS
请求头，一定要设置，必须的。
```python
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
   'Accept-Language': 'zh-CN,zh;q=0.9',
}
```

##### ITEM_PIPELINES
保存项目中启用的pipeline及其顺序的字典。该字典默认为空，值(value)任意。 不过值(value)习惯设定在0-1000范围内。
```python
ITEM_PIPELINES = {
    'gushiwen.pipelines.GushiwenPipeline': 300,
}
```

##### DOWNLOAD_DELAY
下载器在下载同一个网站下一个页面前需要等待的时间（秒），默认为0。该选项可以用来限制爬取速度， 减轻服务器压力。这个应该设置，不能影响人家网站的服务器啊。支持小数:
```python
# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1.5
```

##### DOWNLOAD_TIMEOUT
下载器超时时间(单位: 秒)，默认: 180。下载视频文件时需要设置
```
注意:  
可也使用spider的download_timeout属性为每个爬虫设置此超时，也可以使用Request.meta的download_timeout键为每个请求设置此超时。
```

##### DOWNLOAD_MAXSIZE
默认值：1073741824（1024MB）下载程序将下载的最大响应大小（以字节为单位）。如果要禁用它，请将其设置为0。
```
注意:  
可也使用spider的download_maxsize属性为每个爬虫设置此大小，也可以使用Request.meta的download_maxsize键为每个请求设置此大小。
```

##### DOWNLOAD_WARNSIZE
默认值：33554432（32MB）下载程序将开始发出警告的响应大小（以字节为单位）。如果要禁用它，请将其设置为0。
```
注意:  
可也使用spider的download_warnsize属性为每个爬虫设置此大小，也可以使用Request.meta的download_warnsize键为每个请求设置此大小。
```

## Scrapy默认BASE设置
scrapy对某些内部组件进行了默认设置，这些组件通常情况下是不能被修改的，但是我们在自定义了某些组件以后，比如我们设置了自定义的middleware中间件，需要按照一定的顺序把他添加到组件之中，这个时候需要参考scrapy的默认设置，因为这个顺序会影响scrapy的执行，下面列出了scrapy的默认基础设置。

注意：如果你想要修改以下的某些设置，应该避免直接修改下列内容，而是修改其对应的自定义内容，例如，你想修改下面的`DOWNLOADER_MIDDLEWARES_BASE`的内容，你应该去修改`DOWNLOADER_MIDDLEWARES`这个内容，只是去掉了`_BASE`而已，其他的也是类似这样。

#### DOWNLOADER_MIDDLEWARES_BASE
默认:
```python
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
```
包含Scrapy默认启用的下载中间件的字典。 永远不要在项目中修改该设定，而是修改 DOWNLOADER_MIDDLEWARES 。

#### SPIDER_MIDDLEWARES_BASE
默认:
```python
{
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}
```
保存项目中默认启用的spider中间件的字典。 永远不要在项目中修改该设定，而是修改 SPIDER_MIDDLEWARES 。

#### EXTENSIONS_BASE
默认:
```python
{
    'scrapy.extensions.corestats.CoreStats': 0,
    'scrapy.telnet.TelnetConsole': 0,
    'scrapy.extensions.memusage.MemoryUsage': 0,
    'scrapy.extensions.memdebug.MemoryDebugger': 0,
    'scrapy.extensions.closespider.CloseSpider': 0,
    'scrapy.extensions.feedexport.FeedExporter': 0,
    'scrapy.extensions.logstats.LogStats': 0,
    'scrapy.extensions.spiderstate.SpiderState': 0,
    'scrapy.extensions.throttle.AutoThrottle': 0,
}
```
可用的插件列表。需要注意，有些插件需要通过设定来启用。默认情况下， 该设定包含所有稳定(stable)的内置插件。

#### DOWNLOAD_HANDLERS_BASE
默认:
```python
{
    'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
    'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
    's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler',
}
```
保存项目中默认启用的下载处理器(request downloader handler)的字典。 永远不要在项目中修改该设定，而是修改 DOWNLOADER_HANDLERS 。  
如果需要关闭上面的下载处理器，您必须在项目中的 DOWNLOAD_HANDLERS 设定中设置该处理器，并为其赋值为 None 。

### 说明
即使我们添加了一些我们自定义的组件，scrapy默认的base设置依然会被应用，这样说可能会一头雾水，简单地例子：  
假如我们在middlewares.py文件中定义了一个中间件，名称为MyMiddleware，我们把它添加到settings.py文件里面的`DOWNLOADER_MIDDLEWARES`，且他的执行顺序我们设置为450，最终的设置内容就是：
```python
DOWNLOADER_MIDDLEWARES = {
    'cnblog.middlewares.MyMiddleware':450,
}
```
我们再来看一下默认的DOWNLOADER_MIDDLEWARES_BASE的内容：
```python
DOWNLOADER_MIDDLEWARES_BASE ={
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 550,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.chunked.ChunkedTransferMiddleware': 830,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
```
这个时候，scrapy下载中间件的最终的执行顺序就是，把`DOWNLOADER_MIDDLEWARES`和`DOWNLOADER_MIDDLEWARES_BASE`里面的中间件按照顺序执行，`100>300>350>400>450>500>550>580>590>600>700>750>830>850>900`且全部执行，并不会因为我们定义了一个中间件，而使默认的中间件失效，也就是说，最终的结果其实是合并执行。   
如果我们不想应用某一个默认的中间件，假如`'scrapy.downloadermiddlewares.retry.RetryMiddleware': 500`,那么，就应该在`DOWNLOADER_MIDDLEWARES`里面把它的值设置为None，像下面这样：
```python
DOWNLOADER_MIDDLEWARES = {
    'cnblog.middlewares.MyMiddleware':450,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware':None，
}
```
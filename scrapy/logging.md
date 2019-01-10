## logging
```
scrapy.log已被弃用
```
现在的scrapy使用Python的内置日志记录系统进行事件记录。我们将提供一些简单的示例来帮助您入门，但对于更高级的用例，强烈建议您仔细阅读其文档。

## Log levels
Scrapy提供5层logging级别:  
* logging.CRITICAL - 严重错误(critical)
* logging.ERROR - 一般错误(regular errors)
* logging.WARNING - 警告信息(warning messages)
* logging.INFO - 一般信息(informational messages)
* logging.DEBUG - 调试信息(debugging messages)

## 如何记录信息(log messages)
下面给出如何使用 `logging.WARNING` 级别来记录信息的例子:
```python
import logging
logging.warning("This is a warning")
```
5个级别上都有用于发出日志的快捷方式，并且还有logging.log的通用方法(将给定级别作为参数)，上面的示例可以重写为：
```python
import logging
logging.log(logging.WARNING, "This is a warning")
```

## 在spider中添加log(Logging from Spiders)
scrapy logger在每个spider中提供了一个实例，可以像这样访问和使用：
```python
import scrapy
class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://scrapinghub.com']

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)
```

## logging 配置
* LOG_FILE  
日志文件的位置
* LOG_ENABLED  
日志文件的编码
* LOG_ENABLED  
是否启用日志，如果LOG_FILE未配置而LOG_ENABLED是True，则会在标准错误流上显示日志消息。最后，如果 LOG_ENABLED是False，则不会有任何可见的日志输出。
* LOG_LEVEL  
记录的最低的log级别，将过滤掉那些严重性较低的日志。

#### 在setting文件中配置
```python
LOG_FILE = './log.log'
```

#### 在spider中配置
```python
class DcdappSpider(scrapy.Spider):
    name = 'dcdapp'
    allowed_domains = ['m.dcdapp.com']
    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'autospider.pipelines.DcdAppPipeline': 300,
        },
        # 设置log日志
        'LOG_LEVEL':'DEBUG',
        'LOG_FILE':'./././Log/dcdapp_log.log'
    }
```

#### 在命令行中配置
```python
--logfile FILE
    覆盖 LOG_FILE
--loglevel/-L LEVEL
    覆盖 LOG_LEVEL
--nolog
    设置LOG_ENABLED为False
```


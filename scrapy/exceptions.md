## 异常(Exceptions)
内置异常参考手册(Built-in Exceptions reference)
下面是 Scrapy 提供的常用异常及其用法。

#### DropItem
```python
exception scrapy.exceptions.DropItem
```
该异常由 item pipeline 抛出，用于停止处理 item。  
For example:
```python
from scrapy.exceptions import DropItem

class PricePipeline(object):

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)
```

#### CloseSpider
```python
exception scrapy.exceptions.CloseSpider(reason='cancelled')
```
该异常由 spider 的回调函数(callback)抛出，来暂停/停止 spider。支持的参数:    
* reason (str) – 关闭的原因  

For example:
```python
def parse_page(self, response):
    if 'Bandwidth exceeded' in response.body:
        raise CloseSpider('bandwidth_exceeded')
```

#### IgnoreRequest
```python
exception scrapy.exceptions.IgnoreRequest
```
该异常由调度器(Scheduler)或其他下载中间件抛出，声明忽略该 request。

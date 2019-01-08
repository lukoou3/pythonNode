### Item Pipeline
当Item在Spider中被收集之后，它将会被传递到Item Pipeline，这些Item Pipeline组件按定义的顺序处理Item。  
每个Item Pipeline都是实现了简单方法的Python类，他们接收到Item并通过它执行一些行为，Item pipeline组件中有两个典型的作用，一个是查重并丢弃，第二个是将爬取的数据保存到文件或者数据库中。。  
以下是item pipeline的一些典型应用：  
* 清理HTML数据
* 验证爬取的数据(检查item包含某些字段)
* 查重(并丢弃)
* 将爬取结果保存到数据库或者文件中

### 编写item pipeline
编写item pipeline很简单，item pipiline组件是一个独立的Python类，其中process_item()方法必须实现:
```python
import something

class SomethingPipeline(object):
    def __init__(self):
        """初始化方法"""    
        # 可选实现，做参数初始化等
        # doing something

    def process_item(self, item, spider):
        """
        每个item pipeline组件都需要调用该方法，这个方法必须返回一个具有数据的dict，或是 Item (或任何继承类)对象， 或是抛出 DropItem 异常，被丢弃的item将不会被之后的pipeline组件所处理。
        参数:
            item (Item 对象或者一个dict) – 被爬取的item
            spider (Spider 对象) – 爬取该item的spider
        """
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。
        return item

    def open_spider(self, spider):
        """当spider被开启时，这个方法被调用。"""
        # spider (Spider 对象) – 被开启的spider
        # 可选实现，当spider被开启时，这个方法被调用。

    def close_spider(self, spider):
        """当spider被关闭时，这个方法被调用。"""
        # spider (Spider 对象) – 被关闭的spider
        # 可选实现，当spider被关闭时，这个方法被调用
        
    @classmethod
    def from_crawler(cls, crawler):
        """如果给出，这个类方法将会被调用从Crawler创建一个pipeline实例，它必须返回一个pipeline的新的实例，Crawler对象提供了调用scrapy所有的核心组件的权限，比如你可以调用settings里面的设置项。你会发现，这是非常常用的一个方法，你会经常用到。"""
        #例如：
        return cls(
            mongo_host = crawler.settings.get("MONGO_HOST"),
            mongo_port = crawler.settings.get("MONGO_PORT"),
            mongo_db = crawler.settings.get("MONGO_DB")
        ) 
```

### 启用Item Pipeline组件
为了启用一个Item Pipeline组件，你必须将它的类添加到 ITEM_PIPELINES 配置，就像下面这个例子:
```python
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}
```
分配给每个类的整型值，确定了他们运行的顺序，item按数字从低到高的顺序，通过pipeline，通常将这些数字定义在0-1000范围内。

也可以配置在spider的类属性里：
```python
class mySpider(Spider):
    name = 'name'
    start_urls = ['url']
    custom_settings = {
        'ITEM_PIPELINES': {
        'douban.pipelines.tongcheng_pipeline_mongodb': 300,
        }
    }
    ...
```
## Feed exports
实现爬虫时最经常提到的需求就是能合适的保存爬取到的数据，或者说，生成一个带有爬取数据的“输出文件”（通常叫“输出 feed”），来供其它系统使用。

Scrapy 自带了 Feed 输出，并且支持多种序列化格式（serialization format）及存储方式（storage backends）。
```python
pipelines.py
一般来说，如果你要操作数据库什么的，需要在这里处理items，这里有个process_item的函数，你可以把items写入数据库，但是今天我们用不到数据库，scrapy自带了一个很好的功能就是Feed exports，它支持多种格式的自动输出。所以我们直接用这个就好了，pipelines维持不变

settings.py
Feed 输出需要2个环境变量：
FEED_FORMAT ：指示输出格式，csv/xml/json/
FEED_URI : 指示输出位置，可以是本地，也可以是FTP服务器

FEED_URI = u'file:///G://douban.csv'
FEED_FORMAT = 'CSV'

```

## 序列化方式（serialization formats）
feed 输出使用到了 Item exporters。其自带支持的类型有：  
* JSON  
* JSON Lines  
* CSV  
* XML  

也可以通过 FEED_EXPORTERS 设置扩展支持的属性。

#### JSON
* FEED_FORMAT: json  
* 使用的 exporter: JsonItemExporter  
* 大数据量情况下使用 JSON 请参见 这个警告  

#### JSON lines
* FEED_FORMAT: jsonlines  
* 使用的 exporter: JsonLinesItemExporter  

#### CSV
* FEED_FORMAT: csv    
* 使用的 exporter: CsvItemExporter    

#### XML
* FEED_FORMAT: xml  
* 使用的 exporter: XmlItemExporter  

#### Pickle
* FEED_FORMAT: pickle  
* 使用的 exporter: PickleItemExporter  

#### Marshal
* FEED_FORMAT: marshal  
* 使用的 exporter: MarshalItemExporter  

## 


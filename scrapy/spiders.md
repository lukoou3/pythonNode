### 一、Spiders简介
&emsp;&emsp;Spider类定义了如何爬取某个网站。包括了爬取的动作(例如:是否跟进链接)以及如何从网页的内容中提取结构化数据(爬取item)。简而言之，Spider就是你定义爬取的动作及分析某个网页(或者是有些网页)的地方。

&emsp;&emsp;**对spider来说，爬取的循环类似如下**:
* 1.以初始的URL初始化Request，并设置回调函数。当该request下载完毕并返回时，将生成response，并作为参数传给该回调函数。spider中初始的request是通过调用start_requests() 来获取。start_requests() 读取start_urls中的URL，并以parse为回调函数生成 Request。  
* 2.在回调函数内分析返回的(网页)内容，返回 Item 对象、dict、 Request 或者一个包括三者的可迭代容器。 返回的Request对象之后会经过Scrapy处理，下载相应的内容，并调用设置的callback函数(函数可相同)。  
* 3.在回调函数内，您可以使用 选择器(Selectors) (您也可以使用BeautifulSoup, lxml 或者您想用的任何解析器) 来分析网页内容，并根据分析的数据生成item。  
* 4.最后，由spider返回的item将被存到数据库(由某些 Item Pipeline 处理)或使用 Feed exports 存入到文件中。  

&emsp;&emsp;**scrapy为我们提供了如下的一些spider类来应对不同的爬取需求**： 
* **scrapy.spiders.Spider**  
Spider是最简单的spider。每个其他的spider必须继承自该类(包括Scrapy自带其他spider以及你自己编写的spider)。Spider仅仅提供了 start_requests()的默认实现，读取并请求spider属性中的 start_urls, 并根据返回的结果(resulting responses)调用spider的 parse 方法。
* **scrapy.spiders.CrawlSpider**  
爬取一般网站常用的spider。其定义了一些规则(rule)来提供跟进link的方便的机制。比如一些网站的url通常是这样的http://www.example.com/123.html,  http://www.example.com/456.html 博客类的网站通常会这样，我们可以直接使用这个类提供的Rule来进行网址匹配。当然我们也可以实现自己的spider。
* scrapy.spiders.XMLFeedSpider  
XMLFeedSpider被设计用于通过迭代各个节点来分析XML源(XML feed)。 迭代器可以从 iternodes ， xml ， html 选择。 鉴于 xml 以及 html 迭代器需要先读取所有DOM再分析而引起的性能问题， 一般还是推荐使用 iternodes 。 不过使用 html 作为迭代器能有效应对错误的XML。
* scrapy.spiders.CSVFeedSpider  
该spider除了其按行遍历而不是节点之外其他和XMLFeedSpider十分类似。 而其在每次迭代时调用的是 parse_row() 。
* scrapy.spiders.SitemapSpider  
SitemapSpider使您爬取网站时可以通过 Sitemaps 来发现爬取的URL。其支持嵌套的sitemap，并能从 robots.txt 中获取sitemap的url。

这里我们着重学习前面两种，也是非常常用的两种。  

### 二、scrapy.Spider
    class scrapy.spiders.Spider
&emsp;&emsp;Spider是最简单的spider。每个其他的spider必须继承自该类(包括Scrapy自带其他spider以及你自己编写的spider)。Spider仅仅提供了 start_requests()的默认实现，读取并请求spider属性中的 start_urls, 并根据返回的结果(resulting responses)调用spider的 parse 方法。
##### Spider类属性
* **name**  
定义spider名字的字符串(string)。spider的名字定义了Scrapy如何定位(并初始化)spider，所以其必须是唯一的。name是spider最重要的属性，而且必须。  
一般就是以网站的URL去掉前后缀来命名，如www.baidu.com我们的name就可以为baidu，简单明了。  
* **allowed_domains**  
可选。包含了spider允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。
* **start_urls**  
URL列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。 因此，第一个被获取到的页面的URL将是该列表之一。 后续的URL将会从获取到的数据中提取。  
* **custom_settings**  
运行此爬虫时将覆盖项目配置的设置字典。它必须定义为类属性，因为设置在实例化之前更新。  
有关可用内置设置的列表，请参阅： [内置设置参考](https://scrapy.readthedocs.io/en/latest/topics/settings.html#topics-settings-ref "内置设置参考")  
* **settings**  
运行此爬虫的配置。这是一个 Settings实例，有关此主题的详细介绍，[请参阅设置主题](https://link.jianshu.com/?t=http://scrapy.readthedocs.io/en/latest/topics/settings.html#topics-settings "请参阅设置主题")。

##### Spider类方法
* **start_requests()**  
该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request。该方法仅仅会被Scrapy调用一次，可以将其实现为生成器。  
该方法的默认实现是使用 start_urls 的url生成Request。
    ```python
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
    ```
    我们可以重写该方法来实现定制。比如我们想要一开始就实现一个post请求，或传入cookie实现登录，通过默认的方法可定是不行的。因此我们重写该方法如下。
    ```python
    def start_requests(self):
        return [scrapy.FormRequest("http://www.example.com/login",
                                   formdata={'user': 'john', 'pass': 'secret'},
                                   callback=self.logged_in)]
     
    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], cookies=self.cookies, dont_filter=True)
    ```
* **parse(response)**  
当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。parse 负责处理response并返回处理的数据以及(/或)跟进的URL。  
该方法及其他的Request回调函数必须返回一个包含 Request、dict 或 Item 的可迭代的对象。简单的来说，所谓的回调函数，其实就是告诉spider，在拿到了网站的response以后，交给谁来进行处理后面的页面的解析工作。  
* **closed(reason)** 
当spider关闭时，该函数被调用。我们在此方法中关闭资源。
```python
def closed(self,reason):
    self.client.close()
```

常用的Spider的属性和方法就是这些，下面是一个综合的例子。
```python
import scrapy
from myproject.items import MyItem

class MySpider(scrapy.Spider):
    name = 'cnblog'
    allowed_domains = ['cnblogs.com']

    start_urls = ['http://www.cnblogs.com.com/123.html',
                  'http://www.cnblogs.com.com/234.html', 
                  'http://www.cnblogs.com.com/345.html'
                  ]
                  
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            item = MyItem()
            item['title'] = h3
            yield item

        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)
```
&emsp;&emsp;**请注意看，我们可以在start_requests()方法里面请求多个URL，这会形成一个请求队列，并且可以使用同样的解析方法对response进行解析，parse()方法的返回结果可以也仅可以有两种，官方文档上面说明是三种，其实item和字典我们算做一种，两种返回值的例子都包含在上面，一种是item或者说是字典，scrapy会将item交给item pipeline去进行后续的处理，包括数据的清洗，存储；另一种是Request，此时scrapy会将这个请求放入调度器请求队列，后续会对其进行请求解析。scrapy的引擎也是通过返回的两种类型来区别是交给pipeline还是scheduler进行后续的处理。**

### 二、scrapy.CrawlSpider
    class scrapy.spiders.CrawlSpider
&emsp;&emsp;CrawlSpider继承自Spider，所以具备它的所有特性，参与过网站后台开发的应该会知道，网站的url都是有一定规则的。像django，在view中定义的urls规则就是正则表示的。那么是不是可以根据这个特性来设计爬虫，而不是每次都要用spider分析页面格式，拆解源码。回答是肯定的，scrapy提供了CrawlSpider处理此需求。      
&emsp;&emsp;可以说CrawlSpider就是为全站爬取而生。
##### 查看爬虫模板
scrapy genspider -l
##### 创建crawl模板
scrapy genspider -c crawl [爬虫名字] [域名]
##### Spider类属性和方法
&emsp;&emsp;CrawlSpider是Spider的派生类，Spider类的设计原则是只爬取start_urls中的url，而CrawlSpider类定义了一些规则（rules）来提供跟进链接（link）的方便机制，从爬取的网页中获取link并继续爬取的工作更适合。  
&emsp;&emsp;CrawlSpider除了Spider继承过来的属性外，CrawlSpider类定义了如下的属性和方法。
* **rules**  
一个包含一个(或多个) Rule 对象的集合(list)。 每个 Rule 对爬取网站的动作定义了特定表现。 Rule对象在下边会介绍。 如果多个rule匹配了相同的链接，则根据他们在本属性中被定义的顺序，第一个会被使用。  
* **parse_start_url(response)**  
当start_url的请求返回时，该方法被调用。 该方法分析最初的返回值并必须返回一个 Item 对象或者 一个 Request 对象或者 一个可迭代的包含二者对象。

**当编写爬虫规则时，请避免使用parse 作为回调函数。 由于CrawlSpider使用parse 方法来实现其逻辑，如果 您覆盖了parse 方法，CrawlSpider将会运行失败。**

##### Rule类:爬取规则（Crawling rules）
Rule规则类：
```python
class scrapy.spiders.Rule(
    link_extractor, 
    callback = None, 
    cb_kwargs = None, 
    follow = None, 
    process_links = None, 
    process_request = None
)
```
Rule主要参数：
* **link_extractor**  
一个LinkExtractor对象，用于定义爬取规则。
* **callback**  
这是一个callable或string(该spider中同名的函数将会被调用)。 从link_extractor中每获取到链接时将会调用该函数。该回调函数接受一个response作为其第一个参数， 并返回一个包含 Item 以及(或) Request 对象(或者这两者的子类)的列表(list)。**因为CrawlSpider使用了parse作为回调函数，因此不要覆盖parse作为回调函数自己的回调函数。**
* **cb_kwargs**  
包含传递给回调函数的参数(keyword argument)的字典。
* **follow**  
是一个布尔(boolean)值，指定了根据该规则从response提取的链接是否需要跟进。 如果 callback 为None， follow 默认设置为 True ，否则默认为 False 。
* **process_links**  
是一个callable或string(该spider中同名的函数将会被调用)。 从link_extractor中获取到链接列表时将会调用该函数。该方法主要用来过滤不需要爬取的链接。
* **process_request**  
是一个callable或string(该spider中同名的函数将会被调用)。 该规则提取到每个request时都会调用该函数。该函数必须返回一个request或者None。 (用来过滤request)

##### LinkExtractor类
LinkExtractor是从网页（scrapy.http.Response）中抽取会被follow的链接的对象。  
LinkExtractor在CrawlSpider类(在Scrapy可用)中使用, 通过一套规则,但你也可以用它在你的Spider中,即使你不是从CrawlSpider继承的子类, 因为它的目的很简单: 提取链接｡  
每个LinkExtractor有唯一的公共方法是 extract_links()，它接收一个 Response 对象，并返回一个 scrapy.link.Link 对象。  
LinkExtractors要实例化一次，并且 extract_links 方法会根据不同的 response 调用多次提取链接｡  
```python
class scrapy.linkextractors.LinkExtractor(
    allow = (),
    deny = (),
    allow_domains = (),
    deny_domains = (),
    deny_extensions = None,
    restrict_xpaths = (),
    tags = ('a','area'),
    attrs = ('href'),
    canonicalize = True,
    unique = True,
    process_value = None
)
```
主要参数：
* **allow**  
允许的url。所有满足这个正则表达式的url都会被提取，如果为空，则全部匹配。
* **deny**  
禁止的url。所有满足这个正则表达式的url都不会被提取。
* **allow_domains**  
允许的域名。只有在这个里面指定的域名的url才会被提取。
* **deny_domains**  
禁止的域名。所有在这个里面指定的域名的url都不会被提取。
* **restrict_xpaths**  
严格的xpath。和allow共同过滤链接。


**CrawlSpider示例**：
```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
```
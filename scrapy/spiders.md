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

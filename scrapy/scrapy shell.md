### 一、背景
&emsp;&emsp;Scrapy shell是一个交互式shell，您可以非常快速地调试您的抓取代码，而无需运行spider。它用于测试数据提取代码，但您实际上可以使用它来测试任何类型的代码，因为它也是常规的Python shell。
&emsp;&emsp;该shell用来测试XPath或CSS表达式，查看他们的工作方式及从爬取的网页中提取的数据。在编写您的spider时，该终端提供了交互性测试您的表达式代码的功能，免去了每次修改后运行spider的麻烦。
&emsp;&emsp;一旦熟悉了Scrapy shell，您就会发现它是开发和调试蜘蛛的宝贵工具。

&emsp;&emsp;如果您安装了 IPython ，Scrapy终端将使用 IPython (替代标准Python终端)。 IPython 终端与其他相比更为强大，提供智能的自动补全，高亮输出，及其他特性。
&emsp;&emsp;强烈推荐您安装 IPython ，特别是如果您使用Unix系统(IPython 在Unix下工作的很好)。 详情请参考 IPython installation guide 。

### 二、启动终端
&emsp;&emsp;要启动Scrapy shell，您可以使用如下shell命令：
```python
scrapy shell <url>
```
&emsp;&emsp;打印日志：
```
scrapy shell "http://scrapy.org"
```
&emsp;&emsp;不打印日志：
```python
scrapy shell "http://scrapy.org" --nolog
```

&emsp;&emsp;**是url一定要加引号，以免不能输入特殊字符**

------

&emsp;&emsp;**shell也适用于本地文件**。如果您想要使用网页的本地副本，这可能很方便：
```python
# UNIX-style
scrapy shell ./path/to/file.html
scrapy shell ../other/path/to/file.html
scrapy shell /absolute/path/to/file.html

# File URI
scrapy shell file:///absolute/path/to/file.html
```
&emsp;&emsp;注意，index.html在语法上类似于example.com，所以 shell将index.html视为域名并触发DNS查找错误：
```python
$ scrapy shell index.html
[ ... scrapy shell starts ... ]
[ ... traceback ... ]
twisted.internet.error.DNSLookupError: DNS lookup failed:
address 'index.html' not found: [Errno -5] No address associated with hostname.
```

### 三、可用的快捷命令(shortcut)
* **shelp()** - 打印可用对象及快捷命令的帮助列表
* **fetch(request_or_url)** - 根据给定的请求(request)或URL获取一个新的response，并更新相关的对象
* **view(response)** - 在本机的浏览器打开给定的response。 其会在response的body中添加一个 <base> tag ，使得外部链接(例如图片及css)能正确显示。 注意，该操作会在本地创建一个临时文件，且该文件不会被自动删除。

### 四、可用的Scrapy对象
&emsp;&emsp;Scrapy终端根据下载的页面会自动创建一些方便使用的对象，例如 Response 对象及 Selector 对象(对HTML及XML内容)。
&emsp;&emsp;这些对象有:
* crawler - 当前 Crawler 对象.
* spider - 处理URL的spider。 对当前URL没有处理的Spider时则为一个 Spider 对象。
* **request** - 最近获取到的页面的 Request 对象。 您可以使用 replace() 修改该request。或者 使用 fetch 快捷方式来获取新的request。
* **response** - 包含最近获取到的页面的 Response 对象。
* sel - 根据最近获取到的response构建的 Selector 对象。
* **settings** - 当前的 Scrapy settings

### 四、官网事例
&emsp;&emsp;我们首先抓取https://scrapy.org页面，然后继续抓取https://reddit.com 页面。最后，我们将（Reddit）请求方法修改为POST并重新获取它以获得错误。通过 Ctrl-D(Unix)或 Ctrl-Z(Windows)关闭会话。

首先，我们启动shell：
```python
scrapy shell 'https://scrapy.org' --nolog
```

接着该终端(使用 Scrapy 下载器(downloader))获取 URL 内容并打印可用的对象及快捷命令(注意到以[s]开头的行):
```python
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7f07395dd690>
[s]   item       {}
[s]   request    <GET https://scrapy.org>
[s]   response   <200 https://scrapy.org/>
[s]   settings   <scrapy.settings.Settings object at 0x7f07395dd710>
[s]   spider     <DefaultSpider 'default' at 0x7f0735891690>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser

>>>
```

之后，就可以操作这些对象了：
```python
>>> response.xpath('//title/text()').extract_first()
'Scrapy | A Fast and Powerful Scraping and Web Crawling Framework'

>>> fetch("https://reddit.com")

>>> response.xpath('//title/text()').extract()
['reddit: the front page of the internet']

>>> request = request.replace(method="POST")

>>> fetch(request)

>>> response.status
404

>>> from pprint import pprint

>>> pprint(response.headers)
{'Accept-Ranges': ['bytes'],
 'Cache-Control': ['max-age=0, must-revalidate'],
 'Content-Type': ['text/html; charset=UTF-8'],
 ......
}
>>>
```

### 五、在spider中嵌入启动shell来查看response
&emsp;&emsp;有时您想在 spider 的某个位置中查看被处理的 response可以通过 `scrapy.shell.inspect_response` 函数来实现。
&emsp;&emsp;以下是如何在 spider 中调用该函数的例子:
```python
import scrapy


class MySpider(scrapy.Spider):
    name = "myspider"
    start_urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net",
    ]

    def parse(self, response):
        # We want to inspect one specific response.
        if ".org" in response.url:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

        # Rest of parsing code.
```

&emsp;&emsp;当运行 spider 时，您将得到类似下列的输出:
```python
2014-01-23 17:48:31-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.com> (referer: None)
2014-01-23 17:48:31-0400 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://example.org> (referer: None)
[s] Available Scrapy objects:
[s]   crawler    <scrapy.crawler.Crawler object at 0x1e16b50>
...

>>> response.url
'http://example.org'
```

&emsp;&emsp;接着测试提取代码：
```python
>>> sel.xpath('//h1[@class="fn"]')
[]
```

看来是没有。您可以在浏览器里查看 response 的结果，判断是否是您期望的结果:
```python
>>> view(response)
True
```

最后您可以点击 Ctrl-D(Windows 下 Ctrl-Z)来退出终端，恢复爬取:
```python
>>> ^D
2014-01-23 17:50:03-0400 [myspider] DEBUG: Crawled (200) <GET http://example.net> (referer: None)
```
**注意: 由于该终端屏蔽了 Scrapy 引擎，您在这个终端中不能使用 fetch 快捷命令(shortcut)。 当您离开终端时，spider 会从其停下的地方恢复爬取。**

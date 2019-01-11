## 选择器(Selectors)
当抓取网页时，你做的最常见的任务是从HTML源码中提取数据。现有的一些库可以达到这个目的：  
* BeautifulSoup 是在程序员间非常流行的网页分析库，它基于HTML代码的结构来构造一个Python对象， 对不良标记的处理也非常合理，但它有一个缺点：慢。
* lxml 是一个基于 ElementTree (不是Python标准库的一部分)的python化的XML解析库(也可以解析HTML)。  

Scrapy提取数据有自己的一套机制。它们被称作选择器(seletors)，因为他们通过特定的 XPath 或者 CSS 表达式来“选择” HTML文件中的某个部分。
Scrapy选择器构建于 lxml 库之上，这意味着它们在速度和解析准确性上非常相似。

Selector 与 SelectorList 主要方法：
* **xpath(xpath)**    
* **css(query)**    
* **extract() = getall()**    
* **extract_first() = get()**    
* **re(regex, replace_entities=True)**    
* **re_first(regex, default=None, replace_entities=True)**    

## 使用选择器(selectors)
#### 构造选择器(selectors)
Scrapy selector是以 文字(text) 或 TextResponse 构造的 Selector 实例。 其根据输入的类型自动选择最优的分析方法(XML vs HTML):
```python
>>> from scrapy.selector import Selector
>>> from scrapy.http import HtmlResponse
```
以文字构造:
```python
>>> body = '<html><body><span>good</span></body></html>'
>>> Selector(text=body).xpath('//span/text()').extract()
[u'good']
```
以response构造:
```python
>>> response = HtmlResponse(url='http://example.com', body=body)
>>> Selector(response=response).xpath('//span/text()').extract()
[u'good']
```
为了方便起见，response对象以 .selector 属性提供了一个selector， 您可以随时使用该快捷方法:
```python
>>> response.selector.xpath('//span/text()').extract()
[u'good']
```
更方便地，response对象可以直接调用xpath或css方法:
```python
>>> response.xpath('//span/text()').extract()
[u'good']
```

#### 使用选择器(selectors)
由于在response中使用XPath、CSS查询十分普遍，因此，Scrapy提供了两个实用的快捷方式: response.xpath() 及 response.css():
```python
>>> response.xpath('//title/text()')
[<Selector (text) xpath=//title/text()>]
>>> response.css('title::text')
[<Selector (text) xpath=//title/text()>]
```
如你所见， .xpath() 及 .css() 方法返回一个类 SelectorList 的实例, 它是一个新选择器的列表。这个API可以用来快速的提取嵌套数据。  

为了提取真实的原文数据，你需要调用 .extract() 方法如下:
```python
>>> response.xpath('//title/text()').extract()
[u'Example website']
```

如果只想提取第一个匹配的元素，可以调用选择器 .extract_first()
```python
>>> response.xpath('//div[@id="images"]/a/text()').extract_first()
u'Name: My image 1 '
```

注意CSS选择器可以使用CSS3伪元素(pseudo-elements)来选择文字或者属性节点:
```python
>>> response.css('title::text').extract()
[u'Example website']
```

#### 嵌套选择器(selectors)  
选择器方法( .xpath() or .css() )返回相同类型的选择器列表，因此你也可以对这些选择器调用选择器方法。
```python
links = response.xpath('//a[contains(@href, "image")]')
for index, link in enumerate(links):
    args = (index, link.xpath('@href').extract(), link.xpath('img/@src').extract())
    print 'Link number %d points to url %s and image %s' % args
```

#### 结合正则表达式使用选择器(selectors)
Selector 也有一个 .re() 方法，用来通过正则表达式来提取数据。然而，不同于使用 .xpath() 或者 .css() 方法, .re() 方法返回unicode字符串的列表。所以你无法构造嵌套式的 .re() 调用。

#### 使用相对XPaths
记住如果你使用嵌套的选择器，并使用起始为 / 的XPath，那么该XPath将对文档使用绝对路径，而且对于你调用的 Selector 不是相对路径。所以要在起始用 ./

#### 使用EXSLT扩展
因建于 lxml 之上, Scrapy选择器也支持一些 EXSLT 扩展，可以在XPath表达式中使用这些预先制定的命名空间：

| 前缀 | 命名空间                             | 用途       |
| ---- | ------------------------------------ | ---------- |
| re   | http://exslt.org/regular-expressions | 正则表达式 |
| set  | http://exslt.org/sets                | 集合操作   |

##### 正则表达式		
例如在XPath的 starts-with() 或 contains() 无法满足需求时， test() 函数可以非常有用。  
例如在列表中选择有”class”元素且结尾为一个数字的链接:
```python
>>> from scrapy import Selector
>>> doc = """
... <div>
...     <ul>
...         <li class="item-0"><a href="link1.html">first item</a></li>
...         <li class="item-1"><a href="link2.html">second item</a></li>
...         <li class="item-inactive"><a href="link3.html">third item</a></li>
...         <li class="item-1"><a href="link4.html">fourth item</a></li>
...         <li class="item-0"><a href="link5.html">fifth item</a></li>
...     </ul>
... </div>
... """
>>> sel = Selector(text=doc, type="html")
>>> sel.xpath('//li//@href').extract()
[u'link1.html', u'link2.html', u'link3.html', u'link4.html', u'link5.html']
>>> sel.xpath('//li[re:test(@class, "item-\d$")]//@href').extract()
[u'link1.html', u'link2.html', u'link4.html', u'link5.html']
>>>
```

```
警告  
C语言库 libxslt 不原生支持EXSLT正则表达式，因此 lxml 在实现时使用了Python re 模块的钩子。 因此，在XPath表达式中使用regexp函数可能会牺牲少量的性能。
```

## 一些XPath技巧
根据 [ScrapingHub博客上的文章](https://blog.scrapinghub.com/2014/07/17/xpath-tips-from-the-web-scraping-trenches?_ga=2.168048929.1093675070.1547027638-248628518.1534988719 "ScrapingHub博客上的文章")，在使用带有Scrapy选择器的XPath时，您可能会发现一些有用的技巧。

#### Avoid using contains(.//text(), 'search text') in your XPath conditions. Use contains(., 'search text') instead.
当您需要使用文本内容作为XPath字符串函数的参数时，请避免使用.//text()而使用.。  
这是因为表达式.//text()产生了一组文本元素 - 一个节点集。并且当节点集被转换成字符串，当它是作为参数传递给像字符串功能这恰好contains()或starts-with()，它导致文仅用于第一个元素。  
```python
>>> from scrapy import Selector
>>> sel = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')
>>> xp = lambda x: sel.xpath(x).extract() # let's type this only once
>>> xp('//a//text()') # take a peek at the node-set
   [u'Click here to go to the ', u'Next Page']
>>> xp('string(//a//text())')  # convert it to a string
   [u'Click here to go to the ']
```
A node converted to a string, however, puts together the text of itself plus of all its descendants:
```python
>>> xp('//a[1]') # selects the first a node
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
>>> xp('string(//a[1])') # converts it to string
[u'Click here to go to the Next Page']
```

So, in general:  
GOOD:
```python
>>> xp("//a[contains(., 'Next Page')]")
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
```
BAD:
```python
>>> xp("//a[contains(.//text(), 'Next Page')]")
[]
```
GOOD:
```python
>>> xp("substring-after(//a, 'Next ')")
[u'Page']
```
BAD:
```python
>>> xp("substring-after(//a//text(), 'Next ')")
[u'']
```

#### Beware of the difference between //node[1] and (//node)[1]
//node[1] selects all the nodes occurring first under their respective parents.  
(//node)[1] selects all the nodes in the document, and then gets only the first of them.

注意// node [1]和（// node）[1]之间的区别   
* //node[1] 选择在各自父母下首先出现的所有节点。  
* (//node)[1] 选择文档中的所有节点，然后只获取其中的第一个节点。  
 
```python
>>> from scrapy import Selector
>>> sel=Selector(text="""
....:     <ul class="list">
....:         <li>1</li>
....:         <li>2</li>
....:         <li>3</li>
....:     </ul>
....:     <ul class="list">
....:         <li>4</li>
....:         <li>5</li>
....:         <li>6</li>
....:     </ul>""")
>>> xp = lambda x: sel.xpath(x).extract()
>>> xp("//li[1]") # get all first LI elements under whatever it is its parent
[u'<li>1</li>', u'<li>4</li>']
>>> xp("(//li)[1]") # get the first LI element in the whole document
[u'<li>1</li>']
>>> xp("//ul/li[1]")  # get all first LI elements under an UL parent
[u'<li>1</li>', u'<li>4</li>']
>>> xp("(//ul/li)[1]") # get the first LI element under an UL parent in the document
[u'<li>1</li>']
```

#### When selecting by class, be as specific as necessary
If you want to select elements by a CSS class, the XPath way to do that is the rather verbose:  
`*[contains(concat(' ', normalize-space(@class), ' '), ' someclass ')]`
Let's cook up some examples:
```python
>>> sel = Selector(text='<p class="content-author">Someone</p><p class="content text-wrap">Some content</p>')
>>> xp = lambda x: sel.xpath(x).extract()
```
BAD: doesn't work because there are multiple classes in the attribute
```python
>>> xp("//*[@class='content']")
[]
```
BAD: gets more than we want
```python
>>> xp("//*[contains(@class,'content')]")
[u'<p class="content-author">Someone</p>','<p class="content text-wrap">Some content</p>']
```
GOOD:
```python
>>> xp("//*[contains(concat(' ', normalize-space(@class), ' '), ' content ')]")
[u'<p class="content text-wrap">Some content</p>']
```
And many times, you can just use a CSS selector instead, and even combine the two of them if needed:  
ALSO GOOD:
```python
>>> sel.css(".content").extract()
[u'<p class="content text-wrap">Some content</p>']
>>> sel.css('.content').xpath('@class').extract()
[u'content text-wrap']
```

## 选择器对象参考
#### Selector
```python
class scrapy.selector.Selector（response = None，text = None，type = None ）
```
参数：  
* response 是 HtmlResponse 或 XmlResponse 的一个对象，将被用来选择和提取数据。  
* text 是在 response 不可用时的一个unicode字符串或utf-8编码的文字。将 text 和 response 一起使用是未定义行为。  
* type 定义了选择器类型，可以是 "html", "xml" or None (默认).  
如果 type 是 None ，选择器会根据 response 类型(参见下面)自动选择最佳的类型，或者在和 text 一起使用时，默认为 "html" 。
如果 type 是 None ，并传递了一个 response ，选择器类型将从response类型中推导如下：  
    * "html" for HtmlResponse type
    * "xml" for XmlResponse type
    * "html" for anything else

主要函数：  
* **xpath(query)** 
寻找可以匹配xpath query 的节点，并返回 SelectorList 的一个实例结果，单一化其所有元素。列表元素也实现了 Selector 的接口。  
* **css(query)** 
应用给定的CSS选择器，返回 SelectorList 的一个实例。  
在后台，通过 cssselect 库和运行 .xpath() 方法，CSS查询会被转换为XPath查询。    
* **extract()** 
将匹配到的节点列表返回第一个unicode字符串。    
**extract = get**。 
* **re(regex)**  
应用给定的regex，并返回匹配到的unicode字符串列表。

#### SelectorList
```python
class scrapy.selector.SelectorList
```
SelectorList 类是 list 类的子类，额外实现了Selector的接口。  
SelectorList的extract返回unicode列表，extract_first返回unicode列表的第一个，extract = getall，extract_first = get。

#### Selector 与 SelectorList 部分源码
Selector部分源码：
```python
class Selector(object):
    def xpath(self, query, namespaces=None, **kwargs):
        ...
        return self.selectorlist_cls(result)

    def css(self, query):
        return self.xpath(self._css2xpath(query))   
    
    def re(self, regex, replace_entities=True):
        """
        Apply the given regex and return a list of unicode strings with the
        matches.
        """
        return extract_regex(regex, self.get(), replace_entities=replace_entities)

    def re_first(self, regex, default=None, replace_entities=True):
        """
        Apply the given regex and return the first unicode string which
        matches. If there is no match, return the default value (``None`` if
        the argument is not provided).
        """
        return next(iflatten(self.re(regex, replace_entities=replace_entities)), default)

    def get(self):
        """
        Serialize and return the matched nodes in a single unicode string.
        Percent encoded content is unquoted.
        """
        try:
            return etree.tostring(self.root,
                                  method=self._tostring_method,
                                  encoding='unicode',
                                  with_tail=False)
        except (AttributeError, TypeError):
            if self.root is True:
                return u'1'
            elif self.root is False:
                return u'0'
            else:
                return six.text_type(self.root)
    extract = get

    def getall(self):
        """
        Serialize and return the matched node in a 1-element list of unicode strings.
        """
        return [self.get()] 
```

SelectorList部分源码：
```python
class SelectorList(list):
    """
    The :class:`SelectorList` class is a subclass of the builtin ``list``
    class, which provides a few additional methods.
    """
    
    def xpath(self, xpath, namespaces=None, **kwargs):
        """
        Call the ``.xpath()`` method for each element in this list and return
        their results flattened as another :class:`SelectorList`.

        ``query`` is the same argument as the one in :meth:`Selector.xpath`
        """
        return self.__class__(flatten([x.xpath(xpath, namespaces=namespaces, **kwargs) for x in self]))

    def css(self, query):
        """
        Call the ``.css()`` method for each element in this list and return
        their results flattened as another :class:`SelectorList`.

        ``query`` is the same argument as the one in :meth:`Selector.css`
        """
        return self.__class__(flatten([x.css(query) for x in self]))

    def re(self, regex, replace_entities=True):
        """
        Call the ``.re()`` method for each element in this list and return
        their results flattened, as a list of unicode strings.
        """
        return flatten([x.re(regex, replace_entities=replace_entities) for x in self])

    def re_first(self, regex, default=None, replace_entities=True):
        """
        Call the ``.re()`` method for the first element in this list and
        return the result in an unicode string. If the list is empty or the
        regex doesn't match anything, return the default value (``None`` if
        the argument is not provided).
        """
        for el in iflatten(x.re(regex, replace_entities=replace_entities) for x in self):
            return el
        else:
            return default

    def getall(self):
        """
        Call the ``.get()`` method for each element is this list and return
        their results flattened, as a list of unicode strings.
        """
        return [x.get() for x in self]
    extract = getall

    def get(self, default=None):
        """
        Return the result of ``.get()`` for the first element in this list.
        If the list is empty, return the default value.
        """
        for x in self:
            return x.get()
        else:
            return default
    extract_first = get
```
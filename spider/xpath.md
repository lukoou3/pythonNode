### 一、基本用法
```python
from lxml import etree
html = etree.HTML(response.text)
links = html.xpath("//ul[@class='mod-play-list play-list-num  tab-panel tab-1']/li/a")
```

### 二、基本语法
##### 1、选取节点
Xpath使用路径表达式在XML文档中选取节点。节点是通过沿着路径来选取的，通过路径可以找到我们想要的节点或者节点范围。

| 表达式 | 描述 | 用法 | 说明 |
| ------ | ---- | ---- | ---- |
| nodename | 选取此节点的所有子节点。 | xpath(‘span’) | 选取span元素的所有子节点 |
| / | 从根节点选取 | xpath(‘/div’) | 从根节点上选取div节点 |
| // | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 | xpath(‘//div’) | 从当前节点选取含有div节点的标签 |
| . | 选取当前节点 | xpath(‘./div’) | 选取当前节点下的div标签 |
| .. | 选取当前节点的父节点 | xpath(‘../’) | 回到上一级节点 |
| @ | 选取属性 | xpath(“//div[@id=’1001’]”) | 获取div标签中，含有ID属性且值为1001的标签 |

事例：
```python
xml.xpath(“bookstore”) 表示选取 bookstore 元素的所有子节点
xml.xpath(“/bookstore”) 表示选取根元素 bookstore。
xml.xpath(“bookstore/book”) 选取属于 bookstore 的子元素的所有 book 元素。
xml.xpath(“//book”) 选取所有 book 子元素，而不管它们在文档中的位置。
xml.xpath(“bookstore//book”) 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。
xml.xpath(“//@lang”) 选取名为 lang 的所有属性。
```

##### 2、谓语（Predicates）
谓语用来查找某个特定的节点或者包含某个指定的值的节点。谓语被嵌在方括号中。

| 表达式描述                         | 用法说明                                                                                  |
| ---------------------------------- | ----------------------------------------------------------------------------------------- |
| /bookstore/book[1]                 | 选取属于 bookstore 子元素的第一个 book 元素。                                             |
| /bookstore/book[last()]            | 选取属于 bookstore 子元素的最后一个 book 元素。                                           |
| /bookstore/book[last()-1]          | 选取属于 bookstore 子元素的倒数第二个 book 元素。                                         |
| /bookstore/book[position() < 3]      | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。                                 |
| //title[@lang]                     | 选取所有拥有名为 lang 的属性的 title 元素。                                               |
| //title[@lang='eng']               | 选取所有 title 元素，且这些元素拥有值为 eng 的 lang 属性。                                |
| /bookstore/book[price>35.00]       | 选取 bookstore 元素的所有 book 元素，且其中的 price 元素的值须大于 35.00。                |
| /bookstore/book[price>35.00]/title | 选取 bookstore 元素中的 book 元素的所有 title 元素，且其中的 price 元素的值须大于 35.00。 |

##### 3、通配符
XPath 通配符可用来选取未知的 XML 元素,通配指定节点。

| 表达式 | 描述 | 用法 | 说明 |
| ------ | ---- | ---- | ---- |
| * | 匹配任何元素节点 | xpath（/div/*） | 选取div下的所有子节点 |
| @* | 匹配任何属性节点 | xpath(/div[@*]) | 选取所有带属性的div节点 |
| node() | 匹配任何类型的节点 | xpath(//div[@class=’tb_cls’]).node() | 选择标签为div且类属性为tb_cls的所有标签 |

##### 4、多路径选择
通过在路径表达式中使用“|”运算符，您可以选取若干个路径。

| 用法                                    | 说明                                       |
| --------------------------------------- | ------------------------------------------ |
| xpath（//book/title&#124;//book/price） | 选取 book 元素的所有 title 和 price 元素。 |
| xpath（//title&#124;//price）           | 选取文档中的所有 title 和 price 元素       |

##### 5、轴
轴可定义相对于当前节点的节点集。

| 表达式 | 描述 | 用法 | 说明 |
| ------ | ---- | ---- | ---- |
| ancestor | 选取当前节点的所有先辈（父、祖父等） | `xpath(//div[@id=’123’]/ancestor::*)` | 选择标签为div且ID号为123的所有先辈标签 |
| ancestor-or-self | 选取当前节点的所有先辈（父、祖父等）以及当前节点本身 | `xpath(//div[@id=’123’]/ancestor-or-self::*)` | 选择标签为div且ID号为123的所有先辈标签且包含自己 |
| attribute | 选取当前节点的所有属性 | `xpath(//div[@id=’123’]/attribute::class)` | 选择标签为div且ID号为123的类属性名称 |
| child | 选取当前节点的所有子元素 | `xpath(//div[@id=’123’]/child::book)` | 选择标签为div且ID号为123的所有子元素的为book 节点 |
| descendant | 选取当前节点的所有后代元素（子、孙等） | `xpath(./descendant::*)` | 返回当前节点的所有后代节点（子节点、孙节点） |
| following | 选取文档中当前节点结束标签后的所有节点 | `xpath(./following::*)` | 选取文档中当前节点结束标签后的所有节点 |
| parent | 选取当前节点的父节点 | `xpath(./parent::*)` | 选取当前节点的父节点 |
| preceding | 选取文档中当前节点的开始标签之前的所有节点 | `xpath(//div[@id=’123’]/preceding::*)` | 选择标签为div且ID号为123的开始标签之前的所有节点 |
| preceding-sibling | 选取当前节点之前的所有同级节点 | `xpath(//div[@id=’123’]/preceding-sibling::*)` | 选择标签为div且ID号为123的之前的所有同级节点 |
| self | 选取当前节点 | `xpath(./self::*)` | 选取当前节点 |

###### 轴的语法：
轴名称::节点测试[谓语]


例子：
```python
例子	结果
child::book	选取所有属于当前节点的子元素的 book 节点。
attribute::lang	选取当前节点的 lang 属性。
child::*	选取当前节点的所有子元素。
attribute::*	选取当前节点的所有属性。
child::text()	选取当前节点的所有文本子节点。
child::node()	选取当前节点的所有子节点。
descendant::book	选取当前节点的所有 book 后代。
ancestor::book	选择当前节点的所有 book 先辈。
ancestor-or-self::book	选取当前节点的所有 book 先辈以及当前节点（如果此节点是 book 节点）
child::*/child::price	选取当前节点的所有 price 孙节点。
```

##### 6、XPath 运算符
| 表达式 | 描述 | 用法 | 说明 |
| ------ | ---- | ---- | ---- |
| + | 加法 | 6 + 4 | 10 |
| - | 减法 | 6 - 4 | 2 |
| * | 乘法 | 6 * 4 | 24 |
| div | 除法 | 8 div 4 | 2 |
| = | 等于 | price=9.80 | 如果 price 是 9.80，则返回 true。如果 price 是 9.90，则返回 false。 |
| != | 不等于 | price!=9.80 | 如果 price 是 9.90，则返回 true。如果 price 是 9.80，则返回 false。 |
| < | 小于 | price<9.80 | 如果 price 是 9.00，则返回 true。如果 price 是 9.90，则返回 false。 |
| <= | 小于或等于 | price<=9.80 | 如果 price 是 9.00，则返回 true。如果 price 是 9.90，则返回 false。 |
| > | 大于 | price>9.80 | 如果 price 是 9.90，则返回 true。如果 price 是 9.80，则返回 false。 |
| >= | 大于或等于 | price>=9.80 | 如果 price 是 9.90，则返回 true。如果 price 是 9.70，则返回 false。 |
| or | 或 | price=9.80 or price=9.70 | 如果 price 是 9.80，则返回 true。如果 price 是 9.50，则返回 false。 |
| and | 与 | price>9.00 and price<9.90 | 如果 price 是 9.80，则返回 true。如果 price 是 8.50，则返回 false。 |
| mod | 计算除法的余数 | 5 mod 2 | 1 |

##### 7、常用的功能函数
| 表达式 | 描述 | 用法 | 说明 |
| ------ | ---- | ---- | ---- |
| starts-with | 选取id值以ma开头的div节点 | xpath(‘//div[starts-with(@id,”ma”)]‘) | 选取id值以ma开头的div节点 |
| contains | 选取id值包含ma的div节点 | xpath(‘//div[contains(@id,”ma”)]‘) | 选取id值包含ma的div节点 |
| and | 选取id值包含ma和in的div节点 | xpath(‘//div[contains(@id,”ma”) and contains(@id,”in”)]‘) | 选取id值包含ma和in的div节点 |
| text() | 选取节点文本包含ma的div节点 | xpath(‘//div[contains(text(),”ma”)]‘) | 选取节点文本包含ma的div节点 |

### 三、Xpath高级用法
##### 1、匹配某节点下的所有 .//
```
//获取文档中所有匹配的节点，.获取当前节点，有的时候我们需要获取当前节点下的所有节点，.//一定要结合.使用//，否则都会获取整个文档的匹配结果.
```

##### 2、匹配包含某属性的所有的属性值 //@lang
```python
print tree.xpath('//@code') #匹配所有带有code属性的属性值
>>['84', '104', '223']
```

##### 3、选取若干路径 |
这个符号用于在一个xpath中写多个表达式用，用|分开，每个表达式互不干扰
```python
print tree.xpath('//div[@id="testid"]/h2/text() | //li[@data]/text()') #多个匹配条件
>>[u'\u8fd9\u91cc\u662f\u4e2a\u5c0f\u6807\u9898', '1', '2', '3']
```

##### 4、 Axes（轴）
**child：选取当前节点的所有子元素**
```python
>>print tree.xpath('//div[@id="testid"]/child::ul/li/text()') #child子节点定位
>>['84', '104', '223']

>>print tree.xpath('//div[@id="testid"]/child::*') #child::*当前节点的所有子元素
>>[<Element h2 at 0x21bd148>, <Element ol at 0x21bd108>, <Element ul at 0x21bd0c8>]

>>#定位某节点下为ol的子节点下的所有节点
>>print tree.xpath('//div[@id="testid"]/child::ol/child::*/text()')
>>['1', '2', '3']
```

**attribute：选取当前节点的所有属性**
```python
>>print tree.xpath('//div/attribute::id') #attribute定位id属性值
>>['testid', 'go']

>>print tree.xpath('//div[@id="testid"]/attribute::*') #定位当前节点的所有属性
>>['testid', 'first']
```

**ancestor：父辈元素 / ancestor-or-self：父辈元素及当前元素**
```python
>>print tree.xpath('//div[@id="testid"]/ancestor::div/@price') #定位父辈div元素的price属性
>>['99.8']

>>print tree.xpath('//div[@id="testid"]/ancestor::div') #所有父辈div元素
>>print tree.xpath('//div[@id="testid"]/ancestor-or-self::div') #所有父辈及当前节点div元素
>>[<Element div at 0x23fc108>]
>>[<Element div at 0x23fc108>, <Element div at 0x23fc0c8>]
```

**descendant：后代 / descendant-or-self：后代及当前节点本身,使用方法同上**

**following :选取文档中当前节点的结束标签之后的所有节点**
```python
#定位testid之后不包含id属性的div标签下所有的li中第一个li的text属性
>>print tree.xpath('//div[@id="testid"]/following::div[not(@id)]/.//li[1]/text()')
>>['test1']
```

**namespace：选取当前节点的所有命名空间节点**
```python
>>print tree.xpath('//div[@id="testid"]/namespace::*') #选取命名空间节点
>>[('xml', 'http://www.w3.org/XML/1998/namespace')]
```

**parent：选取当前节点的父节点**
```python
>>#选取data值为one的父节点的子节点中最后一个节点的值
>>print tree.xpath('//li[@data="one"]/parent::ol/li[last()]/text()')
>>['3']
>>#注意这里的用法，parent::父节点的名字
```

**preceding：选取文档中当前节点的开始标签之前的所有节点**
```python
>>#记住是标签开始之前，同级前节点及其子节点
>>print tree.xpath('//div[@id="testid"]/preceding::div/ul/li[1]/text()')[0]
>>时间
>>#下面这两条可以看到其顺序是靠近testid节点的优先
>>print tree.xpath('//div[@id="testid"]/preceding::li[1]/text()')[0]
>>print tree.xpath('//div[@id="testid"]/preceding::li[3]/text()')[0]
>>任务
>>时间
```

**preceding-sibling：选取当前节点之前的所有同级节点**
```python
>>#记住只能是同级节点
>>print tree.xpath('//div[@id="testid"]/preceding-sibling::div/ul/li[2]/text()')[0]
>>print tree.xpath('//div[@id="testid"]/preceding-sibling::li') #这里返回的就是空的了
>>地点
>>[]
```

**self：选取当前节点**
```python
>>#选取带id属性值的div中包含data-h属性的标签的所有属性值
>>print tree.xpath('//div[@id]/self::div[@data-h]/attribute::*')
>>['testid', 'first']
```

组合拳
```python
#定位id值为testid下的ol下的li属性值data为two的父元素ol的兄弟前节点h2的text值
>>print tree.xpath('//*[@id="testid"]/ol/li[@data="two"]/parent::ol/preceding-sibling::h2/text()')[0]
>>这里是个小标题
```

##### 5、position定位
```python
>>print tree.xpath('//*[@id="testid"]/ol/li[position()=2]/text()')[0]
>>2
```

##### 6、条件
```python
>>定位所有h2标签中text值为`这里是个小标题`
>>print tree.xpath(u'//h2[text()="这里是个小标题"]/text()')[0]
>>这里是个小标题
```

##### 7、函数
**count：统计**
```python
>>print tree.xpath('count(//li[@data])') #节点统计
>>3.0
```

**concat：字符串连接**
```python
>>print tree.xpath('concat(//li[@data="one"]/text(),//li[@data="three"]/text())')
>>13
```

**string：解析当前节点下的字符**
```python
>>#string只能解析匹配到的第一个节点下的值，也就是作用于list时只匹配第一个
>>print tree.xpath('string(//li)')
>>时间
```

**local-name：解析节点名称**
```python
>>print tree.xpath('local-name(//*[@id="testid"])') #local-name解析节点名称
>>div
```

**contains(string1,string2)：如果 string1 包含 string2，则返回 true，否则返回 false**
```python
>>tree.xpath('//h3[contains(text(),"H3")]/a/text()')[0] #使用字符内容来辅助定位
>>百度一下
```

一记组合拳
```python
>>#匹配带有href属性的a标签的先辈节点中的div，其兄弟节点中前一个div节点下ul下li中text属性包含“务”字的节点的值
>>print tree.xpath(u'//a[@href]/ancestor::div/preceding::div/ul/li[contains(text(),"务")]/text()')[0]
>>任务
注意：兄弟节点后一个节点可以使用：following-sibling
```

**not：布尔值（否）**
```python
>>print tree.xpath('count(//li[not(@data)])') #不包含data属性的li标签统计
>>18.0
```

**string-length：返回指定字符串的长度**
```python
>>#string-length函数+local-name函数定位节点名长度小于2的元素
>>print tree.xpath('//*[string-length(local-name())<2]/text()')[0]
>>百度一下
```

组合拳2
```python
>>#contains函数+local-name函数定位节点名包含di的元素
>>print tree.xpath('//div[@id="testid"]/following::div[contains(local-name(),"di")]')
>>[<Element div at 0x225e108>, <Element div at 0x225e0c8>]
```

**or：多条件匹配**
```python
>>print tree.xpath('//li[@data="one" or @code="84"]/text()') #or匹配多个条件
>>['1', '84']
>>#也可使用|
>>print tree.xpath('//li[@data="one"]/text() | //li[@code="84"]/text()') #|匹配多个条件
>>['1', '84']
```

```python
组合拳3：floor + div除法 + ceiling
>>#position定位+last+div除法，选取中间两个
>>tree.xpath('//div[@id="go"]/ul/li[position()=floor(last() div 2+0.5) or position()=ceiling(last() div 2+0.5)]/text()')
>>['5', '6']


组合拳4隔行定位：position+mod取余
>>#position+取余运算隔行定位
>>tree.xpath('//div[@id="go"]/ul/li[position()=((position() mod 2)=0)]/text()')
```

**starts-with：以。。开始**
```python
>>#starts-with定位属性值以8开头的li元素
>>print tree.xpath('//li[starts-with(@code,"8")]/text()')[0]
>>84
```

##### 8、数值比较
**<：小于**
```python
>>#所有li的code属性小于200的节点
>>print tree.xpath('//li[@code<200]/text()')
>>['84', '104']
```

**div：对某两个节点的**
```python
属性值做除法
>>print tree.xpath('//div[@id="testid"]/ul/li[3]/@code div //div[@id="testid"]/ul/li[1]/@code')
>>2.65476190476
```

组合拳4：根据节点下的某一节点数量定位
```python
>>#选取所有ul下li节点数大于5的ul节点
>>print tree.xpath('//ul[count(li)>5]/li/text()')
>>['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
```

##### 9、将对象还原为字符串
```python
>>> s = tree.xpath('//*[@id="testid"]')[0] #使用xpath定位一个节点
>>> s
<Element div at 0x2b6ffc8>
>>> s2 = etree.tostring(s) #还原这个对象为html字符串
>>> s2
'<div id="testid">\n\t\t<h2>&#213;&#226;&#192;&#239;&#202;&#199;&#184;&#246;&#208;&#161;&#177;&#234;&#204;&#226;</h2>\n\t\t<ol>\n\t\t\t<li data="one">1</li>\n\t\t\t<li data="two">2</li>\n\t\t\t<li data="three">3</li>\n\t\t</ol>\n\t\t<ul>\n\t\t\t<li code="84">84</li>\n\t\t\t<li code="104">104</li>\n\t\t\t<li code="223">223</li>\n\t\t</ul>\n\t</div>\n\t'
```

##### 10、选取一个属性中的多个值
```python
举例：<div class="mp-city-list-container mp-privince-city" mp-role="provinceCityList">
选择这个div的方案网上有说用and的，但是似乎只能针对不同的属性的单个值,本次使用contains
>>.xpath('div[contains(@class,"mp-city-list-container mp-privince-city")]')
>>当然也可以直接选取其属性的第二个值
>>.xpath('div[contains(@class,"mp-privince-city")]')
>>重点是class需要添加一个@符号
本次验证否定了网上的and，使用了contains,验证环境在scrapy的response.xpath下
```

以上就是目前我整理出的全部内容，说明一点，xpath虽快，但是使用时尽量使用简洁高效的方式，本文旨在定位那些较难的地方使用，刻意追求晦涩难懂的技巧会影响其效率，并不可取。


https://blog.csdn.net/gongbing798930123/article/details/78955597
https://blog.csdn.net/u013332124/article/details/80621638
https://www.jianshu.com/p/1575db75670f

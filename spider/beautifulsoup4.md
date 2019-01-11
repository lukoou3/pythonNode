## Beautiful Soup
Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式.Beautiful Soup会帮你节省数小时甚至数天的工作时间.  
官方中文文档：https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

## 安装 Beautiful Soup
#### 安装beautifulsoup4
* 通过pip安装:   
pip install beautifulsoup4
* 下载[BS4的源码](http://www.crummy.com/software/BeautifulSoup/download/4.x/ "BS4的源码"),然后通过setup.py来安装    
Python setup.py install

#### 安装解析器
Beautiful Soup支持Python标准库中的HTML解析器,还支持一些第三方的解析器,其中一个是 lxml .根据操作系统不同,可以选择下列方法来安装lxml:    
`$ pip install lxml`

另一个可供选择的解析器是纯Python实现的 html5lib , html5lib的解析方式与浏览器相同,可以选择下列方法来安装html5lib:    
`$ pip install html5lib`

下表列出了主要的解析器,以及它们的优缺点:

| 解析器           | 使用方法                             | 优势                                                            | 劣势                                            |
| ---------------- | ------------------------------------ | --------------------------------------------------------------- | ----------------------------------------------- |
| Python标准库     | BeautifulSoup(markup, "html.parser") | Python的内置标准库<br/>执行速度适中<br/>文档容错能力强          | Python 2.7.3 or 3.2.2)前 的版本中文档容错能力差 |
| lxml HTML 解析器 | BeautifulSoup(markup, "lxml")        | 速度快<br/>文档容错能力强                                       | 需要安装C语言库                                 |
| lxml XML 解析器  | BeautifulSoup(markup, "xml")         | 速度快<br/>唯一支持XML的解析器                                  | 需要安装C语言库                                 |
| html5lib         | BeautifulSoup(markup, "html5lib")    | 最好的容错性<br/>以浏览器的方式解析文档<br/>生成HTML5格式的文档 | 速度慢<br/>不依赖外部扩展                       | 

推荐使用lxml作为解析器,因为效率更高. 在Python2.7.3之前的版本和Python3中3.2.2之前的版本,必须安装lxml或html5lib, 因为那些Python版本的标准库中内置的HTML解析方法不够稳定.

## 如何使用
将一段文档传入BeautifulSoup 的构造方法,就能得到一个文档的对象, 可以传入一段字符串或一个文件句柄.
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("index.html"))

soup = BeautifulSoup("<html>data</html>")
```







































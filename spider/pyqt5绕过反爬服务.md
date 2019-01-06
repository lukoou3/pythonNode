https://blog.csdn.net/qq_39802740/article/details/82184781
当遇到使用selenium被网站识别为robot的时候，首先考虑的是换chromedriver,geckodriver,iedriver等
如果都行不通
那么请尝试使用pyqt5
pyqt5不仅可以做界面，他还可以调用强大的QtWebKit模块,QtWebKit是一个基于开源项目 ，WebKit的网页内容渲染引擎，借助该引擎可以更加快捷地将万维 网集成到 Qt 应用中。


可以发现使用pyqt5的时候淘宝官网并没有发现你是使用的第三方浏览器插件。
接下来我们就可以做我们该做的事情。
这里注意一下，pyqt5驱动的浏览器，只能通过注入js来操作页面，这里对js的熟练度要求就比较高了，比如利用js拖动滑块验证等。
简易的打开pyqt5浏览器的代码，js需要自己多多练习，比如抓取数据等。

```python
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

app = QApplication([])
view = QWebEngineView()
view.load(QUrl("http://www.taobao.com/"))
view.show()
page = view.page()

def test():
	page.runjavascript("your javascript")

view.loadFinished.connect(test)

app.exec_()
```

selenium的功能还是比pyqt5的浏览器强大很多，但是在无法绕过反爬虫服务的情况下，可以考虑一下pyqt5，比如一打开selenium就被识别出来，distil networks这种反爬虫服务商，pyqt5是集成的chromium内核源码，因此不会被识别，但是注入js来操控爬虫的方式有点蛋疼，还需多多学习

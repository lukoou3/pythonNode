## 运行生成的代码：
可能是：
```python
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        ...
        #MainWindow.setCentralWidget(self.centralwidget)
        ...
        #MainWindow.setMenuBar(self.menubar)
        ...
        #MainWindow.setStatusBar(self.statusbar)
        ...

    def retranslateUi(self, MainWindow):
        ...
```
可能是：
```python
class Ui_Form(object):
    def setupUi(self, Form):
        ...

    def retranslateUi(self, Form):
        ...
```

我们会发现运行这段代码，窗口是不会出现的。如何使窗口出现呢？下面需要添加一段代码
```python
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()#或者ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
```
**注意：第一种情况生成的代码需要注释3行**

## 实现代码与界面分离
新建一个文件，导入我们设计的untitled .py文件，实现代码与界面分离：
```python
from PyQt5 import QtWidgets
from untitled import Ui_Form
 
class mywindow(QtWidgets.QWidget):
    def __init__(self):
        super(mywindow,self).__init__()
        self.new=Ui_Form()
        self.new.setupUi(self)
 
if __name__=="__main__":
    import sys
 
    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())

```
直接继承界面类：
```python
from PyQt5 import QtWidgets
from untitled import Ui_Form
 
class mywindow(QtWidgets.QWidget,Ui_Form):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
 
if __name__=="__main__":
    import sys
 
    app=QtWidgets.QApplication(sys.argv)
    myshow=mywindow()
    myshow.show()
    sys.exit(app.exec_())
```

#### QScrollArea
很多刚接触QScrollArea的朋友，不知道如何使用QScrollArea，以至于无法显示滚动条。

首先QScrollArea类提供了关于另一个窗口的滚动的视图。一个滚动区域通常用来显示在frame中的子窗口。如果这个子窗口超过了frame的大小，这个视图就会自动提供滚动条，这样子窗口的整个内容，都可以被用户看到。这个子窗口必须被指定函数setWidget()。















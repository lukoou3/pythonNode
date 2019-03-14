## PyQt中MainWindow, QWidget以及Dialog的区别和选择
#### 1. Qt界面分类
在Qt Designer设计界面时，首先需要选择界面模板，主要分为三个类： 
1. Main Window 
2. Widget 
3. Dialog 

#### 2. 三种模板的区别(官方文档介绍)
###### MainWindow

QMainWindow类提供一个有菜单条、锚接窗口（例如工具条）和一个状态条的主应用程序窗口。

主窗口通常用在提供一个大的中央窗口部件（例如文本编辑或者绘制画布）以及周围菜单、工具条和一个状态条。QMainWindow常常被继承，因为这使得封装中央部件、菜单和工具条以及窗口状态变得更容易。继承使创建当用户点击菜单项或者工具条按钮时被调用的槽成为可能。你也可以使用Qt设计器来创建主窗口。我们将简要地回顾一下有关添加菜单项和工具条按钮，然后描述QMainWindow自己的便捷。

###### Widget

QWidget类是所有用户界面对象的基类。

窗口部件是用户界面的一个原子：它从窗口系统接收鼠标、键盘和其它事件，并且在屏幕上绘制自己的表现。每一个窗口部件都是矩形，并且它们按Z轴顺序排列的。一个窗口部件可以被它的父窗口部件或者它前面的窗口部件盖住一部分。

QWidget有很多成员函数，但是它们中的一些有少量的直接功能：例如，QWidget有一个字体属性，但是它自己从来不用。有很多继承它的子类提供了实际的功能，比如QPushButton、QListBox和QTabDialog等等。

###### Dialog

QDialog是最普通的顶级窗口。

不被嵌入到一个父窗口部件的窗口部件被叫做顶级窗口部件。通常情况下，顶级窗口部件是有框架和标题栏的窗口（尽管如果使用了一定的窗口部件标记，创建顶级窗口部件时也可能没有这些装饰。）在Qt中，QMainWindow和和不同的QDialog的子类是最普通的顶级窗口。 
一个没有父窗口部件的窗口部件一直是顶级窗口部件。

#### 3. 选择
大致理解是： 
QMainWindow是完整的窗体，在window上可以加入widget，适合于完整的项目，因为它封装了toolbar，statusbar，central widget，docking area。

QWidget是raw widget，widget也可以容纳其他的widget，但是注意setCentralWidget是只能由mainwindow类调用的。

QDialog派生自QWidget，是顶级窗口，功能也最基础。

#### 4. 在PyQt中初始化类的区别
QMainWindow
```python
from test.py import Ui_MainWindow #通过pyuic产生的test.py中生成类
class mywindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(mywindow,self).__init__(parent)
        self.setupUi(self)
```
QWidget
```python
from test import Ui_Widget 
from PyQt5 import QtWidgets

class mywindow(QtWidgets.QWidget,Ui_Widget):
    def __init__(self,parent = None):
        super(mywindow,self).__init__(parent)
        self.setupUi(self)
```











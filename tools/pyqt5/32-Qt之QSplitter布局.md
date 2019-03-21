## 
PyQt还提供了特殊的布局管理器QSplitter。它可以动态地拖动子控件之间的边界，算是一个动态的布局管理器，QSplitter允许用户拖动子控件的边界控制子控件的大小，并提供一个处理拖曳子控件的控制器 
在QSplitter对象中各子控件默认是横向布局的，可以使用Qt，Vertical进行垂直布局

## QSplitter类中常用的方法
| 方法             | 描述                                            |
| ---------------- | ----------------------------------------------- |
| addWidget()      | 将小控件添加到QSplitter管理器的布局中           |
| indexOf()        | 返回小控件在QSplitter管理器中的索引             |
| insertWidget()   | 根据指定的索引将一个控件插入到QSplitter管理器中 |
| setOrientation() | 设置布局的方向                                  |
|                  | Qt.Horizontal:水平方向                          |
|                  | Qt.Vertical:垂直方向                            |
| setSizes()       | 设置控件的初始大小                              |
| count()          | 返回小控件在QSplitter管理器中的数量             |


## 使用
#### 基本使用
![20180815155134162](/assets/20180815155134162.png)
```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SplitterExample(QWidget):
    def __init__(self):
        super(SplitterExample, self).__init__()
        self.initUI()

    def initUI( self ):
        #设置全局布局为水平布局，设置标题与初始大小窗口
        hbox=QHBoxLayout()
        self.setWindowTitle("QSplitter例子")
        self.setGeometry(300,300,300,200)

        #实例化QFrame控件
        topLeft=QFrame()
        topLeft.setFrameShape(QFrame.StyledPanel)

        bottom=QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)

        #实例化QSplitter控件并设置初始为水平方向布局
        splitter1=QSplitter(Qt.Horizontal)
        textedit=QTextEdit()

        #向Splitter内添加控件。并设置游戏的初始大小
        splitter1.addWidget(topLeft)
        splitter1.addWidget(textedit)
        splitter1.setSizes([100,200])

        #实例化Splitter管理器，添加控件到其中，设置垂直方向
        splitter2=QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        #设置窗体全局布局以及子布局的添加
        hbox.addWidget(splitter2)
        self.setLayout(hbox)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=SplitterExample()
    demo.show()
    sys.exit(app.exec_())
```

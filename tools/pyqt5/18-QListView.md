## QListView
QlistView类用于展示数据，它的子类是QListWIdget。QListView是基于模型（Model）的，需要程序来建立模型，然后再保存数据 

QListWidget是一个升级版本的QListView，它已经建立了一个数据储存模型（QListWidgetItem），直接调用addItem（）函数，就可以添加条目（Item）

QListView是基于Model，而QListWidget是基于Item。
#### QListView类中常用的方法
| 方法           | 描述                                                               |
| -------------- | ------------------------------------------------------------------ |
| setModel()     | 用来设置View所关联的Model，可以使用Python原生的list作为数据源Model |
| selectedItem() | 选中Model的条目                                                    |
| isSelected()   | 判断Model中的某条目是否被选中                                      |

#### QListView的常用信号
| 信号          | 含义                     |
| ------------- | ------------------------ |
| clicked       | 当单击某项时，信号被发射 |
| doubleClicked | 当双击某项时，信号被发射 |

#### 实例：QListView的使用
###### QStringListView的使用：
```python
from PyQt5.QtWidgets import   QMessageBox,QListView, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QStandardItem,QStandardItemModel
from PyQt5.QtCore import QStringListModel,QAbstractListModel,QModelIndex,QSize
import sys

class WindowClass(QMainWindow):
    def __init__(self,parent=None):
        super(WindowClass, self).__init__(parent)
        self.layout=QVBoxLayout()
        self.resize(200,300)
        listModel=QStringListModel()
        listView=QListView()
        items=["张三","李四","小明","JONES"]
        
        listModel.setStringList(items)
        listView.setModel(listModel)
        
        listView.clicked.connect(self.checkItem)

        self.layout.addWidget(listView)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def  checkItem(self,index):
         QMessageBox.information(self,"ListView","选择项是：%d"%(index.row()))

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())
```
![1499671-20181206155754114-605751854](/assets/1499671-20181206155754114-605751854.png)

###### QIconListView的使用：
```python
from PyQt5.QtWidgets import   QMessageBox,QListView, QStatusBar,  QMenuBar,QMenu,QAction,QLineEdit,QStyle,QFormLayout,   QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QStandardItem,QStandardItemModel
from PyQt5.QtCore import QStringListModel,QAbstractListModel,QModelIndex,QSize
import sys

class WindowClass(QMainWindow):
    def __init__(self,parent=None):
        super(WindowClass, self).__init__(parent)
        self.layout=QVBoxLayout()
        self.resize(200,300)
        listView=QListView()
        listView.setViewMode(QListView.ListMode)#或者使用QListView.IconMode  QListView.ListMode
        #listView.setMovement(QListView.Static)
        listView.setIconSize(QSize(20,20))#图标的大小（原始图标大小如果100,100，此时设置草果原始大小则失效）
        listView.setGridSize(QSize(60,40))#每个选项所在网格大小（每个选项外层grid宽高）
        listView.setMaximumHeight(200)#listView整体最大高度
        #listView.setMinimumSize(QSize(200,200))#listView最小面积（一般如果设置最大高和宽属性后就不设置这个属性了）
        #listView.setMaximumSize(QSize(500,500))#listVIew最大面积（一般如果设置最大高和宽属性后就不设置这个属性了）
        listView.setMinimumHeight(120)#listView最小高度

        listView.setResizeMode(QListView.Adjust)
        #listView.setMovement(QListView.Static)#设置图标可不可以移动，默认是可移动的，但可以改成静态的：

        self.item_1=QStandardItem(QIcon("./image/save.ico"), "普通员工A");
        self.item_2 = QStandardItem(QIcon("./image/save.ico"), "普通员工B");

        model=QStandardItemModel()
        model.appendRow(self.item_1)
        model.appendRow(self.item_2)
        listView.setModel(model)

        listView.clicked.connect(self.checkItem)

        self.layout.addWidget(listView)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


    def  checkItem(self,index):
         QMessageBox.information(self,"ListView","选择项是：%d"%(index.row()))

if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())
```
![1499671-20181206155918726-1285768498](/assets/1499671-20181206155918726-1285768498.png)

## 自定义实现QListView
#### 总体介绍
QListView类为模型提供了一个列表或图标视图。
![v2-6597cf966c04fa6644cc1e400c59f54b_hd](/assets/v2-6597cf966c04fa6644cc1e400c59f54b_hd.jpg)

QListView呈现存储在模型（Model）中的项目，可以是简单的非层次列表，也可以是图标集合。该类用于提供以前由QListBox和QIconView类提供的列表和图标视图，但是使用Qt的模型/视图体系结构提供的更灵活的方法。

**注：模型/视图体系结构是PyQt5中一个十分重要的概念。**

QListView类是模型/视图类之一，是Qt的模型/视图框架的一部分。

该视图不显示水平或垂直标题；要显示带有水平标题的项目列表，请改为使用QTreeView。

QListView实现由QAbstractItemView类定义的接口，以允许其显示由QAbstractItemModel类派生的模型提供的数据。

列表视图中的项目可以使用以下两种视图模式之一显示：在ListMode中，项目以简单列表的形式显示；在IconMode中，列表视图采用图标视图的形式，在图标视图中，项目通过文件管理器中的文件等图标显示。默认情况下，列表视图在ListMode中。要更改视图模式，请使用setViewMode()函数，并确定当前视图模式，请使用viewMode()。

这些视图中的项目按列表视图的flow()指定的方向布置。根据视图的movement()状态，这些项目可能会固定或允许移动。

如果模型中的项目不能在流动方向上完全布置，则可以将其分割在视图窗口的边界处；这取决于isWrapping()。当图标视图表示项目时，此属性非常有用。

“如果模型中的项目不能在流动方向上完全布置”，这句话是什么意思？

如果flow()为LeftToRight，则项目将从左至右排列。 如果isWrapping属性为True，则布局将在到达可见区域的右侧时进行换行。 如果此属性为TopToBottom，则项目将从可见区域的顶部进行布局，并在到达底部时进行分割。

resizeMode()和layoutMode()控制项目布局的方式和时间。项目根据其 gridSize()进行间隔，并且可以存在于由gridSize()指定的大小的名义网格内。这些项目可以根据它们的iconSize()而呈现为大图标或小图标。

**成员类型文档**:
![v2-59eadb351911f8c1328ebf0c930b1c5c_hd](/assets/v2-59eadb351911f8c1328ebf0c930b1c5c_hd.jpg)

**类归属**
PyQt5->QtWidgets->QListView

**继承关系**
继承：QAbstractItemView

被继承：QHelpIndexWidget、QListWidget 和 QUndoView

更多详细的介绍请见官网：[QListView](https://doc.qt.io/qt-5/qlistview.html "QListView")












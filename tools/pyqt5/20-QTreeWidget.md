## QTreeWidget
和 QTableWidget类似，一般步骤是先创建一个 QTreeWidget实例，然后设置列数，然后再添加 。

#### QTreeWidget类中的常用方法
| 方法                                 | 描述                                                              |
| ------------------------------------ | ----------------------------------------------------------------- |
| setColumnWidth(int column,int width) | 将指定列的宽度设置为给定的值；Column：指定的列，width：指定的宽度 |
| insertTopLevelItems()                | 在视图的顶层索引中引入项目的列表                                  |
| expandAll()                          | 展开所有节点的树形节点                                            |
| invisibleRootItem()                  | 返回树形控件中不可见的根选项（Root Item）                         |
| selectionItems()                     | 返回所有选定的非隐藏项目的列表内                                  |

#### QTreeWidgetItem类中常用的方法
| 方法                        | 描述                                           |
| --------------------------- | ---------------------------------------------- |
| addChild()                  | 将子项追加到子列表中                           |
| setText()                   | 设置显示的节点文本                             |
| Text()                      | 返回显示的节点文本                             |
| setCheckState(column.state) | 设置指定列的选中状态：Qt.Checked、Qt.Unchecked |
| setIcon(column,icon)        | 在指定的列中显示图标                           |

如下是 pyqt5 的 QTreeWidget 工具调用节点的部分命令，备用：
```python
self.tree = QTreeWidget()

self.tree.topLevelItem(0)；最顶级节点，指定第1个顶级节点；节点编号从0开始。

self.tree.currentItem()；当前节点

self.tree.selectedItems()；鼠标选中的当前节点

self.tree.topLevelItemCount()；最顶级节点的总数

self.tree.topLevelItem(0).child(0)；第1个最顶级节点的第1个子节点

self.tree.topLevelItem(0).child(0).child(0)；第1个最顶级节点的第1个子节点的第1个子节点

self.tree.currentItem().parent()；鼠标选中的当前节点的父节点

self.tree.currentItem().child(0)；鼠标选中的当前节点的第1个子节点

self.tree.currentItem().parent().childCount()；鼠标选中的当前节点的同级节点的总数量

self.tree.expandItem(self.tree.topLevelItem(0))；展开指定节点，指定展开第1个顶级节点

self.tree.collapseItem(self.tree.topLevelItem(0))；收起指定节点，指定收起第1个顶级节点
```

#### 总体介绍
QTreeWidget类提供了一个使用预定义树模型的树视图。

QTreeWidget类是一个十方方便使用的类，它提供了一个标准的Tree小部件，如下图所示的界面。该类基于Qt的Model / View架构，并使用默认模型来保存项目，每一个都是一个QTreeWidgetItem。

不需要Model / View框架灵活性的开发人员可以使用此类轻松创建简单的分层列表。更灵活的方法是将QTreeView与标准项目模型相结合。这允许将数据的存储与其表示分开。

在其最简单的形式中，可以通过以下方式构建树小部件：
```python
treeWidget = QTreeWidget(self)
treeWidget.setColumnCount(1)
root = QTreeWidgetItem(treeWidget)
for i in range(10):
    item = QTreeWidgetItem(root)
    item.setText(0, str(i))
    root.addChild(item)
```
在将项目添加到树部件之前，必须使用setColumnCount()设置列的数量。这允许每个物品具有一个或多个标签或其他装饰。使用的列数可以通过columnCount()函数找到。

该树可以包含一个标题，其中包含控件中每个列的部分。通过使用setHeaderLabels()提供字符串列表来设置每个部分的标签是最容易的，但是可以使用QTreeWidgetItem构造自定义标头并使用setHeaderItem()函数将其插入树中。

树中的项目可以根据预定义的排序顺序按列排序。如果启用排序，则用户可以通过单击列标题来排序项目。可以通过调用setSortingEnabled()来启用或禁用排序。 isSortingEnabled()函数指示是否启用排序。

**类归属**
PyQt5->QtWidgets->QTreeWidget

**继承关系**
PyQt5->QtWidgets->QWidget->QFrame->QAbstractScrollArea->QAbstractItemView->QTreeView->QTreeWidget

更多详细的介绍请见官网：[QTreeWidget](https://doc.qt.io/qt-5/qtreewidget.html "QTreeWidget")

#### 实例
###### QTreeWidget最简单的例子
实现效果：
![1362577-20180511120659834-290580694](/assets/1362577-20180511120659834-290580694.png)
```python
import sys
from PyQt4.QtGui import *

class TreeWidget(QMainWindow):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.setWindowTitle('TreeWidget')
        self.tree = QTreeWidget()  # 实例化一个TreeWidget对象
        self.tree.setColumnCount(2)  # 设置部件的列数为2
        self.tree.setHeaderLabels(['Key', 'Value'])  # 设置头部信息对应列的标识符

        # 设置root为self.tree的子树，故root是根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'root')  # 设置根节点的名称

        # 为root节点设置子结点
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'child1')
        child1.setText(1, 'name1')
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, 'name2')
        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'child3')
        child4 = QTreeWidgetItem(child3)
        child4.setText(0, 'child4')
        child4.setText(1, 'name4')

        self.tree.addTopLevelItem(root)
        self.setCentralWidget(self.tree)  # 将tree部件设置为该窗口的核心框架

app = QApplication(sys.argv)
app.aboutToQuit.connect(app.deleteLater)
tp = TreeWidget()
tp.show()
app.exec_()
```

###### QTreeWidget带图标与样式的例子
代码：
```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt

class TreeWidgetDemo(QMainWindow):
    def __init__(self, parent=None):
        super(TreeWidgetDemo, self).__init__(parent)
        self.setWindowTitle('TreeWidget 例子')

        self.tree=QTreeWidget()
        #设置列数
        self.tree.setColumnCount(2)
        #设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key','Value'])

        #设置根节点
        root=QTreeWidgetItem(self.tree)
        root.setText(0,'Root')
        root.setIcon(0,QIcon('./images/root.png'))

        # todo 优化2 设置根节点的背景颜色
        brush_red=QBrush(Qt.red)
        root.setBackground(0,brush_red)
        brush_blue=QBrush(Qt.blue)
        root.setBackground(1,brush_blue)

        #设置树形控件的列的宽度
        self.tree.setColumnWidth(0,150)

        #设置子节点1
        child1=QTreeWidgetItem()
        child1.setText(0,'child1')
        child1.setText(1,'ios')
        child1.setIcon(0,QIcon('./images/IOS.png'))

        #todo 优化1 设置节点的状态
        child1.setCheckState(0,Qt.Checked)

        root.addChild(child1)

        #设置子节点2
        child2=QTreeWidgetItem(root)
        child2.setText(0,'child2')
        child2.setText(1,'')
        child2.setIcon(0,QIcon('./images/android.png'))

        #设置子节点3
        child3=QTreeWidgetItem(child2)
        child3.setText(0,'child3')
        child3.setText(1,'android')
        child3.setIcon(0,QIcon('./images/music.png'))

        #加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(root)

        #TODO 优化3 给节点添加响应事件
        self.tree.clicked.connect(self.onClicked)

        #节点全部展开
        self.tree.expandAll()
        self.setCentralWidget(self.tree)

    def onClicked(self,qmodeLindex):
        item=self.tree.currentItem()
        print('Key=%s,value=%s'%(item.text(0),item.text(1)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = TreeWidgetDemo()
    tree.show()
    sys.exit(app.exec_())
```
初始运行图如下 
![20180814153927914](/assets/20180814153927914.png)

优化一：设置节点的状态
这里添加了child1的选中状态
```python
child1.setCheckState(0,Qt.Checked)
```
![20180814154208598](/assets/20180814154208598.png)

优化二：设置节点的背景颜色
这里设置了根节点的背景颜色
```python
brush_red=QBrush(Qt.red)
        root.setBackground(0,brush_red)
        brush_blue=QBrush(Qt.blue)
        root.setBackground(1,brush_blue)
```
![201808141543289](/assets/201808141543289.png)

优化三：给节点添加响应事件
点击，会在控制台输出当前地key值与value值
```python
self.tree.clicked.connect(self.onClicked)
def onClicked(self,qmodeLindex):
        item=self.tree.currentItem()
        print('Key=%s,value=%s'%(item.text(0),item.text(1)))
```

###### QTreeView显示文件系统盘的树列表
在上面的例子中，QTreeWidgetItem类的节点是一个个添加上去的，这样有时很不方便，特别是窗口产生比较复杂的树形结构时，一般都是通过QTreeView类来实现的，而不是QTreeWidget类，QTreeView和QTreeWidget类最大的区别就是，QTreeView类可以使用操作系统提供的定制模式，比如文件系统盘的树列表
```python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

if __name__ == '__main__':
    app=QApplication(sys.argv)

    #window系统提供的模式
    model=QDirModel()
    #创建一个QTreeView的控件
    tree=QTreeView()
    #为控件添加模式
    tree.setModel(model)

    tree.setWindowTitle('QTreeView例子')
    tree.resize(640,480)

    tree.show()
    sys.exit(app.exec_())
```
![20180814155133402](/assets/20180814155133402.png)





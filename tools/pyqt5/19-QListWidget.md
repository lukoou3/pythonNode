## QListWidget
QListView是基于Model，而QListWidget是基于Item。
QListWidget类是一个基于条目的接口，用于从列表中添加或删除条目，列表中的每个条目都是一个QListWidgetItem对象，QListWidget可以设置为多重选择

#### QListWidget类中常用的方法
| 方法             | 描述                                    |
| ---------------- | --------------------------------------- |
| addItem()        | 在列表中添加QListWidgetItem对象或字符串 |
| addItems()       | 添加列表中的每个条目                    |
| insertItem()     | 在指定地索引处插入条目                  |
| clear()          | 删除列表的内容                          |
| setCurrentItem() | 设置当前所选的条目                      |
| sortItems()      | 按升序重新排列条目                      |

#### QLIstWidget类中常用的信号
| currentItemChanged | 当列表中的条目发生改变时发射此信号 |
| ------------------ | ---------------------------------- |
| itemClicked        | 当点击列表中的条目时发射此信号     |

最简单的QListWidget例子：
```python
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ListWidget(QListWidget):
    def clicked(self, item):
        QMessageBox.information(self, "ListWidget", "你选择了: " + item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #实例化对象，目的只是单纯的使用里面的槽函数............
    listWidget = ListWidget()

    #设置初始大小，增加条目，设置标题
    listWidget.resize(300, 120)
    listWidget.addItem("Item 1")
    listWidget.addItem("Item 2")
    listWidget.addItem("Item 3")
    listWidget.addItem("Item 4")
    listWidget.setWindowTitle('QListwidget 例子')

    #单击触发绑定的槽函数
    listWidget.itemClicked.connect(listWidget.clicked)


    listWidget.show()
    sys.exit(app.exec_())
```
效果如下 
![20180813095839197](/assets/20180813095839197.png)

#### 总体介绍
QListWidget类提供了一个基于项目(Item)的列表小部件。

QListWidget是一个使用十分方便的类，它提供了一个类似于QListView提供的列表视图，但具有用于添加和移除项目的功能。 QListWidget使用内部模型来管理列表中的每个QListWidgetItem。

对于更灵活的列表视图窗口小部件，请使用带有标准模型的QListView类。

列表小部件的构建方式与其他小部件相同：
```python
listWidget = QListWidget(self)
```
列表小部件的selectionMode()确定可以同时选择列表中的多少个项目，以及是否可以创建项目的复杂选择。这可以使用setSelectionMode()函数进行设置。

有两种方法可以将项目添加到列表中：可以使用列表窗口小部件作为其父窗口小部件来构建它们，也可以在没有父窗口小部件的情况下构建它们，并在稍后将其添加到列表中。如果在构建项目时已经存在列表小部件，则第一种方法更易于使用：
```python
QListWidgetItem("Oak", listWidget)
QListWidgetItem("Fir", listWidget)
QListWidgetItem("Pine", listWidget)
```

如果您需要将新项目插入到特定位置的列表中，则应该在没有父窗口小部件的情况下构建它。然后应该使用insertItem()函数将它放在列表中。列表小部件将取得该项目的所有权。
```python
newItem = QListWidgetItem()
newItem.setText("新项目")
listwidget.insertItem(row, newItem)
```

对于多个项目，可以使用insertItems()代替。

使用count()函数可以找到列表中的项目数。

要从列表中删除项目，请使用takeItem()。

列表中的当前项目可以通过currentItem()找到，并可以通过setCurrentItem()更改。用户还可以通过使用键盘导航或点击不同的项目来更改当前项目。当前项目更改时，currentItemChanged()信号将与新的当前项目和先前当前的项目一起发送。

**类归属**
PyQt5->QtWidgets->QListWidget

**继承关系**
继承：QListView

更多详细的介绍请见官网：[QListWidget](https://doc.qt.io/qt-5/qlistwidget.html "QListWidget")

#### 模拟QQ例子
这次的QQ模拟与上次用QListView实现的相比较，做出了如下修改：

1、鼠标滑动QQ联系人出现过渡效果（这个不是本次重点，不做介绍，后面会专门介绍QSS）

2、会员红名专享

3、转移联系人到指定分组，菜单上不会出现联系人现在所在分组。

4、新增好友（只能在“我的好友”分组中新增，其它分组只能通过“我的好友”转移过去）

5、Ctrl键多选联系人实现批量删除与转移联系人

本次QQ的模拟实现，主要是通过QQ类、ListWidget类，还有一个Dialog_additem这个自定义类组成。同QListView实现的QQ模拟相比较，这里少了QAbstractListModel。为什么？因为已经和QListWidget融合了。至于Dialog_additem这个自定义类，主要是因为我们要新增联系人，至于怎么新增联系人呢？这里我们就通过对话框的形式来实现了。

下面我们重点介绍一下这次实现的关键类ListWidget。本期的QQ类与上期相比较没有大的变化。Dialog_additem是用Qt设计师画的界面，然后生成对话框代码的，比较简单。这两个类不做详细讲解了。

###### ListWidget类
核心代码
```python
from PyQt5.QtWidgets import QListWidget, QMenu, QAction, QMessageBox, QListWidgetItem, QAbstractItemView
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QBrush
from Dialog_additem import Dialog_additem
import Random_Name, random
import sys

class ListWidget(QListWidget):

    map_listwidget = []

    def __init__(self):
        super().__init__()
        self.Data_init()
        self.Ui_init()

    def Data_init(self):
        randomnum = random.sample(range(26), 10)
        for i in randomnum:
            item = QListWidgetItem()
            randname = Random_Name.getname()
            randicon = "./res/"+ str(i) + ".jpg"
            font = QFont()
            font.setPointSize(16)
            item.setFont(font)
            item.setText(randname)
            flag = random.randint(0,5)
            if flag == 1:
                item.setForeground(QBrush(Qt.red))
                item.setToolTip('会员红名尊享')
            item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            item.setIcon(QIcon(randicon))
            self.addItem(item)
    
    def Ui_init(self):
        self.setIconSize(QSize(70,70))
        self.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                        "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                        "QListWidget::Item:hover{background:skyblue; }"
                        "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
                        )
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemSelectionChanged.connect(self.getListitems)
    
    def getListitems(self):
        return self.selectedItems()

    def contextMenuEvent(self, event):
        hitIndex = self.indexAt(event.pos()).column()
        if hitIndex > -1:
            pmenu = QMenu(self)
            pDeleteAct = QAction("删除",pmenu)
            pmenu.addAction(pDeleteAct)
            pDeleteAct.triggered.connect(self.deleteItemSlot)
            if self is self.find('我的好友'):
                pAddItem = QAction("新增好友",pmenu)
                pmenu.addAction(pAddItem)     
                pAddItem.triggered.connect(self.addItemSlot)
            if len(self.map_listwidget) > 1:
                pSubMenu = QMenu("转移联系人至" ,pmenu)
                pmenu.addMenu(pSubMenu)
                for item_dic in self.map_listwidget:
                    if item_dic['listwidget'] is not self:
                        pMoveAct = QAction(item_dic['groupname'] ,pmenu)
                        pSubMenu.addAction(pMoveAct)
                        pMoveAct.triggered.connect(self.move)
            pmenu.popup(self.mapToGlobal(event.pos()))
    
    def deleteItemSlot(self):
        dellist = self.getListitems()
        for delitem in dellist:
            del_item = self.takeItem(self.row(delitem))
            del del_item

    def addItemSlot(self):
        dg = Dialog_additem()
        r = dg.exec()
        if r > 0:
            newitem = QListWidgetItem()
            newname = dg.lineEdit.text()
            newicon = dg.geticonpath()
            font = QFont()
            font.setPointSize(16)
            newitem.setFont(font)
            newitem.setText(newname)
            newitem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            newitem.setIcon(QIcon(newicon))
            self.addItem(newitem)

    def setListMap(self, listwidget):
        self.map_listwidget.append(listwidget)

    def move(self):
        tolistwidget = self.find(self.sender().text())
        movelist = self.getListitems()
        for moveitem in movelist:
            pItem = self.takeItem(self.row(moveitem))
            tolistwidget.addItem(pItem)

    def find(self, pmenuname):
        for item_dic in self.map_listwidget:
            if item_dic['groupname'] == pmenuname:
                return item_dic['listwidget']
```
这个类我们实现了如下功能：

1、鼠标滑动QQ联系人出现过渡效果（这个不是本次重点，不做介绍，后面会专门介绍QSS）

2、会员红名专享

3、转移联系人到指定分组，菜单上不会出现联系人现在所在分组。

4、新增好友（只能在“我的好友”分组中新增，其它分组只能通过“我的好友”转移过去）

5、Ctrl键多选联系人实现批量删除与转移联系人

这里会详细介绍一下与QListView不同的地方的。

```python
map_listwidget = []
```
这个还是类变量，用于记录QListWidget对象与QToolBox分组名称的对应关系的。

```python
def Data_init(self):
    randomnum = random.sample(range(26), 10)
    for i in randomnum:
        item = QListWidgetItem()
        randname = Random_Name.getname()
        randicon = "./res/"+ str(i) + ".jpg"
        font = QFont()
        font.setPointSize(16)
        item.setFont(font)
        item.setText(randname)
        flag = random.randint(0,5)
        if flag == 1:
            item.setForeground(QBrush(Qt.red))
            item.setToolTip('会员红名尊享')
        item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        item.setIcon(QIcon(randicon))
        self.addItem(item)
```
数据初始化，随机生成会员红名等功能。

```python
item = QListWidgetItem()
randname = Random_Name.getname()
randicon = "./res/"+ str(i) + ".jpg"
```
这里我们新建一个QListWidgetItem对象，同时建立起该对象需要用到的名字和图标路径。

那么问题来了，**QListWidgetItem是什么？**

QListWidgetItem类提供了一个用于QListWidget项目视图类的项目。

QListWidgetItem表示QListWidget中的单个项目。每个项目可以保存多条信息，并将适当地显示它们。

项目视图（view）便捷类使用经典的基于项目（item）的界面而不是纯粹的模型/视图（model/view）方法。对于更灵活的列表视图小部件，请考虑使用带有标准模型的QListView类。

列表项通常用于text()和icon()显示文本和图标。这些用setText()和setIcon()函数设置。文本的外观可以用setFont()，setForeground()和setBackground()来定制。列表项中的文本可以使用setTextAlignment()函数进行对齐。工具提示，状态提示和“这是什么？”可以使用setToolTip()，setStatusTip()和setWhatsThis()将帮助添加到列表项中。

默认情况下，项目是可启用的，可选择的，可选定的，并且可以作为拖放操作的来源。

每个项目的标志都可以通过用适当的值调用setFlags()来改变(参见Qt.ItemFlags)。可以使用setCheckState()函数来设定选定，取消选定和半选的项目。相应的checkState()函数指示该项目的当前选定状态。

isHidden()函数可用于确定项目是否隐藏。要隐藏项目，请使用setHidden()。

当继承QListWidgetItem以提供自定义项目时，可以为它们定义新的类型（子类化），使它们可以与标准项目区分开来。对于需要此功能的子类，请确保在构造函数中使用等于或大于UserType的新类型值调用基类构造方法。


```python
font = QFont()
font.setPointSize(16)
item.setFont(font)
item.setText(randname)
```
这里我们设定每个项目（联系人）文本的大小以及内容（随机姓名）。

```python
flag = random.randint(0,5)
if flag == 1:
    item.setForeground(QBrush(Qt.red))
    item.setToolTip('会员红名尊享')
```
这个我们功能就是实现随机会员。setForeground()将列表项目的前景画笔设置为给定画笔，这里是红色，当然也可以是其它颜色，随你。

```python
item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
```
设置联系人名称的对其方式：水平、垂直居中。

```python
item.setIcon(QIcon(randicon))
self.addItem(item)
```
给每个联系人设置图标，然后新增到QListWidget当中。

该属性包含小部件的样式表

如Qt样式表文档中所述，样式表包含对窗口小部件样式的自定义的文本描述。

```python
def Ui_init(self):
    self.setIconSize(QSize(70,70))
    self.setStyleSheet("QListWidget{border:1px solid gray; color:black; }"
                    "QListWidget::Item{padding-top:20px; padding-bottom:4px; }"
                    "QListWidget::Item:hover{background:skyblue; }"
                    "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }"
                    )
    self.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.itemSelectionChanged.connect(self.getListitems)
```
这个函数我们做了一些界面上的设定，其中setStyleSheet()涉及到了QSS方面的知识，这里不做介绍。

```python
self.setSelectionMode(QAbstractItemView.ExtendedSelection)
```
这里我们设定了联系人的选择方式：
![v2-b5d8a6541b90ba79e88f4d20c95e4fe4_r](/assets/v2-b5d8a6541b90ba79e88f4d20c95e4fe4_r.jpg)

```python
self.itemSelectionChanged.connect(self.getListitems)
```
当选择的项目（联系人）改变时，发出此信号，这里我们返回被选中项目对象的列表。

```python
def getListitems(self):
    return self.selectedItems()
```
这里返回被选中的项目对象的列表。

```python
def contextMenuEvent(self, event):
    ...
```
这个实现上下文菜单的函数。

```python
def deleteItemSlot(self):
    dellist = self.getListitems()
    for delitem in dellist:
        del_item = self.takeItem(self.row(delitem))
        del del_item
```
在删除项目（联系人）的时候，我们根据选择的项目进行删除，删除使用takeItem()函数，其参数是当前项目的行号。我们同时在内存上将这个对象删除。

```python
def move(self):
    tolistwidget = self.find(self.sender().text())
    movelist = self.getListitems()
    for moveitem in movelist:
        pItem = self.takeItem(self.row(moveitem))
        tolistwidget.addItem(pItem)
```
这里转移思路和上期一致，获取已选的项目，删除后再增加。

```python
def addItemSlot(self):
    dg = Dialog_additem()
    r = dg.exec()
    if r > 0:
        newitem = QListWidgetItem()
        newname = dg.lineEdit.text()
        newicon = dg.geticonpath()
        font = QFont()
        font.setPointSize(16)
        newitem.setFont(font)
        newitem.setText(newname)
        newitem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        newitem.setIcon(QIcon(newicon))
        self.addItem(newitem)
```
这个就是我们新增联系人的函数。Dialog_additem是我们自定义的对话框类。这里的r值是我们按下OK或者Cancel的返回值，我们在Dialog_additem类中设定了按下OK键返回1，按下Cancel返回-1.若返回值大于0，则我们给QListWidget增加项目（item）。

###### QQ(QToolBox)类
```python
from PyQt5.QtWidgets import QApplication, QToolBox, QListView, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from ListWidget import ListWidget
from PyQt5.QtGui import QIcon
import sys

class QQ(QToolBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('QQ模拟')
        self.setWindowFlags(Qt.Dialog)
        self.setMinimumSize(200,600)
        self.setWhatsThis('这个一个模拟QQ软件')
        self.setWindowIcon(QIcon('./res/log.ico'))
        pListWidget = ListWidget()
        dic_list = {'listwidget':pListWidget, 'groupname':"我的好友"}
        pListWidget.setListMap(dic_list)
        self.addItem(pListWidget, "我的好友") 
        self.show()
    
    def contextMenuEvent(self, event):
        pmenu = QMenu(self)
        pAddGroupAct = QAction("添加分组", pmenu)
        pmenu.addAction(pAddGroupAct) 
        pAddGroupAct.triggered.connect(self.addGroupSlot)  
        pmenu.popup(self.mapToGlobal(event.pos()))
    
    def addGroupSlot(self):
        groupname = QInputDialog.getText(self, "输入分组名", "")
        if groupname[0] and groupname[1]: 
            pListWidget1 = ListWidget()
            self.addItem(pListWidget1, groupname[0])
            dic_list = {'listwidget':pListWidget1, 'groupname':groupname[0]}
            pListWidget1.setListMap(dic_list)
        elif groupname[0] == '' and groupname[1]:
            QMessageBox.warning(self, "警告", "我说你没有填写分组名哦~！")
    
app = QApplication(sys.argv)
qq = QQ()
sys.exit(app.exec_())
```

###### Dialog_additem(QDialog)类
Dialog用QT设计师设计，逻辑和界面分离。

Dialog_additem类：
```python
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from Ui_ui import Ui_Dialog


class Dialog_additem(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog_additem, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(300,150)
        self.flag = False#判断返回的联系人图标是默认的还是自定义的
        self.iconpath = ''
    
    @pyqtSlot(bool)
    def on_radioButton_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        self.flag = False
        if self.pushButton.isEnabled() == True:
            self.pushButton.setEnabled(False)
    
    @pyqtSlot(bool)
    def on_radioButton_2_toggled(self, checked):
        """
        Slot documentation goes here.
        
        @param checked DESCRIPTION
        @type bool
        """
        # TODO: not implemented yet
        # raise NotImplementedError
        self.flag = True
        if self.pushButton.isEnabled() == False:
            self.pushButton.setEnabled(True)
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #raise NotImplementedError
        fname = QFileDialog.getOpenFileName(self, '打开文件','./res/',("Images (*.png *.jpg)"))
        if fname[0]:
            self.iconpath = fname[0]
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        if len(self.lineEdit.text()) == 0:
            QMessageBox.information(self,'提示','好友姓名为空')
            self.lineEdit.setFocus()
        else:
            self.done(1)#给主窗口的返回值

    
    @pyqtSlot()
    def on_buttonBox_rejected(self):   
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.done(-1)#给主窗口的返回值

    def geticonpath(self):
        if self.flag == True:
            return self.iconpath
        else:
            return "./res/default.ico"
```
Ui_Dialog类：
```python
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(457, 180)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/log.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 9, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout_2.addWidget(self.radioButton_2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "学点编程吧--新增好友"))
        self.label.setText(_translate("Dialog", "好友昵称"))
        self.label_2.setText(_translate("Dialog", "好友图标（建议不要超过70*70）"))
        self.radioButton.setText(_translate("Dialog", "默认"))
        self.radioButton_2.setText(_translate("Dialog", "选择图标"))
        self.pushButton.setText(_translate("Dialog", "浏览"))
```
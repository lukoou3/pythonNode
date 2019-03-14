## 支持右键菜单功能
QWidget 及其子类均支持右键菜单功能，通过声明 ContextMenuPolicy 启用菜单

| 选项                  | 描述                                                                 |
| --------------------- | -------------------------------------------------------------------- |
| Qt.DefaultContextMenu | 默认菜单，重写 contextMenuEvent() 实现自定义                         |
| Qt.NoContextMenu      | 无菜单，事件响应传递给部件父级                                       |
| Qt.PreventContextMenu | 无菜单，事件响应不继续传递                                           |
| Qt.ActionsContextMenu | 事件菜单，只响应部件事件，部件子件的事件不响应                       |
| Qt.CustomContextMenu  | 用户自定义菜单，需绑定事件 customContextMenuRequested，并实现 槽函数 |

```python
# self inherit QWidget
self.setContextMenuPolicy(Qt.DefaultContextMenu)  # contextMenuEvent()
self.setContextMenuPolicy(Qt.NoContextMenu)
self.setContextMenuPolicy(Qt.PreventContextMenu)
self.setContextMenuPolicy(Qt.ActionsContextMenu)
self.setContextMenuPolicy(Qt.CustomContextMenu)  # customContextMenuRequested()
```

#### 1、实现用户菜单
```python
class handler_demo(QWidget, Ui_demo):
   def __init__(self):
       super().__init__()
       self.setupUi(self)

       # self inherit QWidget
       self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
       self.table_widget.customContextMenuRequested.connect(self.custom_right_menu)

   def custom_right_menu(self, pos):
       menu = QMenu()
       opt1 = menu.addAction("menu1")
       opt2 = menu.addAction("menu2")
       action = menu.exec_(self.table_widget.mapToGlobal(pos))
       if action == opt1:
           # do something
           return
       elif action == opt2:
           # do something
           return
       else:
           return

```

#### 2、使用事件菜单 # TODO
```python
class handler_demo(QWidget, Ui_demo):
   def __init__(self):
       super().__init__()
       self.setupUi(self)

       # self inherit QWidget
       self.table_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
       self.table_widget.customContextMenuRequested.connect(self.custom_right_menu)

   def custom_right_menu(self, pos):
       menu = QMenu()
       opt1 = menu.addAction("menu1")
       opt2 = menu.addAction("menu2")
       action = menu.exec_(self.table_widget.mapToGlobal(pos))
       if action == opt1:
           # do something
           return
       elif action == opt2:
           # do something
           return
       else:
           return

```

#### 3、重写默认菜单 # TODO
```python
class handler_demo(QWidget, Ui_demo):
   def __init__(self):
       super().__init__()
       self.setupUi(self)

   def contextMenuEvent(self, event):
       menu = QMenu()
       opt1 = menu.addAction("menu1")
       opt2 = menu.addAction("menu2")
       action = menu.exec_(self.table_widget.mapToGlobal(event.pos()))
       if action == opt1:
           # do something
           return
       elif action == opt2:
           # do something
           return

       menu.move(event.pos())
       menu.show()

```

#### QT中的相对位置，绝对位置之间的转换(mapToGlobal,mapFromGlobal)
1. 相对位置：每个Qwidget都能通过pos()获取到相对自己父类窗口的位置，

2. 绝对位置：pWidget->mapToGlobal(QPoint(0,0)) ;将当前控件的相对位置转换为屏幕绝对位置

3. 绝对位置转为相对位置： pWidget->mapFromGlobal(QPoint(0,0)), 将绝对位置对应到控件的相对位置。




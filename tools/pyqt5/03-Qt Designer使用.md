## PyQt5 Qt Designer (Qt设计师)
PyQt5是对Qt所有类进行封装, Qt能开发的东西, PyQt都能开发.
Qt是强大的GUI库之一, 用C++开发, 并且跨平台.
PyQt双许可证, 要么选择GPL(自由软件协议)将代码开源, 要么选择商业许可交商业许可费.
PySide拥有LGPL 2.1授权许可, 可开发 免费开源软件 和 私有商业软件. 把PyQt5代码切换到PySide2代码是相当容易的, 这也是为什么选择学习PyQt5的原因

#### 准备工作
安装PyQt5: pip install pyqt5
安装Qt工具: pip install pyqt5-tools
配置Qt工具系统环境变量: Path=C:\Code\Python_Vir\python1\Lib\site-packages\pyqt5_tools

#### Qt Designer (Qt设计师)使用简介
强大的可视化GUI设计工具, 帮助我们快速开发PyQt.
它生成UI界面为.ui文件, 通过命令将.ui转为.py文件.

###### 1.启动Qt Designer
命令执行designer, 便会弹出以下界面
![20190219135650559](/assets/20190219135650559.png)

最常用的就是创建 Widget(通用窗口) 和 MainWindow(主窗口), 这里我们创建一个 MainWindow.
下面简单介绍下主要功能:
![20190219135706205](/assets/20190219135706205.png)

文件保存为xxx.ui文件, 可以用文本及编辑打开编辑, 其数据是XML格式的.

###### 2.将xxx.ui文件转为xxx.py文件
通过以下命令行执行, 即可生成 designer_demo.py 文件
```python
pyuic5 -o designer_demo.py designer_demo.ui
```

###### 3.运行布局文件
导入并继承它
```python
from designer_demo import Ui_MainWindow
class MyDesiger(QMainWindow, Ui_MainWindow):
```

编写以下代码, 放在designer_demo.py同文件夹下, 运行即可
```python
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from designer_demo import Ui_MainWindow


class MyDesiger(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyDesiger, self).__init__(parent)
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyDesiger()
    ui.show()
    sys.exit(app.exec_())
```

#### 控件箱简介
<ul>
<li>Layouts 布局 (选中控件 -&gt; Lay out(右键) -&gt; 选择布局)
<ul>
<li>Vertical Layout: 垂直布局</li>
<li>Horizontal Layout: 水平布局</li>
<li>Grid Layout: 网格布局 (划分为 行 和 列)</li>
<li>Form Layout: 表单布局 (左列标签, 右列控件)</li>
</ul>
</li>
<li>Containers 容器
<ul>
<li>Group Box</li>
<li>Scroll Area</li>
<li>Tool Box</li>
<li>Tab Widge</li>
<li>Stacked Widget</li>
<li>Frame: 帧容器, 可放入布局 / 控件等</li>
<li>Widget: 窗口容器</li>
<li>MDI Area</li>
<li>Dock Widget</li>
</ul>
</li>
<li>Item Widgets 条目控件
<ul>
<li>List Widget: 列表条目</li>
<li>Tree Widget: 树形条目</li>
<li>Table Widget: 标签页条目</li>
</ul>
</li>
<li>Spacers 间隔(透明)
<ul>
<li>Horizontal Spacer: 水平间隔</li>
<li>Vertical Spacer: 垂直间隔</li>
</ul>
</li>
<li>Buttons 按钮
<ul>
<li>Push Button: 按钮</li>
<li>Tool Button: 工具箱按钮 (…)</li>
<li>Radio Button: 单选框</li>
<li>Check Box: 多选框</li>
<li>Command Link Button:</li>
<li>Dialog Button Box: Dialog 按钮 (ok | cancel)</li>
</ul>
</li>
<li>Input Widgets 输入控件
<ul>
<li>Combo Box: 下拉框</li>
<li>Font Combo Box: 字体下拉框</li>
<li>Line Edit: 行文本编辑框</li>
<li>Text Edit: 文本编辑框</li>
<li>Plain Text Edit: 文本编辑框</li>
<li>Spin Box: 选择整数值</li>
<li>Double Spin Box: 选择浮点数值</li>
<li>Time Edit: 时间选择框</li>
<li>Data Edit: 日期选择框</li>
<li>Data/Time Edit: 日期 时间 选择框</li>
<li>Dial: 圆形滚动表盘</li>
<li>Horizontal Scroll Bar: 水平滚动条</li>
<li>Vertical Scroll Bar: 垂直滚动条</li>
<li>Horizontal Slider: 水平拖动条</li>
<li>Vertical Slider: 垂直拖动条</li>
<li>Key Sequence Edit: 按键编辑框</li>
</ul>
</li>
<li>Display Widgets 显示控件
<ul>
<li>Label: 标签 (显示文字 / 图片等)</li>
<li>Text Browser: 文本浏览(不可编辑)</li>
<li>Graphics View: 绘画</li>
<li>Calendar Widget: 日历</li>
<li>LCD Number: LCD数字显示屏</li>
<li>Progress Bar: 进度条</li>
<li>Horizontal Line: 水平线</li>
<li>Vertical Line: 垂直线</li>
<li>OpenGL Widget: OpenGl</li>
</ul>
</li>
</ul>

#### 控件属性简介
<ul>
<li>objectName: 控件对象名</li>
<li>geometry: 相对坐标(px) x,y,width,height</li>
<li>sizePolicy: 控件大小策略
<ul>
<li>Fixed: 控件有 sizeHint 尺寸且尺寸不变</li>
<li>Minimum: 控件有 sizeHint 最小尺寸, 尺寸可变大</li>
<li>Maximum: 控件有 sizeHint 最大尺寸, 尺寸可变小</li>
<li>Preferred: 控件有 sizeHint 期望尺寸, 有minisizeHint最小尺寸, 尺寸可变大</li>
<li>Expanding: 控件有 minisizeHint 最小尺寸, 希望更大尺寸</li>
<li>MinimumExpanding: 控件有 sizeHint 最小尺寸, 希望更大磁村</li>
<li>Ignored: 无视 sizeHint 和 minisizeHint, 按默认设置</li>
</ul>
</li>
<li>minimumSize: 最小尺寸</li>
<li>maximumSize: 最大尺寸 (固定尺寸: minimumSize=maximumSize)</li>
<li>font: 字体</li>
<li>cursor: 光标</li>
<li>windowTitle: 窗口标题</li>
<li>WindowsIcon: 窗口图标</li>
<li>iconSize: 图标大小</li>
<li>toolTip: 提示泡提示信息</li>
<li>statusTip: 状态栏提示信息</li>
<li>text: 控件文本</li>
<li>shortcut: 快捷键</li>
<li>horizontalSpacer: 水平间距</li>
</ul>

#### 信号(signal)和槽(slot)
PyQt5处理事件有个signal and slot机制, 事件触发产生信号(signal), 当信号发送(emit())时, 连接的槽(slot)便会执行.

信号与槽的连接
```python
sender.signal.connect(receiver.slot)
# 例子
btn.clicked.connect(self.buttonClicked)

```

**快速连接伙伴 (信号槽)**
按F4选择 Edit Signal/Slot 模式 -> 鼠标按住控件1拖拽到控件2上松开 -> 弹出对话框, 选择两边连接事件 -> ok -> 按F3切换回 Edit Widgets 模式

演示:
![20190219135748611](/assets/20190219135748611.gif)

#### 菜单栏
菜单栏通过双击 Type Here 添加一级菜单(File), 点开一级菜单双击 Type Here 添加动作(New File), 若点了后面的+, 并添加动作(Text File), 则动作(New File)将变成子菜单.
![20190219135803651](/assets/20190219135803651.png)

并且我们可以在 动作编辑器 里修改 菜单里的动作
![20190219135819460](/assets/20190219135819460.png)

#### 加入资源文件
Qt Designer中如果在设计UI界面的时候要加入一些图素，图标等资源的时候是不能直接添加进去的，需要在Qt开发目录下编写QRC文件

qrc文件格式如下：
```xml
<RCC>
  <qresource prefix="q">
    <file>/swlogo.png</file>
    <file>/swlogo手机端竖版蓝背景.png</file>
    <file>小众软件/类似QQ.png</file>
  </qresource>
</RCC>
```
如何添加

第一步：

选择   “资源浏览器”
![062035575787434](/assets/062035575787434.png)
点击类似铅笔的button

第二步：

从编辑资源选择击鼠标右键，
![062037098596953](/assets/062037098596953.png)
新建一个aaa.qrc文件，

第三步：

添加资源，先选择一个新前缀，然后添加文件
![062041515783485](/assets/062041515783485.png)

确定之后就可以在需要资源的地方引用资源浏览器的图片或文件了！
![062044548431664](/assets/062044548431664.png)








https://blog.csdn.net/Rozol/article/details/87904498#t1
https://zmister.com/archives/category/guidevelop/pyqt5_basic
http://www.xdbcb8.com/archives/190.html
https://blog.csdn.net/a359680405/article/list/2?t=1&
https://blog.csdn.net/jia666666/article/details/81675009
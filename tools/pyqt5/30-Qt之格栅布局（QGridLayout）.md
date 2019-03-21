## 简述
QGridLayout：格栅布局，也被称作网格布局（多行多列）。

栅格布局将位于其中的窗口部件放入一个网状的栅格之中。QGridLayout需要将提供给它的空间划分成的行和列，并把每个窗口部件插入并管理到正确的单元格。 栅格布局是这样工作的：

它计算了位于其中的空间，然后将它们合理的划分成若干个行（row）和列（column），并把每个由它管理的窗口部件放置在合适的单元之中，这里所指的单元（cell）即是指由行和列交叉所划分出来的空间。

在栅格布局中，行和列本质上是相同的，只是叫法不同而已。下面将重点讨论列，这些内容当然也适用于行。

在栅格布局中，每个列（以及行）都有一个最小宽度（使用setColumnMinimumWidth()设置）以及一个伸缩因子（使用setColumnStretch()设置）。最小宽度指的是位于该列中的窗口部件的最小的宽度，而伸缩因子决定了该列内的窗口部件能够获得多少空间。

## 基本使用
一般情况下我们都是把某个窗口部件放进栅格布局的一个单元中，但窗口部件有时也可能会需要占用多个单元。这时就需要用到addWidget()方法的一个重载版本，原型如下：
```c++
void addWidget(QWidget *, int row, int column, int rowSpan, int columnSpan, Qt::Alignment = 0);
```
这个单元将从row和column开始，扩展到rowSpan和columnSpan指定的倍数的行和列。如果rowSpan或columnSpan的值为-1，则窗口部件将扩展到布局的底部或者右边边缘处。

在创建栅格布局完成后，就可以使用addWidget()，addItem()，以及addLayout()方法向其中加入窗口部件，以及其它的布局。

#### 例子：单一的网格单元格
![20180815111555614](/assets/20180815111555614.png)
```python
import sys
from PyQt5.QtWidgets import QApplication  ,QWidget  , QGridLayout, QPushButton

class Winform(QWidget):
    def __init__(self,parent=None):
        super(Winform,self).__init__(parent)
        self.initUI()

    def initUI(self):            
        #1创建QGridLayout的实例，并设置窗口的布局
        grid = QGridLayout()  
        self.setLayout(grid)  

        #2创建按钮的标签列表
        names = ['Cls', 'Back', '', 'Close',  
                 '7', '8', '9', '/',  
                '4', '5', '6', '*',  
                 '1', '2', '3', '-',  
                '0', '.', '=', '+']  

        #3 在网格中创建一个位置列表       
        positions = [(i,j) for i in range(5) for j in range(4)]  

        #4 创建按钮并通过addWIdget（）方法添加到布局中
        for position, name in zip(positions, names):                
            if name == '':  
                continue  

            button = QPushButton(name)  
            grid.addWidget(button, *position)  

        self.move(300, 150)  
        self.setWindowTitle('网格布局管理例子')  

if __name__ == "__main__":  
        app = QApplication(sys.argv) 
        form = Winform()
        form.show()
        sys.exit(app.exec_())
```

## 常用接口
```c++
addWidget(QWidget *, int row, int column, Qt::Alignment = 0)
addWidget(QWidget *, int row, int column, int rowSpan, int columnSpan, Qt::Alignment = 0) 
```
添加窗口部件至布局。
这个单元将从row和column开始，扩展到rowSpan和columnSpan指定的倍数的行和列。如果rowSpan或columnSpan的值为-1，则窗口部件将扩展到布局的底部或者右边边缘处，Qt::Alignment为对齐方式。

```c++
addLayout(QLayout *, int row, int column, Qt::Alignment = 0) 
addLayout(QLayout *, int row, int column, int rowSpan, int columnSpan, Qt::Alignment = 0)
```
和addWidget类似，这个是添加布局。

```c++
setRowStretch(int row, int stretch)
setColumnStretch(int column, int stretch) 
```
设置行/列的伸缩空间
和QBoxLayout的addStretch功能类似。

```c++
setSpacing(int spacing)
setHorizontalSpacing(int spacing)
setVerticalSpacing(int spacing) 
```
设置间距
setSpacing()可以同时设置水平、垂直间距，设置之后，水平、垂直间距相同。 
setHorizontalSpacing()、setVerticalSpacing()可以分别设置水平间距、垂直间距。

```c++
setRowMinimumHeight(int row, int minSize) 
```
设置行最小高度

```c++
setColumnMinimumWidth(int column, int minSize) 
```
设置列最小宽度

```c++
columnCount() 
```
获取列数

```c++
rowCount() 
```
获取行数

```c++
setOriginCorner(Qt::Corner) 
```
设置原始方向
和QBoxLayout的setDirection功能类似。

## 例子
#### 跨越行和列的网格单元格
![2018081511204046](/assets/2018081511204046.png)
```python
import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,   QTextEdit, QGridLayout, QApplication)  

class Winform(QWidget):
   def __init__(self,parent=None):
       super(Winform,self).__init__(parent)
       self.initUI()

   def initUI(self):            
       titleLabel = QLabel('标题')  
       authorLabel = QLabel('提交人')  
       contentLabel = QLabel('申告内容')  

       titleEdit = QLineEdit()  
       authorEdit = QLineEdit()  
       contentEdit = QTextEdit()  

       grid = QGridLayout()  
       grid.setSpacing(10)  

       grid.addWidget(titleLabel, 1, 0)  
       grid.addWidget(titleEdit, 1, 1)  

       grid.addWidget(authorLabel, 2, 0)  
       grid.addWidget(authorEdit, 2, 1)  

       grid.addWidget(contentLabel, 3, 0)  
       grid.addWidget(contentEdit, 3, 1, 5, 1)  

       self.setLayout(grid)   

       self.setGeometry(300, 300, 350, 300)  
       self.setWindowTitle('故障申告')

if __name__ == "__main__":  
       app = QApplication(sys.argv) 
       form = Winform()
       form.show()
       sys.exit(app.exec_())
```

#### 登录界面
![20160530142555348](/assets/20160530142555348.png)
```c++
/ 构建控件 头像、用户名、密码输入框等
QLabel *pImageLabel = new QLabel(this);
QLineEdit *pUserLineEdit = new QLineEdit(this);
QLineEdit *pPasswordLineEdit = new QLineEdit(this);
QCheckBox *pRememberCheckBox = new QCheckBox(this);
QCheckBox *pAutoLoginCheckBox = new QCheckBox(this);
QPushButton *pLoginButton = new QPushButton(this);
QPushButton *pRegisterButton = new QPushButton(this);
QPushButton *pForgotButton = new QPushButton(this);

pLoginButton->setFixedHeight(30);
pUserLineEdit->setFixedWidth(200);

// 设置头像
QPixmap pixmap(":/Images/logo");
pImageLabel->setFixedSize(90, 90);
pImageLabel->setPixmap(pixmap);
pImageLabel->setScaledContents(true);

// 设置文本
pUserLineEdit->setPlaceholderText(QStringLiteral("QQ号码/手机/邮箱"));
pPasswordLineEdit->setPlaceholderText(QStringLiteral("密码"));
pPasswordLineEdit->setEchoMode(QLineEdit::Password);
pRememberCheckBox->setText(QStringLiteral("记住密码"));
pAutoLoginCheckBox->setText(QStringLiteral("自动登录"));
pLoginButton->setText(QStringLiteral("登录"));
pRegisterButton->setText(QStringLiteral("注册账号"));
pForgotButton->setText(QStringLiteral("找回密码"));

QGridLayout *pLayout = new QGridLayout();
// 头像 第0行，第0列开始，占3行1列
pLayout->addWidget(pImageLabel, 0, 0, 3, 1);
// 用户名输入框 第0行，第1列开始，占1行2列
pLayout->addWidget(pUserLineEdit, 0, 1, 1, 2);
pLayout->addWidget(pRegisterButton, 0, 4);
// 密码输入框 第1行，第1列开始，占1行2列
pLayout->addWidget(pPasswordLineEdit, 1, 1, 1, 2);
pLayout->addWidget(pForgotButton, 1, 4);
// 记住密码 第2行，第1列开始，占1行1列 水平居左 垂直居中
pLayout->addWidget(pRememberCheckBox, 2, 1, 1, 1, Qt::AlignLeft | Qt::AlignVCenter);
// 自动登录 第2行，第2列开始，占1行1列 水平居右 垂直居中
pLayout->addWidget(pAutoLoginCheckBox, 2, 2, 1, 1, Qt::AlignRight | Qt::AlignVCenter);
// 登录按钮 第3行，第1列开始，占1行2列
pLayout->addWidget(pLoginButton, 3, 1, 1, 2);
// 设置水平间距
pLayout->setHorizontalSpacing(10);
// 设置垂直间距
pLayout->setVerticalSpacing(10);
// 设置外间距
pLayout->setContentsMargins(10, 10, 10, 10);
setLayout(pLayout);
```

## 总结
当界面元素较为复杂时，应毫不犹豫的尽量使用栅格布局，而不是使用水平和垂直布局的组合或者嵌套的形式，因为在多数情况下，后者往往会使“局势”更加复杂而难以控制。栅格布局赋予了界面设计器更大的自由度来排列组合界面元素，而仅仅带来了微小的复杂度开销。

当要设计的界面是一种类似于两列和若干行组成的形式时，使用表单布局要比栅格布局更为方便些。

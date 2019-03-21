## 简述
QFormLayout管理输入型控件和关联的标签组成的那些Form表单。

QFormLayout是一个方便的布局类，其中的控件以两列的形式被布局在表单中。左列包括标签，右列包含输入控件，例如：QLineEdit、QSpinBox等。

## 使用
我们可以通过addRow(const QString &labelText, QWidget *field)来创建一个带有给定文本的QLabel及QWidget控件行，它们可以自动的设置为伙伴关系。
```c++
QFormLayout *pLayout = new QFormLayout();
pLayout->addRow(QStringLiteral("用户名："), pUserLineEdit);
pLayout->addRow(QStringLiteral("密码："), pPasswordLineEdit);
pLayout->addRow(QStringLiteral("验证码："), pVerifyLineEdit);
pLayout->setSpacing(10);
pLayout->setMargin(10);
setLayout(pLayout);
```

使用QGridLayout格栅布局编写的比较：
```c++
QGridLayout *pLayout = new QGridLayout();
pLayout->addWidget(pUserNameLabel, 0, 0);
pLayout->addWidget(pUserLineEdit, 0, 1);
pLayout->addWidget(pPasswordLabel, 1, 0);
pLayout->addWidget(pPasswordLineEdit, 1, 1);
pLayout->addWidget(pVerifyLabel, 2, 0);
pLayout->addWidget(pVerifyLineEdit, 2, 1);
pLayout->setSpacing(10);
pLayout->setMargin(10);
setLayout(pLayout);
```

很显然，功能可以实现，但是代码量大了很多。

#### 例子：表单布局的基本使用
![20180815113313534](/assets/20180815113313534.png)
```python
import sys
from PyQt5.QtWidgets import QApplication  ,QWidget ,QFormLayout , QLineEdit, QLabel

class Winform(QWidget):
    def __init__(self,parent=None):
        super(Winform,self).__init__(parent)
        self.setWindowTitle("窗体布局管理例子") 
        self.resize(400, 100)  

        fromlayout = QFormLayout()
        labl1 = QLabel("标签1")
        lineEdit1 = QLineEdit()
        labl2 = QLabel("标签2")
        lineEdit2 = QLineEdit()
        labl3 = QLabel("标签3")
        lineEdit3 = QLineEdit()

        fromlayout.addRow(labl1, lineEdit1)
        fromlayout.addRow(labl2, lineEdit2)
        fromlayout.addRow(labl3, lineEdit3)

        self.setLayout(fromlayout)   

if __name__ == "__main__":  
    app = QApplication(sys.argv) 
    form = Winform()
    form.show()
    sys.exit(app.exec_())
```

## 常用接口
* setRowWrapPolicy(RowWrapPolicy policy)
设置换行策略

QFormLayout::RowWrapPolicy枚举：
控制表单行的显示策略。
| 内容                      | 值  | 描述                                                     | 效果 |
| ------------------------- | --- | -------------------------------------------------------- | ---- |
| QFormLayout::DontWrapRows | 0   | 输入框始终在标签旁边                                                 |  ![20160530170503504](/assets/20160530170503504.png)    |
| QFormLayout::WrapLongRows | 1   | 标签有足够的空间适应，如果最小大小比可用空间大，输入框会被换到下一行 |   ![20160530170514850](/assets/20160530170514850.png)   |
| QFormLayout::WrapAllRows  | 2   | 输入框始终在标签下边                                                 |  ![20160530170530726](/assets/20160530170530726.png)    |

* setWidget(int row, ItemRole role, QWidget *widget)
设置行row所对应的控件，如果role为LabelRole时，设置的为标签所对应的控件，如果role为FieldRole时，设置的为输入框所对应的控件。

QFormLayout::ItemRole枚举：
指定一排控件的类型
| 内容                      | 值  | 描述                   |
| ------------------------- | --- | ---------------------- |
| QFormLayout::LabelRole    | 0   | 标签                   |
| QFormLayout::FieldRole    | 1   | 输入框                 |
| QFormLayout::SpanningRole | 2   | 跨越标签和输入框的控件 |

例如：
```c++
//pLayout->addRow(pUserNameLabel, pUserLineEdit);
pLayout->setWidget(0, QFormLayout::LabelRole, pUserNameLabel);
pLayout->setWidget(0, QFormLayout::FieldRole, pUserLineEdit);
```

* setSpacing(int spacing)  
* setHorizontalSpacing(int spacing)  
* setVerticalSpacing(int spacing)  
设置间距（水平间距、垂直间距）


* QWidget * QFormLayout::labelForField(QWidget * field)
通过field获取field对应的标签，这里不一定是QLabel，返回值为QWidget。

## 总结
当要设计的界面是一种类似于两列和若干行组成的形式时，使用QFormLayout（表单布局）要比QGridLayout（栅格布局）更为方便些。

当界面元素较为复杂时（多行多列），应毫不犹豫的尽量使用栅格布局，而不是使用水平和垂直布局的组合或者嵌套的形式，因为在多数情况下，后者往往会使“局势”更加复杂而难以控制。栅格布局赋予了界面设计器更大的自由度来排列组合界面元素，而仅仅带来了微小的复杂度开销。


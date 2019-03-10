## QWebEngineView
#### QWebEngineView总体介绍
QWebEngineView类提供了一个用于查看和编辑Web文档的小部件。

Web视图是Qt WebEngine Web浏览模块的主要小部件组件。它可以在各种应用程序中用于从Internet实时显示Web内容。

可以使用load()函数将Web站点加载到Web视图。 GET方法始终用于加载URL。

与所有Qt小部件一样，必须调用show()函数才能显示Web视图。下面的代码段说明了这一点：
```python
view = QWebEngineView(self)
view.load(QUrl("http://qt-project.org/"))
view.show()
```
**或者，setUrl()可用于加载网站。如果您有可用的HTML内容，则可以使用setHtml()。**

在视图开始加载时发出loadStarted()信号，并且只要Web视图的元素完成加载(例如嵌入的图像或脚本)，就会发出loadProgress()信号。完全加载视图时会发出loadFinished()信号。它的参数，是True还是Flase，表明加载是成功还是失败。

page()函数返回指向网页对象的指针。 QWebEngineView包含一个QWebEnginePage，它允许访问页面上下文中的QWebEngineHistory。

可以使用title()属性访问HTML文档的标题。此外，网站可以指定一个图标，可以使用属性iconUrl()URL或者使用icon()或其访问该图标。如果标题或图标发生变化，将发出相应的titleChanged()，iconChanged()和iconUrlChanged()信号。 zoomFactor()属性允许通过比例因子缩放网页的内容。

该小部件具有针对元素定制的上下文菜单，并包括在浏览器中有用的操作。对于自定义上下文菜单，或者在菜单或工具栏中嵌入操作，可以通过pageAction()获得各个操作。 Web视图维护返回操作的状态，但允许修改操作属性，如文本或图标。动作语义也可以通过triggerPageAction()直接触发。

如果要为允许用户打开新窗口的网站(如弹出窗口)提供支持，可以继承QWebEngineView并重新实现createWindow()函数。

下面我们演示一下通过QWebEngineView打开百度，简略的代码如下：
```python
view = QWebEngineView(self)
view.load(QUrl("http://www.baidu.com/"))
view.show()
```
我们再演示一个打开本地HTML，简略的代码如下：
```python
view = QWebEngineView(self)
view.load(QUrl("C:/Users/Administrator/Desktop/paoku/index.html"))
view.show()
```
这里特别强调一下：QUrl里面的请放入绝对地址，不要放入类似：”./index.html”这种相对地址，即使是在同一目录下面。

可能你会说：我不，我就要用相对地址，怎么办？

这种情况的解决方式可以是这样的：
```python
view = QWebEngineView(self)
url = QUrl(QFileInfo("./pie-simple.html").absoluteFilePath())
view.load(url)
```
返回包含文件名的绝对路径。
```python
QUrl(QFileInfo("./pie-simple.html").absoluteFilePath())
```
绝对路径名由完整路径和文件名组成。 在Unix上，这将始终以root，’/‘目录开头。 在Windows上，这将始终以’D：/‘开头，其中D是驱动器号，但未映射到驱动器号的网络共享除外，在这种情况下，路径将以’// sharename /‘开头。 QFileInfo将大写驱动器号。

当然Python中也有类似的语言:
```python
url = QUrl(os.path.abspath("./pie-simple.html"))
```

类归属
PyQt5->QtWebEngine->QWebEngineView

继承关系
PyQt5->QObject and QPaintDevice->QWidget->QWebEngineView

更多详细的介绍请见官网：[QWebEngineView](https://doc.qt.io/qt-5/qwebengineview.html "QWebEngineView")

#### 例子
实现效果：
![2018072702151328](/assets/2018072702151328.gif)
核心代码：
```python
def initUi(self):
    self.view = QWebEngineView(self.widget)
    with codecs.open("pie-simple.html", "r", "utf-8") as f:
        html = f.read()
    self.view.setHtml(html)
    self.time = QTimer()
def showPi(self):
    food = self.spinBox_food.value()
    rent = self.spinBox_rent.value()
    electricity = self.spinBox_electricity.value()
    traffic = self.spinBox_traffic.value()
    relationship = self.spinBox_relationship.value()
    taobao = self.spinBox_taobao.value()
    jscode = "showPiChart({}, {}, {}, {}, {}, {});".format(food, traffic, relationship, rent, electricity, taobao)
    self.view.page().runJavaScript(jscode)
def autoShow(self):
    self.spinBox_food.setValue(random.randint(100,10000))
    self.spinBox_rent.setValue(random.randint(100,10000))
    self.spinBox_electricity.setValue(random.randint(100,1000))
    self.spinBox_traffic.setValue(random.randint(100,2000))
    self.spinBox_relationship.setValue(random.randint(100,3000))
    self.spinBox_taobao.setValue(random.randint(100,10000))
@pyqtSlot(bool)
def on_checkBox_toggled(self, flag):
    if flag:
        self.time.start(1000)
        self.time.timeout.connect(self.autoShow)
    else:
        self.time.stop()
@pyqtSlot(int)
def on_spinBox_food_valueChanged(self, n):
    self.showPi()
@pyqtSlot(int)
def on_spinBox_rent_valueChanged(self):
    self.showPi()
@pyqtSlot(int)
def on_spinBox_electricity_valueChanged(self):
    self.showPi()
@pyqtSlot(int)
def on_spinBox_traffic_valueChanged(self):
    self.showPi()
@pyqtSlot(int)
def on_spinBox_relationship_valueChanged(self):
    self.showPi()
@pyqtSlot(int)
def on_spinBox_taobao_valueChanged(self):
    self.showPi()
def __del__(self):
    self.view.deleteLater()
```
上面就是本次功能实现的一些核心代码，还有部分内容我感觉自己看就行了（包括pie-simple.html部分改写），就不讲解了。
```python
self.view = QWebEngineView(self.widget)
with codecs.open("pie-simple.html", "r", "utf-8") as f:
    html = f.read()
self.view.setHtml(html)
```
新建QWebEngineView对象，同时打开pie-simple.html文件，并将HTMl内容在QWebEngineView对象中呈现。

```python
def showPi(self):
    food = self.spinBox_food.value()
    rent = self.spinBox_rent.value()
    electricity = self.spinBox_electricity.value()
    traffic = self.spinBox_traffic.value()
    relationship = self.spinBox_relationship.value()
    taobao = self.spinBox_taobao.value()
    jscode = "showPiChart({}, {}, {}, {}, {}, {});".format(food, traffic, relationship, rent, electricity, taobao)
    self.view.page().runJavaScript(jscode)
```
food、rent、electricity、traffic、relationship、taobao分别表示伙食消费、房租租金、水电气、交通费用、人情往来、淘宝网购的费用。

jscode表示我们希望在pie-simple.html执行javascript的函数showPiChart()：
```js
function showPiChart(var0, var1, var2, var3, var4, var5){
    if (option && typeof option === "object") {
        option["series"][0]["data"][0]["value"] = var0;
        option["series"][0]["data"][1]["value"] = var1;
        option["series"][0]["data"][2]["value"] = var2;
        option["series"][0]["data"][3]["value"] = var3;
        option["series"][0]["data"][4]["value"] = var4;
        option["series"][0]["data"][5]["value"] = var5;
        myChart.setOption(option, true);
    }
}
```

我们将取得的各项开支的值传递给showPiChart()，以便调用执行。

为了便于参数的传递，我们采用format进行字符串的拼接。
 
```python
self.view.page().runJavaScript(jscode)
```
使用runJavaScript()去执行相应的JavaScript代码，重新生成我们新的饼形图。

```python
def autoShow(self):
    self.spinBox_food.setValue(random.randint(100,10000))
    self.spinBox_rent.setValue(random.randint(100,10000))
    self.spinBox_electricity.setValue(random.randint(100,1000))
    self.spinBox_traffic.setValue(random.randint(100,2000))
    self.spinBox_relationship.setValue(random.randint(100,3000))
    self.spinBox_taobao.setValue(random.randint(100,10000))
```
autoShow()旨在设置微调框的值，这个是QTimer对象超时时调用槽函数。

```python
@pyqtSlot(bool)
def on_checkBox_toggled(self, flag):
    if flag:
        self.time.start(1000)
        self.time.timeout.connect(self.autoShow)
    else:
        self.time.stop()
```
我们把自动演示勾上的时候，定时器启动，每隔1秒自动调用autoShow()。否则就取消定时器。

```python
@pyqtSlot(int)
def on_spinBox_food_valueChanged(self, n):
    self.showPi()
```
当微调框的数值发生变化的时候就会调用showPi()，这个就能理解为什么我们改变数值的时候饼形图会发生变化了。其他的类似。

```python
def __del__(self):
    self.view.deleteLater()
```
为什么要加上这句呢？我们以前写的时候很少加上这句啊。因为在执行程序的时候，可能会出现关闭程序QWebEngineView崩溃的情况，加上这句就是让系统加快释放这部分内存，避免QWebEngineView崩溃的情况。




























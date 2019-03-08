## PyQt5安装
#### windows 
```python
pip install PyQt5
pip install PyQt5-tools
```

#### Ubuntu
```python
#安装pyqt5
pip install pyqt5
#安装qtdesigner
sudo apt-get install qt5-default qttools5-dev-tools
```

## PyQt5+python3+pycharm开发环境配置
添加扩展工具：
![2019-03-08 15-59-47屏幕截图](/assets/2019-03-08%2015-59-47屏幕截图.png)
配置参数：
```
在Qt Designer的设置中，Program选择PyQt安装目录中 designer.exe 的路径
Work directory 使用变量 $FileDir$ （点击后面的 Insert macro 按钮可以不用输入双击上屏）
```
![20150422140556771](/assets/20150422140556771.png)
![2019-03-08 16-02-02屏幕截图](/assets/2019-03-08%2016-02-02屏幕截图.png)

```
在PyUIC的设置中，其他的都差不多，Program 写入Python的地址，
Parameters写入-m PyQt5.uic.pyuic  $FileName$ -o $FileNameWithoutExtension$.py
Work directory 使用变量 $FileDir$
```
![20150422140732843](/assets/20150422140732843.png)
![2019-03-08 16-04-14屏幕截图](/assets/2019-03-08%2016-04-14屏幕截图.png)

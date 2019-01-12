## pyinstaller
Python代码转换为exe可执行程序

## pyInstaller安装配置
1、pyInstaller [GitHub地址](https://github.com/pyinstaller/pyinstaller "GitHub地址") 下载

2、解压，执行python setup.py install

## 制作exe
具体的参数用的时候可以去看官方文档，下面列出自己使用的一些例子

```
pyinstaller --add-data page/index.html;page -F tetsHttpServer.py
pyinstaller -F tetsHttpServer.py --add-data page/index.html;page
pyinstaller --add-data page/index.html;page --runtime-tmpdir . -F tetsHttpServer.py

pyi-makespec tetsHttpServer.py
pyinstaller -F tetsHttpServer.spec

pyinstaller -F testAiohttpServer.py

pyinstaller --runtime-tmpdir . --add-data page/index.html;page --add-data page/js/index.js;page/js  -F mapImgServer.py
```
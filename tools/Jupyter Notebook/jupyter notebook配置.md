## JupyterNotebook配置远程登录
https://blog.csdn.net/u014636245/article/details/83652126
总共分为三步  
* 生成配置文件  
* 设置密码  
* 修改配置文件  

### 一、生成配置文件jupyter_notebook_config.py
为了生成配置文件，需要使用下面的jupyter命令
```
jupyter notebook --generate-config
```

此时就会得到一个配置文件，其默认路径一般如下所示：
```
Windows: C:\Users\USERNAME\.jupyter\jupyter_notebook_config.py
OS X: /Users/USERNAME/.jupyter/jupyter_notebook_config.py
Linux: /home/USERNAME/.jupyter/jupyter_notebook_config.py
```

Ubuntu 下一般会保存在~/.jupyter/jupyter_notebook_config.py

### 二、设置登录密码
自动设置(推荐)
在jupyter5.0以后的版本，可以使用jupyter notebook password来设置密码:
```
$ jupyter notebook password
Enter password:  yourcode  #输入密码
Verify password: yourcodeagain   #再次输入密码确认
#运行后结果
[NotebookPasswordApp] Wrote hashed password to /Users/you/.jupyter/jupyter_notebook_config.json    #密码被保存的位置 ~/.jupyter/jupyter_notebook_config.json
```

### 三、修改配置文件
为了能在远程访问jupyter，需要修改刚刚生成的配置文件~/.jupyter/jupyter_notebook_config.py

对于自动模式  
打开配置文件后修改三个地方：
```
c.NotebookApp.ip = '0.0.0.0'    #允许所有ip访问 
c.NotebookApp.open_browser = False    #不打开浏览器
c.NotebookApp.port = 8888             #端口
c.NotebookApp.notebook_dir = '/home/lifengchao/jupyter notebook'  #默认工作目录，而不是使用运行jupyter notebook的目录
```
在浏览器中输入http://10.19.4.6:8888，输入密码访问，可以在其他的电脑上访问

## Jupyter Notebook 修改默认打开的文件夹的位置
上个修改配置中jupyter_notebook_config.py添加c.NotebookApp.notebook_dir = '/home/lifengchao/jupyter notebook'即可


## 删除指定kernel
删除指定kernel：jupyter kernelspec remove icsharpkernel


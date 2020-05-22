# pip和conda包管理器

## conda下TensorFlow安装示例
1.安装 Python 环境。此处建议安装 [Anaconda](https://www.anaconda.com/ "Anaconda") 的 Python 3.7 版本（后文均以此为准），这是一个开源的 Python 发行版本，提供了一个完整的科学计算环境，包括 NumPy、SciPy 等常用科学计算库。当然，你有权选择自己喜欢的 Python 环境。Anaconda 的安装包可在 [这里](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/ "这里") 获得。

2.使用 Anaconda 自带的 conda 包管理器建立一个 Conda 虚拟环境，并进入该虚拟环境。在命令行下输入：
```python
conda create --name tf2 python=3.7      # “tf2”是你建立的conda虚拟环境的名字
conda activate tf2                      # 进入名为“tf2”的conda虚拟环境
```

3.使用 Python 包管理器 pip 安装 TensorFlow。在命令行下输入：
```python
pip install tensorflow
```
等待片刻即安装完毕。

小技巧:

* 也可以使用 conda install tensorflow 来安装 TensorFlow，不过 conda 源的版本往往更新较慢，难以第一时间获得最新的 TensorFlow 版本；    
* 从 TensorFlow 2.1 开始，pip 包 tensorflow 即同时包含 GPU 支持，无需通过特定的 pip 包 tensorflow-gpu 安装 GPU 版本。如果对 pip 包的大小敏感，可使用 tensorflow-cpu 包安装仅支持 CPU 的 TensorFlow 版本。    
* 在 Windows 下，需要打开开始菜单中的 “Anaconda Prompt” 进入 Anaconda 的命令行环境；    
* 如果默认的 pip 和 conda 网络连接速度慢，可以尝试使用镜像，将显著提升 pip 和 conda 的下载速度（具体效果视您所在的网络环境而定）；    
    * 清华大学的 pypi 镜像：https://mirrors.tuna.tsinghua.edu.cn/help/pypi/    
    * 清华大学的 Anaconda 镜像：https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/
* 如果对磁盘空间要求严格（比如服务器环境），可以安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html "Miniconda") ，仅包含 Python 和 Conda，其他的包可自己按需安装。Miniconda 的安装包可在 [这里](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/ "这里") 获得。

## Conda 虚拟环境
在 Python 开发中，很多时候我们希望每个应用有一个独立的 Python 环境（比如应用 1 需要用到 TensorFlow 1.X，而应用 2 使用 TensorFlow 2.0）。这时，Conda 虚拟环境即可为一个应用创建一套 “隔离” 的 Python 运行环境。使用 Python 的包管理器 conda 即可轻松地创建 Conda 虚拟环境。常用命令如下：
```
conda create --name [env-name]      # 建立名为[env-name]的Conda虚拟环境
conda activate [env-name]           # 进入名为[env-name]的Conda虚拟环境
conda deactivate                    # 退出当前的Conda虚拟环境
conda env remove --name [env-name]  # 删除名为[env-name]的Conda虚拟环境
conda env list                      # 列出所有Conda虚拟环境
```



## pip和conda常用命令
pip 是最为广泛使用的 Python 包管理器，可以帮助我们获得最新的 Python 包并进行管理。常用命令如下：
```
pip install [package-name]              # 安装名为[package-name]的包
pip install [package-name]==X.X         # 安装名为[package-name]的包并指定版本X.X
pip install [package-name] --proxy=代理服务器IP:端口号         # 使用代理服务器安装
pip install [package-name] --upgrade    # 更新名为[package-name]的包
pip uninstall [package-name]            # 删除名为[package-name]的包
pip list                                # 列出当前环境下已安装的所有包
```

conda 包管理器是 Anaconda 自带的包管理器，可以帮助我们在 conda 环境下轻松地安装各种包。相较于 pip 而言，conda 的通用性更强（不仅是 Python 包，其他包如 CUDA Toolkit 和 cuDNN 也可以安装），但 conda 源的版本更新往往较慢。常用命令如下：
```
conda install [package-name]        # 安装名为[package-name]的包
conda install [package-name]=X.X    # 安装名为[package-name]的包并指定版本X.X
conda update [package-name]         # 更新名为[package-name]的包
conda remove [package-name]         # 删除名为[package-name]的包
conda list                          # 列出当前环境下已安装的所有包
conda search [package-name]         # 列出名为[package-name]的包在conda源中的所有可用版本
```

conda 中配置代理：在用户目录下的 .condarc 文件中添加以下内容：
```
proxy_servers:
    http: http://代理服务器IP:端口号
```






```python

```
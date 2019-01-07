### 一、scrapy命令行基本命令 与 scrapy项目目录
##### 1、scrapy命令行基本命令
&emsp;&emsp;在终端中输入scrapy得到一下信息：
```python
Scrapy 1.5.0 - no active project

Usage:
  scrapy <command> [options] [args]

Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

  [ more ]      More commands available when run from project directory

Use "scrapy <command> -h" to see more info about a command
```

##### 2、scrapy项目目录结构
&emsp;&emsp;在开始抓取之前，您必须设置一个新的Scrapy项目。输入您要存储代码的目录并运行：

    scrapy startproject tutorial

这将创建一个tutorial包含以下内容的目录：
```python
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

##### 3、可用的工具命令
    scrapy -h
**可以看到所有可用的命令**：
```python
Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

  [ more ]      More commands available when run from project directory
Use "scrapy <command> -h" to see more info about a command
```

`scrapy <command> -h`运行以获取有关每个命令的更多信息


&emsp;&emsp;有两种命令，一种只能在Scrapy项目内部工作（特定于项目的命令）和那些在没有活动的Scrapy项目（全局命令）的情况下工作的命令，尽管从项目内部运行时它们可能表现略有不同（因为他们会使用项目覆盖设置）。

**全局命令**：
```
startproject
genspider
settings
runspider
shell
fetch
view
version
```

**仅限项目的命令**：
```
crawl
check
list
edit
parse
bench
```
### 二、scrapy工程入门命令
##### 制作 Scrapy 爬虫 一般需要4步：
* 新建项目 (scrapy startproject xxx)：新建一个新的爬虫项目
* 明确目标 （编写items.py）：明确你想要抓取的目标
* 制作爬虫 （spiders/xxspider.py）：制作爬虫开始爬取网页
* 存储内容 （pipelines.py）：设计管道存储爬取内容

##### 新建一个scrapy工程目录下
    scrapy startproject projectname

##### 新建一个spider文件
    cd 到scrapy工程目录下
    scrapy genspider spidername "https://www.baidu.com/"


##### 运行spider
    必须在scrapy工程目录下
    scrapy crawl spidername
```python
from scrapy import cmdline

class GushiwenSpider(scrapy.Spider):
    name = 'shiwen'
    ...

if __name__ == "__main__":
    cmdline.execute("scrapy crawl shiwen".split())
```

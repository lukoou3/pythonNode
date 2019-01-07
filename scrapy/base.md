### 一、scrapy框架概览
#### 概览
* Scrapy是用纯Python实现一个为了爬取网站数据、提取结构性数据而编写的应用框架，用途非常广泛。
* 框架的力量，用户只需要定制开发几个模块就可以轻松的实现一个爬虫，用来抓取网页内容以及各种图片，非常之方便。
* Scrapy 使用了 Twisted['twɪstɪd](其主要对手是Tornado)异步网络框架来处理网络通讯，可以加快我们的下载速度，不用自己去实现异步框架，并且包含了各种中间件接口，可以灵活的完成各种需求。

下面是scrapy官网给出的最新的架构图示：
![architecture](/assets/architecture.png)

#### 基本组件
* **引擎（Engine）**  
引擎负责控制数据流在系统中所有组件中流动，并在相应动作发生时触发事件。 详细内容查看下面的数据流(Data Flow)部分。
* **调度器（Scheduler）**  
调度器从引擎接受request并将他们入队，以便之后引擎请求他们时提供给引擎。
* **下载器(Downloader)**  
下载器负责获取页面数据并提供给引擎，而后提供给spider。
* **爬虫（Spiders）**  
Spider是Scrapy用户编写用于分析response并提取item(即获取到的item)或额外跟进的URL的类。 每个spider负责处理一个特定(或一些)网站。
* **管道（Item Pipeline）**  
Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、验证及持久化(例如存取到数据库中)。
* **下载器中间件（Downloader middlewares）**  
下载器中间件是在引擎及下载器之间的特定钩子(specific hook)，处理Downloader传递给引擎的response。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。
* **Spider中间件（Spider middlewares）**  
Spider中间件是在引擎及Spider之间的特定钩子(specific hook)，处理spider的输入(response)和输出(items及requests)。 其提供了一个简便的机制，通过插入自定义代码来扩展Scrapy功能。

#### 数据流向
Scrapy的数据流由执行引擎（Engine）控制，其基本过程如下：
* 1.引擎从Spider中获取到初始Requests。
* 2.引擎将该Requests放入调度器，并请求下一个要爬取的Requests。
* 3.调度器返回下一个要爬取的Requests给引擎
* 4.引擎将Requests通过下载器中间件转发给下载器(Downloader)。
* 5.一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回(response)方向)发送给引擎。
* 6.引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
* 7.Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
* 8.引擎将(Spider返回的)爬取到的Item交给ItemPipeline处理，将(Spider返回的)Request交给调度器，并请求下一个Requests（如果存在的话）。
* 9.(从第一步)重复直到调度器中没有更多地Request。

#### 总结
&emsp;&emsp;Scrapy的各个组件相互配合执行，有的组件负责任务的调度，有的组件负责任务的下载，有的组件负责数据的清洗保存，各组件分工明确。在组件之间存在middleware的中间件，其作用就是功能的拓展，当然还可以根据自身的需求自定义这些拓展功能，比如我们可以在Downloader middlewares里面实现User-Agent的切换，Proxy的切换等等。

### 二、scrapy命令行基本命令 与 scrapy项目目录
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

各目录/文件的作用：  
* scrapy.cfg  
项目的配置文件，带有这个文件的那个目录作为scrapy项目的根目录
* items.py  
定义你所要抓取的字段
* pipelines.py  
管道文件，当spider抓取到内容（item）以后，会被送到这里，这些信息（item）在这里会被清洗，去重，保存到文件或者数据库。
* middlewares.py  
中间件，主要是对功能的拓展，你可以添加一些自定义的功能，比如添加随机user-agent, 添加proxy。
* settings.py  
设置文件，用来设置爬虫的默认信息，相关功能开启与否，比如是否遵循robots协议，设置默认的headers，设置文件的路径，中间件的执行顺序等等。
* spiders/  
在这个文件夹下面，编写你自定义的spider。


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

### 二、scrapy常用命令
#### 简介
&emsp;&emsp;Scrapy是通过Scrapy命令行工具进行控制的，包括创建新的项目，爬虫的启动，相关的设置，Scrapy提供了两种内置的命令，分别是全局命令和项目命令，顾名思义，全局命令就是在任意位置都可以执行的命令，而项目命令只有在你新创建了项目之后，在项目目录中才可以执行的命令。在这里，简单的介绍一些常用的命令。
#### 全局命令
* **startproject**  
语法: `scrapy startproject <project_name>`  
这个命令是scrapy最为常用的命令之一，它将会在当前目录下创建一个名为 <project_name>的项目。  
* settings  
语法: scrapy settings [options]   
该命令将会输出Scrapy默认设定，当然如果你在项目中运行这个命令将会输出项目的设定值。    
* runspider  
语法: scrapy runspider <spider_file.py>  
在未创建项目的情况下，运行一个编写在Python文件中的spider。
* **shell**  
语法: `scrapy shell [url]`  
以给定的URL(如果给出)或者空(没有给出URL)启动Scrapy shell。  
例如，scrapy shell http://www.baidu.com将会打开百度URL，启动交互式命令行，可以用来做一些测试。      
* fetch    
语法: scrapy fetch <url>  
使用Scrapy下载器(downloader)下载给定的URL，并将获取到的内容送到标准输出。简单的来说，就是打印url的html代码。  
* view    
语法: scrapy view <url>  
在你的默认浏览器中打开给定的URL，并以Scrapy spider获取到的形式展现。 有些时候spider获取到的页面和普通用户看到的并不相同，一些动态加载的内容是看不到的， 因此该命令可以用来检查spider所获取到的页面。  
* version  
语法: scrapy version [-v]  
输出Scrapy版本。配合 -v 运行时，该命令同时输出Python, Twisted以及平台的信息。  
#### 项目命令
* **crawl**  
语法: `scrapy crawl <spider_name>`  
使用你项目中的spider进行爬取，即启动你的项目。这个命令将会经常用到，我们会在后面的内容中经常使用。
* check  
语法: crapy check [-l] <spider>  
运行contract检查，检查你项目中的错误之处。
* list  
语法: scrapy list  
列出当前项目中所有可用的spider。每行输出一个spider。
* **genspider**  
语法: `scrapy genspider [-t template] <name> <domain>`  
在当前项目中创建spider。该方法可以使用提前定义好的模板来生成spider。您也可以自己创建spider的源码文件。

**上述命令中，startproject，crawl，genspider是最常用的命令**

### 三、scrapy工程入门命令
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

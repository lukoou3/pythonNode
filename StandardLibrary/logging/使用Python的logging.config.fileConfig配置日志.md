## 使用Python的logging.config.fileConfig配置日志
`https://blog.csdn.net/cxx654/article/details/83216337`

Python的logging.config.fileConfig方式配置日志，通过解析conf配置文件实现。文件 logglogging.conf 配置如下：
```properties
[loggers]
keys=root,fileLogger,rotatingFileLogger
 
[handlers]
keys=consoleHandler,fileHandler,rotatingFileHandler
 
[formatters]
keys=simpleFormatter
 
[logger_root]
level=DEBUG
handlers=consoleHandler
 
[logger_fileLogger]
level=DEBUG
# 该logger中配置的handler
handlers=fileHandler
# logger 的名称
qualname=fileLogger
propagate=0
 
[logger_rotatingFileLogger]
level=DEBUG
# 这样配置，rotatingFileLogger中就同时配置了consoleHandler,rotatingFileHandler
# consoleHandler 负责将日志输出到控制台
# rotatingFileHandler 负责将日志输出保存到文件中
handlers=consoleHandler,rotatingFileHandler
qualname=rotatingFileLogger
propagate=0
 
[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)
 
[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('logs/logging.log', 'a')
 
[handler_rotatingFileHandler]
class=handlers.RotatingFileHandler
level=WARNING
formatter=simpleFormatter
args=("logs/rotating_logging.log", "a", 1*1024*1024, 5)
 
[formatter_simpleFormatter]
#format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
format=%(asctime)s - %(module)s - %(thread)d - %(levelname)s : %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

以上配置文件主要包含以下几部分：

* loggers : 配置logger信息。必须包含一个名字叫做root的logger，当使用无参函数logging.getLogger()时，默认返回root这个logger，其他自定义logger可以通过 logging.getLogger("fileLogger") 方式进行调用    
* handlers:定义声明handlers信息。常用的handlers包括 StreamHandler（仅将日志输出到kong控制台）、FileHandler（将日志信息输出保存到文件）、RotaRotatingFileHandler（将日志输出保存到文件中，并设置单个日志wenj文件的大小和日志文件个数）    
* formatter : 设置日志格式    
* logger_xxx : 对loggers中声明的logger进行逐个配置，且要一一对应    
* handler_xxx : 对handlers中声明的handler进行逐个配置，且要一一对应    
* formatter_xxx : 对声明的formatterjinx进行配置  

代码示例
```python
logging.config.fileConfig("logging.conf")
 
# 输出日志到控制台,获取的是root对应的logger
console_logger = logging.getLogger()
 
# 输出日志到单个文件
file_logger = logging.getLogger(name="fileLogger")
 
# rotatingFileLogger中额consoleHandler输出到控制台，rotatingHandler输出日志到文件
rotating_logger = logging.getLogger(name="rotatingFileLogger")
```

友情提示

进行以上配置后，在项目中需要进行日志输出的地方通过logging.getLogger()方式就可以获取到du应的logger，然后就可以使用logger.info("xxx")jinx进行日志输出了。

使用这种方式配置日志，一定要在项目的入口函数中就调用 logging.config.fileConfig("logging.conf")函数，因为 logging.conf 文件中，在handler中配置的是日志文件的相对地址，如果在其他代码文件中进行调用，由于相对地址的原因，将导致日志文件会出现在yixi意想不到的位置。



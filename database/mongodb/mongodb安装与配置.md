## 安装mongodb
windows直接下载exe安装即可，安装目录：

![2019-01-13_165332](/assets/2019-01-13_165332.png)


配置环境变量：
添加到环境变量：D:\apps\mongodb\bin

## 配置mongodb
#### 创建配置文件
可以在D:\apps\mongodb中手动创建两个空文件夹

D:\apps\mongodb\data\db

D:\apps\mongodb\log

并在D:\apps\mongodb\log下面创建一个空的mongo.log

在D:\apps\mongodb\config创建一个文件mongodb.conf，配置如下：
```
dbpath=D:\apps\mongodb\data\db           # 数据库文件
logpath=D:\apps\mongodb\log\mongodb.log    # 日志文件
logappend=true                        # 日志采用追加模式，配置后mongodb日志会追加到现有的日志文件，不会重新创建一个新文件
journal=true                        # 启用日志文件，默认启用
quiet=true                            # 这个选项可以过滤掉一些无用的日志信息，若需要调试使用请设置为 false
port=27017                            # 端口号 默认为 27017
```

#### 使用配置文件启动mongodb服务
执行一下命令：
```
sc create MongoDB binPath= "D:\apps\mongodb\bin\mongod.exe --service --config=D:\apps\mongodb\config\mongodb.conf"
```

#### 删除mongodb的windows服务
如果你不再需要mongodb的windows服务，可以手动将它删除
```
sc delete MongoDB
```

或者在mongodb的bin目录运行以下命令
```
mongod --remove --serviceName "MongoDB"
```

## Ubuntu中mongodb服务无法启动的问题
#### 主要问题
虽然能够成功安装MongoDB，并且能够正常启动MongoDB服务，但是当Ubuntu重启或者服务关掉之后，再次启动就会遇到下列问题
![1917338942-5979aa8820188_articlex](/assets/1917338942-5979aa8820188_articlex.png)

这个时候尝试下面的命令，会启动MongoDB，但是这个终端不能关闭
```
sudo mongod
```


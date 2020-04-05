
## 创建空壳虚拟机

新建虚拟机
![](assets/markdown-img-paste-20200404224457907.png)

下一步
![](assets/markdown-img-paste-20200404224612537.png)

选稍后
![](assets/markdown-img-paste-2020040422480922.png)

安装Linux系统对应的CentOS版，应该是vm15版本的原因没有CentOS 64的选项。
![](assets/markdown-img-paste-20200404225118935.png)
![](assets/markdown-img-paste-20200404225129153.png)

虚拟机命名和定位磁盘位置
![](assets/markdown-img-paste-20200404225409970.png)

处理器配置，看自己是否是双核、多核
![](assets/markdown-img-paste-20200404225510530.png)

设置内存为2GB
![](assets/markdown-img-paste-20200404225603442.png)

网络设置NAT
![](assets/markdown-img-paste-20200404225723734.png)

默认下一步
![](assets/markdown-img-paste-20200404225802507.png)

默认下一步
![](assets/markdown-img-paste-2020040422584602.png)


新建虚拟磁盘
![](assets/markdown-img-paste-20200404230028637.png)


设置磁盘容量
![](assets/markdown-img-paste-20200404230200242.png)

默认下一步，你在哪里存储这个磁盘文件
![](assets/markdown-img-paste-20200404230257183.png)

新建虚拟机向导配置完成
![](assets/markdown-img-paste-20200404230356885.png)

没必要使用声卡、打印机等
![](assets/markdown-img-paste-20200404230624778.png)

点完成。

## 连接镜像
右键设置
![](assets/markdown-img-paste-20200404231116935.png)

加载ISO
![](assets/markdown-img-paste-2020040423133371.png)

下面就可以开机安装系统了
![](assets/markdown-img-paste-20200404231436660.png)

## 安装系统
![](assets/markdown-img-paste-20200404231436660.png)

初始化欢迎进入页面，回车选择第一个开始安装配置，此外，在Ctrl+Alt可以实现Windows主机和VM之间窗口的切换
![](assets/markdown-img-paste-20200404231642643.png)

是否对CD媒体进行测试，直接跳过Skip
![](assets/markdown-img-paste-20200404231716850.png)

CentOS欢迎页面，直接点击Next
![](assets/markdown-img-paste-20200404231740677.png)

选择英文，工作中都是英文
![](assets/markdown-img-paste-20200404232250350.png)

默认美式键盘
![](assets/markdown-img-paste-20200404232443626.png)

默认
![](assets/markdown-img-paste-20200404232604685.png)

默认，格式化硬盘
![](assets/markdown-img-paste-20200404232648654.png)

主机名
![](assets/markdown-img-paste-20200404232826833.png)

选择时区，可以点击图形选择
![](assets/markdown-img-paste-20200404232938140.png)

设置root密码 （一定记住），123456就行了
![](assets/markdown-img-paste-20200404233148510.png)

硬盘分区，选自定义
![](assets/markdown-img-paste-20200404233125599.png)

根分区新建
![](assets/markdown-img-paste-2020040423350184.png)
![](assets/markdown-img-paste-20200404233515275.png)

创建Boot（引导）分区
![](assets/markdown-img-paste-20200404233911207.png)

创建swap分区
![](assets/markdown-img-paste-20200404234129429.png)

根目录所有的数据的分区(使用剩余大小)
![](assets/markdown-img-paste-20200404234510750.png)

下一步
![](assets/markdown-img-paste-20200404234731189.png)

格式化设备
![](assets/markdown-img-paste-2020040423481477.png)

![](assets/markdown-img-paste-20200404234913292.png)

下一步，安装引导程序
![](assets/markdown-img-paste-20200404235047125.png)

reboot(用的是最小化的安装包，比一般的少好几步)
![](assets/markdown-img-paste-20200404235329157.png)

## 开机配置
reboot后登录
![](assets/markdown-img-paste-20200404235541677.png)

查看ip配置
![](assets/markdown-img-paste-20200405000224186.png)

mac地址是由vm分配的(克隆的时候需要修改和这个一样)
![](assets/markdown-img-paste-20200405000432943.png)

配置ip
![](assets/markdown-img-paste-20200405001807653.png)

service network restart
![](assets/markdown-img-paste-20200405002022646.png)

ping一下百度和外面的本机，试试
![](assets/markdown-img-paste-20200405002210699.png)

外面的本机ping虚拟机试试
![](assets/markdown-img-paste-20200405002331364.png)

vm的网络配置(之前就配好了)
![](assets/markdown-img-paste-20200405002535109.png)

关闭防火墙&Selinux
```
service iptables stop
chkconfig iptables off

vi /etc/selinux/config
#修改这一行禁用
SELINUX=disabled
```
![](assets/markdown-img-paste-20200405003140971.png)

![](assets/markdown-img-paste-20200405003332822.png)

![](assets/markdown-img-paste-20200405003547626.png)

删除/etc/udev/rules.d/70-persistent-net.rules
```
rm -fr /etc/udev/rules.d/70-persistent-net.rules
```
![](assets/markdown-img-paste-20200405003901307.png)

poweroff关机

### 为什么要删除70-persistent-net.rules
VM：默认维护，每一台克隆，或，新建的虚拟机，MAC地址不重复

如果虚拟机保留 /etc/udev/rules.d/70-persistent-net.rules这个文件，在通过该虚拟机克隆的时候:
```
1，文件被带到新的虚拟机中
2，vm变更了新的虚拟机的mac地址
so：新机器不能使用eth0接口
你配置的/etc/sysconfig/network-scripts/ifcfg-eth0就不能应用
```

也可以保留这个文件，不过克隆后需要修改这个文件。删除这个文件简单方便一点。

## 对克隆模板拍摄快照
![](assets/markdown-img-paste-20200405004614224.png)

![](assets/markdown-img-paste-20200405004723983.png)

![](assets/markdown-img-paste-20200405004900775.png)

## 克隆节点
在最干净的快照克隆
![](assets/markdown-img-paste-20200405005126461.png)

![](assets/markdown-img-paste-2020040500522212.png)

使用完整的克隆
![](assets/markdown-img-paste-20200405005256511.png)

![](assets/markdown-img-paste-20200405005354494.png)

![](assets/markdown-img-paste-20200405005424919.png)

继续克隆node02、node03
![](assets/markdown-img-paste-20200405005720643.png)

## 配置克隆的节点
ip配置
![](assets/markdown-img-paste-2020040501034600.png)

配置主机名
vi /etc/sysconfig/network
![](assets/markdown-img-paste-2020040501065732.png)


hosts配置映射
vi /etc/hosts
![](assets/markdown-img-paste-20200405011242107.png)


每个节点都一样，主机名修改重启才生效。


还需要创建一个普通的用户，不能老是使用root用户。
![](assets/markdown-img-paste-20200405013210309.png)

配置 hadoop 用户 sudoer 权限
```
在 root 账号下，命令终端输入：vi /etc/sudoers

找到 root ALL=(ALL) ALL 这一行，

然后在他下面添加一行(yy复制行，p粘贴，i修改用户名)：

hadoop ALL=(ALL) ALL

保存，退出
```
![](assets/markdown-img-paste-20200405091258510.png)
 

poweroff关机，拍快照，方便以后环境清零测试。


重启之后在外面的Windows配置虚拟机的主机映射：
```
c:/windows/system32/drivers/etc/hosts   
```

```
192.168.216.31 node01
192.168.216.32 node02
192.168.216.33 node03
```



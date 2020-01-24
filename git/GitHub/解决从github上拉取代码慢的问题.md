## 解决访问github慢,从github上拉取代码慢的问题
1.获取Github相关网站的ip

访问`https://www.ipaddress.com`，找到页面中下方的IP Address Tools - Quick Links，分别输入`github.global.ssl.fastly.net`和`github.com`，查询ip地址。

2.修改本地host文件

Mac为例，命令行下输入：`sudo vi /etc/host`，然后输入电脑的密码，打开host文件。
Window为例 `C:\Windows\System32\drivers\etc`

3.增加host映射

参考如下，增加`github.global.ssl.fastly.net`和`github.com`的映射。
```
151.101.113.194   github.global.ssl.fastly.net
192.30.253.112   github.com
```

4.更新DNS缓存

命令行输入：`ipconfig /flushdns`，使增加的映射生效。

5.大功告成

接下来就可以随意访问Github和clone代码了。


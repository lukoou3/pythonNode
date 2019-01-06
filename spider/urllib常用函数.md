### 一、urllib常用函数
我还是用rquests吧

### 二、urllib.parse常用函数
##### 1、urllib.parse.urlparse(url)
解析url的协议，端口，域名，路径等
```
# 返回的结果其实是一个元组,我们可以通过索引来获取,也可以用属性名来获取 ：
# ParseResult的属性 scheme(:// 协议),netloc(/ 域名),path(访问路径),params(; 参数),query(查询条件),fragment(# 锚点)
#也可以直接访问ParseResult的其他属性如hostname
```

##### 2、urllib.parse.urljoin(base, url）
用于合并url
```python
urljoin("https://api.bbbbbb.me/yuujx/?url=","jiexi/?url=https://youku.com")
#'https://api.bbbbbb.me/yuujx/jiexi/?url=https://youku.com'
urljoin("https://api.bbbbbb.me/yuujx/?url=","/jiexi/?url=https://youku.com")
#'https://api.bbbbbb.me/jiexi/?url=https://youku.com'
urljoin("https://api.bbbbbb.me/yuujx/?url=","hppts://api.aa.com/jiexi/?url=https://youku.com")
#'hppts://api.aa.com/jiexi/?url=https://youku.com'
```

##### 3、urllib.parse.quote(url)
将内容转化为URL编码的格式

##### 4、urllib.parse.unquote(url)
进行URL解码

##### 5、urllib.parse.urlencode(dict)
序列化字典类型转换为URL编码后str

##### 6、urllib.parse.parse_qs(query)
反序列化将请求参数转回字典参数

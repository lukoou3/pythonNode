https://www.cnblogs.com/dachenzi/p/8242713.html
## 一、jinja2介绍
目前主流的模板系统，最常用的就是jinja2和mako。  
jinja2是Flask作者开发的一个模板系统，起初是仿django模板的一个模板引擎，为Flask提供模板支持，由于其灵活，快速和安全等优点被广泛使用。

#### jinja2的优点
jinja2之所以被广泛使用是因为它具有以下优点：    
* 相对于Template，jinja2更加灵活，它提供了控制结构，表达式和继承等。   
* 相对于Mako，jinja2仅有控制结构，不允许在模板中编写太多的业务逻辑。  
* 相对于Django模板，jinja2性能更好。  
* Jinja2模板的可读性很棒。  

#### 安装jinja2
pip install jinja2

## 二、jinja2语法
#### 1、基本语法
在jinja2中，存在三种语法：

* 控制结构 {% %}  
* 变量取值 {{ }}  
* 注释 {# #}  

下面是一个简单的jinja2例子
```
{# This is jinja code
 
    {% for file in filenames %}
    ...
    {% endfor %}
 
#}
```

#### 2、jinja2变量
jinja2模板中使用 {{ }} 语法表示一个变量，它是一种特殊的占位符。当利用jinja2进行渲染的时候，它会把这些特殊的占位符进行填充/替换，jinja2支持python中所有的Python数据类型比如列表、字段、对象等。
```
<p>this is a dicectory:{{ mydict['key'] }} </p>
<p>this is a list:{{ mylist[3] }} </p>
<p>this is a object:{{ myobject.something() }} </p>
```





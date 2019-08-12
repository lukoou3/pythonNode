## 字符串编码
Python3对Unicode字符的原生支持

Python2中使用 ASCII 码作为默认编码方式导致string有两种类型str和unicode，Python3只支持unicode的string。python2和python3字节和字符对应关系为：
```
- 编码&字符串 

   字符串：
      py2: 
         unicode         v = u"root"    本质上用unicode存储（万国码）
         (str/bytes)     v = "root"     本质用字节存储
     py3:         
         str             v = "root"     本质上用unicode存储（万国码）
         bytes           v = b"root"    本质上用字节存储
　编码：
　　py2: 
   　　- ascii 
  　　 文件头可以修改：#-*- encoding:utf-8 -*-
　　 py3:
  　　 - utf-8
   　　文件头可以修改：#-*- encoding:utf-8 -*-
```

## Unicode
Python 2 有 ASCII str() 类型，unicode() 是单独的，不是 byte 类型。

现在， 在 Python 3，我们最终有了 Unicode (utf-8) 字符串，以及一个字节类：byte 和 bytearrays。

Python3.X 源码文件默认使用utf-8编码

Python 2.x
```python
>>> str = "我爱北京天安门"
>>> str
'\xe6\x88\x91\xe7\x88\xb1\xe5\x8c\x97\xe4\xba\xac\xe5\xa4\xa9\xe5\xae\x89\xe9\x97\xa8'
>>> str = u"我爱北京天安门"
>>> str
u'\u6211\u7231\u5317\u4eac\u5929\u5b89\u95e8'
```

Python 3.x
```python
>>> str = "我爱北京天安门"
>>> str
'\xe6\x88\x91\xe7\x88\xb1\xe5\x8c\x97\xe4\xba\xac\xe5\xa4\xa9\xe5\xae\x89\xe9\x97\xa8'
>>> str = u"我爱北京天安门"
>>> str
u'\u6211\u7231\u5317\u4eac\u5929\u5b89\u95e8'
```

## print语法使用（print 从语句变为函数）
print语句被python3废弃，统一使用print函数

**print 换行和不换行区别**：
python2  print 不换行使用","即可
python3  print 不换行使用end=""

Python 2
```python
>>> str = "我爱北京天安门"
>>> str
'我爱北京天安门'
```
结果
```
Python 2.7.6
Hello, World!
text print more text on the same line
```

Python 3
```python
print('Python', python_version())
print('Hello, World!')
print("some text,", end="")
print(' print more text on the same line')
```
结果
```
Python 3.5.6
Hello, World!
some text, print more text on the same line
```

## 从键盘录入字符串
Python3中input得到的为str；Python2的input的到的为int型，Python2的raw_input得到的为str类型

**统一一下：Python3中用input，Python2中用row_input，都输入为str**

## 一些废弃类差异
1、print语句被python3废弃，统一使用print函数print语句被python3废弃，统一使用print函数    

2、exec语句被python3废弃，统一使用exec函数exec语句被python3废弃，统一使用exec函数    

3、execfile语句被Python3废弃，推荐使用exec(open("./filename").read())execfile语句被Python3废弃，推荐使用exec(open("./filename").read())    

4、不相等操作符"<>"被Python3废弃，统一使用"!="不相等操作符"<>"被Python3废弃，统一使用"!="    

5、long整数类型被Python3废弃，统一使用intlong整数类型被Python3废弃，统一使用int    

6、xrange函数被Python3废弃，统一使用range，Python3中range的机制也进行修改并提高了大数据集生成效率xrange函数被Python3废弃，统一使用range，Python3中range的机制也进行修改并提高了大数据集生成效率    

7、Python3中这些方法再不再返回list对象：dictionary关联的keys()、values()、items()，zip()，map()，filter()，但是可以通过list强行转换：Python3中这些方法再不再返回list对象：dictionary关联的keys()、values()、items()，zip()，map()，filter()，但是可以通过list强行转换：    
```python
mydict={"a":1,"b":2,"c":3}
mydict.keys()  #<built-in method keys of dict object at 0x000000000040B4C8>
list(mydict.keys()) #['a', 'c', 'b']
```

8、迭代器iterator的next()函数被Python3废弃，统一使用next(iterator)迭代器iterator的next()函数被Python3废弃，统一使用next(iterator)    

9、raw_input函数被Python3废弃，统一使用input函数raw_input函数被Python3废弃，统一使用input函数    

10、字典变量的has_key函数被Python废弃，统一使用in关键词字典变量的has_key函数被Python废弃，统一使用in关键词    

11、file函数被Python3废弃，统一使用open来处理文件，可以通过io.IOBase检查文件类型file函数被Python3废弃，统一使用open来处理文件，可以通过io.IOBase检查文件类型    

12、apply函数被Python3废弃apply函数被Python3废弃    

13、异常StandardError 被Python3废弃，统一使用Exception异常StandardError 被Python3废弃，统一使用Exception

## range 与 xrange
python2中range返回列表；xrange() 创建迭代对象，这个表现十分像生成器（比如。“惰性求值”）。但是这个 xrange-iterable 是无穷的，意味着你可以无限遍历。

python 3 中，range() 是像 xrange() 那样实现以至于一个专门的 xrange() 函数都不再存在（在 Python 3 中xrange() 会抛出命名异常）。

## 打开文件
原： file( ..... )
或 open(.....)

改为：
只能用 open(.....)

## 除法运算
Python3中/表示真除，%表示取余，//表示地板除（结果取整）；Python2中/表示根据除数被除数小数点位得到结果，//同样表示地板除

统一一下：Python3中/表示真除，%表示取余，//结果取整；Python2中带上小数点/表示真除，%表示取余，//结果取整

Python 2
```python
print '3 / 2 =', 3 / 2
print '3 // 2 =', 3 // 2
print '3 / 2.0 =', 3 / 2.0
print '3 // 2.0 =', 3 // 2.0
```
```
3 / 2 = 1
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

Python 3
```python
print('3 / 2 =', 3 / 2)
print('3 // 2 =', 3 // 2)
print('3 / 2.0 =', 3 / 2.0)
print('3 // 2.0 =', 3 // 2.0)
```
```
3 / 2 = 1.5
3 // 2 = 1
3 / 2.0 = 1.5
3 // 2.0 = 1.0
```

## 异常抛出和捕捉机制区别
Python2
```python
raise IOError, "file error" #抛出异常
except NameError, err:  #捕捉异常
```

Python3
```python
raise IOError("file error") #抛出异常
except NameError as err: #捕捉异常
```

## for循环中变量值区别
Python2，for循环会修改外部相同名称变量的值
```python
i = 1
print （'comprehension: ', [i for i in range(5)]）
print （'after: i =', i  ） #i=4
```

Python3，for循环不会修改外部相同名称变量的值
```python
i = 1
print （'comprehension: ', [i for i in range(5)]）
print （'after: i =', i  ） #i=1
```

## chr( K ) 与 ord( c )
python2
```
chr( K )   将编码K 转为字符，K的范围是 0 ~ 255
ord( c )   取单个字符的编码, 返回值的范围: 0 ~ 255
```
python3
```
chr( K )   将编码K 转为字符，K的范围是 0 ~ 65535
ord( c )   取单个字符的编码, 返回值的范围: 0 ~ 65535
```

应该是Python3使用unicode编码的原因，和java的字符串和字符一样

## 比较操作符区别
Python2中任意两个对象都可以比较
```python
11 < 'test' #True
```
Python3中只有同一数据类型的对象可以比较
```python
11 < 'test' # TypeError: unorderable types: int() < str()
```

## map、filter 和 reduce
这三个函数号称是函数式编程的代表。在 Python3.x 和 Python2.x 中也有了很大的差异。

首先我们先简单的在 Python2.x 的交互下输入 map 和 filter,看到它们两者的类型是 built-in function(内置函数):
```python
>>> filter
<built-in function filter>
>>> map
<built-in function map>
>>> filter
<built-in function filter>
```

它们输出的结果类型都是列表:
```python
>>> map(lambda x:x *2, [1,2,3])
[2, 4, 6]
>>> filter(lambda x:x %2 ==0,range(10))
[0, 2, 4, 6, 8]
>>>
```

但是在Python 3.x中它们却不是这个样子了：
```python
>>> map
<class 'map'>
>>> map(print,[1,2,3])
<map object at 0x10d8bd400>
>>> filter
<class 'filter'>
>>> filter(lambda x:x % 2 == 0, range(10))
<filter object at 0x10d8bd3c8>
>>>
```
首先它们从函数变成了类，其次，它们的返回结果也从当初的列表成了一个可迭代的对象, 我们尝试用 next 函数来进行手工迭代:
```python
>>> f =filter(lambda x:x %2 ==0, range(10))
>>> next(f)
0
>>> next(f)
2
>>> next(f)
4
>>> next(f)
6
>>>
```

对于比较高端的 reduce 函数，它在 Python 3.x 中已经不属于 built-in 了，被挪到 functools 模块当中。






















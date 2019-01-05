## 一、简介
python中的collections模块中有一些特殊的容器类型，有时会很方便。
collections是日常工作中的重点、高频模块，常用类型有：

    计数器（Counter）
    双向队列（deque）
    默认字典（defaultdict）
    有序字典（OrderedDict）
    可命名元组（namedtuple）
    
## 二、常用函数
### 1、namedtuple
namedtuple 是一个函数，它用来创建一个自定义的元组对象，并且规定了元组元素的个数，并可以用属性而不是索引来引用元组的某个元素。可以通过 namedtuple 来定义一种数据类型，它具备元组的不变性，又可以根据属性来引用，十分方便。
collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)
创建一个具名元组需要两个参数，一个是类名，另一个是类的各个字段的名字。后者可以是由数个字符串组成的可迭代对象，或者是由空格分隔开的字段名组成的字符串。

例子：
```python
from collections import namedtuple

p = namedtuple("person", "name,age,sex")
zhanglin = p("zhanglin",30,"male")
print(zhanglin.name,zhanglin.age)
City = namedtuple('City', 'name country population coordinates')
Mytuple = namedtuple('Mytuple', ['x','y'])
```

### 2、Counter
collections.Counter([iterable-or-mapping])
Counter作为字典dicit（）的一个子类用来进行hashtable计数，将元素进行数量统计，计数后返回一个字典，键值为元素，值为元素个数

常用方法：
    
    most_common(int)	按照元素出现的次数进行从高到低的排序，返回前int个元素的字典
    elements	返回经过计算器Counter后的元素，返回的是一个迭代器
    update	和set集合的update一样，对集合进行并集更新
    substract	和update类似，只是update是做加法，substract做减法,从另一个集合中减去本集合的元素
    iteritems	返回由Counter生成的字典的所有item
    iterkeys	返回由Counter生成的字典的所有key
    itervalues	返回由Counter生成的字典的所有value

例子：
```python
from collections import Counter

str = "abcbcaccbbad"
li = ["a","b","c","a","b","b"]
d = {"1":3, "3":2, "17":2}

#Counter获取各元素的个数，返回字典
print ("Counter(s):", Counter(str))
print ("Counter(li):", Counter(li))
print ("Counter(d):", Counter(d))

#most_common(int)按照元素出现的次数进行从高到低的排序，返回前int个元素的字典
d1 = Counter(str)
print ("d1.most_common(2):",d1.most_common(2))

#elements返回经过计算器Counter后的元素，返回的是一个迭代器
print ("sorted(d1.elements()):", sorted(d1.elements()))
print ('''("".join(d1.elements())):''',"".join(d1.elements()))
#若是字典的话返回value个key
d2 = Counter(d)
print("若是字典的话返回value个key:", sorted(d2.elements()))

#update和set集合的update一样，对集合进行并集更新
print ("d1.update("sas1"):",d1.update("sas1"))
```
aaa

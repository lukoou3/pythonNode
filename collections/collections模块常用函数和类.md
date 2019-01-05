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
p = namedtuple("person", "name,age,sex")
zhanglin = p("zhanglin",30,"male")
print(zhanglin.name,zhanglin.age)
City = namedtuple('City', 'name country population coordinates')
Mytuple = namedtuple('Mytuple', ['x','y'])
'''

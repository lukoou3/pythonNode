## 常用的函数
    itertools.groupby(iterable, key=None)
用于对序列进行分组，其中，iterable 是一个可迭代对象，keyfunc 是分组函数，用于对 iterable 的连续项进行分组，如果不指定，则默认对 iterable 中的连续相同项进行分组，返回一个 (key, sub-iterator) 的迭代器。  
注意使用此函数一定要对iterable先排序

    itertools.zip_longest(*iterables[,fillvalue=none])
zip_longest跟zip 类似，但迭代过程会持续到所有可迭代对象的元素都被迭代完。如果有指定 fillvalue，则会用其填充缺失的值，否则为 None。

    itertools.count(start=0,step=1)
返回以start为开头，步长step的无限序列迭代器

    itertools.cycle(iterable)
保存对象的副本，并无限重复返回每一个元素

    itertools.accumulate(iterable[, func])
对iterable对象内的每个元素依次做func运算，更新并输出，func要求为二目运算，详见operator模块

    itertools.chain(*iterables)
接收多个可迭代对象作为参数，将它们『连接』起来，作为一个新的迭代器返回。

## 一、itertools 模块简介
&emsp;&emsp;我们知道，迭代器的特点是：惰性求值（Lazy evaluation），即只有当迭代至某个值时，它才会被计算，这个特点使得迭代器特别适合于遍历大文件或无限集合等，因为我们不用一次性将它们存储在内存中。
&emsp;&emsp;Python 内置的 itertools 模块包含了一系列用来产生不同类型迭代器的函数或类，这些函数的返回都是一个迭代器，我们可以通过 for 循环来遍历取值，也可以使用 next() 来取值。
&emsp;&emsp;itertools 模块提供的迭代器函数有以下几种类型：
* `无限迭代器`：生成一个无限序列，比如自然数序列 1, 2, 3, 4, ...；
* ``有限迭代器``：接收一个或多个序列（sequence）作为参数，进行组合、分组和过滤等；
* ``组合生成器``：序列的排列、组合，求序列的笛卡儿积等；

#### 1、Infinite Iterators
    itertools.count(start=0,step=1)
返回以start为开头，步长step的无限序列迭代器

    itertools.cycle(iterable)
保存对象的副本，并无限重复返回每一个元素

    itertools.repeat(object[,times])
创建一个迭代器，重复生成object，times（如果已提供）指定重复计数，如果未提供times，将无止尽返回该对象

#### 2、Iterators terminating on the shortest input sequence
    itertools.accumulate(iterable[, func])
对iterable对象内的每个元素依次做func运算，更新并输出，func要求为二目运算，详见operator模块

    itertools.chain(*iterables)
接收多个可迭代对象作为参数，将它们『连接』起来，作为一个新的迭代器返回。

    itertools.chain.from_iterable(iterable)
将单个iterable中的所有元素拼接输出。

    itertools.compress(data,selectors)
可用于对数据进行筛选，当 selectors 的某个元素为 true 时，则保留 data 对应位置的元素，否则去除

    itertools.dropwhile(predicate, iterable)
其中，predicate 是函数，iterable 是可迭代对象。对于 iterable 中的元素，如果 predicate(item) 为 true，则丢弃该元素，否则返回该项及所有后续项。

    itertools.filterfalse(predicate, iterable)
输出为错的要素

    itertools.groupby(iterable, key=None)
用于对序列进行分组，其中，iterable 是一个可迭代对象，keyfunc 是分组函数，用于对 iterable 的连续项进行分组，如果不指定，则默认对 iterable 中的连续相同项进行分组，返回一个 (key, sub-iterator) 的迭代器。
注意使用此函数一定要对iterable先排序

    itertools.islice(iterable, stop)
    itertools.islice(iterable, start, stop[, step])
是切片选择，其中iterable 是可迭代对象，start 是开始索引，stop 是结束索引，step 是步长，start 和 step 可选。

    itertools.starmap(function, iterable)
类似 map 操作，它的使用形式如：imap(func, iter1, iter2, iter3, ...)，starmap 返回一个迭代器，元素为 func(i1, i2, i3, ...)，i1，i2 等分别来源于 iter, iter2。

    itertools.takewhile(predicate, iterable)
与filterfalse()的判断条件相反。

    itertools.tee(iterable, n=2)
tee 用于从 iterable 创建 n 个独立的迭代器，以元组的形式返回，n 的默认值是 2。

    itertools.zip_longest(*iterables[,fillvalue=none])
zip_longest跟zip 类似，但迭代过程会持续到所有可迭代对象的元素都被迭代完。如果有指定 fillvalue，则会用其填充缺失的值，否则为 None。

#### 3、Combinatoric generators
    itertools.product(*iterables[,repeat=1])
用于求多个可迭代对象的笛卡尔积，它跟嵌套的 for 循环等价，其中，repeat 是一个关键字参数，用于指定重复生成序列的次数。

    itertools.permutations(iterable[,r])
permutations 用于生成一个排列，其中，r 指定生成排列的元素的长度，如果不指定，则默认为可迭代对象的元素长度。

    itertools.combinations(iterable, r)
combinations 用于求序列的组合，其中，r 指定生成组合的元素的长度。

    itertools.combinations_with_replacement(iterable, r)
combinations_with_replacement 和 combinations 类似，但它生成的组合包含自身元素。

## 二、官网例子
##### Infinite iterators:
| Iterator | Arguments     | Results                                        | Example                     |
| -------- | ------------- | ---------------------------------------------- | --------------------------- |
| count()  | start, [step] | start, start+step, start+2*step, …             | count(10)-->1011121314...   |
| cycle()  | p             | p0, p1, … plast, p0, p1, …                     | cycle('ABCD')-->ABCDABCD... |
| repeat() | elem [,n]     | elem, elem, elem, … endlessly or up to n times | repeat(10,3)-->101010       |

##### Iterators terminating on the shortest input sequence:
| Iterator              | Arguments                   | Results                                       | Example                                           |
| --------------------- | --------------------------- | --------------------------------------------- | ------------------------------------------------- |
| accumulate()          | p [,func]                   | p0, p0+p1, p0+p1+p2, ...                      | accumulate([1,2,3,4,5])-->1361015                 |
| chain()               | p, q, ...                   | p0, p1, ... plast, q0, q1, ...                | chain('ABC','DEF')-->ABCDEF                       |
| chain.from_iterable() | iterable                    | p0, p1, ... plast, q0, q1, ...                | chain.from_iterable(['ABC','DEF'])-->ABCDEF       |
| compress()            | data, selectors             | (d[0] if s[0]), (d[1] if s[1]), ...           | compress('ABCDEF',[1,0,1,0,1,1])-->ACEF           |
| dropwhile()           | pred, seq                   | seq[n], seq[n+1], starting when pred fails    | dropwhile(lambdax:x<5,[1,4,6,4,1])-->641          |
| filterfalse()         | pred, seq                   | elements of seq where pred(elem) is false     | filterfalse(lambdax:x%2,range(10))-->02468        |
| groupby()             | iterable[, key]             | sub-iterators grouped by value of key(v)      |                                                   |
| islice()              | seq, [start,] stop [, step] | elements from seq[start:stop:step]            | islice('ABCDEFG',2,None)-->CDEFG                  |
| starmap()             | func, seq                   | func(*seq[0]), func(*seq[1]), ...             | starmap(pow,[(2,5),(3,2),(10,3)])-->3291000       |
| takewhile()           | pred, seq                   | seq[0], seq[1], until pred fails              | takewhile(lambdax:x<5,[1,4,6,4,1])-->14           |
| tee()                 | it, n                       | it1, it2, ... itn  splits one iterator into n |                                                   |
| zip_longest()         | p, q, ...                   | (p[0], q[0]), (p[1], q[1]), ...               | zip_longest('ABCD','xy',fillvalue='-')-->AxByC-D- |

##### Combinatoric iterators:
| Iterator                                | Arguments            | Results                                                       |
| --------------------------------------- | -------------------- | ------------------------------------------------------------- |
| product()                               | p, q, ... [repeat=1] | cartesian product, equivalent to a nested for-loop            |
| permutations()                          | p[, r]               | r-length tuples, all possible orderings, no repeated elements |
| combinations()                          | p, r                 | r-length tuples, in sorted order, no repeated elements        |
| combinations_with_replacement()         | p, r                 | r-length tuples, in sorted order, with repeated elements      |
| product('ABCD',repeat=2)                |                      | AAABACADBABBBCBDCACBCCCDDADBDCDD                              |
| permutations('ABCD',2)                  |                      | ABACADBABCBDCACBCDDADBDC                                      |
| combinations('ABCD',2)                  |                      | ABACADBCBDCD                                                  |
| combinations_with_replacement('ABCD',2) |                      | AAABACADBBBCBDCCCDDD                                          |

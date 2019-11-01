https://www.cnblogs.com/dodoye/p/6218192.html
[toc]

## 一、正则表达式的特殊字符：
| 特殊字符 | 意义说明 |
| --- | --- |
| '.' | 匹配包括换行符以内的任意一个字符。点号，在普通模式，它匹配除换行符外的任意一个字符。 |
| '^' | 匹配一个字符串的开始，在 MULTILINE 模式下，也将匹配任意一个新行的开始，尖尖号。 |
| '$' | 匹配一个字符串的结尾或者字符串最后面的换行符，在 MULTILINE 模式下，也匹配任意一行的行尾，美元符号。 |
| '*' | 匹配*前面re的重复0次或者任意多次，而且总是试图尽量多次地匹配，星号。 |
| '+' | 匹配+前面re的重复0次或者1次，如果有的话，也尽量匹配1次，加号。 |
| '?' | 匹配？前面re的重复0次或者1次，如果有的话，也尽量匹配1次，问号。 |
| *?， +?， ?? | 可以看到'*'，'+'和'?'都是贪婪的，但这也许并不是我们说要的，所以，可以在后面加个问号，将策略改为非贪婪，只匹配尽量少的RE，也就是第一个匹配结果。 |
| {m} | m是一个数字，匹配{m}前面的re重复m次。 |
| {m,n} | m和n都是数字，匹配{m,n}前面的RE重复m到n次，例如a{3,5}匹配3到5个连续的a。注意，如果省略m，将匹配0到n个前面的RE；如果省略n，将匹配n到无穷多个前面的RE；当然中间的逗号是不能省略的，不然就变成前面那种形式了。 |
| {m,n}? | {m,n}，也是贪婪的，a{3,5}如果有5个以上连续a的话，会匹配5个，这个也可以通过加问号改变。a{3,5}?如果可能的话，将只匹配3个a。 |
| '\' | 反斜杆，转义'*'，'?'等特殊字符，或者指定一个特殊序列,强烈建议用raw字符串来表述正则。 |
| [] | 方括号，用于指定一个字符的集合。可以单独列出字符，也可以用'-'连接起止字符以表示一个范围。特殊字符在中括号里将失效，比如[akm$]就表示字符'a'，'k'，'m'，或'$'，在这里$也变身为普通字符了。[a-z]匹配任意一个小写字母，[a-zA-Z0-9]匹配任意一个字母或数字。如果你要匹配']'或'-'本身，你需要加反斜杆转义，或者是将其置于中括号的最前面，比如[]]可以匹配']'。还可以对一个字符集合取反，以匹配任意不在这个字符集合里的字符，取反操作用一个'^'放在集合的最前面表示，放在其他地方的'^'将不会起特殊作用。例如[^5]将匹配任意不是'5'的字符；[^^]将匹配任意不是'^'的字符。注意：在中括号里+、*、(、)这类字符将会失去特殊含义，仅作为普通字符。反向引用也不能在中括号内使用。 |
| '&#124;' | 管道符号，A和B是任意的RE，那么A&#124;B就是匹配A或者B的一个新的RE。任意个数的RE都可以像这样用管道符号间隔连接起来。这种形式可以被用于组中。对于目标字符串，被'&#124;'分割的RE将自左至右一一被测试，一旦有一个测试成功，后面的将不再被测试，即使后面的RE可能可以匹配更长的串，换句话说，'&#124;'操作符是非贪婪的。要匹配字面意义上的'&#124;'，可以用反斜杆转义：\ &#124;，或是包含在反括号内：[&#124;]。 |
| (...) | 匹配圆括号里的RE匹配的内容，并指定组的开始和结束位置。组里面的内容可以被提取，也可以采用\number这样的特殊序列，被用于后续的匹配。要匹配字面意义上的'('和')'，可以用反斜杆转义：\(、\)，或是包含在反括号内：[(]、[)]。 |
| (?...) | 这是一个表达式的扩展符号。'?'后的第一个字母决定了整个表达式的语法和含义，除了(?P...)以外，表达式不会产生一个新的组。(?iLmsux)表示'i'、'L'、'm'、's'、'u'、'x'里的一个或多个字母。表达式不匹配任何字符，但是指定相应的标志：re.I(忽略大小写)、re.L(依赖locale)、re.M(多行模式)、re.S(.匹配所有字符)、re.U(依赖Unicode)、re.X(详细模式)。关于各个模式的区别。使用这个语法可以代替在re.compile()的时候或者调用的时候指定flag参数。另外，还要注意(?x)标志如果有的话，要放在最前面。 |
| (?:...) | 匹配内部的RE所匹配的内容，但是不建立组。 |
| (?P<name>...) | 和普通的圆括号类似，但是子串匹配到的内容将可以用命名的name参数来提取。组的name必须是有效的python标识符，而且在本表达式内不重名。命名了的组和普通组一样，也用数字来提取，也就是说名字只是个额外的属性。 |
| (?#...) | 注释，圆括号里的内容会被忽略。 |
| (?=...) | 如果 ... 匹配接下来的字符，才算匹配，但是并不会消耗任何被匹配的字符。例如 Isaac (?=Asimov) 只会匹配后面跟着 'Asimov' 的 'Isaac '，这个叫做“前瞻断言”。 |
| (?!...) | 和(?=...)相反，只匹配接下来的字符串不匹配 ... 的串，这叫做“反前瞻断言”。 |
| (?<=...) | 只有当当前位置之前的字符串匹配 ... ，整个匹配才有效，这叫“后顾断言”。字符串'abcdef'可以匹配正则(?<=abc)def，因为会后向查找3个字符，看是否为abc。所以内置的子RE，需要是固定长度的，比如可以是abc、a&#124;b，但不能是a*、a{3,4}。注意这种RE永远不会匹配到字符串的开头。 |
| (?<!...) | 这个叫做“反后顾断言”，子RE需要固定长度的，含义是前面的字符串不匹配 ... 整个才算匹配。 |
| (?(id/name)yes-pattern&#124;no-pattern) | 如有由id或者name指定的组存在的话，将会匹配yes-pattern，否则将会匹配no-pattern，通常情况下no-pattern也可以省略。例如：(<)?(\w+@\w+(?:\.\w+)+)(?(1)>)可以匹配 '<user@host.com>' 和 'user@host.com'，但是不会匹配 '<user@host.com'。 |


### 正则表达式特殊序列符号：
| 特殊序列符号 | 意义说明 |
| --- | --- |
| \number | 匹配number所指的组相同的字符串。组的序号从1开始。例如：(.+) \1可以匹配'the the'和'55 55'，但不匹配'the end'。这种序列在一个正则表达式里最多可以有99个，如果number以0开头，或是有3位以上的数字，就会被当做八进制表示的字符了。同时，这个也不能用于方括号内。 |
| \A | 只匹配字符串的开始。 |
| \b | 匹配单词边界（包括开始和结束），这里的“单词”，是指连续的字母、数字和下划线组成的字符串。注意，\b的定义是\w和\W的交界，所以精确的定义有赖于UNICODE和LOCALE这两个标志位。 |
| \B | 和\b相反，\B匹配非单词边界。也依赖于UNICODE和LOCALE这两个标志位。 |
| \d | 相当于[0-9] |
| \D | 和\d相反。相当于[^0-9] |
| \s | 匹配任何空白字符，等效于[ \t\n\r\f\v] |
| \S | 和\s相反，匹配任意非空白字符:[^\t\n\r\r\v] |
| \w | 匹配任意数字和字母:[a-zA-Z0-9] |
| \W | 和\w相反，匹配任意非数字和字母:[^a-zA-Z0-9] |
| \Z | 只匹配字符串的结尾。 |

例子：
```python
1、'$'演示:
普通模式下，foo.$去搜索'foo1\nfoo2\n'只会找到'foo2′，但是在 MULTILINE 模式，还能找到 ‘foo1′，而且就用一个 $ 去搜索'foo\n'的话，会找到两个空的匹配：一个是最后的换行符，一个是字符串的结尾。如下演示：
#'$'演示
>>> re.findall('(foo.$)', 'foo1\nfoo2\n')
['foo2']
>>> re.findall('(foo.$)', 'foo1\nfoo2\n')
['foo2']
>>> re.findall('(foo.$)', 'foo1\nfoo2\n', re.MULTILINE)
['foo1', 'foo2']
>>> re.findall('($)', 'foo\n')
['', '']

2、*?， +?， ??演示：
>>> re.findall('<(.*)>', '<H1>title</H1>')
['H1>title</H1']
>>> re.findall('<(.*?)>', '<H1>title</H1>')
['H1', '/H1']
>>> re.search('<(.*)>', '<H1>title</H1>').group()
'<H1>title</H1>'
>>> re.search('<(.*?)>', '<H1>title</H1>').group()
'<H1>'

3、(?...)演示：和指定了re.MULTILINE是一样的效果
>>> re.findall('(?m)(foo.$)', 'foo1\nfoo2\n')
['foo1', 'foo2']

4、(?P<name>...)演示：
>>> m=re.match('(?P<var>[a-zA-Z_]\w*)', 'abc=123')
>>> m.group('var') #通过var参数取值
'abc'
>>> m.group(1)#通过数字取值
'abc'
>>> re.match('<(?P<tagname>\w*)>.*</(?P=tagname)>', '<h1>xxx</h2>')  #这个不匹配
>>> re.match('<(?P<tagname>\w*)>.*</(?P=tagname)>', '<h1>xxx</h1>')  #这个匹配
<_sre.SRE_Match object; span=(0, 12), match='<h1>xxx</h1>'>

5、(?<=...)演示：
>>> m = re.search('(?<=-)\w+', 'spam-egg')
>>> m.group(0)
'egg'
```

## 二、正则表达式的编译标志：
| 标志 | 含义 |
| ---- | ---- |
| re.I，re.IGNORECASE | 让正则表达式忽略大小写，这样一来，[A-Z]也可以匹配小写字母了。此特性和locale无关。 |
| re.L，re.LOCALE | 让\w、\W、\b、\B、\s和\S依赖当前的locale。 |
| re.M，re.MULTILINE | 影响'^'和'$'的行为，指定了以后，'^'会增加匹配每行的开始（也就是换行符后的位置）；'$'会增加匹配每行的结束（也就是换行符前的位置）。 |
| re.S，re.DOTALL | 影响'.'的行为，平时'.'匹配除换行符以外的所有字符，指定了本标志以后，也可以匹配换行符。 |
| re.U，re.UNICODE | 让\w、\W、\b、\B、\d、\D、\s和\S依赖Unicode库。 |
| re.X，re.VERBOSE | 运用这个标志，你可以写出可读性更好的正则表达式：除了在方括号内的和被反斜杠转义的以外的所有空白字符，都将被忽略，而且每行中，一个正常的井号后的所有字符也被忽略，这样就可以方便地在正则表达式内部写注释了。 |


下面两个正则表达式是等效的
```python
a = re.compile(r"""\d +  # the integral part
                   \.    # the decimal point
                   \d *  # some fractional digits""", re.X)
b = re.compile(r"\d+\.\d*")
```

```python
如果你希望在正则表达式中使用re.VERBOSE 来编写注释，还希望使用re.IGNORECASE 来忽略大小写，该怎么办？遗憾的是，re.compile()函数只接受一个值作为它的第二参数。可以使用管道字符（|）将变量组合起来，从而绕过这个限制。管道字符在这里称为“按位或”操作符。
所以，如果希望正则表达式不区分大小写，并且句点字符匹配换行，就可以这样构造re.compile()调用：
>>> someRegexValue = re.compile('foo', re.IGNORECASE | re.DOTALL)
使用第二个参数的全部3 个选项，看起来像这样：
>>> someRegexValue = re.compile('foo', re.IGNORECASE | re.DOTALL | re.VERBOSE)
```

## 三、re模块主要的功能函数：
    常用的功能函数包括：compile、search、match、split、findall（finditer）、sub（subn）

### 1、search
    re.search(pattern, string[, flags])
    search (string[, pos[, endpos]])
作用：把正则表达式语法转化成正则表达式对象，可以用它进行匹配 match()，search()以及其他方法

#### flags定义包括：
| 标志 | 含义 |
| ---- | ---- |
| re.I，re.IGNORECASE | 让正则表达式忽略大小写，这样一来，[A-Z]也可以匹配小写字母了。此特性和locale无关。 |
| re.L，re.LOCALE | 让\w、\W、\b、\B、\s和\S依赖当前的locale。 |
| re.M，re.MULTILINE | 影响'^'和'$'的行为，指定了以后，'^'会增加匹配每行的开始（也就是换行符后的位置）；'$'会增加匹配每行的结束（也就是换行符前的位置）。 |
| re.S，re.DOTALL | 影响'.'的行为，平时'.'匹配除换行符以外的所有字符，指定了本标志以后，也可以匹配换行符。 |
| re.U，re.UNICODE | 让\w、\W、\b、\B、\d、\D、\s和\S依赖Unicode库。 |
| re.X，re.VERBOSE | 运用这个标志，你可以写出可读性更好的正则表达式：除了在方括号内的和被反斜杠转义的以外的所有空白字符，都将被忽略，而且每行中，一个正常的井号后的所有字符也被忽略，这样就可以方便地在正则表达式内部写注释了。 |

#### 所以如果在单个程序中多次使用表达式，则使用re.compile()并保存生成的正则表达式对象以便重用将会更有效。

例子：
```python
prog = re.compile(pattern)
result = prog.match(string)
相当于：
result = re.match(pattern, string)
```

### 2、search
    re.search(pattern, string[, flags])
    search (string[, pos[, endpos]])
作用：在字符串中查找匹配正则表达式模式的第一个位置，返回 MatchObject 的实例，如果没有找到匹配的位置，则返回 None。

```python
>>> re.search(r'[ab]',"aaaasdfg")
<_sre.SRE_Match object; span=(0, 1), match='a'>
```

### 3、match
    re.match(pattern, string[, flags])
    match(string[, pos[, endpos]])
作用：match() 函数只在字符串的开始位置尝试匹配正则表达式，也就是只报告从位置 0 开始的匹配情况，而 search() 函数是扫描整个字符串来查找匹配。如果想要搜索整个字符串来寻找匹配，应当用 search()。
请注意，即使在MULTILINE模式下，re.match()只会匹配字符串的开头，而不是每行的开头。

```python
>>> re.match("a", "abcdef")
<_sre.SRE_Match object; span=(0, 1), match='a'>
```

#### search（）与match（）的区别
match()只匹配字符串的开头！

```python
看例子：
>>> re.match("c", "abcdef")    # No match
>>> re.search("c", "abcdef")   # Match
<_sre.SRE_Match object; span=(2, 3), match='c'>

以正值开始的正则表达式’^’可用于search()限制字符串开始处的匹配：

>>> re.match("c", "abcdef")    # No match
>>> re.search("^c", "abcdef")  # No match
>>> re.search("^a", "abcdef")  # Match
<_sre.SRE_Match object; span=(0, 1), match='a'>

但是请注意，在MULTILINE模式中，match()只匹配字符串的开头，而使用search()正则表达式’^’匹配每行的开头。
>>> re.match('X', 'A\nB\nX', re.MULTILINE)  # No match
>>> re.search('^X', 'A\nB\nX', re.MULTILINE)  # Match
<_sre.SRE_Match object; span=(4, 5), match='X'>
```

### 4、findall
    re.findall(pattern, string[, flags])
    findall(string[, pos[, endpos]])
作用：返回字符串中模式的所有非重叠匹配项，作为字符串列表。 字符串从左到右扫描，匹配按找到的顺序返回。 如果模式中存在一个或多个组，则返回组的列表; 如果该模式有多个组，这将是一个元组列表。

```python
>>> re.findall(r'a',"aboisdhiajhsasa")
['a', 'a', 'a', 'a']
#这个返回的就是元组的列表
>>> re.findall('(\d+)\.(\d+)\.(\d+)\.(\d+)', 'My IP is 192.168.0.2, and your is
192.168.0.3.')
[('192', '168', '0', '2'), ('192', '168', '0', '3')]
```

#### 作为findall()方法的返回结果的总结，请记住下面两点：
```python
1．如果调用在一个没有分组的正则表达式上，例如\d\d\d-\d\d\d-\d\d\d\d，方法
findall()将返回一个匹配字符串的列表，例如['415-555-9999', '212-555-0000']。
2．如果调用在一个有分组的正则表达式上，例如(\d\d\d)-(\d\d\d)-(\d\d\d\d)，方
法findall()将返回一个字符串的元组的列表（每个分组对应一个字符串），例如[('415',
'555', '1122'), ('212', '555', '0000')]。
```

### 5、sub
    re.sub(pattern, repl, string[, count, flags])
    sub(repl, string[, count=0])
说明：在字符串 string 中找到匹配正则表达式 pattern 的所有子串，用另一个字符串 repl 进行替换。如果没有找到匹配 pattern 的串，则返回未被修改的 string。Repl 既可以是字符串也可以是一个函数。

**Repl 既可以是字符串也可以是一个函数**：回调函数的参数是match对象

```python
#!/usr/bin/env python
import re
p = re.compile('(one|two|three)')
print(p.sub('num','one word two words three words apple',2))
 #输出结果：
num word num words three words apple

re.sub(r'www\.(.*)\..{3}',r'\1','hello,www.dxy.com')
'hello,dxy'
# r'1' 是第一组的意思
#通过正则匹配找到符合规则的"www.dxy.com" ，取得 组1字符串 去替换 整个匹配。

如果repl是个函数，每次pattern被匹配到的时候，都会被调用一次，传入一个匹配到的MatchObject对象，需要返回一个字符串，在匹配到的位置，就填入返回的字符串。
>>> def dashrepl(matchobj):
...     if matchobj.group(0) == '-': return ' '
...     else:return '-'
>>> re.sub('-{1,2}', dashrepl, 'pro----gram-files')
'pro--gram files'

零长度的匹配也会被替换
>>> re.sub('x*', '-', 'abcxxd')
'-a-b-c-d-'

特殊地，在替换字符串里，如果有\g这样的写法，将匹配正则的命名组（前面介绍过的，(?P...)这样定义出来的东西）。\g这样的写法，也是数字的组，也就是说，\g<2>一般和\2是等效的，但是万一你要在\2后面紧接着写上字面意义的0，你就不能写成\20了（因为这代表第20个组），这时候必须写成\g<2>0，另外，\g<0>代表匹配到的整个子串。
>>> re.sub('-(\d+)-', '-\g<1>0\g<0>', 'a-11-b-22-c')
'a-110-11-b-220-22-c'
```

### 6、split
    re.split(pattern, string[, maxsplit=0, flags=0])
    split(string[, maxsplit=0])
由模式发生的分割字符串。如果在模式中使用捕获圆括号，则模式中所有组的文本也将作为结果列表的一部分返回。如果maxsplit不为零，则最多 发生maxsplit分割，并将其余的字符串作为列表的最后一个元素返回。

举例：
```python
>>> re.split('\W+', 'Words, words, words.')
['Words', 'words', 'words', '']
>>> re.split('(\W+)', 'Words, words, words.')
['Words', ', ', 'words', ', ', 'words', '.', '']
>>> re.split('\W+', 'Words, words, words.', 1)
['Words', 'words, words.']
>>> re.split('[a-f]+', '0a3B9', flags=re.IGNORECASE)
['0', '3', '9']

如果分隔符中存在捕获组，并且匹配字符串的开头，则结果将以空字符串开头。字符串的末尾也是一样：
>>> re.split('(\W+)', '...words, words...')
['', '...', 'words', ', ', 'words', '...', '']
```

### 7、finditer
    re.finditer(pattern, string[, flags])
    finditer(string[, pos[, endpos]])
说明：和 findall 类似，在字符串中找到正则表达式所匹配的所有子串，并组成一个迭代器返回。

```python
>>> for m in re.finditer('\w+', 'hello, world!'):
...     print(m.group())
...
hello
world
```

### 8、Match object对象
    The result of re.match() and re.search().Match objects always have a boolean value of True.
    上面的函数中，只有match、search返回Match object，其他的函数没有

事例：
a、
```python
pat = re.compile(r'www\.(.*)\.(.*)')       #用()表示1个组，2个组
m = pat.match('www.dxy.com')
m.group()                                  #默认为0，表示匹配整个字符串
'www.dxy.com'
m.group(1)                                 #返回给定组1匹配的子字符串
'dxy'
m.group(2)
'com'
```


b、
```python
prog = re.compile(r'(?P<tagname>abc)(.*)(?P=tagname)')
result1 = prog.match('abclfjlad234sjldabc')
print(result1)
print(result1.groups())
print result1.group('tagname')
print(result1.group(2))
print(result1.groupdict())

>>>
<_sre.SRE_Match object at 0x027B6CC8>
('abc', 'lfjlad234sjld')
abc
lfjlad234sjld
{'tagname': 'abc'}

解释：
我们可以看到result1已经由字符串转换成了一个正则对象。
resule.groups()可以查看出来所有匹配到的数据，每个()是一个元素，最终返回一个tuple
group()既可以通过下标（从1开始）的方式访问，也可以通过分组名进行访问。
groupdict只能显示有分组名的数据
```

-----------

```
group([group1, …]):
```
获得一个或多个分组截获的字符串；指定多个参数时将以元组形式返回。group1可以使用编号也可以使用别名；编号0代表整个匹配的子串；不填写参数时，返回group(0)；没有截获字符串的组返回None；截获了多次的组返回最后一次截获的子串。
```
groups([default]):
```
以元组形式返回全部分组截获的字符串。相当于调用group(1,2,…last)。default表示没有截获字符串的组以这个值替代，默认为None。
```
groupdict([default]):
```
返回以有别名的组的别名为键、以该组截获的子串为值的字典，没有别名的组不包含在内。default含义同上。

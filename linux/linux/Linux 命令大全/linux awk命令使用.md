linux awk命令使用

awk是一个强大的文本分析工具，相对于grep的查找，sed的编辑，awk在其对数据分析并生成报告时，显得尤为强大。简单来说awk就是把文件逐行的读入，以空格为默认分隔符将每行切片，切开的部分再进行各种分析处理。

使用方法   ： awk '{pattern + action}' {filenames}

尽管操作可能会很复杂，但语法总是这样，其中 pattern 表示 AWK 在数据中查找的内容，而 action 是在找到匹配内容时所执行的一系列命令。花括号（{}）不需要在程序中始终出现，但它们用于根据特定的模式对一系列指令进行分组。 pattern就是要表示的正则表达式，用斜杠括起来。

awk语言的最基本功能是在文件或者字符串中基于指定规则浏览和抽取信息，awk抽取信息后，才能进行其他文本操作。完整的awk脚本通常用来格式化文本文件中的信息。通常，awk是以文件的一行为处理单位的。awk每接收文件的一行，然后执行相应的命令，来处理文本。


```sh
1、打印文件的第一列(域) ： awk '{print $1}' filename
2、打印文件的前两列(域) ： awk '{print $1,$2}' filename
3、打印完第一列，然后打印第二列 ： awk '{print $1 $2}' filename
4、打印文本文件的总行数 ： awk 'END{print NR}' filename
5、打印文本第一行 ：awk 'NR==1{print}' filename
6、打印文本第二行第一列 ：sed -n "2, 1p" filename | awk 'print $1'
```

## 一、awk的用法
```sh
awk 'BEGIN{ commands } pattern{ commands } END{ commands }'
```
第一步：运行BEGIN{ commands }语句块中的语句。

第二步：从文件或标准输入(stdin)读取一行。然后运行pattern{ commands }语句块，它逐行扫描文件，从第一行到最后一行反复这个过程。直到文件所有被读取完成。

第三步：当读至输入流末尾时。运行END{ commands }语句块。

BEGIN语句块在awk開始从输入流中读取行之前被运行，这是一个可选的语句块，比方变量初始化、打印输出表格的表头等语句通常能够写在BEGIN语句块中。

END语句块在awk从输入流中读取全然部的行之后即被运行。比方打印全部行的分析结果这类信息汇总都是在END语句块中完毕，它也是一个可选语句块。

pattern语句块中的通用命令是最重要的部分，它也是可选的。假设没有提供pattern语句块，则默认运行{ print }，即打印每个读取到的行。awk读取的每一行都会运行该语句块。

这三个部分缺少任何一部分都可以。


## 二、awk的内置变量
* $0 当前记录（这个变量中存放着整个行的内容）    
* $1~$n 当前记录的第n个字段，字段间由FS分隔    
* F、FS 输入字段分隔符 默认是空格或Tab    
* NF 当前记录中的字段个数，就是有多少列    
* NR 已经读出的记录数，就是行号，从1开始，如果有多个文件话，这个值也是不断累加中。    
* FNR 当前记录数，与NR不同的是，这个值会是各个文件自己的行号    
* RS 输入的记录分隔符， 默认为换行符    
* OFS 输出字段分隔符， 默认也是空格    
* ORS 输出的记录分隔符，默认为换行符    
* FILENAME 当前输入文件的名字


查看测试文件：
```sh
~/codes$ cat order.txt 
jack 2015-01-01 10
tony 2015-01-02 15
jack 2015-02-03 23
tony 2015-01-04 29
jack 2015-01-05 46
jack 2015-04-06 42
tony 2015-01-07 50
jack 2015-01-08 55
mart 2015-04-08 62
mart 2015-04-09 68
neil 2015-05-10 12
mart 2015-04-11 75
neil 2015-06-12 80
mart 2015-04-13 94
```

输出正行,在这里awk 后面没有BEGIN和END，跟着的是pattern，也就是每一行都会经过这个命令
```sh
~/codes$ head -n 3 order.txt | awk '{print $0}'
jack 2015-01-01 10
tony 2015-01-02 15
jack 2015-02-03 23
```

输出第一列
```sh
~/codes$ head -n 3 order.txt | awk '{print $1}'
jack
tony
jack
```

输出第一列，每行的列数
```sh
~/codes$ head -n 3 order.txt | awk '{print $1,NF}'
jack 3
tony 3
jack 3
```

输出最后一列
```sh
~/codes$ head -n 3 order.txt | awk '{print $NF}'
10
15
23
```

输出倒数第二列
```sh
~/codes$ head -n 3 order.txt | awk '{print $(NF-1)}'
2015-01-01
2015-01-02
2015-02-03
```

指定分隔符
```sh
~/codes$ head -n 3 order.txt | awk -F2015- '{print $1,$2}'
jack  01-01 10
tony  01-02 15
jack  02-03 23
~/codes$ head -n 3 order.txt | awk -F'2015-' '{print $1,$2}'
jack  01-01 10
tony  01-02 15
jack  02-03 23
~/codes$ head -n 3 order.txt | awk -FS2015- '{print $1,$2}'
jack 2015-01-01 10 
tony 2015-01-02 15 
jack 2015-02-03 23
```

多分隔符的使用：
```
[root@localhost ftl]# awk -F "[/]" 'NR == 4 {print $0,"\n",$1}' /etc/passwd
这里以/为分隔符，多个分隔符利用[]然后在里面写分隔符即可
```

利用正则过滤多个空格
```
[root@localhost ~]# ifconfig |grep eth* | awk -F '[ ]+' '{print $1}'
```

简单的正则，\d是不支持的
```sh
~/codes$ head -n 3 order.txt | awk -F'[0-9]+' '{print $1,$2,$3}'
jack  - -
tony  - -
jack  - -
```

输出行号，带着看看输出中逗号的作用
```sh
codes$ head -n 3 order.txt | awk '{print NR,$1,$3}'
1 jack 10
2 tony 15
3 jack 23
codes$ head -n 3 order.txt | awk '{print NR$1,$3}'
1jack 10
2tony 15
3jack 23
codes$ head -n 3 order.txt | awk '{print NR $1,$3}'
1jack 10
2tony 15
3jack 23
codes$ head -n 3 order.txt | awk '{print NR " " $1,$3}'
1 jack 10
2 tony 15
3 jack 23
```

查询第3行到第7行的第二列
```sh
~/codes$ awk '{if(NR>=3 && NR<=7) print NR,$2}' order.txt
3 2015-02-03
4 2015-01-04
5 2015-01-05
6 2015-04-06
7 2015-01-07
```

查询第3行到第7行的第二列，利用pattern（awk 'BEGIN{ commands } pattern{ commands } END{ commands }'）
```sh
~/codes$ awk 'NR>=3&&NR<=7{print NR,$2}' order.txt
3 2015-02-03
4 2015-01-04
5 2015-01-05
6 2015-04-06
7 2015-01-07
~/codes$ awk 'NR>=3 && NR<=7{print NR,$2}' order.txt
3 2015-02-03
4 2015-01-04
5 2015-01-05
6 2015-04-06
7 2015-01-07
```

添加了BEGIN和END
```sh
codes$ head -n 3 order.txt | awk  'BEGIN{print "name orderdate cost "} {print $1,$2,$3}'
name orderdate cost 
jack 2015-01-01 10
tony 2015-01-02 15
jack 2015-02-03 23
codes$ head -n 3 order.txt | awk  'BEGIN{print "name orderdate cost "} {print $1,$2,$3} END{print "1 2 3"}'
name orderdate cost 
jack 2015-01-01 10
tony 2015-01-02 15
jack 2015-02-03 23
1 2 3
```

## 二、awk的输出：print和printf
⑴、print的使用格式：
```sh
print item1, item2, ...
```

要点：

①、各项目之间使用逗号隔开，而输出时则以空白字符分隔；

②、输出的item可以为字符串或数值、当前记录的字段(如$1)、变量或awk的表达式；数值会先转换为字符串，而后再输出；

③、print命令后面的item可以省略，此时其功能相当于print $0, 因此，如果想输出空白行，则需要使用print ""；

注意，在AWK中，$表示字段，用户变量不需要加$，这是AWK与shell或者Perl不同之处！在shell中，变量定义时不加$，再次引用时则需要用$，而在Perl中，无论定义和引用时都需要加$ (Perl中$表示标量，另有@和%符号表示数组和Hash变量)。

⑵、printf的使用格式
```sh
printf format, item1, item2, ...
```

format格式的指示符都以%开头，后跟一个字符,

```sh
codes$ head -n 3 order.txt | awk '{printf "%5s %12s %3s\n",$1,$2,$3}'
 jack   2015-01-01  10
 tony   2015-01-02  15
 jack   2015-02-03  23
codes$ head -n 3 order.txt | awk '{printf "%5s%12s%3s\n",$1,$2,$3}'
 jack  2015-01-01 10
 tony  2015-01-02 15
 jack  2015-02-03 23
```

## 三、变量和赋值
除了awk的内置变量，awk还可以自定义变量, awk中的循环语句同样借鉴于C语言，支持while、do/while、for、break、continue，这些关键字的语义和C语言中的语义完全相同。

如下引入变量sum，统计py文件的大小：
```sh
root@ubuntu:~# ls -l  *.py | awk '{sum+=$5} END {print sum}'
574
```

统计某个文件夹下的大于100k文件的数量和总和
```sh
ls -l|awk '{if($5>100){count++; sum+=$5}} {print "Count:" count,"Sum: " sum}'  【因为awk会轮询统计，所以会显示整个过程】
ls -l|awk '{if($5>100){count++; sum+=$5}} END{print "Count:" count,"Sum: " sum}' 【天界END后只显示最后的结果】
```

`awk -v # 设置变量`
-v 选项定义的变量在脚本运行之前即存在，可以在脚本的 BEGIN 流程中被调用；
```sh
~/codes$ awk -v num1=23.4 -v num2=45.5 'BEGIN{print num1+num2}'
68.9
```

这里面似乎数字和字符串相加返回原数字，注意下面是如何取第二列的
```sh
codes$ head -n 3 order.txt | awk -v a=1 '{print $1,$1+a}'
jack 1
tony 1
jack 1
codes$ head -n 3 order.txt | awk -v a=1 '{print $1,$(1+a)}'
jack 2015-01-01
tony 2015-01-02
jack 2015-02-03
```

## 四、模式和操作

⑴、模式可以是以下任意一个：

* /正则表达式/：使用通配符的扩展集。    
* 关系表达式：可以用下面运算符表中的关系运算符进行操作，可以是字符串或数字的比较，如$2>$1选择第二个字段比第一个字段长的行。    
* 模式匹配表达式：用运算符~(匹配)和~!(不匹配)。    
* 模式，模式：指定一个行的范围。该语法不能包括BEGIN和END模式。    
* BEGIN：让用户指定在第一条输入记录被处理之前所发生的动作，通常可在这里设置全局变量。    
* END：让用户在最后一条输入记录被读取之后发生的动作。

⑵、操作由一人或多个命令、函数、表达式组成，之间由换行符或分号隔开，并位于大括号内。主要有四部份：

* 变量或数组赋值    
* 输出命令    
* 内置函数    
* 控制流命令

## 五、awk模式使用

### 1、正则表达式，格式为/regex/
这个模式匹配的是正行

过滤以j开头的所有行，打印每一行
```sh
codes$ awk '/^j/{print $0}' order.txt 
jack 2015-01-01 10
jack 2015-02-03 23
jack 2015-01-05 46
jack 2015-04-06 42
jack 2015-01-08 55
```

过滤以0开头的所有行，打印每一行
```sh
codes$ awk '/0$/{print $0}' order.txt 
jack 2015-01-01 10
tony 2015-01-07 50
neil 2015-06-12 80
```

过滤包含05的所有行，打印每一行
```sh
codes$ awk '/05/{print $0}' order.txt 
jack 2015-01-05 46
neil 2015-05-10 12
```

过滤不包含05的所有行（模式取反），打印每一行
```sh
~/codes$ awk '!/05/{print $0}' order.txt
jack 2015-01-01 10
tony 2015-01-02 15
jack 2015-02-03 23
tony 2015-01-04 29
jack 2015-04-06 42
tony 2015-01-07 50
jack 2015-01-08 55
mart 2015-04-08 62
mart 2015-04-09 68
mart 2015-04-11 75
neil 2015-06-12 80
mart 2015-04-13 94
```

### 2、模式匹配表达式
用运算符`~(匹配)和~!(不匹配)`。

可以匹配某一列，该语法不能包括BEGIN和END模式。
```
x~y:x为字符串，y为模式，如果x可以被模式匹配则为真，否则为假
x!~y:与x~y相反
```

过滤第二列包含2015-04的所有行，打印每一行
```sh
codes$ awk '$2 ~ "2015-04"{print $0}' order.txt 
jack 2015-04-06 42
mart 2015-04-08 62
mart 2015-04-09 68
mart 2015-04-11 75
mart 2015-04-13 94
codes$ awk '$2 ~ /2015-04/{print $0}' order.txt 
jack 2015-04-06 42
mart 2015-04-08 62
mart 2015-04-09 68
mart 2015-04-11 75
mart 2015-04-13 94
```

过滤第二列不包含2015-01和2015-04的所有行（模式取反），打印每一行
```sh
codes$ awk '$2 !~ /2015-0[14]/{print $0}' order.txt 
jack 2015-02-03 23
neil 2015-05-10 12
neil 2015-06-12 80

```

### 3、关系表达式
可以用下面章节中的关系运算符进行操作，可以是字符串或数字的比较，如`$2>$1`选择第二个字段比第一个字段长的行。

过滤第三列大于50所有行，打印每一行
```sh
codes$ awk '$3>50{print $0}' order.txt 
jack 2015-01-08 55
mart 2015-04-08 62
mart 2015-04-09 68
mart 2015-04-11 75
neil 2015-06-12 80
mart 2015-04-13 94
```

过滤第三列大于50小于80所有行，打印每一行
```sh
codes$ awk '$3>50 && $3<80{print $0}' order.txt 
jack 2015-01-08 55
mart 2015-04-08 62
mart 2015-04-09 68
mart 2015-04-11 75
```
打印第四行
```sh
codes$ awk 'NR==4{print $0}' order.txt
tony 2015-01-04 29
```

### 5、指定范围，格式为pattern,pattern2

看一下数据
```sh
~/codes$ awk '{print NR,$0}' order.txt
1 jack 2015-01-01 10
2 tony 2015-01-02 15
3 jack 2015-02-03 23
4 tony 2015-01-04 29
5 jack 2015-01-05 46
6 jack 2015-04-06 42
7 tony 2015-01-07 50
8 jack 2015-01-08 55
9 mart 2015-04-08 62
10 mart 2015-04-09 68
11 neil 2015-05-10 12
12 mart 2015-04-11 75
13 neil 2015-06-12 80
14 mart 2015-04-13 94
```

过滤第4行到第7行的所有行，打印每一行
```sh
~/codes$ awk 'NR==4,NR==7{print $0}' order.txt
tony 2015-01-04 29
jack 2015-01-05 46
jack 2015-04-06 42
tony 2015-01-07 50
```

过滤第3列等于23到第2列包含的所有行（可以看到是以第一次匹配的为准的，后面包含05的都没有打印出来），打印每一行
```sh
:~/codes$ awk '$3==23,$2~"05"{print $0}' order.txt
jack 2015-02-03 23
tony 2015-01-04 29
jack 2015-01-05 46

```

### 6、BEGIN/END, 特殊模式
BEGIN表示awk进行处理前执行一次操作
END表示awk处理完最后一行结束前执行一次操作


打印文本文件的总行数 ： 
```sh
~/codes$ awk 'END{print NR}' order.txt 
14
```

使用BEGIN打印表头
```sh
codes$ head -n 3 order.txt | awk  'BEGIN{print "name orderdate cost "} {print $1,$2,$3}'
name orderdate cost 
jack 2015-01-01 10
tony 2015-01-02 15
jack 2015-02-03 23
```

使用BEGIN打印表头
```sh
codes$ head -n 3 order.txt | awk  'BEGIN{printf "%-8s%-12s%-6s\n","name","orderdate","cost"} {printf "%-8s%-12s%-6s\n", $1,$2,$3}'
name    orderdate   cost  
jack    2015-01-01  10    
tony    2015-01-02  15    
jack    2015-02-03  23
```

使用END打印表尾
```sh
codes$ head -n 3 order.txt | awk  'BEGIN{printf "%-8s%-12s%-6s\n","name","orderdate","cost"} {printf "%-8s%-12s%-6s\n", $1,$2,$3} END{print "END OFFILE..."}'
name    orderdate   cost  
jack    2015-01-01  10    
tony    2015-01-02  15    
jack    2015-02-03  23    
END OFFILE...
```

## 六、awk的操作符

1、算术操作符
```
-x 负值
+x 转换为数值，正值
x^y x**y  次方
x/y
x*y
x-y
x+y
x%y
```

2、字符串操作符
```
+  实现字符串连接    "ab"+"cd"    abcd
```

3、赋值操作符
```
=
+=
-+
*=
、=
%=
^=
**=
```

4、比较操作符
```
x<y
x<=y
x>y
x>=y
x==y
x!=y
x~y:x为字符串，y为模式，如果x可以被模式匹配则为真，否则为假
x!~y:与x~y相反
```

5、布尔值
```
awk中，任何非0值或非空字符串都为真，反之就为假
```
6、逻辑关系符
```
&& 与
|| 或者
```
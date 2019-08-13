# argparse模块
## 一、argparse介绍
argparse 是 Python 内置的一个用于命令项选项与参数解析的模块，通过在程序中定义好我们需要的参数，argparse 将会从 sys.argv 中解析出这些参数，并自动生成帮助和使用信息。当然，Python 也有第三方的库可用于命令行解析，而且功能也更加强大，比如 docopt，Click。

使用argparse模块，主要有三个步骤：  
* 创建 ArgumentParser() 对象  
* 调用 add_argument() 方法添加参数  
* 使用 parse_args() 解析添加的参数  

```python
1: import argparse　　#导入模块
2: parser = argparse.ArgumentParser()　　#创建解析对象
3: parser.add_argument()　　#向该对象中添加使用到的命令行选项和参数
4: parser.parser_args()　　#解析命令行
```

一个简单的示例脚本test_argparse.py：
```python
#encoding=utf-8
import argparse
 
def main(args):
    print("--address {0}".format(args.code_address))    #args.address会报错，因为指定了dest的值
    print("--flag {0}".format(args.flag))   #如果命令行中该参数输入的值不在choices列表中，则报错
    print("--port {0}".format(args.port))   #prot的类型为int类型，如果命令行中没有输入该选项则报错
    print("-l {0}".format(args.log))  #如果命令行中输入该参数，则该值为True。因为为短格式"-l"指定了别名"--log"，所以程序中用args.log来访问
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--address", default=80, help="the port number.", dest="code_address")
    parser.add_argument("--flag", choices=['.txt', '.jpg', '.xml', '.png'], default=".txt", help="the file type")
    parser.add_argument("--port", type=int, required=True, help="the port number.")
    parser.add_argument("-l", "--log", default=False, action="store_true", help="active log info.")
 
    args = parser.parse_args()
    main(args)
```

## 二、argparse源码注释
### 1、ArgumentParser类
ArgumentParser类的源码（ipython中查看）：
```python
Source:        
class ArgumentParser(_AttributeHolder, _ActionsContainer):
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - prog -- The name of the program (default: sys.argv[0])
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
        - allow_abbrev -- Allow long options to be abbreviated unambiguously
    """

    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True):


Init signature: argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=<class 'argparse.HelpFormatter'>, pr
efix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True, allow_abbrev=True)
```
其中的参数都有默认值，当运行程序时由于参数不正确或者当调用parser.print_help()方法时，会打印这些描述信息。一般只需要传递参数description。


### 2、ArgumentParser类的add_argument方法
ArgumentParser类add_argument方法的源码（ipython中查看）：
```python
Signature: parser.add_argument(*args, **kwargs)
Source:   
    def add_argument(self, *args, **kwargs):
        """
        add_argument(dest, ..., name=value, ...)
        add_argument(option_string, option_string, ..., name=value, ...)
        """
```

```
add_argument(name or flags... [, action] [, nargs] [, const] [, default] [, type] [, choices] [, required] [, help] [, metavar] [, dest])
```

其中的常用参数解释如下：
```
name or flags: 命令行参数名或者选项，如-p, --port

action:

　　　　store: 默认的action模式，存储值到指定变量

　　　　store_const: 存储值在参数的const部分指定，常用来实现非布尔的命令行flag

　　　　store_true/store_false: 布尔开关。store_true的默认值为False，若命令行有输入该布尔开关则值为True。store_false相反

　　　　append: 存储值到列表，该参数可以重复使用

　　　　append_const: 存储值到列表，存储值在参数的const部分指定

　　　　count: 统计参数简写的输入个数

　　　　version: 输出版本信息，然后退出脚本

nargs: 命令行参数的个数，一般用通配符表示： ？表示只用一个，*表示0到多个，+表示1到多个

default: 默认值

type: 参数的类型，默认是string类型，还可以是float、int和布尔等类型

choices: 输入值的范围，参数可允许的值的一个容器。

required: 默认为False，若为True则表示该参数必须输入。可选参数是否可以省略 (仅针对可选参数)。

help: 使用的帮助提示信息

dest: 参数在程序中的对应的变量名称，如：add_argument("-a", dest="code_name")，在脚本中用parser.code_name来访问该命令行选项的值
```

## 三、argparse使用
### 1、定位参数（positional arguments）
来看一个例子 - 计算一个数的平方：
```python
# -*- coding: utf-8 -*-
 
import argparse
 
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number", type=int)
args = parser.parse_args()
print args.square**2
```

将上面的代码保存为文件 argparse_usage.py，在终端运行，结果如下：
```sh
$ python argparse_usage.py 9
81
```

### 2、可选参数（optional arguments）
所谓可选参数，也就是命令行参数是可选的，有两种方式：
一种是通过一个-来指定的短参数，如 -h；
一种是通过–来指定的长参数，如 --help；
这两种方式可以同存，也可以只存在一个 。

例子：
```python
# -*- coding: utf-8 -*-
 
import argparse
 
parser = argparse.ArgumentParser()
 
parser.add_argument("--square", help="display a square of a given number", type=int)
parser.add_argument("--cubic", help="display a cubic of a given number", type=int)
 
args = parser.parse_args()
 
if args.square:
    print args.square**2
 
if args.cubic:
    print args.cubic**3

```

将上面的代码保存为文件 argparse_usage.py，在终端运行，结果如下：
```sh
$ python argparse_usage.py --h
usage: argparse_usage.py [-h] [--square SQUARE] [--cubic CUBIC]
 
optional arguments:
  -h, --help       show this help message and exit
  --square SQUARE  display a square of a given number
  --cubic CUBIC    display a cubic of a given number
 
$ python argparse_usage.py --square 8
64
 
$ python argparse_usage.py --cubic 8
512
 
$ python argparse_usage.py 8
usage: argparse_usage.py [-h] [--square SQUARE] [--cubic CUBIC]
argparse_usage.py: error: unrecognized arguments: 8
 
$ python argparse_usage.py  # 没有输出
```


再看一个例子：
```python
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# cat test3.py
#!/usr/bin/env python
# encoding: utf-8
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print "verbosity turned on"
```

注意这一行：
```
parser.add_argument("-v", "--verbosity", help="increase output verbosity")
```
**定义了可选参数 -v 或 --verbosity，通过解析后，其值保存在args.verbosity变量中**

用法如下：
```sh
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# python test3.py -v 6
verbosity turned on
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# python test3.py --verbosity 1
verbosity turned on
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# python test3.py --help
usage: test3.py [-h] [-v VERBOSITY]

optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSITY, --verbosity VERBOSITY
                        increase output verbosity
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# python test3.py -v
usage: test3.py [-h] [-v VERBOSITY]
test3.py: error: argument -v/--verbosity: expected one argument
```
测试1中，通过-v来指定参数值
测试2中，通过–verbosity来指定参数值
测试3中，通过-h来打印帮助信息
测试4中，没有给-v指定参数值，所以会报错

### 3、action=‘store_true’
上一个用法中 -v 必须指定参数值，否则就会报错，有没有像 -h 那样，不需要指定参数值的呢，答案是有，通过定义参数时指定 action=“store_true” 即可，用法如下
```python
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# cat  test4.py
#!/usr/bin/env python
# encoding: utf-8
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args = parser.parse_args()
if args.verbose:
    print "verbosity turned on"
```

测试：
```sh
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# python  test4.py -v
verbosity turned on
root@iZ2zee0spkwcgvz4do5kt2Z:/tmp/arg# python  test4.py -h
usage: test4.py [-h] [-v]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
```

**第一个例子中，-v 没有指定任何参数也可，其实存的是True和False，如果出现，则其值为True，否则为False**

### 4、类型 type
默认的参数类型为str，如果要进行数学计算，需要对参数进行解析后进行类型转换，如果不能转换则需要报错，这样比较麻烦
argparse提供了对参数类型的解析，如果类型不符合，则直接报错。


### 5、可选值choices=[]
使用choices参数

### 6、参数默认值default
使用default参数





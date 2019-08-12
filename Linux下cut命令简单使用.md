# Linux下cut命令简单使用
cut命令是用来剪下文本文件里的数据，文本文件可以是字段类型或是字符类型。
```sh
cut -f 2,3 test.txt
```


## cut语法格式
其语法格式为：
cut  [-bn] [file] 或 cut [-c] [file]  或  cut [-df] [file]

使用说明：
cut 命令从文件的每一行剪切字节、字符和字段并将这些字节、字符和字段写至标准输出。
如果不指定 File 参数，cut 命令将读取标准输入。必须指定 -b、-c 或 -f 标志之一。


主要参数：  
* -b ：以字节为单位进行分割。这些字节位置将忽略多字节字符边界，除非也指定了 -n 标志。    
* -c ：以字符为单位进行分割。    
* **-d** ：自定义分隔符，默认为制表符。    
* **-f** ：与-d一起使用，指定显示哪个区域。    
* -n ：取消分割多字节字符。仅和 -b 标志一起使用。如果字符的最后一个字节落在由 -b 标志的 List 参数指示的<br />范围之内，该字符将被写出；否则，该字符将被排除。


**cut一般以什么为依据呢? 也就是说，我怎么告诉cut我想定位到的剪切内容呢?**

cut命令主要是接受三个定位方法：
```
第一，字节（bytes），用选项-b
第二，字符（characters），用选项-c
第三，域（fields），用选项-f
```

我们主要使用按属性(域)和按字符分割

例如有一个学生报表信息，包含No、Name、Mark、Percent：
```sh
cat test.txt

No Name Mark Percent
01 tom 69 91
02 jack 71 87
03 alex 68 98
```

## 以属性(域)为定位标志
使用 -f 选项提取指定字段：
```sh
cut -f 1 test.txt
结果：
No
01
02
03
```

```sh
cut -f 2,3 test.txt
结果：
Name Mark
tom 69
jack 71
alex 68
```

使用 -d 选项指定字段分隔符：
```sh
cat test2.txt

No;Name;Mark;Percent
01;tom;69;91
02;jack;71;87
03;alex;68;98

cut -f 2 -d ";" test2.txt
结果：
Name
tom
jack
alex
```

## 以字符为定位标志
准备数据：
```sh
cat test.txt

abcdefghijklmnopqrstuvwxyz
abcdefghijklmnopqrstuvwxyz
abcdefghijklmnopqrstuvwxyz
abcdefghijklmnopqrstuvwxyz
abcdefghijklmnopqrstuvwxyz
```

打印第1个到第3个字符：
```sh
cut -c 1-3 test.txt
结果：
abc
abc
abc
abc
abc
```

打印前2个字符：
```sh
cut -c -2 test.txt
结果：
ab
ab
ab
ab
ab
```

打印从第5个字符开始到结尾：
```sh
cut -c 5- test.txt
结果：
efghijklmnopqrstuvwxyz
efghijklmnopqrstuvwxyz
efghijklmnopqrstuvwxyz
efghijklmnopqrstuvwxyz
efghijklmnopqrstuvwxyz
```

## 在 Windows上安装 jupyter notebook 的 spark核心
### 需要安装spylon-kernel
这个玩意，就是能在jupyter下使用spark核的关键了。之前也试过toree，但是怎么弄都不成功，后来在coding的建议下，使用这个spylon-kernel就成功了。 

安装也特别简单，cmd后，只要敲这2条命令就可以了： 

```
pip install spylon-kernel 
python -m spylon_kernel install
```

这个时候，CMD下，敲jupyter kernelspec list，应该就能看到，有3个核心
![](assets/markdown-img-paste-20190530001054746.png)

把这个核心复制到d盘
![](assets/markdown-img-paste-2019053000121756.png)
![](assets/markdown-img-paste-20190530001201407.png)

似乎据说：
这个spylon-kernel要求：
```
Apache Spark 2.1.1 compiled for Scala 2.11 
Jupyter Notebook 
Python 3.5+ 
```
所以这3个条件应该是必须满足的。

### 测试使用spylon-kernel
![](assets/markdown-img-paste-20190530001517295.png)

![](assets/markdown-img-paste-20190530001703355.png)

还是可以的，哈哈！
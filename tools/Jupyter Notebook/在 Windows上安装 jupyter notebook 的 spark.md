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

### 修改spylon-kernel改DataFrame显示类pandas
修改spylon-kernel的scala_magic.py的eval（执行scala代码）函数
```python
    def eval(self, code, raw):
        """Evaluates Scala code.

        Parameters
        ----------
        code: str
            Code to execute
        raw: bool
            True to return the raw result of the evalution, False to wrap it with
            MetaKernel classes

        Returns
        -------
        metakernel.process_metakernel.TextOutput or metakernel.ExceptionWrapper or
        the raw result of the evaluation
        """
        from IPython.display import HTML 
        
        intp = self._get_scala_interpreter()
        try:
            res = intp.interpret(code.strip())
            if raw:
                self.res = intp.last_result()
                return self.res
            else:
                if res:
                    if("<table border=" in res):
                        self.res = intp.last_result()
                        return HTML(self.res)
                    else:
                        return TextOutput(res)
        except ScalaException as ex:
            # Get the kernel response so far
            resp = self.kernel.kernel_resp
            # Wrap the exception for MetaKernel use
            resp['status'] = 'error'
            tb = ex.scala_message.split('\n')
            first = tb[0]
            assert isinstance(first, str)
            eclass, _, emessage = first.partition(':')
            return ExceptionWrapper(eclass, emessage, tb)
```
主要就是增加了
```python
                    if("<table border=" in res):
                        self.res = intp.last_result()
                        return HTML(self.res)
```

### 解决Windows乱码问题
这个工具的原理是用python调用scala的repl交互式工具，输出是从scala的repl返回的，估计打开windows的repl输出编码问题，修改一下就行。

默认输出的`D:\Python37\Lib\site-packages\py4j\java_gateway.py`的JavaObject类的`toByteArray().decode("utf-8")`，其实直接调用`__str__`方法即可，此方法调用的是java的toString()方法，可以调用的java对象的方法和属性在_methods和_field_names中，可以调用的方法很少，

**修改**：
```python
# 修改D:\Python37\Lib\site-packages\spylon_kernel\scala_interpreter.py
# 修改class ScalaInterpreter(object)的interpret方法
def interpret(self, code):
    """Interprets a block of Scala code.

    Follow this with a call to `last_result` to retrieve the result as a
    Python object.

    Parameters
    ----------
    code : str
        Scala code to interpret

    Returns
    -------
    str
        String output from the scala REPL

    Raises
    ------
    ScalaException
        When there is a problem interpreting the code
    """
    # Ensure the cell is not incomplete. Same approach taken by Apache Zeppelin.
    # https://github.com/apache/zeppelin/blob/3219218620e795769e6f65287f134b6a43e9c010/spark/src/main/java/org/apache/zeppelin/spark/SparkInterpreter.java#L1263
    code = 'print("")\n'+code

    try:
        res = self.jimain.interpret(code, False)
        #pyres = self.jbyteout.toByteArray().decode("utf-8")
        # 解决乱码
        pyres = str(self.jbyteout)
        # The scala interpreter returns a sentinel case class member here
        # which is typically matched via pattern matching.  Due to it
        # having a very long namespace, we just resort to simple string
        # matching here.
        result = res.toString()
        if result == "Success":
            return pyres
        elif result == 'Error':
            raise ScalaException(pyres)
        elif result == 'Incomplete':
            raise ScalaException(pyres or '<console>: error: incomplete input')
        return pyres
    finally:
        self.jbyteout.reset()
```

其实修改的就这一行：
```python
#pyres = self.jbyteout.toByteArray().decode("utf-8")
# 解决乱码
pyres = str(self.jbyteout)
```

## spylon-kernel的使用
看官网地址
https://pypi.org/project/spylon-kernel/0.1.5/

github地址
https://github.com/Valassis-Digital-Media/spylon-kernel

配置例子：
```
%%init_spark
launcher.jars = ["file://some/jar.jar"]
launcher.master = "local[4]"
launcher.conf.spark.executor.cores = 8
```

```
%%init_spark
launcher.num_executors = 4
launcher.executor_cores = 2
launcher.driver_memory = '4g'
launcher.conf.set("spark.sql.catalogImplementation", "hive")
```

官方的一个例子，似乎可以在同一个文件中使用scala和python
[basic_example.ipynb](examples/basic_example.ipynb "basic_example.ipynb")

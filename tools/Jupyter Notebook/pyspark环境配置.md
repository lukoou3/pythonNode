# pyspark环境配置
scala版本的jupyter notebook中虽然也支持写python语句，但是需要写一行魔法指令，不是很方便，在python中直接使用pyspark，更加方便一点，利用python在数据分析方面的优势可以方便的对统计结果可视化显示，同时有些在java中不方便处理的也可以交给python处理，比如使用jieba切词。

## windows中pyspark环境配置

### Spark环境变量
不管使用java，scala还是python，Spark环境变量是必须的，同时Spark也需要hadoop的环境。

在环境变量中配置SPARK_HOME指定解压的路径,配置环境变量
```
SPARK_HOME
D:\apps\spark-2.3.3-bin-hadoop2.7
```

### 安装py4j模块
python和java通信的模块

本来这样就行了
```
pip install py4j
```

虚拟桌面中没有网络，直接把spark安装目录中的`D:\apps\spark-2.3.3-bin-hadoop2.7\python\lib`中的py4j解压复制到`D:\apps\Anaconda3\Lib\site-packages`目录就行了


### 安装pyspark模块

本来这样就行了
```
pip install pyspark
```

虚拟桌面中没有网络，直接把spark安装目录中的`D:\apps\spark-2.3.3-bin-hadoop2.7\python\lib`中的pyspark解压复制到`D:\apps\Anaconda3\Lib\site-packages`目录就行了


### PYSPARK_PYTHON环境变量
由于我的环境中同时安装了python和Anaconda，我需要使用Anaconda中的python，所以需要指定python的解析器路径。

运行python spark 代码时spark默认的使用的python版本使环境变量中指定的版本。会导致与指定的python解析器的python版本不一致。这时需要在环境变量中指定下PYSPARK_PYTHON环境变量即可，值为指定的python解析器路径。
```
PYSPARK_PYTHON
D:\apps\Anaconda3\python.exe
```

### python开发spark原理
使用python api编写pyspark代码提交运行时，为了不破坏spark原有的运行架构，会将写好的代码首先在python解析器中运行(cpython)，Spark代码归根结底是运行在JVM中的，这里python借助Py4j实现Python和Java的交互,即通过Py4j将pyspark代码“解析”到JVM中去运行。例如，在pyspark代码中实例化一个SparkContext对象，那么通过py4j最终在JVM中会创建scala的SparkContext对象及后期对象的调用、在JVM中数据处理消息的日志会返回到python进程中、如果在代码中会回收大量结果数据到Driver端中，也会通过socket通信返回到python进程中。这样在python进程和JVM进程之间就有大量通信。

python开发spark，需要进行大量的进程间的通信，如果通信量过大，会出现“socket write error”错误，应尽量少使用回收数据类算子，也可以调节回收日志的级别，降低进程之间的通信。

### 测试
jupter中测试的转的md。


```python
# 测试模块是否安装上
import py4j
import pyspark
```


```python
from pyspark import SparkContext, SparkConf
```


```python
conf = SparkConf().setAppName("test_pyspark").setMaster("local[2]")
sc = SparkContext(conf=conf)
```


```python
sc
```





<div>
<p><b>SparkContext</b></p>

<p><a href="http://WIN-UMC26.bj-dptechnology.net:4040">Spark UI</a></p>

<dl>
  <dt>Version</dt>
    <dd><code>v2.3.3</code></dd>
  <dt>Master</dt>
    <dd><code>local[2]</code></dd>
  <dt>AppName</dt>
    <dd><code>test_pyspark</code></dd>
</dl>
</div>
        




```python
from pyspark.sql import SparkSession
```


```python
spark = SparkSession.builder.getOrCreate()
spark
```





<div>
    <p><b>SparkSession - in-memory</b></p>
    
<div>
<p><b>SparkContext</b></p>

<p><a href="http://WIN-UMC26.bj-dptechnology.net:4040">Spark UI</a></p>

<dl>
  <dt>Version</dt>
    <dd><code>v2.3.3</code></dd>
  <dt>Master</dt>
    <dd><code>local[2]</code></dd>
  <dt>AppName</dt>
    <dd><code>test_pyspark</code></dd>
</dl>
</div>

</div>
        




```python
spark.sparkContext is sc
```




    True




```python
rdd = sc.parallelize([0, 2, 3, 4, 6])
rdd
```




    ParallelCollectionRDD[0] at parallelize at PythonRDD.scala:194




```python
rdd.map(lambda x: x*2).collect()
```




    [0, 4, 6, 8, 12]




```python
resources_path = "D:/apps/spark-2.3.3-bin-hadoop2.7/examples/src/main/resources"
import os
```


```python
df = spark.read.csv(os.path.join(resources_path, "people.csv"), sep=";", header=True)
df
```




    DataFrame[name: string, age: string, job: string]




```python
df.show()
```

    +-----+---+---------+
    | name|age|      job|
    +-----+---+---------+
    |Jorge| 30|Developer|
    |  Bob| 32|Developer|
    +-----+---+---------+
    
    


```python
df.toPandas()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>age</th>
      <th>job</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Jorge</td>
      <td>30</td>
      <td>Developer</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bob</td>
      <td>32</td>
      <td>Developer</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Select only the "name" column
df.select("name").show()
```

    +-----+
    | name|
    +-----+
    |Jorge|
    |  Bob|
    +-----+
    
    


```python
# Select everybody, but increment the age by 1
df.select(df['name'], df['age'] + 1).show()
```

    +-----+---------+
    | name|(age + 1)|
    +-----+---------+
    |Jorge|     31.0|
    |  Bob|     33.0|
    +-----+---------+
    
    


```python
df['name'], df['age'] + 1
```




    (Column<b'name'>, Column<b'(age + 1)'>)




```python
# Select people older than 21
df.filter(df['age'] > 21).show()
```

    +-----+---+---------+
    | name|age|      job|
    +-----+---+---------+
    |Jorge| 30|Developer|
    |  Bob| 32|Developer|
    +-----+---+---------+
    
    


```python
# Count people by age
df.groupBy("age").count().show()
```

    +---+-----+
    |age|count|
    +---+-----+
    | 30|    1|
    | 32|    1|
    +---+-----+
    
    


```python
df.createOrReplaceTempView("people")
```


```python
sqlDF = spark.sql("SELECT * FROM people")
sqlDF.show()
```

    +-----+---+---------+
    | name|age|      job|
    +-----+---+---------+
    |Jorge| 30|Developer|
    |  Bob| 32|Developer|
    +-----+---+---------+
    
    


```python
spark.sql("select count(*) from people").show()
```

    +--------+
    |count(1)|
    +--------+
    |       2|
    +--------+
    
    


```python
spark.sql("select age,count(name) count from people group by age").show()
```

    +---+-----+
    |age|count|
    +---+-----+
    | 30|    1|
    | 32|    1|
    +---+-----+
    
    


```python

```



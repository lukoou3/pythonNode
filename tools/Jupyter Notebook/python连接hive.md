官方文档提供了一个使用 pyhs2 连接 hive 的例子，这本来很好的嘛。

结果去 Github：https://github.com/BradRuderman/pyhs2 瞅了一眼，很遗憾 pyhs2 项目已经不维护了。

不过，提供了两个很不错的替代项目：https://github.com/cloudera/impyla、https://github.com/dropbox/PyHive

## 一、使用impyla 连接 hiveserver2
### 1、启动hiveserver2
需要hive开启jdbc服务：
```sh
[hadoop@hadoop01 hive-1.2.1]$ bin/hiveserver2 start > logs/beeline.log 2>&1 &
[1] 3118
```

### 2、安装impyla
安装impyla
```
pip install impyla
```
执行代码后报一些模块不存在，安装这些依赖

安装thrift_sasl
```
pip install thrift_sasl==0.2.1
```
报错（windows），使用下面的命令
```
pip install thrift_sasl==0.2.1 --no-deps
```

安装thrift
```
pip install thrift
```

安装thriftpy
```
pip install thriftpy
```

### 3、报错解决
执行数据库连接后，出现问题
```
File "D:\Python37\Lib\site-packages\thrift_sasl\__init__.py", line 94, in _send_message
self._trans.write(header + body)
TypeError: can't concat str to bytes
```

修改：
```python
def _send_message(self, status, body):
  header = struct.pack(">BI", status, len(body))
  self._trans.write(header + body)
  self._trans.flush()
```
为：
```python
def _send_message(self, status, body):
  header = struct.pack(">BI", status, len(body))
  if(type(body) is str):
      body = body.encode()
  self._trans.write(header + body)
  self._trans.flush()
```

### 4、连接hive
```python
from impala.dbapi import connect
from impala.util import as_pandas

# PLAIN 代表不启用认证，也就是 hive.server2.authentication 的默认值：NONE。
# user是hadoop的用户名，不设置的话，执行有MapReduce的任务时会报权限错误
conn = connect(host='hadoop01', port=10000, auth_mechanism="PLAIN", user='hadoop')
cursor = conn.cursor()
```

```python
cursor.execute('show databases')
cursor.fetchall()
```
[('da_test',), ('default',), ('testdb',)]

```python
#The Cursor object also exposes the iterator interface, which is buffered (controlled by cursor.arraysize):
cursor.execute('show databases')
for row in cursor:
    print(row)
```
('da_test',)
('default',)
('testdb',)

```python
#You can also get back a pandas DataFrame object
cursor.execute('show databases')
as_pandas(cursor)
```
database_name
0	da_test
1	default
2	testdb

```python
cursor.execute("load data local inpath '/home/hadoop/hivetables/student.txt' overwrite into table student")
```

```python
cursor.execute("select * from student limit 5")
cursor.description  # prints the result set's schema
```
[('student.id', 'INT', None, None, None, None, None),
 ('student.name', 'STRING', None, None, None, None, None)]

```python
cursor.execute("select * from student limit 5")
results = cursor.fetchall()
results
```
[(1, 'liuyifei'), (2, 'libingbing'), (3, 'yangmi'), (4, 'tangyan'), (5, '小明')]


```python
#The Cursor object also exposes the iterator interface, which is buffered (controlled by cursor.arraysize):
cursor.execute("select * from student limit 5")
for row in cursor:
    print(row)
```
(1, 'liuyifei')
(2, 'libingbing')
(3, 'yangmi')
(4, 'tangyan')
(5, '小明')

```python
#You can also get back a pandas DataFrame object
cursor.execute("select * from student limit 10")
df = as_pandas(cursor)
df
```
student.id	student.name
0	1	liuyifei
1	2	libingbing
2	3	yangmi
3	4	tangyan
4	5	小明
5	6	小花

```python
%time cursor.execute("select count(*) count from student")
as_pandas(cursor)
```
count
0	6


## python执行hive脚本
https://github.com/1275195766/PyTestpjc/blob/0b352c1402e74d0188163b12e9ccb2e9844717d9/dw_fg_lac_cell_stay_dur_yyyymm/hqltools1.py

https://github.com/kztttt/python/blob/c79d5ca0d3f8e6136a4199932cd1670b6fdd15f0/test/hqltools.py
## pymsql
`https://segmentfault.com/a/1190000014619788#articleHeader11`

pymysql是Python中操作MySQL的模块，其使用方法和MySQLdb几乎相同。但目前pymysql支持python3.x而后者不支持3.x版本。

本文测试python版本：3.5.2。mysql版本：5.7.18

### 一、安装
pip install pymysql

### 二、使用操作
#### 1. 执行SQL
```python
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')

# 创建游标, 查询数据默认为元组类型
cursor = conn.cursor()


# 执行SQL，并返回收影响行数
row1 = cursor.execute("update users set password = '123'")
print(row1)
# 执行SQL，并返回受影响行数
row2 = cursor.execute("update users set password = '456' where id > %s", (1,))
print(row2)
# 执行SQL，并返回受影响行数（使用pymysql的参数化语句防止SQL注入）
row3 = cursor.executemany("insert into users(username, password, email)values(%s, %s, %s)", [("ceshi3", '333', 'ceshi3@11.com'), ("ceshi4", '444', 'ceshi4@qq.com')])
print(row3)

# 提交，不然无法保存新建或者修改的数据
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
```
提示：存在中文的时候，连接需要添加charset='utf8'，否则中文显示乱码。

#### 2、获取查询数据
```python
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')

# 创建游标, 查询数据默认为元组类型
cursor = conn.cursor()
cursor.execute("select * from users")

# 获取第一行数据
row_1 = cursor.fetchone()
print(row_1)
# 获取前n行数据
row_n = cursor.fetchmany(3)
print(row_n)
# 获取所有数据
row_3 = cursor.fetchall()
print(row_3)


# 提交，不然无法保存新建或者修改的数据
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
```

### 3、获取新创建数据自增ID
可以获取到最新自增的ID，也就是最后插入的一条数据ID
```python
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')

# 创建游标, 查询数据默认为元组类型
cursor = conn.cursor()

cursor.executemany("insert into users(username, password, email)values(%s, %s, %s)", [("ceshi3", '333', 'ceshi3@11.com'), ("ceshi4", '444', 'ceshi4@qq.com')])
new_id = cursor.lastrowid
print(new_id)

# 提交，不然无法保存新建或者修改的数据
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
```

#### 4、移动游标
操作都是靠游标，那对游标的控制也是必须的
```python
注：在fetch数据时按照顺序进行，可以使用cursor.scroll(num,mode)来移动游标位置，如：
 
cursor.scroll(1,mode='relative') # 相对当前位置移动
cursor.scroll(2,mode='absolute') # 相对绝对位置移动
```

#### 5、fetch数据类型
关于默认获取的数据是元组类型，如果想要或者字典类型的数据，即：
```python
import pymysql

# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')

# 游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
# 左连接查询
r = cursor.execute("select * from users as u left join articles as a on u.id = a.user_id where a.user_id = 2")
result = cursor.fetchall()
print(result)

# 查询一个表的所有字段名
c = cursor.execute("SHOW FULL COLUMNS FROM users FROM blog")
cc = cursor.fetchall()


# 提交，不然无法保存新建或者修改的数据
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
```

#### 6、调用存储过程
a、调用无参存储过程
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
#游标设置为字典类型
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#无参数存储过程
cursor.callproc('p2')  #等价于cursor.execute("call p2()")
 
row_1 = cursor.fetchone()
print row_1
 
conn.commit()
cursor.close()
conn.close()
```
b、调用有参存储过程
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
 
cursor.callproc('p1', args=(1, 22, 3, 4))
#获取执行完存储的参数,参数@开头
cursor.execute("select @p1,@_p1_1,@_p1_2,@_p1_3")  
# {u'@_p1_1': 22, u'@p1': None, u'@_p1_2': 103, u'@_p1_3': 24}
row_1 = cursor.fetchone()
print row_1
 
conn.commit()
cursor.close()
conn.close()
```

### 三、关于pymysql防注入
#### 1、字符串拼接查询，造成注入
正常查询语句：
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
cursor = conn.cursor()
username = "ceshi1"
password = "ceshi1passwd"
# 正常构造语句的情况
sql = "select username, password from users where user='%s' and pass='%s'" % (username, password)
# sql = select username, password from users where user='ceshi1' and pass='ceshi1passwd'
row_count = cursor.execute(sql) 
row_1 = cursor.fetchone()
print row_count, row_1
 
conn.commit()
cursor.close()
conn.close()
```
构造注入语句：
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
cursor = conn.cursor()
 
username = "u1' or '1'-- "
password = "u1pass"
sql="select username, password from users where username='%s' and password='%s'" % (username, password)
 
# 拼接语句被构造成下面这样，永真条件，此时就注入成功了。因此要避免这种情况需使用pymysql提供的参数化查询。
# select user,pass from tb7 where user='u1' or '1'-- ' and pass='u1pass'
 
row_count = cursor.execute(sql)
row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()
```

#### 2、避免注入，使用pymysql提供的参数化语句
正常参数化查询
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
cursor = conn.cursor()
username="u1"
password="u1pass"
#执行参数化查询
row_count=cursor.execute("select username,password from tb7 where username=%s and password=%s",(username,password))
row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()
```
构造注入，参数化查询注入失败。
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
cursor = conn.cursor()
 
username="u1' or '1'-- "
password="u1pass"
#执行参数化查询
row_count=cursor.execute("select username,password from users where username=%s and password=%s",(username,password))
#内部执行参数化生成的SQL语句，对特殊字符进行了加\转义，避免注入语句生成。
# sql=cursor.mogrify("select username,password from users where username=%s and password=%s",(username,password))
# print sql
#select username,password from users where username='u1\' or \'1\'-- ' and password='u1pass'被转义的语句。
 
row_1 = cursor.fetchone()
print row_count,row_1
 
conn.commit()
cursor.close()
conn.close()
```

结论：excute执行SQL语句的时候，必须使用参数化的方式，否则必然产生SQL注入漏洞。

#### 3、使用存mysql储过程动态执行SQL防注入
```sql
使用MYSQL存储过程自动提供防注入，动态传入SQL到存储过程执行语句。
delimiter \\
DROP PROCEDURE IF EXISTS proc_sql \\
CREATE PROCEDURE proc_sql (
  in nid1 INT,
  in nid2 INT,
  in callsql VARCHAR(255)
  )
BEGIN
  set @nid1 = nid1;
  set @nid2 = nid2;
  set @callsql = callsql;
    PREPARE myprod FROM @callsql;
--   PREPARE prod FROM 'select * from users where nid>? and nid<?';  传入的值为字符串，？为占位符
--   用@p1，和@p2填充占位符
    EXECUTE myprod USING @nid1,@nid2;
  DEALLOCATE prepare myprod;
 
END\\
delimiter ;
set @nid1=12;
set @nid2=15;
set @callsql = 'select * from users where nid>? and nid<?';
CALL proc_sql(@nid1,@nid2,@callsql)
```

pymsql中调用
```python
import pymysql
 
conn = pymysql.connect(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8')
cursor = conn.cursor()
sql1="select * from users where nid>? and nid<?"
cursor.callproc('proc_sql', args=(11, 15, sql1))
 
rows = cursor.fetchall()
print rows
conn.commit()
cursor.close()
conn.close()
```

### 四、使用with简化连接过程
```python
# 使用with简化连接过程，每次都连接关闭很麻烦，使用上下文管理，简化连接过程
import pymysql
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='blog', passwd='123456', db='blog', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# 执行sql
with mysql() as cursor:
    # 左连接查询
    r = cursor.execute("select * from users as u left join articles as a on u.id = a.user_id where a.user_id = 2")
    result = cursor.fetchall()
    print(result)
```


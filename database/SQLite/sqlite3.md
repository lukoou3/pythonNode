# sqlite3
QLite是一种嵌入式数据库，它的数据库就是一个文件。由于SQLite本身是C写的，而且体积很小，所以，经常被集成到各种应用程序中，甚至在iOS和Android的App中都可以集成。

SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说没有独立的维护进程，所有的维护都来自于程序本身。

Python就内置了SQLite3，所以，在Python中使用SQLite，不需要安装任何东西，直接使用。

在使用SQLite前，我们先要搞清楚几个概念：  
* 表是数据库中存放关系数据的集合，一个数据库里面通常都包含多个表，比如学生的表，班级的表，学校的表，等等。表和表之间通过外键关联。  
* 要操作关系数据库，首先需要连接到数据库，一个数据库连接称为Connection；  
* 连接到数据库后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后，获得执行结果。  

## sqlite3模块总体介绍
```
在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
数据库文件，而是直接打开该数据库文件。
    连接对象可以是硬盘上面的数据库文件，也可以是建立在内存中的，在内存中的数据库
    执行完任何操作后，都不需要提交事务的(commit)

    创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
    创建在内存上面： conn = sqlite3.connect('"memory:')

    下面我们一硬盘上面创建数据库文件为例来具体说明：
    conn = sqlite3.connect('c:\\test\\hongten.db')
    其中conn对象是数据库链接对象，而对于数据库链接对象来说，具有以下操作：

        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

    cu = conn.cursor()
    这样我们就创建了一个游标对象：cu
    在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
    对于游标对象cu，具有以下具体操作：

        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动
```

## sqlite3模块主要类和方法介绍
以下是重要的 sqlite3 模块程序，可以满足您在 Python 程序中使用 SQLite 数据库的需求。如果您需要了解更多细节，请查看 Python sqlite3 模块的官方文档。

**sqlite3.connect(database [,timeout ,other optional arguments])**    
该 API 打开一个到 SQLite 数据库文件 database 的链接。您可以使用 ":memory:" 来在 RAM 中打开一个到 database 的数据库连接，而不是在磁盘上打开。如果数据库成功打开，则返回一个连接对象。

当一个数据库被多个连接访问，且其中一个修改了数据库，此时 SQLite 数据库被锁定，直到事务提交。timeout 参数表示连接等待锁定的持续时间，直到发生异常断开连接。timeout 参数默认是 5.0（5 秒）。

如果给定的数据库名称 filename 不存在，则该调用将创建一个数据库。如果您不想在当前目录中创建数据库，那么您可以指定带有路径的文件名，这样您就能在任意地方创建数据库。

**connection.cursor([cursorClass])**    
该例程创建一个 cursor，将在 Python 数据库编程中用到。该方法接受一个单一的可选的参数 cursorClass。如果提供了该参数，则它必须是一个扩展自 sqlite3.Cursor 的自定义的 cursor 类。

**cursor.execute(sql [, optional parameters])**    
该例程执行一个 SQL 语句。该 SQL 语句可以被参数化（即使用占位符代替 SQL 文本）。sqlite3 模块支持两种类型的占位符：问号和命名占位符（命名样式）。

例如：cursor.execute("insert into people values (?, ?)", (who, age))

**connection.execute(sql [, optional parameters])**    
该例程是上面执行的由光标（cursor）对象提供的方法的快捷方式，它通过调用光标（cursor）方法创建了一个中间的光标对象，然后通过给定的参数调用光标的 execute 方法。

**cursor.executemany(sql, seq_of_parameters)**    
该例程对 seq_of_parameters 中的所有参数或映射执行一个 SQL 命令。

**connection.executemany(sql[, parameters])**    
该例程是一个由调用光标（cursor）方法创建的中间的光标对象的快捷方式，然后通过给定的参数调用光标的 executemany 方法。

**cursor.executescript(sql_script)**    
该例程一旦接收到脚本，会执行多个 SQL 语句。它首先执行 COMMIT 语句，然后执行作为参数传入的 SQL 脚本。所有的 SQL 语句应该用分号（;）分隔。

**connection.executescript(sql_script)**    
该例程是一个由调用光标（cursor）方法创建的中间的光标对象的快捷方式，然后通过给定的参数调用光标的 executescript 方法。

**connection.total_changes()**    
该例程返回自数据库连接打开以来被修改、插入或删除的数据库总行数。

**connection.commit()**    
该方法提交当前的事务。如果您未调用该方法，那么自您上一次调用 commit() 以来所做的任何动作对其他数据库连接来说是不可见的。

**connection.rollback()**    
该方法回滚自上一次调用 commit() 以来对数据库所做的更改。

**connection.close()**    
该方法关闭数据库连接。请注意，这不会自动调用 commit()。如果您之前未调用 commit() 方法，就直接关闭数据库连接，您所做的所有更改将全部丢失！

**cursor.fetchone()**    
该方法获取查询结果集中的下一行，返回一个单一的序列，当没有更多可用的数据时，则返回 None。

**cursor.fetchmany([size=cursor.arraysize])**    
该方法获取查询结果集中的下一行组，返回一个列表。当没有更多的可用的行时，则返回一个空的列表。该方法尝试获取由 size 参数指定的尽可能多的行。

**cursor.fetchall()**    
该例程获取查询结果集中所有（剩余）的行，返回一个列表。当没有可用的行时，则返回一个空的列表。

## sqlite3使用
#### 连接数据库
下面的 Python 代码显示了如何连接到一个现有的数据库。如果数据库不存在，那么它就会被创建，最后将返回一个数据库对象。
```python
import sqlite3

conn = sqlite3.connect('test.db')
```
在这里，您也可以把数据库名称复制为特定的名称 :memory:，这样就会在 RAM 中创建一个数据库。现在，让我们来运行上面的程序，在当前目录中创建我们的数据库 test.db。您可以根据需要改变路径。

#### 创建表
下面的 Python 代码段将用于在先前创建的数据库中创建一个表：
```python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute('''CREATE TABLE COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')

conn.commit()
conn.close()
```

#### INSERT 操作
下面的 Python 程序显示了如何在上面创建的 COMPANY 表中创建记录：
```python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) VALUES (1, 'Paul', 32, 'California', 20000.00 )");

conn.commit()
conn.close()
```

#### SELECT 操作
下面的 Python 程序显示了如何从前面创建的 COMPANY 表中获取并显示记录：
查询返回的可迭代对象的元素为元组
```python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "ADDRESS = ", row[2]
   print "SALARY = ", row[3], "\n"

conn.close()
```

#### UPDATE 操作
下面的 Python 代码显示了如何使用 UPDATE 语句来更新任何记录，然后从 COMPANY 表中获取并显示更新的记录：
```python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")

conn.commit()
conn.close()
```

#### DELETE 操作
下面的 Python 代码显示了如何使用 DELETE 语句删除任何记录，然后从 COMPANY 表中获取并显示剩余的记录：
```python
import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()

c.execute("DELETE from COMPANY where ID=2;")

conn.commit()
conn.close()
```

#### 防止SQL注入
使用`?`占位符，参数作为第二个参数传进去：
```python
# Never do this -- insecure!
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchone())

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
```

#### Using shortcut methods
Using the nonstandard execute(), executemany() and executescript() methods of the Connection object, your code can be written more concisely because you don’t have to create the (often superfluous) Cursor objects explicitly. Instead, the Cursor objects are created implicitly and these shortcut methods return the cursor objects. This way, you can execute a SELECT statement and iterate over it directly using only a single call on the Connection object.
```python
import sqlite3

persons = [
    ("Hugo", "Boss"),
    ("Calvin", "Klein")
    ]

con = sqlite3.connect(":memory:")

# Create the table
con.execute("create table person(firstname, lastname)")

# Fill the table
con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)

# Print the table contents
for row in con.execute("select firstname, lastname from person"):
    print(row)

print("I just deleted", con.execute("delete from person").rowcount, "rows")
```

#### Accessing columns by name instead of by index
One useful feature of the sqlite3 module is the built-in sqlite3.Row class designed to be used as a row factory.

Rows wrapped with this class can be accessed both by index (like tuples) and case-insensitively by name:
```python
import sqlite3

con = sqlite3.connect(":memory:")
con.row_factory = sqlite3.Row

cur = con.cursor()
cur.execute("select 'John' as name, 42 as age")
for row in cur:
    assert row[0] == row["name"]
    assert row["name"] == row["nAmE"]
    assert row[1] == row["age"]
    assert row[1] == row["AgE"]
```

#### Using the connection as a context manager
Connection objects can be used as context managers that automatically commit or rollback transactions. In the event of an exception, the transaction is rolled back; otherwise, the transaction is committed:
```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("create table person (id integer primary key, firstname varchar unique)")

# Successful, con.commit() is called automatically afterwards
with con:
    con.execute("insert into person(firstname) values (?)", ("Joe",))

# con.rollback() is called after the with block finishes with an exception, the
# exception is still raised and must be caught
try:
    with con:
        con.execute("insert into person(firstname) values (?)", ("Joe",))
except sqlite3.IntegrityError:
    print("couldn't add Joe twice")
```

## 让Python更加充分的使用Sqlite3
一下内容来自互联网。  

我最近在涉及大量数据处理的项目中频繁使用 sqlite3。我最初的尝试根本不涉及任何数据库，所有的数据都将保存在内存中，包括字典查找、迭代和条件等查询。这很好，但可以放入内存的只有那么多，并且将数据从磁盘重新生成或加载到内存是一个繁琐又耗时的过程。

我决定试一试sqlite3。因为只需打开与数据库的连接，这样可以增加可处理的数据量，并将应用程序的加载时间减少到零。此外，我可以通过 SQL 查询替换很多Python逻辑语句。

我想分享一些关于这次经历的心得和发现。

#### 1. 使用大量操作

如果你需要在数据库中一次性插入很多行，那么你真不应该使用 execute。sqlite3 模块提供了批量插入的方式：executemany。

而不是像这样做：
```python
for row in iter_data():
    connection.execute('INSERT INTO my_table VALUES (?)', row)
```

你可以利用这个事实，即 executemany 接受元组的生成器作为参数：
```python
connection.executemany(
 'INSERT INTO my_table VALUE (?)',
  iter_data()
)
```

这不仅更简洁，而且更高效。实际上，sqlite3 在幕后利用 executemany 实现 execute，但后者插入一行而不是多行。

我写了一个小的基准测试，将一百万行插入空表（数据库在内存中）：
executemany: 1.6 秒
execute: 2.7 秒

#### 2.你不需要游标
一开始我经常搞混的事情就是，光标管理。在线示例和文档中通常如下：
```python
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()
# Do something with cursor
```

但大多数情况下，你根本不需要光标，你可以直接使用连接对象（本文末尾会提到）。像execute和executemany类似的操作可以直接在连接上调用。以下是一个证明此事的示例：
```python
import sqlite3
 
connection = sqlite3(':memory:')
 
# Create a table
connection.execute('CREATE TABLE events(ts, msg)')
 
# Insert values
connection.executemany(
    'INSERT INTO events VALUES (?,?)',
    [
        (1, 'foo'),
        (2, 'bar'),
        (3, 'baz')
    ]
)
 
# Print inserted rows
for row in connnection.execute('SELECT * FROM events'):
    print(row)
```

#### 3. 光标（Cursor）可被用于迭代
你可能经常会看到使用fetchone或fetchall来处理SELECT查询结果的示例。但是我发现处理这些结果的最自然的方式是直接在光标上迭代：
```python
for row in connection.execute('SELECT * FROM events'):
    print(row)
```
这样一来，只要你得到足够的结果，你就可以终止查询，并且不会引起资源浪费。当然，如果事先知道你需要多少结果，可以改用LIMIT SQL语句，但Python生成器是非常方便的，可以让你将数据生成与数据消耗分离。

#### 4. 使用Context Managers（上下文管理器）
即使在处理SQL事务的中间，也会发生讨厌的事情。为了避免手动处理回滚或提交，你可以简单地使用连接对象作为上下文管理器。 在以下示例中，我们创建了一个表，并错误地插入了重复的值：
```python
import sqlite3
connection = sqlite3.connect(':memory:')
 
with connection:
    connection.execute(
        'CREATE TABLE events(ts, msg, PRIMARY KEY(ts, msg))')
 
try:
    with connection:
        connection.executemany('INSERT INTO events VALUES (?, ?)', [
            (1, 'foo'),
            (2, 'bar'),
            (3, 'baz'),
            (1, 'foo'),
        ])
except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
    print('Could not complete operation:', e)
    
# No row was inserted because transaction failed
for row in connection.execute('SELECT * FROM events'):
    print(row)
    
connection.close()
```

#### 使用Pragmas
…当它真的有用时

在你的程序中有几个 pragma 可用于调整 sqlite3 的行为。特别地，其中一个可以改善性能的是synchronous：
```python
connection.execute('PRAGMA synchronous = OFF')
 ```
你应该知道这可能是危险的。如果应用程序在事务中间意外崩溃，数据库可能会处于不一致的状态。所以请小心使用！ 但是如果你要更快地插入很多行，那么这可能是一个选择。

#### 6. 推迟索引创建
假设你需要在数据库上创建几个索引，而你需要在插入很多行的同时创建索引。把索引的创建推迟到所有行的插入之后可以导致实质性的性能改善。

#### 7. 使用占位符插入 Python 值
使用 Python 字符串操作将值包含到查询中是很方便的。但是这样做非常不安全，而 sqlite3 给你提供了更好的方法来做到这一点：
```python
# Never do this -- insecure!
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

# Do this instead
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
print(c.fetchone())

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
```

## 解析SQLite中的常见问题与总结详解
一下内容来自互联网。 

1、 创建数据
如果不往数据库里面添加任何的表，这个数据库等于没有建立，不会在硬盘上产生任何文件，如果数据库已经存在，则会打开这个数据库。 

2、 如何通过sqlite3.dll与sqlite3.def生成sqlite3.lib文件
LIB /DEF:sqlite3.def /machine:IX86

3、 sqlite3_open打开一个数据库时，如果数据库不存在就会新生成一个数据库文件。如果接着执行其他查询语句就会失败，比如sqlite3_prepare，编程中出现明明指定了数据库而且里面也有数据，为什么查询失败了，主要是数据库名路径不对引起的。一般的做法是先检查数据库文件是否存在，如果存在就使用sqlite3_open打开数据库；否则创建一个新的数据库。

4、 如何建立自动增长字段
声明为INTEGER PRIMARY KEY的列将会自动增长。

5、SQLite3支持何种数据类型？
NULL
INTEGER
REAL
TEXT
BLOB
但实际上，sqlite3也接受如下的数据类型：
smallint 16位元的整数。
interger 32位元的整数。
decimal(p,s) p精确值和s大小的十进位整数，精确值p是指全部有几个数(digits)大小值，s是指小数点後有几位数。如果没有特别指定，则系统会设为p=5; s=0。
float 32位元的实数。
double 64位元的实数。
char(n) n长度的字串，n不能超过254。
varchar(n)长度不固定且其最大长度为n的字串，n不能超过4000。
graphic(n)和char(n)一样，不过其单位是两个字元double-bytes，n不能超过127。这个形态是为了支援两个字元长度的字体，例如中文字。
vargraphic(n)可变长度且其最大长度为n的双字元字串，n不能超过2000。
date包含了年份、月份、日期。
time包含了小时、分钟、秒。
timestamp包含了年、月、日、时、分、秒、千分之一秒。

6、SQLite允许向一个integer型字段中插入字符串
这 是一个特性，而不是一个bug。SQLite不强制数据类型约束。任何数据都可以插入任何列。你可以向一个整型列中插入任意长度的字符串，向布尔型列中插 入浮点数，或者向字符型列中插入日期型值。在CREATE TABLE中所指定的数据类型不会限制在该列中插入任何数据。任何列均可接受任意长度的字符串（只有一种情况除外：标志为INTEGER PRIMARY KEY的列只能存储64位整数，当向这种列中插数据除整数以外的数据时，将会产生错误。

但SQLite确实使用声明的列类型来指示你所期望的格式。所以，例如你向一个整型列中插入字符串时，SQLite会试图将该字符串转换成一个整数。如果可以转换，它将插入该整数；否则，将插入字符串。这种特性有时被称为类型或列亲和性(type or column affinity).

7、为什么SQLite不允许在同一个表不同的两行上使用0和0.0作主键？
主键必须是数值类型，将主键改为TEXT型将不起作用。
每一行必须有一个唯一的主键。对于一个数值型列，SQLite认为'0'和'0.0'是相同的，因为他们在作为整数比较时是相等的(参见上一问题)。所以，这样值就不唯一了。

8、多个应用程序或一个应用程序的多个实例可以同时访问同一个数据库文件吗？
 
多个进程可同时打开同一个数据库。多个进程可以同时进行SELECT操作，但在任一时刻，只能有一个进程对数据库进行更改。
 
SQLite使用读、写锁控制对数据库的访问。（在Win95/98/ME等不支持读、写锁的系统下，使用一个概率性的模拟来代替。）但使用时要注意：如果数据库文件存放于一个NFS文件系统上，这种锁机制可能不能正常工作。这 是因为fcntl()文件锁在很多NFS上没有正确的实现。在可能有多个进程同时访问数据库的时候，应该避免将数据库文件放到NFS上。在Windows 上，Microsoft的文档中说：如果使用FAT文件系统而没有运行share.exe守护进程，那么锁可能是不能正常使用的。那些在Windows上 有很多经验的人告诉我：对于网络文件，文件锁的实现有好多Bug，是靠不住的。如果他们说的是对的，那么在两台或多台Windows机器间共享数据库可能 会引起不期望的问题。

我们意识到，没有其它嵌入式的SQL数据库引擎能象SQLite这样处理如此多的并发。SQLite允许多个进程同时打开一个数据库，同时读一个数据库。当有任何进程想要写时，它必须在更新过程中锁住数据库文件。但那通常只是几毫秒的时间。其它进程只需等待写进程干完活结束。典型地，其它嵌入式的SQL数据库引擎同时只允许一个进程连接到数据库。

但 是，Client/Server数据库引擎（如PostgreSQL, MySQL,或Oracle）通常支持更高级别的并发，并且允许多个进程同时写同一个数据库。这种机制在Client/Server结构的数据库上是可能 的，因为总是有一个单一的服务器进程很好地控制、协调对数据库的访问。如果你的应用程序需要很多的并发，那么你应该考虑使用一个 Client/Server结构的数据库。但经验表明，很多应用程序需要的并发，往往比其设计者所想象的少得多。

当SQLite试图访问一个被其它进程锁住的文件时，缺省的行为是返回SQLITE_BUSY。可以在C代码中使用sqlite3_busy_handler()或sqlite3_busy_timeout() API函数调整这一行为。

9、SQLite线程安全吗？
线程是魔鬼（Threads are evil）。避免使用它们。
SQLite 是线程安全的。由于很多用户会忽略我们在上一段中给出的建议，我们做出了这种让步。但是，为了达到线程安全，SQLite在编译时必须将 SQLITE_THREADSAFE预处理宏置为1。在Windows和Linux上，已编译的好的二进制发行版中都是这样设置的。如果不确定你所使用的 库是否是线程安全的，可以调用sqlite3_threadsafe()接口找出。

10、在SQLite数据库中如何列出所有的表和索引？
如果你运行sqlite3命令行来访问你的数据库，可以键入“.tables”来获得所有表的列表。或者，你可以输入“.schema”来看整个数据库模式，包括所有的表的索引。输入这些命令，后面跟一个LIKE模式匹配可以限制显示的表。

11、SQLite数据库有已知的大小限制吗？
在Windows和Unix下，版本2.7.4的SQLite可以达到2的41次方字节(2T字节)。老版本的为2的31次方字节(2G字节)。
SQLite版本2.8限制一个记录的容量为1M。SQLite版本3.0则对单个记录容量没有限制。
表名、索引表名、视图名、触发器名和字段名没有长度限制。但SQL函数的名称(由sqlite3_create_function() API函数创建)不得超过255个字符。

12、在SQLite中，VARCHAR字段最长是多少？
SQLite不强制VARCHAR的长度。你可以在SQLITE中声明一个VARCHAR(10)，SQLite还是可以很高兴地允许你放入500个字符。并且这500个字符是原封不动的，它永远不会被截断。
 
13、在SQLite中，如何在一个表上添加或删除一列？
SQLite有有限地ALTER TABLE支持。你可以使用它来在表的末尾增加一列，可更改表的名称。如果需要对表结构做更复杂的改变，则必须重新建表。重建时可以先将已存在的数据放到一个临时表中，删除原表，创建新表，然后将数据从临时表中复制回来。

如，假设有一个t1表，其中有"a", "b", "c"三列，如果要删除列c，以下过程描述如何做:

BEGIN TRANSACTION;
CREATE TEMPORARY TABLE t1_backup(a,b);
INSERT INTO t1_backup SELECT a,b FROM t1;
DROP TABLE t1;
CREATE TABLE t1(a,b);
INSERT INTO t1 SELECT a,b FROM t1_backup;
DROP TABLE t1_backup;
COMMIT;

14、在SQLite中支持分页吗？
 
SQLite分页是世界上最简单的。如果我要去11-20的Account表的数据Select * From Account Limit 9 Offset 10;
以上语句表示从Account表获取数据，跳过10行，取9行。这个特性足够让很多的web中型网站使用这个了。也可以这样写 select * from account limit10,9和上面的的效果一样。这种写法MySQL也支持。

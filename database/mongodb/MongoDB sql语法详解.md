### MongoDB 创建数据库
语法
```sql
use DATABASE_NAME
```
如果数据库不存在，则创建数据库，否则切换到指定数据库。

创建一个 souyunku 的数据库，使用 db 命令查看
```sql
> use souyunku
switched to db souyunku
> db
souyunku
>
```

查看所有数据库使用show dbs
```sql
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
test    0.000GB
> 
```

可以看到，刚创建的数据库 souyunku 并不在数据库的列表中， 要显示它，我们需要向 souyunku 数据库插入一些数据。
```sql
> db.souyunku.insert({"name":"关注公众号，搜云库，专注于开发技术的研究与知识分享"})
WriteResult({ "nInserted" : 1 })
> show dbs
admin     0.000GB
config    0.000GB
local     0.000GB
souyunku  0.000GB
test      0.000GB
>
```
MongoDB 中默认的数据库为 test，如果你没有创建新的数据库，集合将存放在 test 数据库中。

**注意: 在 MongoDB 中，集合只有在内容插入后才会创建! 就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建。**

### MongoDB 创建数据库
MongoDB 删除数据库的语法
```sql
db.dropDatabase()
```

实例
以下操作会把souyunku 数据删除
查看所有数据库
```sql
> show dbs
admin     0.000GB
config    0.000GB
local     0.000GB
souyunku  0.000GB
test      0.000GB
```

切换到souyunku 数据库
```sql
> use souyunku
switched to db souyunku
```

使用db.dropDatabase() 删除数据库
```sql
> db.dropDatabase()
{ "dropped" : "souyunku", "ok" : 1 }
```

看到已经删除了
```sql
> show dbs
admin   0.000GB
config  0.000GB
local   0.000GB
test    0.000GB
>
```

### MongoDB 创建集合
MongoDB 中使用 createCollection() 方法来创建集合。  
语法格式：
```sql
db.createCollection(name, options)
```

参数说明：
* name: 要创建的集合名称  
* options: 可选参数, 指定有关内存大小及索引的选项  

options 可以是如下参数：

| 字段 | 类型 | 描述 |
| ---- | ---- | ---- |
| capped | 布尔 | （可选）如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。当该值为 true 时，必须指定 size 参数。 |
| autoIndexId | 布尔 | （可选）如为 true，自动在 _id 字段创建索引。默认为 false。 |
| size | 数值 | （可选）为固定集合指定一个最大值（以字节计）。如果 capped 为 true，也需要指定该字段。 |
| max | 数值 | （可选）指定固定集合中包含文档的最大数量。 |

在插入文档时，MongoDB 首先检查固定集合的 size 字段，然后检查 max 字段。

实例:
在 test 数据库中创建 runoob 集合：
```sql
> use test
switched to db test
> db.createCollection("runoob")
{ "ok" : 1 }
>
```

如果要查看已有集合，可以使用 show collections 命令：
```sql
> show collections
runoob
system.indexes
```

下面是带有几个关键参数的 createCollection() 的用法：

创建固定集合 mycol，整个集合空间大小 6142800 KB, 文档最大个数为 10000 个。
```sql
> db.createCollection("mycol", { capped : true, autoIndexId : true, size : 
   6142800, max : 10000 } )
{ "ok" : 1 }
>
```

在 MongoDB 中，你不需要创建集合。当你插入一些文档时，MongoDB 会自动创建集合。
```sql
> db.mycol2.insert({"name" : "菜鸟教程"})
> show collections
mycol2
...
```

### MongoDB 删除集合
MongoDB 中使用 drop() 方法来删除集合。  
语法格式：
```sql
db.collection.drop()
```
返回值:
如果成功删除选定集合，则 drop() 方法返回 true，否则返回 false。

实例

在数据库 mydb 中，我们可以先通过 show collections 命令查看已存在的集合：
```sql
>use mydb
switched to db mydb
>show collections
mycol
mycol2
system.indexes
runoob
>
```

接着删除集合 mycol2 :
```sql
>db.mycol2.drop()
true
>
```

### MongoDB 插入文档
如果该集合不在该数据库中， MongoDB 会自动创建该集合并插入文档。  
MongoDB 使用 insert() 或 save() 方法向集合中插入文档，语法如下：
```sql
db.COLLECTION_NAME.insert(document)
```
如果不指定 _id 字段 save() 方法类似于 insert() 方法。如果指定 _id 字段，则会更新该 _id 的数据。


3.2 版本后还有以下几种语法可用于插入文档:  
* **db.collection.insertOne()**:向指定集合中插入一条文档数据。  
* **db.collection.insertMany()**:向指定集合中插入多条文档数据。  

```sql
#  插入单条数据
> var document = db.collection.insertOne({"a": 3})
> document
{
        "acknowledged" : true,
        "insertedId" : ObjectId("571a218011a82a1d94c02333")
}

#  插入多条数据
> var res = db.collection.insertMany([{"b": 3}, {'c': 4}])
> res
{
        "acknowledged" : true,
        "insertedIds" : [
                ObjectId("571a22a911a82a1d94c02337"),
                ObjectId("571a22a911a82a1d94c02338")
        ]
}
```

### MongoDB 更新文档
update() 方法用于更新已存在的文档。语法格式如下：
```sql
db.collection.update(
   <query>,
   <update>,
   {
     upsert: <boolean>,
     multi: <boolean>,
     writeConcern: <document>
   }
)
```
参数说明：

* **query** : update的查询条件，类似sql update查询内where后面的。  
* **update** : update的对象和一些更新的操作符（如$,$inc...）等，也可以理解为sql update查询内set后面的  
* **upsert** : 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入。  
* **multi** : 可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新。  
* **writeConcern** :可选，抛出异常的级别。  

实例
```sql
db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})

#以上语句只会修改第一条发现的文档，如果你要修改多条相同的文档，则需要设置 multi 参数为 true。
db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}},{multi:true})

更多实例
只更新第一条记录：
db.col.update( { "count" : { $gt : 1 } } , { $set : { "test2" : "OK"} } );

全部更新：
db.col.update( { "count" : { $gt : 3 } } , { $set : { "test2" : "OK"} },false,true );

全部添加进去:
db.col.update( { "count" : { $gt : 5 } } , { $set : { "test5" : "OK"} },true,true );
```

### MongoDB 删除文档
MongoDB remove()函数是用来移除集合中的数据。
MongoDB数据更新可以使用update()函数。在执行remove()函数前先执行find()命令来判断执行的条件是否正确，这是一个比较好的习惯。

remove() 方法已经过时了，现在官方推荐使用 **deleteOne()** 和 **deleteMany()** 方法。

如删除集合下全部文档：
```sql
> db.col.deleteMany({})
{ "acknowledged" : true, "deletedCount" : 2 }
> db.col.find()
> 
```

删除 title 等于 "搜云库" 的全部文档：
```sql
> db.collection.deleteMany({ title : "搜云库"})
{ "acknowledged" : true, "deletedCount" : 2 }
> 
```

删除 weixin 等于 "souyunku" 的一个文档：
```sql
> db.col.insert({weixin:"souyunku"})
WriteResult({ "nInserted" : 1 })
> db.col.deleteOne({weixin:"souyunku"})
{ "acknowledged" : true, "deletedCount" : 1 }
```

### MongoDB 查询文档
MongoDB 查询文档使用 find() 或 findOne() 方法。

find() 方法以非结构化的方式来显示所有文档。  
语法
```sql
db.collection.find(query, projection)
```
* query ：可选，使用查询操作符指定查询条件  
* projection ：可选，使用投影操作符指定返回的键。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）。  

如果你需要以易读(格式化)的方式来读取数据，可以使用 pretty() 方法，语法格式如下：
```sql
>db.col.find().pretty()
```

#### MongoDB 与 RDBMS Where 语句比较
| 操作       | 格式                   | 范例                                      | RDBMS中的类似语句     |
| ---------- | ---------------------- | ----------------------------------------- | --------------------- |
| 等于       | `{<key>:<value>}`        | `db.col.find({"by":"菜鸟教程"}).pretty()`   | where by = '菜鸟教程' |
| 小于       | `{<key>:{$lt:<value>}}`  | `db.col.find({"likes":{$lt:50}}).pretty()`  | where likes < 50      |
| 小于或等于 | `{<key>:{$lte:<value>}}` | `db.col.find({"likes":{$lte:50}}).pretty()` | where likes <= 50     |
| 大于       | `{<key>:{$gt:<value>}}`  | `db.col.find({"likes":{$gt:50}}).pretty()`  | where likes > 50      |
| 大于或等于 | `{<key>:{$gte:<value>}}` | `db.col.find({"likes":{$gte:50}}).pretty()` | where likes >= 50     |
| 不等于     | `{<key>:{$ne:<value>}}`  | `db.col.find({"likes":{$ne:50}}).pretty()`  | where likes != 50     |

#### MongoDB AND 条件
MongoDB 的 find() 方法可以传入多个键(key)，每个键(key)以逗号隔开，即常规 SQL 的 AND 条件。语法格式如下：
```sql
>db.col.find({key1:value1, key2:value2}).pretty()
```

#### MongoDB OR 条件
MongoDB OR 条件语句使用了关键字 `$or`,语法格式如下：
```sql
>db.col.find(
   {
      $or: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```
以下实例中，我们演示了查询键 by 值为 菜鸟教程 或键 title 值为 MongoDB 教程 的文档。
```sql
>db.col.find({$or:[{"by":"菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()
```

#### AND 和 OR 联合使用
以下实例演示了 AND 和 OR 联合使用，类似常规 SQL 语句为： 'where likes>50 AND (by = '菜鸟教程' OR title = 'MongoDB 教程')'
```sql
>db.col.find({"likes": {$gt:50}, $or: [{"by": "菜鸟教程"},{"title": "MongoDB 教程"}]}).pretty()
```

### MongoDB 条件操作符
MongoDB中条件操作符有：
```sql
(>) 大于 - $gt
(<) 小于 - $lt
(>=) 大于等于 - $gte
(<= ) 小于等于 - $lte
```
简写说明：
```sql
$gt -------- greater than  >

$gte --------- gt equal  >=

$lt -------- less than  <

$lte --------- lt equal  <=

$ne ----------- not equal  !=

$eq  --------  equal  =
```

```sql
#获取 "col" 集合中 "likes" 大于 100 的数据：
db.col.find({likes : {$gt : 100}})
#类似于SQL语句：
Select * from col where likes > 100;

#获取"col"集合中 "likes" 大于等于 100 的数据：
db.col.find({likes : {$gte : 100}})
#类似于SQL语句：
Select * from col where likes >=100;

获取"col"集合中 "likes" 大于100，小于 200 的数据：
db.col.find({likes : {$lt :200, $gt : 100}})
类似于SQL语句：
Select * from col where likes>100 AND  likes<200;
```

### MongoDB Limit与Skip方法
limit()方法接受一个数字参数，该参数指定从MongoDB中读取的记录条数。
```sql
>db.COLLECTION_NAME.find().limit(NUMBER)
```

skip()方法来跳过指定数量的数据，skip方法同样接受一个数字参数作为跳过的记录条数。
```sql
>db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)
```

```sql
#显示查询文档中的两条记录：
> db.col.find({},{"title":1,_id:0}).limit(2)
#显示第二条文档数据
>db.col.find({},{"title":1,_id:0}).limit(1).skip(1)
```

### MongoDB 排序
在 MongoDB 中使用 sort() 方法对数据进行排序，sort() 方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序排列，而 -1 是用于降序排列。
```sql
>db.COLLECTION_NAME.find().sort({KEY:1})
```

skip(), limilt(), sort()三个放在一起执行的时候，执行的顺序是先 sort(), 然后是 skip()，最后是显示的 limit()。

### MongoDB 索引
MongoDB使用 createIndex() 方法来创建索引。  
createIndex()方法基本语法格式如下所示：
```sql
>db.collection.createIndex(keys, options)
```
语法中 Key 值为你要创建的索引字段，1 为指定按升序创建索引，如果你想按降序来创建索引指定为 -1 即可。

实例
```sql
>db.col.createIndex({"title":1})
#也可以设置使用多个字段创建索引（关系型数据库中称作复合索引）。
>db.col.createIndex({"title":1,"description":-1})
```

```sql
1、查看集合索引
db.col.getIndexes()

2、查看集合索引大小
db.col.totalIndexSize()

3、删除集合所有索引
db.col.dropIndexes()

4、删除集合指定索引
db.col.dropIndex("索引名称")
```

createIndex() 接收可选参数，可选参数列表如下：

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| background | Boolean | 建索引过程会阻塞其它数据库操作，background可指定以后台方式创建索引，即增加 "background" 可选参数。  "background" 默认值为false。 |
| unique | Boolean | 建立的索引是否唯一。指定为true创建唯一索引。默认值为false. |
| name | string | 索引的名称。如果未指定，MongoDB的通过连接索引的字段名和排序顺序生成一个索引名称。 |
| dropDups | Boolean | 3.0+版本已废弃。在建立唯一索引时是否删除重复记录,指定 true 创建唯一索引。默认值为false. |
| sparse | Boolean | 对文档中不存在的字段数据不启用索引；这个参数需要特别注意，如果设置为true的话，在索引字段中不会查询出不包含对应字段的文档.。默认值为false. |
| expireAfterSeconds | integer | 指定一个以秒为单位的数值，完成 TTL设定，设定集合的生存时间。 |
| v | index version | 索引的版本号。默认的索引版本取决于mongod创建索引时运行的版本。 |
| weights | document | 索引权重值，数值在 1 到 99,999 之间，表示该索引相对于其他索引字段的得分权重。 |
| default_language | string | 对于文本索引，该参数决定了停用词及词干和词器的规则的列表。 默认为英语 |
| language_override | string | 对于文本索引，该参数指定了包含在文档中的字段名，语言覆盖默认的language，默认值为 language. |


## 一、安装pymongo
pip install pymongo

## 二、pymongo使用
### 连接mongodb
Making a Connection with MongoClient：
```python
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
#Or use the MongoDB URI format:
client = MongoClient('mongodb://localhost:27017/')
#
client = MongoClient(host=host,port=port,tz_aware=False)
```

### 连接数据库与表
Getting a Database：
```python
db = client.get_database(dbname)
#或者
db = client.test_database
#或者
db = client['test-database']
```
Getting a Collection：
```python
collection = db.get_collection(collectionname)
#或者
collection = db.test_collection
#或者
collection = db['test-collection']
```
**MongoDB中的集合（数据库）都是惰性创建的只有有数据插入时才会被创建。**

db权限验证:
```python
db.authenticate('username', 'password')
```

### Collection主要方法
操作Collection方法和MongoDB的命令基本一样
##### 插入
```python
insert_one(document)
insert_many(documents)
```
##### 删除
```python
delete_one(filter)
delete_many(filter)
```
##### 查询
```python
find_one(filter=None, projection=None, skip=0,limit=0...)
find(filter=None, projection=None, skip=0,limit=0...)
```

##### 更新
update_one(self, filter, update, upsert=False,...)
update_many(self, filter, update, upsert=False,...)

##### Collection部分源码
Collection部分源码：
```python
class Collection(common.BaseObject):
    def insert_one(self, document, bypass_document_validation=False,
                   session=None):
        """Insert a single document."""
        
    def insert_many(self, documents, ordered=True,
                    bypass_document_validation=False, session=None):
        """Insert an iterable of documents."""
    
    def update_one(self, filter, update, upsert=False,
                   bypass_document_validation=False,
                   collation=None, array_filters=None, session=None):
        """Update a single document matching the filter."""
        
    def update_many(self, filter, update, upsert=False, array_filters=None,
                    bypass_document_validation=False, collation=None,
                    session=None):
        """Update one or more documents that match the filter."""
        
    def delete_one(self, filter, collation=None, session=None):
        """Delete a single document matching the filter."""
        
    def delete_many(self, filter, collation=None, session=None):
        """Delete one or more documents matching the filter."""
    
    def find_one(self, filter=None, *args, **kwargs):
        """Get a single document from the database."""
        cursor = self.find(filter, *args, **kwargs)
        for result in cursor.limit(-1):
            return result
        return None
        
    def find(self, *args, **kwargs):
        """Query the database."""
        return Cursor(self, *args, **kwargs)
        
    def delete_one(self, filter, collation=None, session=None):
        """Delete a single document matching the filter."""
        
    def delete_many(self, filter, collation=None, session=None):
        """Delete one or more documents matching the filter."""

    def create_index(self, keys, session=None, **kwargs):
        """Creates an index on this collection.

        Takes either a single key or a list of (key, direction) pairs.

        To create a single key ascending index on the key ``'mike'`` we just
        use a string argument::

          >>> my_collection.create_index("mike")

        For a compound index on ``'mike'`` descending and ``'eliot'``
        ascending we need to use a list of tuples::

          >>> my_collection.create_index([("mike", pymongo.DESCENDING),
          ...                             ("eliot", pymongo.ASCENDING)])
        """
class Cursor(object):
    """A cursor / iterator over Mongo query results.
    """
    def __init__(self, collection, filter=None, projection=None, skip=0,
                 limit=0, no_cursor_timeout=False,
                 cursor_type=CursorType.NON_TAILABLE,
                 sort=None, allow_partial_results=False, oplog_replay=False,
                 modifiers=None, batch_size=0, manipulate=True,
                 collation=None, hint=None, max_scan=None, max_time_ms=None,
                 max=None, min=None, return_key=False, show_record_id=False,
                 snapshot=False, comment=None, session=None):
                 
     def limit(self, limit):
         """Limits the number of results to be returned by this cursor."""
         self.__empty = False
         self.__limit = limit
         return self
         
     def skip(self, skip):
         """Skips the first `skip` results of this cursor"""
         self.__skip = skip
         return self
         
     def sort(self, key_or_list, direction=None):
         """Sorts this cursor's results.

         Pass a field name and a direction, either
         :data:`~pymongo.ASCENDING` or :data:`~pymongo.DESCENDING`::

             for doc in collection.find().sort('field', pymongo.ASCENDING):
                 print(doc)

         To sort by multiple fields, pass a list of (key, direction) pairs::

             for doc in collection.find().sort([
                     ('field1', pymongo.ASCENDING),
                     ('field2', pymongo.DESCENDING)]):
                 print(doc)

         Parameters:
           - `key_or_list`: a single key or a list of (key, direction)
             pairs specifying the keys to sort on
           - `direction` (optional): only used if `key_or_list` is a single
             key, if not given :data:`~pymongo.ASCENDING` is assumed
         """
         self.__check_okay_to_chain()
         keys = helpers._index_list(key_or_list, direction)
         self.__ordering = helpers._index_document(keys)
         return self
         
    def count(self, with_limit_and_skip=False):
        """**DEPRECATED** - Get the size of the results set for this query."""
        
    def __iter__(self):
        return self
```

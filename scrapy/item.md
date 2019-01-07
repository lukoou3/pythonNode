### 一、item
&emsp;&emsp;抓取的主要目标是从非结构化源（通常是网页）中提取结构化数据。scrapy spider可以像Python一样返回提取的数据。虽然方便和熟悉，但Python缺乏结构：很容易在字段名称中输入拼写错误返回不一致的数据，尤其是在具有许多spider的较大项目中。  
&emsp;&emsp;为了定义通用输出数据格式，Scrapy提供了Item类。 Item对象是用于收集抓取数据的简单容器。它们提供类似dict的 API，并具有用于声明其可用字段的方便语法。  
&emsp;&emsp;**Item类似与dict，不过Item对象只能够给已经声明的字段赋值**  

### 二、测试item
##### 声明item
```python
import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
```

##### 声明item
```python
import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)
```

##### 创建item
```python
>>> product = Product()
>>> product = Product(name='Desktop PC', price=1000)
```

##### 设置访问字段
```python
>>> product = Product(name='Desktop PC', price=1000)
>>> product['name']
Desktop PC
>>> product.get('name')
Desktop PC

>>> product['last_updated']
Traceback (most recent call last):
    ...
KeyError: 'last_updated'

>>> product.get('last_updated', 'not set')
not set

>>> product['last_updated'] = 'today'
>>> product['last_updated']
today

>>> product['lala'] = 'test' # 设置未声明的字段会抛出异常
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```

##### 访问所有字段值
&emsp;&emsp;要访问所有字段值，只需使用典型的dict API：
```python
>>> product.keys()
['price', 'name']

>>> product.items()
[('price', 1000), ('name', 'Desktop PC')]
```

##### 复制item
```python
>>> product2 = Product(product)
>>> print product2
Product(name='Desktop PC', price=1000)

>>> product3 = product2.copy()
>>> print product3
Product(name='Desktop PC', price=1000)
```

##### 从item到dict
```python
>>> dict(product) # create a dict from all populated values
{'price': 1000, 'name': 'Desktop PC'}
```

##### 从dict到item
```python
>>> Product({'name': 'Laptop PC', 'price': 1500})
Product(price=1500, name='Laptop PC')

>>> Product({'name': 'Laptop PC', 'lala': 1500}) # warning: unknown field in dict
Traceback (most recent call last):
    ...
KeyError: 'Product does not support field: lala'
```

**注意：item与dict的copy方法都是浅拷贝，在属性中有list等属性时要使用深拷贝**
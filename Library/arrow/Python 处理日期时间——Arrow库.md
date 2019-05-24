
# Python 处理日期时间——Arrow库
## 简介
Python针对日期时间的处理提供了大量的package，类和方法，但在可用性上来看非常繁琐和麻烦

第三方库Arrow提供了一个合理的、人性化的方法来创建、操作、格式转换的日期，时间，和时间戳，帮助我们使用较少的导入和更少的代码来处理日期和时间。

```
pip install arrow
```


```python
import arrow
```

github地址：https://github.com/crsmithdev/arrow/

## 快速入门
```python
>>> import arrow
>>> utc = arrow.utcnow()
>>> utc
<Arrow [2013-05-11T21:23:58.970460+00:00]>

>>> utc = utc.shift(hours=-1)
>>> utc
<Arrow [2013-05-11T20:23:58.970460+00:00]>

>>> local = utc.to('US/Pacific')
>>> local
<Arrow [2013-05-11T13:23:58.970460-07:00]>

>>> arrow.get('2013-05-11T21:23:58.970460+00:00')
<Arrow [2013-05-11T21:23:58.970460+00:00]>

>>> local.timestamp
1368303838

>>> local.format()
'2013-05-11 13:23:58 -07:00'

>>> local.format('YYYY-MM-DD HH:mm:ss ZZ')
'2013-05-11 13:23:58 -07:00'

>>> local.humanize()
'an hour ago'

>>> local.humanize(locale='ko_kr')
'1시간 전'
```

## arrow的使用
### 获取时间
#### 获取当前时间
通过utcnow()和now()分别获取了utc时间和local时间，最终获取的是一个Arrow时间对象，通过这个对象我们可以做各种时间转换。
获取当前时间：


```python
utc = arrow.utcnow()
utc
```




    <Arrow [2019-05-24T09:55:39.188649+00:00]>




```python
local = arrow.now()
local
```




    <Arrow [2019-05-24T17:55:39.246968+08:00]>




```python
local.timestamp
```




    1558691739



时区转换：


```python
utc.to('US/Pacific')
```




    <Arrow [2019-05-24T02:55:39.188649-07:00]>




```python
utc.to('local')
```




    <Arrow [2019-05-24T17:55:39.188649+08:00]>




```python
utc.to('local').to('utc')
```




    <Arrow [2019-05-24T09:55:39.188649+00:00]>




```python
arrow.now('US/Pacific')
```




    <Arrow [2019-05-24T02:55:39.539537-07:00]>



#### 从时间戳获得Arrow对象
时间戳可以是int，float或者可以转化为float的字符串


```python
arrow.get()
```




    <Arrow [2019-05-24T09:55:39.605278+00:00]>




```python
arrow.get(1558688192.277)#传的是秒数
```




    <Arrow [2019-05-24T08:56:32.277000+00:00]>




```python
arrow.get(1558688192)
```




    <Arrow [2019-05-24T08:56:32+00:00]>




```python
arrow.get('1558688192.277')
```




    <Arrow [2019-05-24T08:56:32.277000+00:00]>




```python
arrow.get('1558688192.277').to('local')
```




    <Arrow [2019-05-24T16:56:32.277000+08:00]>



可以看出arrow.get获得是utc时间的arrow对象

#### 从字符串获得Arrow对象
将字符串转换为arrow对象    arrow.get(string[,format_string])


```python
arrow.get('2018-02-24 12:30:45', 'YYYY-MM-DD HH:mm:ss')
```




    <Arrow [2018-02-24T12:30:45+00:00]>




```python
arrow.get('2018-02-24 12:30:45', 'YYYY-MM-DD HH:mm:ss').to('local')
```




    <Arrow [2018-02-24T20:30:45+08:00]>



遵循ISO-8601的字符串不需要格式字符串参数即可转换


```python
arrow.get('2018-02-24T13:00:00.000-07:00')
```




    <Arrow [2018-02-24T13:00:00-07:00]>



#### 通过年月日等数字创建Arrow对象


```python
arrow.get(2018, 5, 5, 12, 30, 45)
```




    <Arrow [2018-05-05T12:30:45+00:00]>




```python
arrow.get(2018, 5, 5)
```




    <Arrow [2018-05-05T00:00:00+00:00]>



### arrow对象的属性
获取datetime


```python
now = arrow.utcnow()
now.datetime
```




    datetime.datetime(2019, 5, 24, 9, 55, 40, 213796, tzinfo=tzutc())




```python
now = arrow.now()
now.datetime
```




    datetime.datetime(2019, 5, 24, 17, 55, 40, 263673, tzinfo=tzlocal())



**获取时间戳**


```python
now.timestamp
```




    1558691740



Get a naive datetime, and tzinfo:


```python
now.naive
```




    datetime.datetime(2019, 5, 24, 17, 55, 40, 263673)




```python
now.tzinfo
```




    tzlocal()



Call datetime functions that return properties(转为标准库对象):


```python
now.date()
```




    datetime.date(2019, 5, 24)




```python
now.time()
```




    datetime.time(17, 55, 40, 263673)



获取年月日等


```python
now.year
```




    2019




```python
now.day
```




    24



### 时间推移
shift方法获取某个时间之前或之后的时间,关键字参数为years,months,weeks,days,hours，seconds，microseconds
```python
shift(**kwargs)
````


```python
now.shift(weeks=+3)    #三周后
```




    <Arrow [2019-06-14T17:55:40.263673+08:00]>




```python
now.shift(days=-1)     #一天前 
```




    <Arrow [2019-05-23T17:55:40.263673+08:00]>




```python
now.shift(weekday=6)   #距离now最近的星期日，weekday从0到6
```




    <Arrow [2019-05-26T17:55:40.263673+08:00]>




```python
now.shift(years=1)  # 明年
```




    <Arrow [2020-05-24T17:55:40.263673+08:00]>




```python
now.shift(years=+1)  # 明年
```




    <Arrow [2020-05-24T17:55:40.263673+08:00]>



### 时间替换
返回一个被替换后的arrow对象，原对象不变
```python
replace(**kwargs)
```


```python
now.replace(hour=9)
```




    <Arrow [2019-05-24T09:55:40.263673+08:00]>



### 格式化输出  format([format_string])


```python
now.format()
```




    '2019-05-24 17:55:40+08:00'




```python
now.format('YYYY-MM-DD HH:mm:ss ZZ')
```




    '2019-05-24 17:55:40 +08:00'




```python
now.format('YYYY-MM-DD HH:mm:ss')
```




    '2019-05-24 17:55:40'



### Convert(时区转换)
Convert to timezones by name or tzinfo:


```python
utc = arrow.utcnow()
utc
```




    <Arrow [2019-05-24T09:55:41.288592+00:00]>




```python
utc.to('local')
```




    <Arrow [2019-05-24T17:55:41.288592+08:00]>




```python
utc.to('+08:00')
```




    <Arrow [2019-05-24T17:55:41.288592+08:00]>




```python
utc.to('US/Pacific')
```




    <Arrow [2019-05-24T02:55:41.288592-07:00]>



### 时间范围和区间 
span(string),floor(),ceil()    
arrow.Arrow.span_range(),arrow.Arrow.range()


```python
now
```




    <Arrow [2019-05-24T17:55:40.263673+08:00]>




```python
now.span('hour')    #a所在的时间区间
```




    (<Arrow [2019-05-24T17:00:00+08:00]>,
     <Arrow [2019-05-24T17:59:59.999999+08:00]>)




```python
now.floor('hour')   #a所在区间的开始
```




    <Arrow [2019-05-24T17:00:00+08:00]>




```python
now.ceil('hour')    #a所在区间的结尾
```




    <Arrow [2019-05-24T17:59:59.999999+08:00]>




```python
start = arrow.get(2018, 2, 24, 12, 30)
end = arrow.get(2018, 2, 24, 15, 20)
```


```python
for r in arrow.Arrow.span_range('hour',start,end):    #获取start，end之间的时间区间
    print(r)
```

    (<Arrow [2018-02-24T12:00:00+00:00]>, <Arrow [2018-02-24T12:59:59.999999+00:00]>)
    (<Arrow [2018-02-24T13:00:00+00:00]>, <Arrow [2018-02-24T13:59:59.999999+00:00]>)
    (<Arrow [2018-02-24T14:00:00+00:00]>, <Arrow [2018-02-24T14:59:59.999999+00:00]>)
    (<Arrow [2018-02-24T15:00:00+00:00]>, <Arrow [2018-02-24T15:59:59.999999+00:00]>)



```python
for r in arrow.Arrow.range('hour',start,end):        #获取间隔单位时间的时间
    print(r)
```

    2018-02-24T12:30:00+00:00
    2018-02-24T13:30:00+00:00
    2018-02-24T14:30:00+00:00


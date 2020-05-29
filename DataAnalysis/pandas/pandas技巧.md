# pandas技巧

## DataFrame去重
```python
In [1]: import pandas as pd

In [2]:  df = pd.DataFrame({'colA' : list('AABCA'), 'colB' : list('AABDA'),'col
   ...: C' : [100,100,30,50,20], 'colD': [100,100,60,80,50]})

In [3]: df
Out[3]:
  colA colB  colC  colD
0    A    A   100   100
1    A    A   100   100
2    B    B    30    60
3    C    D    50    80
4    A    A    20    50
# 按全量字段去重, 保留第一个(默认)
In [4]: df2 = df.drop_duplicates()

In [5]: df2
Out[5]:
  colA colB  colC  colD
0    A    A   100   100
2    B    B    30    60
3    C    D    50    80
4    A    A    20    50
# 按指定字段去重, 保留第一个
In [6]: df3 = df.drop_duplicates(subset=['colA', 'colB'], keep='first');df3
Out[6]:
  colA colB  colC  colD
0    A    A   100   100
2    B    B    30    60
3    C    D    50    80

# 按全量字段去重, 保留最后一个
In [25]: df3 = df.drop_duplicates(keep='last')

In [26]: df3
Out[26]:
  colA colB  colC  colD
1    A    A   100   100
2    B    B    30    60
3    C    D    50    80
4    A    A    20    50


```













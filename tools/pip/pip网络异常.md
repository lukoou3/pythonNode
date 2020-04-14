# pip网络异常

不知道为啥网络的基础host为啥没了
```
lifengchao@lifengchao-YangTianM4601c-00:~$ pip install scikit-learn
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fa5b8831278>: Failed to establish a new connection: [Errno 101] 网络不可达',)': /simple/scikit-learn/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fa5b88314e0>: Failed to establish a new connection: [Errno 101] 网络不可达',)': /simple/scikit-learn/
WARNING: Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fa5b8831160>: Failed to establish a new connection: [Errno 101] 网络不可达',)': /simple/scikit-learn/
WARNING: Retrying (Retry(total=1, connect=None, read=None, redirect=None, status=None)) after connection broken by 'NewConnectionError('<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x7fa5b8831668>: Failed to establish a new connection: [Errno 101] 网络不可达',)': /simple/scikit-learn/
^CERROR: Operation cancelled by user
```

手动指定一下网络地址：
使用
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple
```
```
lifengchao@lifengchao-YangTianM4601c-00:~$ pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple scikit-learn
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting scikit-learn
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/5e/d8/312e03adf4c78663e17d802fe2440072376fee46cada1404f1727ed77a32/scikit_learn-0.22.2.post1-cp36-cp36m-manylinux1_x86_64.whl (7.1 MB)
     |████████████████████████████████| 7.1 MB 20 kB/s 
Requirement already satisfied: numpy>=1.11.0 in /usr/local/lib/python3.6/dist-packages (from scikit-learn) (1.15.4)
Collecting joblib>=0.11
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/28/5c/cf6a2b65a321c4a209efcdf64c2689efae2cb62661f8f6f4bb28547cf1bf/joblib-0.14.1-py2.py3-none-any.whl (294 kB)
     |████████████████████████████████| 294 kB 233 kB/s 
Requirement already satisfied: scipy>=0.17.0 in ./.local/lib/python3.6/site-packages (from scikit-learn) (1.1.0)
Installing collected packages: joblib, scikit-learn
Successfully installed joblib-0.14.1 scikit-learn-0.22.2.post1
```





















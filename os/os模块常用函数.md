### 一、os下常用函数
1、**os.makedirs(path)**
创建文件夹(父目录不存在自动创建)
```python
if not os.path.exists(downloadPath):
    os.makedirs(downloadPath)
```

2、**os.remove(pathorfile)**
删除文件夹

3、**os.listdir()**
返回文件夹下的文件名(带后缀)列表
Return a list containing the names of the files in the directory

4、**os.rename(sourceFile, targetFile)**
相对于linux下的mv，移动和修改文件名

### 二、os.path下常用函数
##### 1、os.path.exists(path)
判断路径是否存在

##### 2、os.path.join(path, *paths)
用于连接路径
Join two (or more) paths.

##### 3、os.path.split(path)
返回文件的路径和文件名(带后缀)
```python
dirname,filename=os.path.split('/home/ubuntu/python_coding/split_func/split_function.py')
# dirname：/home/ubuntu/python_coding/split_func
#filename：split_function.py
```

##### 4、os.path.splitext(path)
将文件名和扩展名分开
```python
fname,fename=os.path.splitext('/home/ubuntu/python_coding/split_func/split_function.py')
# fname is:/home/ubuntu/python_coding/split_func/split_function
#fename is:.py
```

判断要下载的video是否已经下过了：
```python
downloaded_names = {os.path.splitext(d)[0] for d in os.listdir(downloadPath)}
for href,name in self.download_links:
    if name in downloaded_names:
        continue
    self.download_video_one_yuujx(href,name,path=downloadPath)
```

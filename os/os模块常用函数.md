### 一、os下常用函数
##### 1、**os.makedirs(path)**
创建文件夹(父目录不存在自动创建)
```python
if not os.path.exists(downloadPath):
    os.makedirs(downloadPath)
```

##### 2、**os.remove(pathorfile)**
删除文件夹

##### 3、**os.listdir()**
返回文件夹下的文件名(带后缀)列表
Return a list containing the names of the files in the directory

##### 4、**os.rename(sourceFile, targetFile)**
相对于linux下的mv，移动和修改文件名

##### 5、**os.walk(top, topdown=True, οnerrοr=None, followlinks=False)**
**输入参数**：

* top：所需遍历目录的路径    
* topdown：True时，则优先遍历top目录，否则优先遍历top的子目录(默认为True)    
* onerror：参数oneerror的默认值是"None",表示忽略文件遍历时产生的错误，如果不为空，则提供一个自定义函数提示错误信息，后边遍历抛出异常，需要一个 callable 对象，当walk需要异常时，会调用    
* followlinks：True时，则会遍历目录下的快捷方式(linux 下是 symbolic    
* link)实际所指的目录(默认False)

**返回值**：

* 返回值是一个生成器(generator),也就是需要不断的遍历它，来获得所有的内容。    
* 每次遍历的对象都是返回的是一个三元组**(root,dirs,files)**。这个三元组表示当前遍历的目录的信息，从top根目录开始到top根目录的每个子目录。    
* root 是当前遍历目录的相对路径    
* dirs 是一个 list ，内容是当前目录的子目录名称(不包括子目录)    
* files 同样是 list , 内容是当前目录的文件名称(不包括子目录)

对于某如下格式文件夹，执行以下代码（注：os.sep用来替换/符号更加稳定），打印如下
![](assets/markdown-img-paste-2019092222500959.png)
```python
#coding=utf-8
import os
 
p = "D:"+os.sep+"test"+os.sep+"tina"+os.sep+"dist"
for parent, dirname, filenames in os.walk(p):
    print parent
    print dirname
    print filenames
    print "------------------------"
```
输出
```
D:\test\tina\dist
['xxx']
['server.exe']
------------------------
D:\test\tina\dist\xxx
[]
['\xd0\xc2\xbd\xa8\xce\xc4\xb1\xbe\xce\xc4\xb5\xb5.txt']
------------------------
```

**打印文件夹下所有文件**：
```python
import  os
def walk(path):
    if not os.path.exists(path):
        return -1
    for parent,dirs,names in os.walk(path):
        for filename in names:
            print(os.path.join(parent,filename)) #路径和文件名连接构成完整路径
if __name__=='__main__':
    path = r"D:\pycharmWork\Toolbox"
    walk(path)
```

##### python递归目录下的所有文件
```python
import os
# 方法一： os.walk实现
def items_dir(rootname):
    l = []
    for main_dir, dirs, file_name_list in os.walk(rootname):
        # print('1',main_dir)
        # print('2',dirs)
        # print('3',file_name_list)
        for file in file_name_list:
            file_path = os.path.join(main_dir,file)
            print(file_path)
            l.append(file_path)
    return l

# items_dir('C:\\HXK\\code')

#===================================================#
#方法2 递归实现，os.listdir()
def list_all_files(rootdir):
    _files = []
    l1 = os.listdir(rootdir)# 列出文件夹下的所有目录和文件
    for i in range(0,len(l1)):
        path = os.path.join(rootdir, l1[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)

    return _files

print(list_all_files('C:\\HXK\\code'))
```

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

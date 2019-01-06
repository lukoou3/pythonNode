### 一、简介
shutil高级文件操作模块：
shutil模块提供了大量的文件的高级操作。特别针对文件拷贝和删除，主要功能为目录和文件操作以及压缩操作。对单个文件的操作也可参见os模块。

### 二、常用函数
###### 1、shutil.copy(src, dst)
    功能：复制文件
    返回值：复制之后的路径

###### 2、shutil.copy2(src, dst)
    功能：复制文件，保留元数据
    返回值：复制之后的路径

###### 3、shutil.copyfile(src, dst)
    功能：复制文件，如果是链接文件，将复制新文件，不复制链接shutil.copytree(src, dst, symlinks=False, ignore=None) 递归的去拷贝文件夹
    返回值：复制之后的路径

###### 4、shutil.copytree(src, dst, symlinks=False, ignore=None)
    功能：递归的去拷贝文件夹
    返回值：目标目录的路径
```python
shutil.copytree('folder1', 'folder2', ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))
shutil.copytree('f1', 'f2', symlinks=True, ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))
shutil.ignore_patterns(*patterns)
```

###### 5、shutil.rmtree(path[, ignore_errors[, onerror]])
    功能：递归的去删除文件

###### 6、shutil.move(src, dst)
    功能：递归的去移动文件，它类似mv命令，其实就是重命名。
    返回值：目标地址

### 三、shutil模块的压缩与解压缩方法
###### 1、make_archive(base_name, format, root_dir=None, base_dir=None,...)
    创建压缩包并返回文件路径

###### 2、unpack_archive()
    功能：解包操作
    格式：shutil.unpack_archive('归档文件路径','解包目标文件夹')
    返回值:None
    注意：文件夹不存在会新建文件夹

###### 3、get_archive_formats()

    功能：获取当前系统已注册的归档文件格式（后缀）
    格式：shutil.get_archive_formats()
    返回值：列表   [(后缀,解释),(后缀,解释),(后缀,解释)...]

###### 4、get_unpack_formats()
    功能：获取当前系统已经注册的解包文件格式(后缀)
    格式:shutil.get_unpack_formats()
    返回值：列表   [(后缀,解释),(后缀,解释),(后缀,解释)...]

### 三、make_archive与unpack_archive参数解释
```python
1、make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0,
                 dry_run=0, owner=None, group=None, logger=None)
```
用于创建打包文件(如：zip或tar)，并返回文件的绝对路径名称

``参数说明``:

    base_name : 创建的目标文件名，包括路径，减去任何特定格式的扩展。
    format : 压缩包格式。”zip”, “tar”, “bztar”或”gztar”中的一个。
    root_dir : 打包时切换到的根路径。也就是说，开始打包前，会先执行路径切换，切换到root_dir所指定的路径。默认值为当前路径
    base_dir : 开始打包的路径。也就是说，该命令会对base_dir所指定的路径进行打包，默认值为 root_dir ，即打包切换后的当前目录。亦可指定某一特定子目录，从而实现打包的文件包含此统一的前缀路径

base_dir用来打出包含前缀路径的压缩包(毕竟打出一个没有前缀目录的压缩包，某些情况下解包到当前路径是件比较崩溃的事情)
owner 和 group 为创建tar包时使用，默认为用户当前的 owner & group

```python
2、unpack_archive(filename, extract_dir=None, format=None)
```
    filename：是解压缩档案的路径。
    extract_dir：是解压缩存档的目标目录的路径。如果未提供，则使用当前工作目录。
    format：是存档格式：“zip”，“tar”，“gztar”，“bztar”或“xztar”之一。或者注册的任何其他格式 register_unpack_format()。如果未提供，unpack_archive() 将使用存档文件扩展名，并查看是否为该扩展注册了解包器。如果没有找到，ValueError则引发a。

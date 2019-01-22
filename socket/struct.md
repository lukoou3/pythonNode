## struct 模块
Python是一门非常简洁的语言，对于数据类型的表示，不像其他语言预定义了许多类型（如：在C#中，光整型就定义了8种）

它只定义了六种基本类型：字符串，整数，浮点数，元组（set），列表（array），字典（key/value）

通过这六种数据类型，我们可以完成大部分工作。但python有时需要处理二进制数据，例如 存取文件，socket操作时.这时候，可以使用python的struct模块来完成.可以用struct来处理c语言中的结构体.

## struct 主要函数简介
#### 1、pack(fmt, *args)
按照给定的格式(fmt)，把数据封装成字符串(实际上是类似于c结构体的字节流)
```python
def pack(fmt, *args):
    """
    pack(fmt, v1, v2, ...) -> bytes
    
    Return a bytes object containing the values v1, v2, ... packed according
    to the format string fmt.  See help(struct) for more on format strings.
    """
    return b""
```

#### 2、unpack(fmt, string)
按照给定的格式(fmt)解析字节流string，返回解析出来的tuple
```python
def unpack(fmt, string):
    """
    unpack(fmt, buffer) -> (v1, v2, ...)
    
    Return a tuple containing values unpacked according to the format string
    fmt.  The buffer's size in bytes must be calcsize(fmt). See help(struct)
    for more on format strings.
    """
    pass
```

#### 3、calcsize(fmt)
计算给定的格式(fmt)占用多少字节的内存
```python
def calcsize(fmt):
    """
    calcsize(fmt) -> integer
    
    Return size in bytes of the struct described by the format string fmt.
    """
    return 0
```

#### 4、pack_into(fmt, buffer, offset, *args)
类似于pack(fmt, *args)，只是把数据储存在buffer中
```python
def pack_into(fmt, buffer, offset, *args): 
    """
    pack_into(fmt, buffer, offset, v1, v2, ...)
    
    Pack the values v1, v2, ... according to the format string fmt and write
    the packed bytes into the writable buffer buf starting at offset.  Note
    that the offset is a required argument.  See help(struct) for more
    on format strings.
    """
    pass
```

#### 5、unpack_from(fmt, buffer, offset=0)
unpack(fmt, string)，只是从buffer中取出数据
```python
def unpack_from(fmt, buffer, offset=0):
    """
    unpack_from(fmt, buffer, offset=0) -> (v1, v2, ...)
    
    Return a tuple containing values unpacked according to the format string
    fmt.  The buffer's size, minus offset, must be at least calcsize(fmt).
    See help(struct) for more on format strings.
    """
    pass
```

## struct fmt类型表
#### fmt支持的格式
| Format | C Type           | Python type        | Standard size | Notes    |
| ------ | ---------------- | ------------------ | ------------- | -------- |
| x      | pad byte         | no value           |               |          |
| c      | char             | string of length 1 | 1             |          |
| b      | signedchar       | integer            | 1             | (3)      |
| B      | unsignedchar     | integer            | 1             | (3)      |
| ?      | _Bool            | bool               | 1             | (1)      |
| h      | short            | integer            | 2             | (3)      |
| H      | unsignedshort    | integer            | 2             | (3)      |
| i      | int              | integer            | 4             | (3)      |
| I      | unsignedint      | integer            | 4             | (3)      |
| l      | long             | integer            | 4             | (3)      |
| L      | unsignedlong     | integer            | 4             | (3)      |
| q      | longlong         | integer            | 8             | (2), (3) |
| Q      | unsignedlonglong | integer            | 8             | (2), (3) |
| f      | float            | float              | 4             | (4)      |
| d      | double           | float              | 8             | (4)      |
| s      | char[]           | string             | 1             |          |
| p      | char[]           | string             |               |          |
| P      | void*            | integer            |               | (5), (3) |
```
注1.q和Q只在机器支持64位操作系统有意义
注2.每个格式前可以有一个数字，表示个数
注3.s格式表示一定长度的字符串，4s表示长度为4的字符串，但是p表示的是pascal字符串
注4.P用来转换一个指针，其长度和机器字长相关
注5.最后一个可以用来表示指针类型的，占4个字节
```
#### fmt字节对齐方式
为了同c中的结构体交换数据，还要考虑有的c或c++编译器使用了字节对齐，通常是以4个字节为单位的32位系统，故而struct根据本地机器字节顺序转换.可以用格式中的第一个字符来改变对齐方式.定义如下：   
| CHARACTER | BYTE ORDER             | SIZE     | ALIGNMENT |
| --------- | ---------------------- | -------- | --------- |
| @         | native                 | native   | native    |
| =         | native                 | standard | none      |
| <         | little-endian          | standard | none      |
| >         | big-endian             | standard | none      |
| !         | network (= big-endian) | standard | none      |

使用方法是放在fmt的第一个位置，就像`@5s6sif`

## 事例
#### 示例一
比如有一个结构体
```c
struct Header
{
    unsigned short id;
    char[4] tag;
    unsigned int version;
    unsigned int count;
}
```
通过socket.recv接收到了一个上面的结构体数据，存在字符串s中，现在需要把它解析出来，可以使用unpack()函数.
```python
import struct

id, tag, version, count = struct.unpack("!H4s2I", s)
```
上面的格式字符串中，!表示我们要使用网络字节顺序解析，因为我们的数据是从网络中接收到的，在网络上传送的时候它是网络字节顺序的.后面的H表示 一个unsigned short的id,4s表示4字节长的字符串，2I表示有两个unsigned int类型的数据.
就通过一个unpack，现在id, tag, version, count里已经保存好我们的信息了.

同样，也可以很方便的把本地数据再pack成struct格式.
```python
ss = struct.pack("!H4s2I", id, tag, version, count)
```
pack函数就把id, tag, version, count按照指定的格式转换成了结构体Header，ss现在是一个字符串(实际上是类似于c结构体的字节流)，可以通过 socket.send(ss)把这个字符串发送出去.

#### 示例二
```python
import struct

values = (1, 'abc', 2.7)
s = struct.Struct('I3sf')

packed_data = s.pack(*values)
unpacked_data = s.unpack(packed_data)
```

#### 示例三
利用buffer，使用pack_into和unpack_from方法  

使用二进制打包数据的场景大部分都是对性能要求比较高的使用环境。而在上面提到的pack方法都是对输入数据进行操作后重新创建了一个内存空间用于返回，也就是说我们每次pack都会在内存中分配出相应的内存资源，这有时是一种很大的性能浪费。struct模块还提供了pack_into() 和 unpack_from()的方法用来解决这样的问题，也就是对一个已经提前分配好的buffer进行字节的填充，而不会每次都产生一个新对象对字节进行存储。

```python
import struct
import binascii
import ctypes
 
values= (1,'abc',2.7)
s= struct.Struct('I3sf')
prebuffer= ctypes.create_string_buffer(s.size)
print 'Before :',binascii.hexlify(prebuffer)
s.pack_into(prebuffer,0,*values)
print 'After pack:',binascii.hexlify(prebuffer)
unpacked= s.unpack_from(prebuffer,0)
print 'After unpack:',unpacked
```
输出：  
```
Before : 000000000000000000000000 
After pack: 0100000061626300cdcc2c40 
After unpack: (1, 'abc', 2.700000047683716) 
```

对比使用pack方法打包，pack_into 方法一直是在对prebuffer对象进行操作，没有产生多余的内存浪费。另外需要注意的一点是，pack_into和unpack_from方法均是对string buffer对象进行操作，并提供了offset参数，用户可以通过指定相应的offset，使相应的处理变得更加灵活。例如，我们可以把多个对象pack到一个buffer里面，然后通过指定不同的offset进行unpack：
```python
import struct
import binascii
import ctypes
 
values1= (1,'abc',2.7)
values2= ('defg',101)
s1= struct.Struct('I3sf')
s2= struct.Struct('4sI')
 
prebuffer= ctypes.create_string_buffer(s1.size+s2.size)
print 'Before :',binascii.hexlify(prebuffer)
s1.pack_into(prebuffer,0,*values1)
s2.pack_into(prebuffer,s1.size,*values2)
print 'After pack:',binascii.hexlify(prebuffer)
print s1.unpack_from(prebuffer,0)
print s2.unpack_from(prebuffer,s1.size)
```
输出：  
```
Before : 0000000000000000000000000000000000000000 
After pack: 0100000061626300cdcc2c406465666765000000 
(1, 'abc', 2.700000047683716) 
('defg', 101)
```
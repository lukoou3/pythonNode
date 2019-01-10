## downloading files
scrapy为下载文件提供了可重用的 item pipelines，这些pipelines的继承关系：
```
MediaPipeline
    FilesPipeline
        ImagesPipeline
```
MediaPipeline类是文件下载的抽象类，我们使用FilesPipeline和ImagesPipeline来下载文件和图片，他们有以下的一些特点：  
#### FilesPipeline
* 避免重新下载最近已经下载过的数据  
* 指定存储路径  

**FilesPipeline的典型工作流程如下**：  
* 在一个爬虫里，你抓取一个项目，把其中图片的URL放入 file_urls 组内。  
* 项目从爬虫内返回，进入项目管道。  
* 当项目进入 FilesPipeline，file_urls 组内的URLs将被Scrapy的调度器和下载器（这意味着调度器和下载器的中间件可以复用）安排下载，当优先级更高，会在其他页面被抓取前处理。项目会在这个特定的管道阶段保持“locker”的状态，直到完成文件的下载（或者由于某些原因未完成下载）。  
* 当文件下载完后，另一个字段(files)将被更新到结构中。这个组将包含一个字典列表，其中包括下载文件的信息，比如下载路径、源抓取地址（从 file_urls 组获得）和图片的校验码(checksum)。 files 列表中的文件顺序将和源 file_urls 组保持一致。如果某个图片下载失败，将会记录下错误信息，图片也不会出现在 files 组中。  

#### ImagesPipeline
* 避免重新下载最近已经下载过的数据  
* 指定存储路径  
* 将所有下载的图片转换成通用的格式（JPG）和模式（RGB）  
* 缩略图生成  
* 检测图像的宽/高，确保它们满足最小限制 
 
和FilesPipeline类似，除了默认的字段名不同，image_urls保存图片URL地址，images保存下载后的图片信息。当然，它还提供了一些拓展功能，比如图片的缩略图，过滤图片的尺寸。  
注意：你需要安装Pillow 库来实现ImagesPipeline的拓展功能。

## 使用FilesPipeline和ImagesPipeline
```Python
##导入
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
```
#### 启用MediaPipeline
对于FilesPipeline：
```Python
ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}
```
对于ImagesPipeline：
```
IITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}
```
可以同时使用ITEM_PIPELINES和IITEM_PIPELINES
#### 配置下载文件储存位置
必须配置文件储存位置，否则MediaPipeline将不会起作用：  
```Python
对于FilesPipeline：，配置FILES_STORE：
FILES_STORE = '/path/to/valid/dir'
对于ImagesPipeline，配置IMAGES_STORE：
IMAGES_STORE = '/path/to/valid/dir'
```
##### 默认文件的储存（File system storage）
The files are stored using a `SHA1 hash` of their URLs for the file names.

For example, the following image URL:
```
http://www.example.com/image.jpg
```
Whose SHA1 hash is:
```
3afec3b4765f8f0a07b78f98c07b83f013567a0a
```
Will be downloaded and stored in the following file:
```
<IMAGES_STORE>/full/3afec3b4765f8f0a07b78f98c07b83f013567a0a.jpg
```
Where:  
* <IMAGES_STORE> is the directory defined in IMAGES_STORE setting for the Images Pipeline.  
* full is a sub-directory to separate full images from thumbnails (if used). For more info see Thumbnail generation for images.  

言而总之默认文件的名称是文件url的`SHA1 hash`值，其储存在`FILES_STORE/full/`或`IMAGES_STORE/full/`下

#### 允许重定向
默认情况下，媒体管道会忽略重定向，即HTTP重定向到媒体文件URL请求将意味着媒体下载被视为失败。
要处理媒体重定向，请将此设置设置为True：
```Python
MEDIA_ALLOW_REDIRECTS = True
```

#### 其他配置
```Python
# 同时启用图片和文件管道
ITEM_PIPELINES = {
                  'scrapy.pipelines.images.ImagesPipeline': 1,
                  'scrapy.pipelines.files.FilesPipeline': 2,
                 }
FILES_STORE = 'D:'  # 文件存储路径
IMAGES_STORE = 'D' # 图片存储路径

# 避免下载最近90天已经下载过的文件内容
FILES_EXPIRES = 90
# 避免下载最近90天已经下载过的图像内容
IMAGES_EXPIRES = 30

# 设置图片缩略图
IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (250, 250),
}
# 图片过滤器，最小高度和宽度，低于此尺寸不下载
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110
```

## 扩展FilesPipeline或ImagesPipeline
我们下载文件一般不直接用FilesPipeline或ImagesPipeline，我们选择扩展他们已实现我们一些需求（文件路径、文件名修改）。    
FilesPipeline部分源码：
```Python
class FilesPipeline(MediaPipeline):
    MEDIA_NAME = "file"
    EXPIRES = 90
    STORE_SCHEMES = {
        '': FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
    }
    DEFAULT_FILES_URLS_FIELD = 'file_urls'
    DEFAULT_FILES_RESULT_FIELD = 'files'

    def media_downloaded(self, response, request, info):
        ...
        return {'url': request.url, 'path': path, 'checksum': checksum}

    ##一下都是重写MediaPipeline的方法
    ### Overridable Interface
    
    #生成需要下载文件的请求
    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get(self.files_urls_field, [])]

    def file_downloaded(self, response, request, info):
        path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)
        return checksum

    #item所有url下载完成后
    def item_completed(self, results, item, info):
        ""Called per item when all media requests has been processed"""
        if isinstance(item, dict) or self.files_result_field in item.fields:
            item[self.files_result_field] = [x for ok, x in results if ok]
        return item

    #返回文件的储存路径
    def file_path(self, request, response=None, info=None):
        ...
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
        return 'full/%s%s' % (media_guid, media_ext)
```

#### 重写 get_media_requests(item, info)
FilesPipeline从这个方法的返回的Request下载文件。  
```Python
def get_media_requests(self, item, info):
    for file_url in item['file_urls']:
        yield scrapy.Request(file_url)
```
这些请求将由FilesPipeline处理，当它们全部完成下载后，结果将以2元素的元组列表形式传送到 item_completed(results, item, info) 方法的results，每个元组包含 (success, file_info_or_error):  
* **success** 是一个布尔值，当图片成功下载时为 True ，因为某个原因下载失败为False  
* **file_info_or_error** 是一个包含下列关键字的字典（如果成功为 True ）或者出问题时为 Twisted Failure 。
    * **ur**l - 文件下载的url。这是从 get_media_requests() 方法返回请求的url。
    * **path** - 文件存储的路径（类似 IMAGES_STORE）
    * **checksum** - 图片内容的 MD5 hash

item_completed() 接收的元组列表与 get_media_requests() 方法返回请求的顺序相一致。下面是 results 参数的一个典型值:
```python
[(True,
  {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
   'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
   'url': 'http://www.example.com/files/product1.pdf'}),
 (False,
  Failure(...))]
```

#### 重写 item_completed(results, item, info)
当单个item的所有文件请求都已完成（完成下载或由于某种原因失败）时调用此方法。 
该item_completed方法必须返回将发送到后续Pipeline的输出，因此您必须返回（或删除）该item，就像在其他任何管道中一样。  
下面item_completed是在item的file_paths字段中存储下载的文件路径（在结果中传递）的方法示例，如果item不包含任何文件，则删除该item：  
```Python
from scrapy.exceptions import DropItem

def item_completed(self, results, item, info):
    file_paths = [x['path'] for ok, x in results if ok]
    if not file_paths:
        raise DropItem("Item contains no files")
    item['file_paths'] = file_paths
    return item
```

#### 重写 file_path(request, response=None, info=None)
此方法返回每个下载文件的储存路径
```Python
def file_path(self, request, response=None, info=None):
    url = request.url
    media_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
    media_ext = os.path.splitext(url)[1]  # change to request.url after deprecation
    return 'full/%s%s' % (media_guid, media_ext)
```

#### 扩展FilesPipeline的示例
1、重写item_completed修改下载路径
```Python
import scrapy
import os
import re
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.files import FilesPipeline

class ScrapydownloadtestPipeline(FilesPipeline):
    FILES_STORE = get_project_settings().get("FILES_STORE")

    def get_media_requests(self, item, info):
        yield scrapy.Request(item["file_url"],
            meta={"download_timeout":3000,#下载器在超时前等待的时间量（以秒为单位）默认： 180
                  "download_maxsize":4294967296,#默认值：1073741824（1024MB）下载程序将下载的最大响应大小（以字节为单位）。如果要禁用它，请将其设置为0。
                  "download_warnsize":209715200#默认值：33554432（32MB）下载程序将开始发出警告的响应大小（以字节为单位）。如果要禁用它，请将其设置为0。
                  })

    def item_completed(self, results, item, info):
        file_info = [x for ok,x in results if ok]
        if len(file_info)==0:
            return
        mp4 = ".mp4"
        match = re.search(r".+(\.\w+)$",file_info[0]["url"])
        if match:
            mp4 = match.group(1)
        os.rename(self.FILES_STORE + "/" + file_info[0]["path"],
                  self.FILES_STORE + "/" + item["file_name"]+mp4)
```

2、重写file_path修改下载路径
```Python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.files import FilesPipeline

class Mp3LoadPipeline(FilesPipeline):
    FILES_STORE = get_project_settings().get("FILES_STORE")

    def open_spider(self, spider):
        self.spiderinfo = self.SpiderInfo(spider)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.implicitly_wait(0)
        self.driver.get("file:///D:/Program%20Files/pythonide/js/text.html")


    def get_media_requests(self, item, info):
        name = item["name"]
        url = item["url"]
        tital = item["tital"]

        if item["urldecode"]:
            url = self.driver.execute_script('return mygetUrl('+url+')')
        if url:
            yield scrapy.Request(url,
                                 meta={
                                     "mp3info": {"title": name, "mp3name": tital},
                                     "download_timeout": 3000,  # 下载器在超时前等待的时间量（以秒为单位）默认： 180
                                     "download_maxsize": 4294967296,
                                     # 默认值：1073741824（1024MB）下载程序将下载的最大响应大小（以字节为单位）。如果要禁用它，请将其设置为0。
                                     "download_warnsize": 209715200
                                     # 默认值：33554432（32MB）下载程序将开始发出警告的响应大小（以字节为单位）。如果要禁用它，请将其设置为0。
                                 })



    def file_path(self, request, response=None, info=None):
        mp3info = request.meta["mp3info"]
        return '{0}/{1}'.format(mp3info["title"],mp3info["mp3name"].replace("\"","").replace("'","")
                                .replace("/", "").replace(":", "").replace("*", "").replace("?", "")
                                .replace("<", "").replace(">", "").replace("|", "")+".mp3")

    def close_spider(self, spider):
        if self.driver:
            self.driver.close()
```

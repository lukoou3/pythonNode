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

https://www.cnblogs.com/cnkai/p/7400467.html
https://www.cnblogs.com/moon-future/p/5545828.html
https://docs.scrapy.org/en/latest/topics/media-pipeline.html

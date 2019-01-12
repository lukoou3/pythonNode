## epub
EPub格式的电子书其实是一个压缩包文件，里面有几个按照规范定义的文件，所谓标准，就是规范EPub文件中某些文件的格式、内容和位置等等。因此，如果我们想要自己制作一本EPub格式的电子书，首先要了解要制作的内容压缩为zip文件前的文件结构是什么，一个典型的EPub的文件结构是这样的：  
![228457-b27f6e0f234f547b.webp](/assets/228457-b27f6e0f234f547b.webp_no1o5sozt.jpg)

其实结构可以更简单，下面给出我用Python语言构建的EPub文件的文件结构：
![228457-41766ea24e969997.webp](/assets/228457-41766ea24e969997.webp.jpg)

对比一下可以看出来有些文件并不是必须的，下面简单介绍一下EPub文件的目录结构：

### mimetype文件
这个内容是固定的，就一行
```
application/epub+zip
```

表明可以被EPub工具打开或zip工具打开

### META-INF文件夹
根据OCF（Open Container Format）标准，该文件夹包含一个文件container.xml，内容如下：
```
<?xml version="1.0" encoding="UTF-8" ?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles> 
    <rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/> </rootfiles>
</container>
```
它的功能是告诉阅读器电子书根文件路径以及打开方式，如果你修改了content.opf的名字或者把它放在其他位置，应该写明完整的路径。

### OEBPS文件夹
OEBPS目录用于存放OPS文档、OPF文档、CSS文档、NCX文档， OEBPS这个名字是可变的，可以根据containter.xml进行配置。这里是OPS文件夹。

#### opf文件：
content.opf文件的内容：
```
<?xml version="1.0" encoding="UTF-8" ?>
<package version="2.0" unique-identifier="PrimaryID" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:title>thisisbooktitle</dc:title>
<dc:creator>frank</dc:creator>
<dc:description>this is description</dc:description>
<meta name="cover" content="cover"/>
</metadata>
<manifest>
<item id='chapter1.html' href='chapter1.html' media-type='application/xhtml+xml'/>
<item id='chapter2.html' href='chapter2.html' media-type='application/xhtml+xml'/>
<item id="ncx" href="content.ncx" media-type="application/x-dtbncx+xml"/>
<item id="cover" href="cover.jpg" media-type="image/jpeg"/>
</manifest>
<spine toc="ncx">
<itemref idref='chapter1.html'/>
<itemref idref='chapter2.html'/>
</spine>
</package>
```
这是一个标准的XML文件，遵循OPF规范，主要属性有：
* metadata  
包括dc-metadata和x-metadata，dc-metadata有：
    ```
    <title>:题名
    <creator>：责任者
    <subject>：主题词或关键词
    <description>：内容描述
    <contributor>：贡献者或其它次要责任者
    <date>：日期
    <type>：类型
    <format>：格式
    <identifier>：标识符
    <source>：来源
    <language>：语种
    <relation>：相关信息
    <coverage>：履盖范围
    <rights>：权限描述
    ```
如果是未知属性可以用x-metadata描述
* menifest  
文件列表， 列出OEBPS文档及相关的文档，由一个子元素构成，<item id="" href="" media-type="">,该元素由三个属性构成：
    ```
    id:表示文件的ID号
    href：文件的相对路径
    media-type：文件的媒体类型
    ```
* spine toc="ncx"
表明书籍的阅读次序，其中有一个元素itemref idref=""，idref是menifest中的id
* opf还有很多其他属性，实际中用的并不多，即使用到也是一目了然的，如有需要可以连猜带蒙+搜索引擎。

#### ncx文件
content.ncx文件的内容：
```
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
<head>
  <meta name="dtb:uid" content=" "/>
  <meta name="dtb:depth" content="-1"/>
  <meta name="dtb:totalPageCount" content="0"/>
  <meta name="dtb:maxPageNumber" content="0"/>
</head>
 <docTitle><text>thisisbooktitle</text></docTitle>
 <docAuthor><text>frank</text></docAuthor>
<navMap>
<navPoint id='chapter1.html' class='level1' playOrder='1'>
<navLabel> <text>chapter1.html</text> </navLabel>
<content src='chapter1.html'/></navPoint>
<navPoint id='chapter2.html' class='level1' playOrder='2'>
<navLabel> <text>chapter2.html</text> </navLabel>
<content src='chapter2.html'/></navPoint>
</navMap>
</ncx>
```
该文件的作用是描述电子书的目录结构，这里的content.ncx文件并没有很明显的体现。有兴趣的话可以解压一本EPub格式的电子书看一看。

## epub添加注释
```
<body>
  <p class="h2"><br/></p>

  <p>千门万户曈曈日，总把新桃换旧符。<sup><a class="duokan-footnote" href="#B_12" style="text-decoration: none!important"><img alt="" src="../Images/note.png"/></a></sup></p>
   
  <div style="margin-left: 0em" class="duokan-footnote-content">
    <hr/>
  </div>

  <ol class="duokan-footnote-content">
    <li class="duokan-footnote-item" id="B_12"><p class="footnote"><a href="#A_002" style="text-decoration: none!important">米歇尔·奈伊<span class="kh_fs">（Michel Ney，1769–1815）</span>，法国军人，拿破仑一世麾下的18名“帝国元帅”之一。</a>​</p></li>  
  </ol>
</body>
```

## 掌阅中注释有弹出的效果
注释代码：
```
<img alt="" class="zhangyue-footnote" src="../Images/note-original.png" zy-footnote="注释内容" />
```

涉及的CSS代码：
```python
img.zhangyue-footnote {
    width: 0.85em; 
}
```

使用解压软件打开EPub文件，在META-INF文件夹里添加一个扩展名为.xml的文件。此XML文件命名为“zhangyue-expansion.xml”（使用记事本新建一个文本文档，粘贴下面的代码，然后重命名文件名并修改文件扩展名），内容如下：

```
<?xml version="1.0" encoding="UTF-8"?>
<zhangyue-expansion version="3.4.2">
  <book_id></book_id>
</zhangyue-expansion>
```
必须要有这个文件哦！


例子：
```
<p class="bodycontent">9月5日是阳历<img alt="" class="zhangyue-footnote" src="../Images/note-original.png" zy-footnote="阳历（又称太阳历，英语：Solar Calendar），为据地球围绕太阳公转轨道位置，或地球上所呈现出太阳直射点的周期性变化，所制定的历法；不据月亮的月相周期，岁实为365.2421897日，有大小月之分，一、三、五、七、八、十、十二月各三十一日；四、六、九、十一月各三十日。而二月平年二十八日，闰年二十九日。"/>年的第248天（闰年是249天），离一年的结束还有117天。</p>
```


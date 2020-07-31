[toc]

# 转换网上文章到markdown
自己刚开始是不做笔记的，但是后来发现学的东西过一段时间就会忘记，到用的时候还要百度或者重新去学习实现，很浪费时间。于是开始用markdown写笔记，有的是自己写的，有的是抄网上的，这里就说说怎么抄网上的。期初是在浏览器里复制的，一个一个复制大markdown笔记中，时间长了自己也会感觉烦，都是重复的操作，于是就有了用代码实现转换的想法。

刚开始就只是装换一个片段，比如转换html table和li，之后就干脆把整片文章全部装换了，每个网站的布局都是一样的，这样写了一个网站的装换之后，摘抄别人的文章就快多了，几乎是不需要时间的，爽歪歪。

## 测试
刚开始是在知乎上测试的，用的xpath解析html，后来发现xpath虽然在一般的爬虫上比较好用，但是在解析复杂的dom结构上还是差点意思，于是就改用了BeautifulSoup。

BeautifulSoup是用面向对象的思想实现的，在解析dom树和修改dom元素更改html内容方面还是比较好用的。BeautifulSoup的功能要比xpath强大的多，如果提取的内容很复杂还是用BeautifulSoup好。

用xpath测试的代码(可以忽略)：

test_zhihu_html.py
```python
# coding:utf-8

from lxml import etree
import re
import os
import shutil
from urllib.parse import unquote
import requests
import hashlib

math_re = re.compile(r"""<img src="https://www.zhihu.com/equation\?tex=(.+?)"[^>]*?>""")
# "<b.*?>(.{3,}?)</b>"
b_re = re.compile(r"<b[^<>]*?>([^<>]{2,}?)</b>")
link_re = re.compile(r"""<a href="(.+?)"[^<>]*?>([^<>]{2,}?)</a>""")
img_re = re.compile(r"""<img src="(.+?)"[^<>]*?>""")
img_re2 = re.compile(
    r"""<figure data-size="normal"><noscript><img[^<>]*?/></noscript><img src="([^<>]+?)"[^<>]*?></figure>""")
img_re3 = re.compile(
    r"""<figure data-size="normal"><noscript><img[^<>]*?/></noscript><img src="([^<>]+?)"[^<>]*?><figcaption>([^<>]*?)</figcaption></figure>""")

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


def replace_b(match):
    text = match.group(1)
    if text[-1] in ["，", ",", "。"]:
        return "**" + text[:-1] + "**" + text[-1]
    else:
        return "**" + text + "**"


def replace_link(match):
    link = match.group(1)
    start = "https://link.zhihu.com/?target="
    if start in link:
        link = link[len(start):]
    return """[{1}]({0} "{1}")""".format(unquote(link), match.group(2))


def zhihu_question_to_markdown(text):
    """<div class="RichContent RichContent--unescapable">"""
    #text = text.replace("""<b class="">""", "**").replace("""</b>""", "**")
    text = b_re.sub(replace_b, text)
    text = math_re.sub(lambda m: "$%s$" % unquote(m.group(1).replace("+", "%20")), text)
    text = img_re3.sub(r"""<p>![](\1)\n`\2`</p>""", text)
    text = img_re2.sub(r"""<p>![](\1)</p>""", text)

    text = img_re.sub(
        r""" ![](https://pics1.baidu.com/feed/203fb80e7bec54e733ed1d961a943d564ec26a63.jpeg?token=ffc7ba1203bb3433e42e0d5f1cd17ce8) """, text)
    #text = link_re.sub(r"""[\2](\1 "\2")""", text)
    text = link_re.sub(replace_link, text)
    text = text.replace("<br>", "    \n").replace("<br/>", "    \n")
    html = etree.HTML(text)
    rst = "\n\n".join(["".join(p.xpath(".//text()")).strip()
                       for p in html.xpath("//div[@class='RichContent-inner']/span/p | //div[@class='Post-RichTextContainer']/div/p")])
    return rst.replace("\n\n\n", "\n")


def make_md5(raw):
    """计算出一个字符串的MD5值"""
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()


def markdown_img_use_local(text, img_path="assets"):
    """将md文件中的http形式的img下载到本地并替换"""
    def download_img(url):
        response = requests.get(url, headers=headers)
        suffix = ".png"
        if url.rfind(".") > 0:
            suffix_ = url[url.rfind("."):]
            if suffix_ in [".jpg", ".png"]:
                suffix = suffix_
        name = make_md5(url) + suffix
        path = os.path.join(img_path, name)
        if not os.path.exists(path):
            with open(path, "wb") as fp:
                fp.write(response.content)
        return name

    if not os.path.exists(img_path):
        os.makedirs(img_path)

    img_re = re.compile(r"!\[\]\((http.*?)\)")
    imgs = set(img_re.findall(text))
    print("共需转换%d张图片" % len(imgs))
    url_names = [(url, download_img(url)) for url in imgs]
    for url, name in url_names:
        text = text.replace(url, "assets/" + name)
    return text


if __name__ == "__main__":    
    #text = requests.get("https://zhuanlan.zhihu.com/p/32181306", headers=headers).text
    text = """

 """
    text = zhihu_question_to_markdown(text)
    path = "assets"
    if os.path.exists(path):
        shutil.rmtree(path)
    text = markdown_img_use_local(text, path)
    print(text)

```

## 知乎文章转换
zhihu_html2md_usebs.py：
```python
# coding:utf-8
from bs4 import BeautifulSoup
from  bs4.element import Tag, NavigableString, Comment
import re, os
import requests
from urllib.parse import unquote
import hashlib

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}

def make_md5(raw):
    """计算出一个字符串的MD5值"""
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()

def out_ele_text_recursive(ele, sep="", strip=True):
    """格式化输出ele内的文本，会格式化br、p、div等添加\n"""
    if isinstance(ele, NavigableString):
        return ele.strip() if strip else ele.string
    texts = []
    pre_sibling = None
    for child in ele.contents:
        if pre_sibling is not None and pre_sibling.name in ("br", "p", "div"):
            texts.append("\n")
        pre_sibling = child
        if child.name == "script" or child.name == "style":
            continue
        if isinstance(child, Tag):
            texts.append(out_ele_text_recursive(child))
        elif type(child) == NavigableString:
            # NavigableString是str的子类
            texts.append(child.strip() if strip else child.string)
    return sep.join(texts)

class ZhihuHtmlMdConvert():
    def __init__(self, line_append = "\n\n", first_mdtitle_prefix="##"):
        self.line_append = line_append
        self.first_mdtitle_prefix = first_mdtitle_prefix

    def convert_link(self, tag):
        """原地转换超链接为Markdown格式"""
        prefix = "https://link.zhihu.com/?target="
        for link in tag.findAll("a"):
            link_url, link_text = link.get("href", default=""), link.get_text(strip=True)
            if prefix in link_url:
                link_url = link_url[len(prefix):]
            md_link = """[{1}]({0} "{1}")""".format(unquote(link_url), link_text)
            link.replace_with(md_link)

    def convert_figure(self, tag):
        """转换知乎页面中的figure标签"""
        for figure in tag.findAll("figure"):
            figcaption = figure.find("figcaption")  # 图片的注释元素
            img = figure.select_one("> img")
            if img is None:
                img = figure.select_one("img")
            note = figcaption.string if figcaption else ""
            img_url = img.get("src", "") if img else ""
            replace_tag = Tag(name="p")
            if note:
                md_img = "![]({0})\n`{1}`".format(img_url, note)
            else:
                md_img = "![]({0})".format(img_url)
            replace_tag.string = md_img
            figure.replace_with(replace_tag)

    def convert_img(self, tag):
        for img in tag.findAll("img"):
            img_url = img.get("src", "")
            md_img = " ![]({0}) ".format(img_url)
            img.replace_with(md_img)

    def convert_math_expression(self, tag):
        """转换知乎页面中的数学公式"""
        prefix = "https://www.zhihu.com/equation?tex="
        for img in tag.findAll("img", src=re.compile(r"^https://www.zhihu.com/equation\?tex=")):
            math = img.get("src", "")[len(prefix):]
            math = unquote(math.replace("+", "%20"))
            math_md = "$$%s$$" % math if r"\tag" in math else "$%s$" % math
            if r"\begin" in math_md or r"\end" in math_md:
                begin_re = re.compile(r"\\begin\s*\{[^\{\}]*?\}")
                end_re = re.compile(r"\\end\s*\{[^\{\}]*?\}")
                math_md = begin_re.sub("", math_md)
                math_md = end_re.sub("", math_md)
                math_md = math_md.replace(r"&=", "=").replace("& =", "=").replace(r"&\approx", r"\approx").replace(r"& \cdots", r"\cdots").replace(r"& \leq", r" \leq").replace(r"& & \geq", r" & \geq")
                if not math_md.startswith("$$"):
                    math_md = "$%s$" % math_md

            img.replace_with(math_md)

    def convert_btag(self, tag):
        for b in tag.findAll(["b", "strong"]):
            str_tags = list(filter(lambda e: type(e) == NavigableString and e.strip(), b.contents[::-1]))
            str_last = str_tags[0] if str_tags else None
            b.insert_before("**")
            if str_last and str_last.strip()[-1] in ["，", ",", ";", "；", "。", "！"]:
                str_last.replace_with( str_last.strip()[:-1] + "**" + str_last.strip()[-1] )
            else:
                b.insert_after("**")

    def convert_htag(self, tag):
        title_prefix = self.first_mdtitle_prefix
        h_tags = tag.findAll(re.compile(r"^h\d$"))
        h_names = {h_tag.name:int(h_tag.name[1:]) for h_tag in h_tags}
        for index,(h_name, _) in enumerate(sorted(h_names.items(), key=lambda x:x[1]), start=0):
            h_names[h_name] = index
        # 没有h标签，转换<p><b>一、</b></p>等
        if len(h_tags) == 0:
            title_re = re.compile(r"^[\d一二三四五六七八]")
            h_tags = tag.findAll( lambda ele: ele.name == "p" and ele.find("b") and title_re.match(ele.get_text(strip=True)) and  ele.get_text(strip=True) == ele.find("b").get_text(strip=True) )
        for h_tag in h_tags:
            if h_tag.get_text(strip=True) == "":
                continue
            # 看源码相当于jquery的text()
            h_tag.string = title_prefix + "#"*h_names.get(h_tag.name, 0) + " " + h_tag.get_text(strip=True)

    def html_to_markdown(self, html, use_local_img_replace_net=False, img_path=None):
        if use_local_img_replace_net and img_path is None:
            raise Exception("必须设置img_path")

        soup = BeautifulSoup(html, "lxml")
        content_div = soup.select_one(".Post-RichTextContainer > div, .RichContent-inner > span")
        if content_div is None:
            content_div = soup.select_one(".Post-RichTextContainer > div")
        self.convert_math_expression(content_div) # 这个必须在img转换之前
        self.convert_figure(content_div)
        self.convert_link(content_div)# a在img之前，img可能在a中
        self.convert_img(content_div)
        self.convert_htag(content_div) # 这个必须在b转换之前,h标签中可能有b标签
        self.convert_btag(content_div)

        text = self.out_tag_text_recursive(content_div)
        if use_local_img_replace_net:
            text = self.markdown_use_local_img(text, img_path)
        return text

    def markdown_use_local_img(self, text, img_path):
        """将md文件中的http形式的img下载到本地并替换"""
        def download_img(url):
            """下载图片并返回文件名"""
            response = requests.get(url, headers=headers)
            suffix = ".png"
            if url.rfind(".") > 0:
                suffix_ = url[url.rfind("."):]
                if suffix_ in [".jpg", ".png", ".gif"]:
                    suffix = suffix_
            name = make_md5(url) + suffix
            path = os.path.join(img_path, name)
            if not os.path.exists(path):
                with open(path, "wb") as fp:
                    fp.write(response.content)
            return name

        if not os.path.exists(img_path):
            os.makedirs(img_path)

        md_img_re = re.compile(r"!\[\]\((http.*?)\)")
        imgs = set(md_img_re.findall(text))
        print("共需转换%d张图片" % len(imgs))
        url_names = [(url, download_img(url)) for url in imgs]
        for url, name in url_names:
            text = text.replace(url, "assets/" + name)
        return text

    def out_tag_text_recursive(self, tag, sep="", strip=True):
        """格式化输出ele内的文本，会格式化br、p、div等添加\n"""
        line_append = self.line_append
        if isinstance(tag, NavigableString):
            return tag.strip() if strip else tag.string
        if tag.name == "ul" or tag.name == "ol":
            return self.out_ul_text(tag)
        if tag.name == "code":
            return self.out_code_text(tag)

        texts = []
        pre_sibling = None
        for child in tag.contents:
            if pre_sibling is not None and pre_sibling.name in ("br", "p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
                # 最多连续加三个\n
                if  "".join(texts[-4:]).endswith("\n\n") and (line_append == "\n\n" or line_append == "\n"):
                    if not "".join(texts[-4:]).endswith("\n\n\n"):
                        texts.append("\n")
                else:
                    texts.append(line_append)
            elif child.name in ("p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
                # 最多连续加三个\n
                if  "".join(texts[-4:]).endswith("\n\n") and (line_append == "\n\n" or line_append == "\n"):
                    if not "".join(texts[-4:]).endswith("\n\n\n"):
                        texts.append("\n")
                else:
                    texts.append(line_append)
            pre_sibling = child            
            if child.name == "script" or child.name == "style":
                continue
            if isinstance(child, Tag):
                texts.append(self.out_tag_text_recursive(child))
            elif type(child) == NavigableString:
                # NavigableString是str的子类
                texts.append(child.strip() if strip else child.string)
        return sep.join(texts)

    def out_ul_text(self, tag):
        lis = tag.select("> li")
        return "    \n".join(["* " + li.get_text(strip=True) for li in lis])

    def out_code_text(self, tag):
        class_ = " ".join( tag.get("class", ["python"]) )
        if "python" in class_:
            class_ = "python"
        code = tag.get_text()
        return "```%s\n%s\n```" % (class_, code)


if __name__ == '__main__':
    txt = """aa"""
    with open("txt", encoding="utf-8") as fp:
        txt = fp.read()
    convert = ZhihuHtmlMdConvert(first_mdtitle_prefix="###")
    txt = convert.html_to_markdown(txt, True , r"assets")
    print(txt)

```

## 腾讯云文章转换
这个代码有很多多余的，这是在知乎的基础上直接改的，很多无用的解析未删除。

tencentcloud_html2md_usebs.py：
```python
# coding:utf-8
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment
import re
import os
import requests
from urllib.parse import unquote
import hashlib

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


def make_md5(raw):
    """计算出一个字符串的MD5值"""
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()


def out_ele_text_recursive(ele, sep="", strip=True):
    """格式化输出ele内的文本，会格式化br、p、div等添加\n"""
    if isinstance(ele, NavigableString):
        return ele.strip() if strip else ele.string
    texts = []
    pre_sibling = None
    for child in ele.contents:
        if pre_sibling is not None and pre_sibling.name in ("br", "p", "div"):
            texts.append("\n")
        pre_sibling = child
        if child.name == "script" or child.name == "style":
            continue
        if isinstance(child, Tag):
            texts.append(out_ele_text_recursive(child))
        elif type(child) == NavigableString:
            # NavigableString是str的子类
            texts.append(child.strip() if strip else child.string)
    return sep.join(texts)


class TencentCloudHtmlMdConvert():
    def __init__(self, line_append="\n\n", first_mdtitle_prefix="##", default_pre_lang="xml"):
        self.line_append = line_append
        self.first_mdtitle_prefix = first_mdtitle_prefix
        self.default_pre_lang = default_pre_lang

    def convert_link(self, tag):
        """原地转换超链接为Markdown格式"""
        prefix = "https://link.zhihu.com/?target="
        for link in tag.findAll("a"):
            link_url, link_text = link.get("href", default=""), link.get_text(strip=True)
            if prefix in link_url:
                link_url = link_url[len(prefix):]
            md_link = """[{1}]({0} "{1}")""".format(unquote(link_url), link_text)
            link.replace_with(md_link)

    def convert_figure(self, tag):
        """转换知乎页面中的figure标签"""
        for figure in tag.findAll("figure"):
            figcaption = figure.find("figcaption")  # 图片的注释元素
            img = figure.select_one("> img")
            if img is None:
                img = figure.select_one("img")
            note = figcaption.string if figcaption else ""
            img_url = img.get("src", "") if img else ""
            replace_tag = Tag(name="p")
            if note:
                md_img = "![]({0})\n`{1}`".format(img_url, note)
            else:
                md_img = "![]({0})".format(img_url)
            replace_tag.string = md_img
            figure.replace_with(replace_tag)

    def convert_img(self, tag):
        for img in tag.findAll("img"):
            img_url = img.get("src", "")
            md_img = " ![]({0}) ".format(img_url)
            img.replace_with(md_img)

    def convert_math_expression(self, tag):
        """转换知乎页面中的数学公式"""
        prefix = "https://www.zhihu.com/equation?tex="
        for img in tag.findAll("img", src=re.compile(r"^https://www.zhihu.com/equation\?tex=")):
            math = img.get("src", "")[len(prefix):]
            math = unquote(math.replace("+", "%20"))
            math_md = "$$%s$$" % math if r"\tag" in math else "$%s$" % math
            if r"\begin" in math_md or r"\end" in math_md:
                begin_re = re.compile(r"\\begin\s*\{[^\{\}]*?\}")
                end_re = re.compile(r"\\end\s*\{[^\{\}]*?\}")
                math_md = begin_re.sub("", math_md)
                math_md = end_re.sub("", math_md)
                math_md = math_md.replace(r"&=", "=").replace("& =", "=").replace(r"&\approx", r"\approx").replace(
                    r"& \cdots", r"\cdots").replace(r"& \leq", r" \leq").replace(r"& & \geq", r" & \geq")
                if not math_md.startswith("$$"):
                    math_md = "$%s$" % math_md

            img.replace_with(math_md)

    def convert_btag(self, tag):
        for b in tag.findAll(["b", "strong"]):
            str_tags = list(filter(lambda e: type(e) == NavigableString and e.strip(), b.contents[::-1]))
            str_last = str_tags[0] if str_tags else None
            b.insert_before("**")
            if str_last and str_last.strip()[-1] in ["，", ",", ";", "；", "。", "！"]:
                str_last.replace_with(str_last.strip()[:-1] + "**" + str_last.strip()[-1])
            else:
                b.insert_after("**")

    def convert_htag(self, tag):
        title_prefix = self.first_mdtitle_prefix
        h_tags = tag.findAll(re.compile(r"^h\d$"))
        h_names = {h_tag.name: int(h_tag.name[1:]) for h_tag in h_tags}
        for index, (h_name, _) in enumerate(sorted(h_names.items(), key=lambda x: x[1]), start=0):
            h_names[h_name] = index
        # 没有h标签，转换<p><b>一、</b></p>等
        if len(h_tags) == 0:
            title_re = re.compile(r"^[\d一二三四五六七八]")
            h_tags = tag.findAll(lambda ele: ele.name == "p" and ele.find("b") and title_re.match(
                ele.get_text(strip=True)) and ele.get_text(strip=True) == ele.find("b").get_text(strip=True))
        for h_tag in h_tags:
            if h_tag.get_text(strip=True) == "":
                continue
            # 看源码相当于jquery的text()
            h_tag.string = title_prefix + "#" * h_names.get(h_tag.name, 0) + " " + h_tag.get_text(strip=True)

    def html_to_markdown(self, html, use_local_img_replace_net=False, img_path=None, ud_convert=None):
        if use_local_img_replace_net and img_path is None:
            raise Exception("必须设置img_path")

        soup = BeautifulSoup(html, "lxml")
        content_div = soup.select_one("div.J-articleContent")
        if ud_convert is not None:
            ud_convert(content_div)
        self.convert_math_expression(content_div)  # 这个必须在img转换之前
        self.convert_figure(content_div)
        self.convert_link(content_div)  # a在img之前，img可能在a中
        self.convert_img(content_div)
        self.convert_htag(content_div)  # 这个必须在b转换之前,h标签中可能有b标签
        self.convert_btag(content_div)

        text = self.out_tag_text_recursive(content_div)
        if use_local_img_replace_net:
            text = self.markdown_use_local_img(text, img_path)
        return text

    def markdown_use_local_img(self, text, img_path):
        """将md文件中的http形式的img下载到本地并替换"""
        def download_img(url):
            """下载图片并返回文件名"""
            response = requests.get(url, headers=headers)
            suffix = ".png"
            if url.rfind(".") > 0:
                suffix_ = url[url.rfind("."):]
                if suffix_ in [".jpg", ".png", ".gif"]:
                    suffix = suffix_
            name = make_md5(url) + suffix
            path = os.path.join(img_path, name)
            if not os.path.exists(path):
                with open(path, "wb") as fp:
                    fp.write(response.content)
            return name

        if not os.path.exists(img_path):
            os.makedirs(img_path)

        md_img_re = re.compile(r"!\[\]\((http.*?)\)")
        imgs = set(md_img_re.findall(text))
        print("共需转换%d张图片" % len(imgs))
        print(imgs)
        url_names = [(url, download_img(url)) for url in imgs]
        for url, name in url_names:
            text = text.replace(url, "assets/" + name)
        return text

    def out_tag_text_recursive(self, tag, sep="", strip=True):
        """格式化输出ele内的文本，会格式化br、p、div等添加\n"""
        line_append = self.line_append
        if isinstance(tag, NavigableString):
            return tag.strip() if strip else tag.string
        if tag.name == "ul" or tag.name == "ol":
            return self.out_ul_text(tag)
        if tag.name == "code":
            return self.out_code_text(tag)
        if tag.name == "pre":
            return self.out_pre_text(tag)

        texts = []
        pre_sibling = None
        for child in tag.contents:
            if pre_sibling is not None and pre_sibling.name in ("br", "p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
                # 最多连续加三个\n
                if "".join(texts[-4:]).endswith("\n\n") and (line_append == "\n\n" or line_append == "\n"):
                    if not "".join(texts[-4:]).endswith("\n\n\n"):
                        texts.append("\n")
                else:
                    texts.append(line_append)
            elif child.name in ("p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
                # 最多连续加三个\n
                if "".join(texts[-4:]).endswith("\n\n") and (line_append == "\n\n" or line_append == "\n"):
                    if not "".join(texts[-4:]).endswith("\n\n\n"):
                        texts.append("\n")
                else:
                    texts.append(line_append)
            pre_sibling = child
            if child.name == "script" or child.name == "style":
                continue
            if isinstance(child, Tag):
                texts.append(self.out_tag_text_recursive(child))
            elif type(child) == NavigableString:
                # NavigableString是str的子类
                texts.append(child.strip() if strip else child.string)
        return sep.join(texts)

    def out_ul_text(self, tag):
        lis = tag.select("> li")
        return "    \n".join(["* " + li.get_text(strip=True) for li in lis])

    def out_code_text(self, tag):
        code = tag.get_text()
        return "`%s`" % (code)

    def out_pre_text(self, tag):
        text = tag.get_text()
        return "```%s\n%s\n```" % (self.default_pre_lang, text)


def ud_convert(tag):
    for h3 in tag.findAll("h3"):
        h3.name = "p"


def ud_convert2(tag):
    for h3 in tag.findAll("h3"):
        h3.name = "p"
        h3.string = "**%s**" % h3.string.strip()


if __name__ == '__main__':
    txt = """aa"""
    with open("txt", encoding="utf-8") as fp:
        txt = fp.read()
    convert = TencentCloudHtmlMdConvert(first_mdtitle_prefix="##", default_pre_lang="scala")
    txt = convert.html_to_markdown(txt, True, r"assets", ud_convert=None)
    print(txt)

```

### 获取某个作者的所有文章并筛选
获取某个作者某种类型的文章。使用js，在浏览器的控制台中测试。

```js
var datas = [];
for(var i=1; i<=4; i++){
    $.ajax({url:"https://cloud.tencent.com/developer/services/ajax/column/article?action=FetchColumnArticles", 
        method:'POST',
        contentType:'application/json;charset=utf-8',
        data : '{"action": "FetchColumnArticles", "payload": {"columnId": 6110, "tagId": 0, "pageNumber": '+i+', "pageSize": 50}}',
        success : function(data) {
            datas.push(data);
        }
    })
}

list = datas.flatMap(x => x.data.list)

list.filter(x => x.title.toLowerCase().indexOf("spark") != -1)

list.filter(x => x.title.toLowerCase().indexOf("spark") != -1).map(x => x.articleId+", "+ x.title)

["1336623, Spark History Server配置", "1336620, Spark性能调优02-代码调优", "1336614, Spark性能调优06-JVM调优", "1336602, Spark性能调优05-Shuffle调优", "1336581, SparkStreaming 写数据到 HBase，由于共用连接造成的数据丢失问题", "1336562, spark读写HBase之使用hortonworks的开源框架shc（一）：源码编译以及测试工程创建", "1336561, Spark读写HBase之使用Spark自带的API以及使用Bulk Load将大量数据导入HBase", "1336560, spark读写HBase之使用hortonworks的开源框架shc（二）：入门案例", "1426273, Spark on Yarn资源配置", "1336641, Spark伪分布式集群搭建", "1336640, Spark完全分布式集群搭建", "1336636, Spark常用Transformations算子(一)", "1336634, Spark HA集群搭建", "1336632, Spark-RDD持久化", "1336631, Spark性能调优03-数据本地化调优", "1336628, Spark性能调优01-资源调优", "1336627, Spark常用Transformations算子(二)", "1336626, Spark常用Actions算子", "1336625, Spark性能调优04-数据倾斜调优"]


list.filter(x => x.title.toLowerCase().indexOf("spark性能调优") != -1).map(x => x.articleId+", "+ x.title)
["1336620, Spark性能调优02-代码调优", "1336614, Spark性能调优06-JVM调优", "1336602, Spark性能调优05-Shuffle调优", 
"1336631, Spark性能调优03-数据本地化调优", "1336628, Spark性能调优01-资源调优", "1336625, Spark性能调优04-数据倾斜调优"]

//-----------------------------------------------------------------------------------------------

var datas = [];
for(var i=1; i<=5; i++){
    $.ajax({url:"https://cloud.tencent.com/developer/services/ajax/column/article?action=FetchColumnArticles", 
        method:'POST',
        contentType:'application/json;charset=utf-8',
        data : '{"action": "FetchColumnArticles", "payload": {"columnId": 1494, "tagId": 0, "pageNumber": '+i+', "pageSize": 50}}',
        success : function(data) {
            datas.push(data);
        }
    })
}

list = datas.flatMap(x => x.data.list)

list.filter(x => x.title.toLowerCase().indexOf("数据仓库") != -1).sort((a,b) => a.articleId - b.articleId)

list.filter(x => x.title.toLowerCase().indexOf("数据仓库") != -1).sort((a,b) => a.articleId - b.articleId).map(x => x.articleId+", "+ x.title)

["1136023, 数据仓库中的模型设计", "1136050, 漫谈大数据和数据仓库", "1136065, 数据仓库概念总结", "1136125, 技术资源推荐（数据仓库篇）", 
"1396888, 漫谈数据仓库和范式", "1396891, 一种通用的数据仓库分层方法", "1396893, 数据仓库实践之业务数据矩阵的设计", "1396898, 数据仓库表的标准和规范关注点", 
"1396915, 数据仓库的一些建议", "1396917, 聊一聊数据仓库的 KPI 怎么定", "1401625, 闲聊数据库和数据仓库的区别", "1498060, 数据百问系列：关于数据仓库，什么样的产品是好的Partener？", 
"1512004, 辨析BI、数据仓库、数据湖和数据中台内涵及差异点(建议收藏)", "1536019, 小尝试：基于指标体系的数据仓库搭建和数据可视化", "1538942, 小案例：数据仓库搭建中的流量日志维度表案例", 
"1551875, 数据仓库系列：如何优雅地规划数仓体系", "1586605, 戴着枷锁跳舞：漫谈重构数据仓库的辛酸", "1594250, 【实践案例分享】58全站用户行为数据仓库建设及实践", "1607476, 推荐数据仓库的必读书", 
"1618075, 数据百问系列：数据库和数据仓库的区别是什么？"]
```

## 博客园文章转换
这个代码有很多多余的，这是在知乎的基础上直接改的，很多无用的解析未删除。

cnblogs_html2md_usebs.py：
```python
# coding:utf-8
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Comment
import re
import os
import requests
from urllib.parse import unquote
import hashlib


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}


def make_md5(raw):
    """计算出一个字符串的MD5值"""
    md5 = hashlib.md5()
    md5.update(raw.encode())
    return md5.hexdigest()


def out_ele_text_recursive(ele, sep="", strip=True):
    """格式化输出ele内的文本，会格式化br、p、div等添加\n"""
    if isinstance(ele, NavigableString):
        return ele.strip() if strip else ele.string
    texts = []
    pre_sibling = None
    for child in ele.contents:
        if pre_sibling is not None and pre_sibling.name in ("br", "p", "div"):
            texts.append("\n")
        pre_sibling = child
        if child.name == "script" or child.name == "style":
            continue
        if isinstance(child, Tag):
            texts.append(out_ele_text_recursive(child))
        elif type(child) == NavigableString:
            # NavigableString是str的子类
            texts.append(child.strip() if strip else child.string)
    return sep.join(texts)


class CnblogsHtmlMdConvert():
    def __init__(self, line_append="\n\n", first_mdtitle_prefix="##", default_pre_lang="xml"):
        self.line_append = line_append
        self.first_mdtitle_prefix = first_mdtitle_prefix
        self.default_pre_lang = default_pre_lang

    def convert_link(self, tag):
        """原地转换超链接为Markdown格式"""
        prefix = "https://link.zhihu.com/?target="
        for link in tag.findAll("a"):
            link_url, link_text = link.get("href", default=""), link.get_text(strip=True)
            if prefix in link_url:
                link_url = link_url[len(prefix):]
            md_link = """[{1}]({0} "{1}")""".format(unquote(link_url), link_text)
            link.replace_with(md_link)

    def convert_figure(self, tag):
        """转换知乎页面中的figure标签"""
        for figure in tag.findAll("figure"):
            figcaption = figure.find("figcaption")  # 图片的注释元素
            img = figure.select_one("> img")
            if img is None:
                img = figure.select_one("img")
            note = figcaption.string if figcaption else ""
            img_url = img.get("src", "") if img else ""
            replace_tag = Tag(name="p")
            if note:
                md_img = "![]({0})\n`{1}`".format(img_url, note)
            else:
                md_img = "![]({0})".format(img_url)
            replace_tag.string = md_img
            figure.replace_with(replace_tag)

    def convert_img(self, tag):
        for img in tag.findAll("img"):
            img_url = img.get("src", "")
            md_img = " ![]({0}) ".format(img_url)
            img.replace_with(md_img)

    def convert_math_expression(self, tag):
        """转换知乎页面中的数学公式"""
        prefix = "https://www.zhihu.com/equation?tex="
        for img in tag.findAll("img", src=re.compile(r"^https://www.zhihu.com/equation\?tex=")):
            math = img.get("src", "")[len(prefix):]
            math = unquote(math.replace("+", "%20"))
            math_md = "$$%s$$" % math if r"\tag" in math else "$%s$" % math
            if r"\begin" in math_md or r"\end" in math_md:
                begin_re = re.compile(r"\\begin\s*\{[^\{\}]*?\}")
                end_re = re.compile(r"\\end\s*\{[^\{\}]*?\}")
                math_md = begin_re.sub("", math_md)
                math_md = end_re.sub("", math_md)
                math_md = math_md.replace(r"&=", "=").replace("& =", "=").replace(r"&\approx", r"\approx").replace(
                    r"& \cdots", r"\cdots").replace(r"& \leq", r" \leq").replace(r"& & \geq", r" & \geq")
                if not math_md.startswith("$$"):
                    math_md = "$%s$" % math_md

            img.replace_with(math_md)

    def convert_btag(self, tag):
        for b in tag.findAll(["b", "strong"]):
            str_tags = list(filter(lambda e: type(e) == NavigableString and e.strip(), b.contents[::-1]))
            str_last = str_tags[0] if str_tags else None
            b.insert_before("**")
            if str_last and str_last.strip()[-1] in ["，", ",", ";", "；", "。", "！"]:
                str_last.replace_with(str_last.strip()[:-1] + "**" + str_last.strip()[-1])
            else:
                b.insert_after("**")

    def convert_htag(self, tag):
        title_prefix = self.first_mdtitle_prefix
        h_tags = tag.findAll(re.compile(r"^h\d$"))
        h_names = {h_tag.name: int(h_tag.name[1:]) for h_tag in h_tags}
        for index, (h_name, _) in enumerate(sorted(h_names.items(), key=lambda x: x[1]), start=0):
            h_names[h_name] = index
        # 没有h标签，转换<p><b>一、</b></p>等
        if len(h_tags) == 0:
            title_re = re.compile(r"^[\d一二三四五六七八]")
            h_tags = tag.findAll(lambda ele: ele.name == "p" and ele.find("b") and title_re.match(
                ele.get_text(strip=True)) and ele.get_text(strip=True) == ele.find("b").get_text(strip=True))
        for h_tag in h_tags:
            if h_tag.get_text(strip=True) == "":
                continue
            # 看源码相当于jquery的text()
            h_tag.string = title_prefix + "#" * h_names.get(h_tag.name, 0) + " " + h_tag.get_text(strip=True)

    def html_to_markdown(self, html, use_local_img_replace_net=False, img_path=None, ud_convert=None):
        if use_local_img_replace_net and img_path is None:
            raise Exception("必须设置img_path")

        soup = BeautifulSoup(html, "lxml")
        content_div = soup.select_one("div#cnblogs_post_body")
        if ud_convert is not None:
            ud_convert(content_div)
        self.convert_math_expression(content_div)  # 这个必须在img转换之前
        self.convert_figure(content_div)
        self.convert_link(content_div)  # a在img之前，img可能在a中
        self.convert_img(content_div)
        self.convert_htag(content_div)  # 这个必须在b转换之前,h标签中可能有b标签
        self.convert_btag(content_div)

        text = self.out_tag_text_recursive(content_div)
        if use_local_img_replace_net:
            text = self.markdown_use_local_img(text, img_path)
        return text

    def markdown_use_local_img(self, text, img_path):
        """将md文件中的http形式的img下载到本地并替换"""
        def download_img(url):
            """下载图片并返回文件名"""
            response = requests.get(url, headers=headers)
            suffix = ".png"
            if url.rfind(".") > 0:
                suffix_ = url[url.rfind("."):]
                if suffix_ in [".jpg", ".png", ".gif"]:
                    suffix = suffix_
            name = make_md5(url) + suffix
            path = os.path.join(img_path, name)
            if not os.path.exists(path):
                with open(path, "wb") as fp:
                    fp.write(response.content)
            return name

        if not os.path.exists(img_path):
            os.makedirs(img_path)

        md_img_re = re.compile(r"!\[\]\((http.*?)\)")
        imgs = set(md_img_re.findall(text))
        print("共需转换%d张图片" % len(imgs))
        print(imgs)
        url_names = [(url, download_img(url)) for url in imgs]
        for url, name in url_names:
            text = text.replace(url, "assets/" + name)
        return text

    def out_tag_text_recursive(self, tag, sep="", strip=True):
        """格式化输出ele内的文本，会格式化br、p、div等添加\n"""
        line_append = self.line_append
        if isinstance(tag, NavigableString):
            return tag.strip() if strip else tag.string
        if tag.name == "ul" or tag.name == "ol":
            return self.out_ul_text(tag)
        if tag.name == "code":
            return self.out_code_text(tag)
        if tag.name == "pre":
            return self.out_pre_text(tag)

        texts = []
        pre_sibling = None
        for child in tag.contents:
            if pre_sibling is not None and pre_sibling.name in ("br", "p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
                # 最多连续加三个\n
                if "".join(texts[-4:]).endswith("\n\n") and (line_append == "\n\n" or line_append == "\n"):
                    if not "".join(texts[-4:]).endswith("\n\n\n"):
                        texts.append("\n")
                else:
                    texts.append(line_append)
            elif child.name in ("p", "div", "ul", "ol", "h1", "h2", "h3", "h4", "h5"):
                # 最多连续加三个\n
                if "".join(texts[-4:]).endswith("\n\n") and (line_append == "\n\n" or line_append == "\n"):
                    if not "".join(texts[-4:]).endswith("\n\n\n"):
                        texts.append("\n")
                else:
                    texts.append(line_append)
            pre_sibling = child
            if child.name == "script" or child.name == "style":
                continue
            if isinstance(child, Tag):
                texts.append(self.out_tag_text_recursive(child))
            elif type(child) == NavigableString:
                # NavigableString是str的子类
                texts.append(child.strip() if strip else child.string)
        return sep.join(texts)

    def out_ul_text(self, tag):
        lis = tag.select("> li")
        return "    \n".join(["* " + li.get_text(strip=True) for li in lis])

    def out_code_text(self, tag):
        code = tag.get_text()
        return "`%s`" % (code)

    def out_pre_text(self, tag):
        text = tag.get_text()
        return "```%s\n%s\n```" % (self.default_pre_lang, text)


def ud_convert(tag):
    for h3 in tag.findAll("h3"):
        h3.name = "p"


def ud_convert2(tag):
    for h3 in tag.findAll("h3"):
        h3.name = "p"
        h3.string = "**%s**" % h3.string.strip()


if __name__ == '__main__':
    txt = """aa"""
    with open("txt", encoding="utf-8") as fp:
        txt = fp.read()
    convert = CnblogsHtmlMdConvert(first_mdtitle_prefix="##", default_pre_lang="sql")
    txt = convert.html_to_markdown(txt, True, r"assets", ud_convert=None)
    print(txt)

```




```python

```


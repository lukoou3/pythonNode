## FFmpeg
FFmpeg是用于操作视频与音频的库，用处很多

## FFmpeg安装
1：下载
转到 http://ffmpeg.zeranoe.com/builds/ 并下载32或64位静态版本（取决于您的系统）。

2：解压缩

3：添加到环境变量
最后，我们需要将包含ffmpeg.exe文件的bin文件夹  添加到我们的系统路径中，以便我们轻松地运行命令。

## FFmpeg命令
下面只是一些我用过的命令

### 合并视频
先创建一个文本文件filelist.txt，然后输出以下内容：
```
file 'input1.mkv'
file 'input2.mkv'
file 'input3.mkv'
```
然后：
```
ffmpeg -f concat -i filelist.txt -c copy output.mkv
```

例子：
```python
def down_m3u8(requests_session,text,name,path="./"):
    urls = [line.strip() for line in text.split("\n") if '.ts' in line]
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(down_videos_for_concat(urls,name,requests_session))
    loop.close()

    cache_files = ["{}_{}".format(name, i) for i, url in enumerate(urls, start=100)]
    with open("{}_list".format(name), "w", encoding="utf-8") as fp:
        for cache_file in cache_files:
            fp.write("file '{}'\n".format(cache_file))
    subprocess.call(
        ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', "{}_list".format(name), '-c', 'copy', name + ".ts"]
    )
    for cache_file in cache_files:
        os.remove(cache_file)
    os.remove("{}_list".format(name))
```

### 剪切视频
使用streamlink下载直播视频并从中剪切视频例子：
```
#使用streamlink下载直播视频
streamlink https://www.panda.tv/312911 best -o zhou.mp4

#剪切视频
ffmpeg -i zhou.mp4 -ss 03:14:50 -to 04:41:50 -acodec copy -vcodec copy 002.mp4
ffmpeg -i zhou.mp4 -ss 04:41:50 -to 06:10:20 -acodec copy -vcodec copy 002.mp4
ffmpeg -i zhou.mp4 -ss 06:10:36 -to 07:41:38 -acodec copy -vcodec copy 家有喜事.mp4
ffmpeg -i zhou.mp4 -ss 07:41:43 -to 09:20:06 -acodec copy -vcodec copy 武状元苏乞儿.mp4
ffmpeg -i 001.mp4 -ss 01:43:03 -to 03:14:44 -acodec copy -vcodec copy 情圣.mp4
ffmpeg -i 001.mp4 -ss 00:09:55 -to 01:42:50 -acodec copy -vcodec copy 无敌幸运星.mp4

```


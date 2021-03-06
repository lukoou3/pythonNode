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

### 提取音频
参考网站：`https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg`


```
ffmpeg -i 飞花令第二季.mp4 -vn -acodec copy 飞花令第二季.m4a

# 不要前面的一段
ffmpeg -i 飞花令第二季.mp4 -ss 00:00:18 -vn -acodec copy 飞花令第二季.m4a
ffmpeg -i 飞花令第三季.mp4 -ss 00:00:16 -vn -acodec copy 飞花令第三季.m4a

ffmpeg -i 飞花令第二季.mp4 -ss 00:00:18 -q:a 0 -map a 飞花令第二季.mp3
ffmpeg -i 飞花令第三季.mp4 -ss 00:00:16 -q:a 0 -map a 飞花令第三季.mp3
```

To extract the audio stream without re-encoding:
```
ffmpeg -i input-video.avi -vn -acodec copy output-audio.aac
```
* -vn is no video.  
* -acodec copy says use the same audio stream that's already in there.

Read the output to see what codec it is, to set the right filename extension.


To encode a high quality MP3 from an AVI best use -q:a for variable bit rate:
```
ffmpeg -i sample.avi -q:a 0 -map a sample.mp3
```

If you want to extract a portion of audio from a video use the -ss option to specify the starting timestamp, and the -t option to specify the encoding duration, eg from 3 minutes and 5 seconds in for 45 seconds:
```
ffmpeg -i sample.avi -ss 00:03:05 -t 00:00:45.0 -q:a 0 -map a sample.mp3
```
* The timestamps need to be in HH:MM:SS.xxx format or in seconds.  
* If you don't specify the -t option it will go to the end.

### 合并音频
之前的提取的音频中中间有一部分不需要，需要合并一下：

```
# 提取第一段需要的音频
ffmpeg -i 飞花令第二季.mp3 -ss 00:00:00 -to 00:24:54 -vn -acodec copy 001.mp3
# 提取第二段需要的音频
ffmpeg -i 飞花令第二季.mp3 -ss 00:27:52 -vn -acodec copy 002.mp3

# 合并音频
ffmpeg -i "concat:001.mp3|002.mp3" -c copy 005.mp3
```

### 直接提取MP3不成功
不知道怎么回事，下载的一些avi格式的视频提取MP3不成功，但是可以提取数wav格式的。

查到可以从wav转MP3
```
ffmpeg -i 01_linux_hadoop_zk.avi -vn -acodec copy 01_linux_hadoop_zk.wav 
ffmpeg -i 01_linux_hadoop_zk.wav -acodec libmp3lame 01_linux_hadoop_zk.mp3
```

这个可以一步完成：
```
ffmpeg -i 02_hive.avi -vn -acodec libmp3lame 02_hive.mp3
ffmpeg -i 03_flume.avi -vn -acodec libmp3lame 03_flume.mp3
ffmpeg -i 04_kafka.avi -vn -acodec libmp3lame 04_kafka.mp3
ffmpeg -i 05_1.avi -vn -acodec libmp3lame 05_1.mp3
ffmpeg -i 05_2.avi -vn -acodec libmp3lame 05_2.mp3
ffmpeg -i "concat:05_1.mp3|05_2.mp3" -c copy 05.mp3
ffmpeg -i 06_项目架构.avi -vn -acodec libmp3lame 06_项目架构.mp3
ffmpeg -i 07_数仓项目总结.avi -vn -acodec libmp3lame 07_数仓项目总结.mp3
ffmpeg -i 08_spark面试题讲解.wmv -vn -acodec libmp3lame 08_spark面试题讲解.mp3
ffmpeg -i 09_数仓项目.avi -vn -acodec libmp3lame 09_数仓项目.mp3
ffmpeg -i 10_项目中遇到问题.avi -vn -acodec libmp3lame 10_项目中遇到问题.mp3
ffmpeg -i 11_项目经验1.avi -vn -acodec libmp3lame 11_项目经验1.mp3
ffmpeg -i 12_项目经验2.avi -vn -acodec libmp3lame 12_项目经验2.mp3
ffmpeg -i 13_项目讲解.avi -vn -acodec libmp3lame 13_项目讲解.mp3
```


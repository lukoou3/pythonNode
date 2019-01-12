# coding=utf-8
import os
import sys
import math
import asyncio
import aiohttp
import aiofiles
import progressbar
from aiohttp import web
from threading import Thread

try:
    basepath = sys._MEIPASS
except:
    basepath = "./"
routes = web.RouteTableDef()

@routes.get('/')
async def start(request):
    async with aiofiles.open(os.path.join(basepath, "page/index.html"), 'r', encoding="utf-8") as f:
        text = await f.read()
    return web.Response(text=text, content_type="text/html")

@routes.post('/download')
async def download(request):
    params = await request.post()
    try:
        imgxy = [float(params["minX"]), float(params["minY"]),
                 float(params["maxX"]), float(params["maxY"])]
    except Exception as e:
        return web.json_response({'error': '500'}, status=404)
    imgxyArray = getImgxyArray(imgxy)
    imgxyArray[:10] = getImgxyArray([8182944.69, 2039050.5, 15039759.58, 7054488.21])[:10]
    #imgxyArray[10:15] = getImgxyArray([12849821.11, 4758749.11, 13082407.79, 4993886.96])[10:15]
    # imgxyArray[15:] = getImgxyArray([12849821.11, 4758749.11, 13082407.79, 4993886.96])[15:]
    if not downloadImgCondition["downloading"]:
        Thread(target=downloadImgs, args=(imgxyArray, "D:\map\dacMapImg2")).start()
    return web.Response(text="")

def getImgxyArray(imgxy):
    imgxyArray = list()
    for zoomLevel in range(1, 19):
        imgxyArray.append([math.floor(xy / (2 ** (18 - zoomLevel) * 256)) for xy in imgxy])
    return imgxyArray

downloadImgCondition = {"downloading": False}
mapfeature = "20181120&scale=1&ak=8d6c8b8f3749aed6b1aff3aad6f40e37&styles=t%3Awater%7Ce%3Aall%7Cc%3A%230d0d88ff%2Ct%3Aland%7Ce%3Aall%7Cc%3A%23011843ff%2Ct%3Aboundary%7Ce%3Ag%7Cc%3A%23064f85%2Ct%3Amanmade%7Ce%3Aall%7Cv%3Aoff%2Ct%3Aboundary%7Ce%3Ag.f%7Cc%3A%23029fd4%2Ct%3Abuilding%7Ce%3Aall%7Cc%3A%231a5787ff%2Ct%3Alabel%7Ce%3Al.t.f%7Cv%3Aon%7Cc%3A%23000000ff%2Ct%3Apoi%7Ce%3Al.t.s%7Cc%3A%231e1c1c%2Ct%3Ahighway%7Ce%3Aall%7Cc%3A%230b5394ff%2Ct%3Agreen%7Ce%3Aall%7Cc%3A%23274e13ff%2Ct%3Aarterial%7Ce%3Ag%7Cc%3A%23444444ff%2Ct%3Arailway%7Ce%3Al.t.f%7Cc%3A%23ffffffff%2Ct%3Asubway%7Ce%3Al.t.f%7Cc%3A%23ff00ffff%7Cs%3A61%2Ct%3Alocal%7Ce%3Ag%7Cc%3A%234f4848ff%2Ct%3Asubway%7Ce%3Al.i%7Cc%3A%23000000ff%2Ct%3Arailway%7Ce%3Aall%7Cv%3Aoff%2Ct%3Apoi%7Ce%3Al.t.f%7Cc%3A%23ffffffff%2Ct%3Aroad%7Ce%3Al.t.f%7Cc%3A%2338761dff%7Cl%3A80%7Cs%3A61%2Ct%3Aroad%7Ce%3Al.t.s%7Cl%3A-57%7Cs%3A-72%2Ct%3Acity%7Ce%3Al.t.f%7Cc%3A%23ffffffff%7Cl%3A-82%7Cs%3A61%7Ch%3A%23000000%2Ct%3Acity%7Ce%3Al.t.s%7Cc%3A%23ffffffff"
baseurls = ["http://api0.map.bdimg.com/customimage/tile?", "http://api1.map.bdimg.com/customimage/tile?",
            "http://api2.map.bdimg.com/customimage/tile?"]

def downloadImgs(imgxylist, basepath="/home/lifengchao/map/北京东城区/dacMapImg", mapfeature=mapfeature):
    async def download_one(semaphore, session, x, y, z):
        path = os.path.join(basepath, str(z), str(x))
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, "{}.jpg".format(z))
        if os.path.exists(path):  # 图片已存在,如果链接对应的图片已存在，则忽略下载
            return {'ignored': True  # 用于告知download_one()的调用方，此图片被忽略下载
            }
        return {'ignored': True  # 用于告知download_one()的调用方，此图片被忽略下载
                }

        url = "{}&x={}&y={}&z={}&udt={}".format(baseurls[(x + y) % 3], x, y, z, mapfeature)
        try:
            async with semaphore:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_content = await response.read()  # Binary Response Content: access the response body as bytes, for non-text requests
                    else:
                        raise aiohttp.ClientError()
        except Exception as e:
            return {
                'failed': True  # 用于告知download_one()的调用方，请求此图片URL时失败了
            }

        async with aiofiles.open(path, 'wb') as f:
            await f.write(image_content)
        return {
            'failed': False  # 用于告知download_one()的调用方，此图片被成功下载
        }

    async def download_many(imgxylist):
        async def download_buffer():
            nonlocal ignored_images,failed_images,visited_images
            to_do_iter = asyncio.as_completed(do_list)
            for i, future in enumerate(to_do_iter):
                result = await future
                if result.get('ignored'):
                    ignored_images += 1
                else:
                    if result.get('failed'):
                        failed_images += 1
                    else:
                        visited_images += 1
                bar.update(count - 100000 + i)
            do_list.clear()

        async with aiohttp.ClientSession() as session:  # aiohttp建议整个应用只创建一个session，不能为每个请求创建一个seesion
            semaphore = asyncio.Semaphore(900)  # 用于限制并发请求数量
            length = 0
            for  imgxy in imgxylist:
                length += (imgxy[2] + 1 - imgxy[0])*(imgxy[3] + 1 - imgxy[1])
            to_do = (download_one(semaphore, session, j, k, zoom)
                     for zoom, imgxy in enumerate(imgxylist, start=1) if zoom > -1 for j in
                     range(imgxy[0], imgxy[2] + 1) for k in range(imgxy[1], imgxy[3] + 1))

            find_images = length  # 发现的总图片链接数
            ignored_images = 0  # 被忽略的图片数
            visited_images = 0  # 请求成功的图片数
            failed_images = 0  # 请求失败的图片数

            with progressbar.ProgressBar(max_value=find_images) as bar:
                count = 0
                do_list = []
                for do in to_do:
                    count += 1
                    do_list.append(do)
                    if(count %100000 == 0):
                        await download_buffer()
                if do_list:
                    await download_buffer()

        print('Find [{}] images, ignored [{}] images, visited [{}] images, failed [{}] images'.format(
            find_images, ignored_images, visited_images, failed_images))

    if downloadImgCondition["downloading"]:
        return
    downloadImgCondition["downloading"] = True
    if sys.platform != 'win32':
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)  # syncio程序中的每个线程都有自己的事件循环，但它只会在主线程中为你自动创建一个事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_many(imgxylist))
    loop.close()
    downloadImgCondition["downloading"] = False

if __name__ == "__main__":
    app = web.Application()
    routes.static('/js', os.path.join(basepath, "page/js"))
    app.add_routes(routes)
    web.run_app(app,port=8000)
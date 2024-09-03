#!/usr/bin/env python
# coding: utf-8
import requests
import re

# 根据url获取网页html内容
def getHtmlContent(url):
    page = requests.get(url)
    return page.text
# 从html中解析出所有jpg图片的url
# 百度贴吧html中jpg图片的url格式为：<img ... src="XXX.jpg" width=...>
def getJPGs(html):
    # 解析jpg图片url的正则
    # jpgReg = re.compile(r'<img.+?src="(.+?\.jpg)" width')
    # jpgReg = re.compile(r'<img.+?height.+?src="(.+?\.jpg)"')
    jpgReg = re.compile(r'<img.+?src="(.+?\.jpg)" .+?width')
    # 注：这里最后加一个'width'是为了提高匹配精确度
    # 解析出jpg的url列表
    jpgs = re.findall(jpgReg,html)
    print(jpgs)
    return jpgs

# 用图片url下载图片并保存成制定文件名
def downloadJPG(imgUrl,fileName):
    # 可自动关闭请求和响应的模块
    from contextlib import closing
    with closing(requests.get(imgUrl,stream = True)) as resp:
        with open(fileName,'wb') as f:
            for chunk in resp.iter_content(128):
                f.write(chunk)
# 批量下载图片，默认保存到当前目录下
import os
def batchDownloadJPGs(imgUrls,path = './'):
    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists(path):
        os.makedirs(path)
        print('创建新的文件夹')
    # 用于给图片命名
    count = 1
    for url in imgUrls:
        downloadJPG(url,''.join([path,'{0}.jpg'.format(count)]))
        print('下载完成第{0}张图片'.format(count))
        count = count + 1

# 封装：从百度贴吧网页下载图片
def download(url):
    html = getHtmlContent(url)
    jpgs = getJPGs(html)
    batchDownloadJPGs(jpgs)

def main():

    # url = 'http://tieba.baidu.com/p/2256306796'
    # url = 'https://tieba.baidu.com/p/2256306796?pn=3'
    # url = 'http://tieba.baidu.com/p/6291530603'   #改变网址，查看网页源代码中需要爬取的图片链接特点，来设置【正则表达式】
    url = 'https://tieba.baidu.com/p/6244370068?png=4'
    download(url)

if __name__ == '__main__':
    main()







import cv2 as cv
import sys
import numpy as np
import signal, os, subprocess
import requests
# 下载网络视频到本地

urlPath = "https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1557886955xa/1557886955xa_1559297690876.mp4"

print('准备下载视频:')
cap1 = requests.get(urlPath) #获取该地址下的内容
cap1Data = cap1.content #读取文件字节
if cap1Data:
    file_path='{}'.format(os.getcwd()+"/inter2.mp4") #在当前路径给视频命名
    print('文件为:'+file_path)
    # if not os.path.exists(file_path):
    with open(file_path,'wb') as f: #打开文件,并定义权限为"读写"
        f.write(cap1Data) #将视频字节写入文件
        f.close() #关闭文件
        print("视频下载完毕")

# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import os
import requests
import time


def muti_imgs():
    global imgurl1, imgurl2, imgurl3, imgurl4, imgurl5, imgurl6
    global imgPath1, imgPath2, imgPath3, imgPath4, imgPath5, imgPath6
    global ewmurl1, ewmurl2, ewmurl3, ewmurl4, ewmurl5, ewmurl6
    global ewmPath1, ewmPath2, ewmPath3, ewmPath4, ewmPath5, ewmPath6
    global img1, img2, img3, img4, img5, img6
    global ewm1, ewm2, ewm3, ewm4, ewm5, ewm6
    # 图片地址:
    imgurl1 = "https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1558607850so/1558607850so_1559727629962.jpg"
    imgurl2 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/1558607850so_1559728496083_0_4278649B321E_0.jpg"
    imgurl3 = "https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1558607850so/1558607850so_1559730997445.jpg"
    imgurl4 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/1558607850so_1559731467391_0_4278649B321E_0.jpg"
    imgurl5 = "https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1558607850so/1558607850so_1559726753085.jpg"
    imgurl6 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/1558607850so_1559730729580_0_4278649B321E_0.jpg"
    # 获取图片
    imgPath1 = requests.get(imgurl1)
    imgPath2 = requests.get(imgurl2)
    imgPath3 = requests.get(imgurl3)
    imgPath4 = requests.get(imgurl4)
    imgPath5 = requests.get(imgurl5)
    imgPath6 = requests.get(imgurl6)
    # 二维码地址
    ewmurl1 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png"
    ewmurl2 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png"
    ewmurl3 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png"
    ewmurl4 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png"
    ewmurl5 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png"
    ewmurl6 = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png"
    # 获取二维码
    ewmPath1 = requests.get(ewmurl1)
    ewmPath2 = requests.get(ewmurl2)
    ewmPath3 = requests.get(ewmurl3)
    ewmPath4 = requests.get(ewmurl4)
    ewmPath5 = requests.get(ewmurl5)
    ewmPath6 = requests.get(ewmurl6)
    # 所有图片,解码成图片矩阵
    img1 = cv.imdecode(np.fromstring(imgPath1.content, np.uint8), 1)  # ewmPath1.content 是读取的远程文件的字节流
    img2 = cv.imdecode(np.fromstring(imgPath2.content, np.uint8), 1)
    img3 = cv.imdecode(np.fromstring(imgPath3.content, np.uint8), 1)
    img4 = cv.imdecode(np.fromstring(imgPath4.content, np.uint8), 1)
    img5 = cv.imdecode(np.fromstring(imgPath5.content, np.uint8), 1)
    img6 = cv.imdecode(np.fromstring(imgPath6.content, np.uint8), 1)
    ewm1 = cv.imdecode(np.fromstring(ewmPath1.content, np.uint8), 1)  # ewmPath1.content 是读取的远程文件的字节流
    ewm2 = cv.imdecode(np.fromstring(ewmPath2.content, np.uint8), 1)
    ewm3 = cv.imdecode(np.fromstring(ewmPath3.content, np.uint8), 1)
    ewm4 = cv.imdecode(np.fromstring(ewmPath4.content, np.uint8), 1)
    ewm5 = cv.imdecode(np.fromstring(ewmPath5.content, np.uint8), 1)
    ewm6 = cv.imdecode(np.fromstring(ewmPath6.content, np.uint8), 1)
muti_imgs()
# 全屏窗口,这样就可以自适应图片大小
cv.namedWindow('imgWindow', cv.WINDOW_NORMAL)  # 获取窗口名字
cv.resizeWindow('imgWindow', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)  # 画面全屏
cv.setWindowProperty('imgWindow', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)  # 窗口全屏

# print(img1.shape)
imgWidth = img1.shape[1] # 获取图片宽
imgHeight = img1.shape[0] # 获取图片高
# 二维码在图片上的四个点位置
ewmW1 = imgWidth - 530
ewmW2 = imgWidth - 100
ewmH1 = imgHeight - 530
ewmH2 = imgHeight - 100
while True:
    # 分别给所有图片加上二维码
    img1[ewmH1:ewmH2, ewmW1:ewmW2] = ewm1
    img2[ewmH1:ewmH2, ewmW1:ewmW2] = ewm2
    img3[ewmH1:ewmH2, ewmW1:ewmW2] = ewm3
    img4[ewmH1:ewmH2, ewmW1:ewmW2] = ewm4
    img5[ewmH1:ewmH2, ewmW1:ewmW2] = ewm5
    img6[ewmH1:ewmH2, ewmW1:ewmW2] = ewm6
    # 水平叠加
    imgs_1 = np.hstack([img1, img2, img3])
    imgs_2 = np.hstack([img4, img5, img6])
    # 创建中白条,用于写字
    noneCen = np.ones(shape = (500, 8640, 3))
    noneCen = np.uint8(noneCen * 255) #把类型转为与图片一致的unit8类型
    # 垂直叠加
    imgs = np.vstack((imgs_1, noneCen, imgs_2)) #目前H = 4820, W = 8640
    # 写字
    strTxt = "我是please tell me"
    strTxt.encode('utf-8').decode("unicode_escape")
    cv.putText(imgs, str(strTxt), (500, 2660), cv.FONT_HERSHEY_SIMPLEX, 100, (0, 0, 0), 10)
    cv.imshow("imgWindow", imgs)
    if cv.waitKey(10000) & 0xFF == ord('q'):
        break
    # 一定时间后,再次刷新图片
    print("刷新了!!!")
    muti_imgs()
cv.destroyAllWindows()
# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import os, subprocess
import requests
import time
import json
import _thread
from PIL import Image, ImageDraw, ImageFont

# 播放背景音乐
def playMusic():
    global mPlay
    mPlay = subprocess.Popen(["python", "backMusic.py", "music.mp3"])
playMusic()

# 获取图片和二维码
def muti_imgs():
    # 用数组把每组图片装起来
    global imgList, ewmList
    imgList = []
    ewmList = []
    try:
        allImg = requests.get("https://iva.siiva.com/admin/task/list?project_id=pr_1539766931&limit=6&state=complete")
    except:
        print("出错啦!")
        mPlay.terminate()
    else:
        for i in range(0, 6):
            activity_id = json.loads(allImg.text).get('list')[i].get('activity_id')
            taskId = json.loads(allImg.text).get('list')[i].get('task').get('taskId')
            # 图片
            imgName = 'https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/' + activity_id + '/' + taskId + '_display.jpg'
            imgList.append(imgName)
            # 二维码
            ewmName = 'https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/' + taskId + '.png'
            ewmList.append(ewmName)
        print("图片:", imgList)
        print("二维码:", ewmList)

    global imgurl1, imgurl2, imgurl3, imgurl4, imgurl5, imgurl6
    global imgPath1, imgPath2, imgPath3, imgPath4, imgPath5, imgPath6
    global ewmurl1, ewmurl2, ewmurl3, ewmurl4, ewmurl5, ewmurl6
    global ewmPath1, ewmPath2, ewmPath3, ewmPath4, ewmPath5, ewmPath6
    global img1, img2, img3, img4, img5, img6
    global ewm1, ewm2, ewm3, ewm4, ewm5, ewm6
    # 图片地址:
    imgurl1 = imgList[0]
    imgurl2 = imgList[1]
    imgurl3 = imgList[2]
    imgurl4 = imgList[3]
    imgurl5 = imgList[4]
    imgurl6 = imgList[5]
    # 获取图片
    imgPath1 = requests.get(imgurl1)
    imgPath2 = requests.get(imgurl2)
    imgPath3 = requests.get(imgurl3)
    imgPath4 = requests.get(imgurl4)
    imgPath5 = requests.get(imgurl5)
    imgPath6 = requests.get(imgurl6)
    # 二维码地址
    ewmurl1 = ewmList[0]
    ewmurl2 = ewmList[1]
    ewmurl3 = ewmList[2]
    ewmurl4 = ewmList[3]
    ewmurl5 = ewmList[4]
    ewmurl6 = ewmList[5]
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
# 开始先调用一次
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

# # 创建中白条,用于写字
noneCen = np.ones(shape = (500, 8640, 3))
noneCen = np.uint8(noneCen * 255) #把类型转为与图片一致的unit8类型
# 写字
img_PIL = Image.fromarray(cv.cvtColor(noneCen, cv.COLOR_BGR2RGB))
font = ImageFont.truetype('NotoSansCJK-Black.ttc', 100) #文字字体和大小
fillColor = (255, 0, 0) #文字颜色
position = (100, 100) #文字位置
strTxt = "请扫描二维码"
strTxt = strTxt.decode('utf8')
draw = ImageDraw.Draw(img_PIL)
draw.text(position, strTxt, font=font, fill=fillColor)
txtImg = cv.cvtColor(np.asarray(img_PIL), cv.COLOR_RGB2BGR)
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
    # 垂直叠加
    imgs = np.vstack((imgs_1, txtImg, imgs_2)) #目前H = 4820, W = 8640
    cv.imshow("imgWindow", imgs)
    if cv.waitKey(60000) & 0xFF == ord('q'):
        mPlay.terminate()  # 关闭音频
        break
    # 一定时间后,再次刷新图片
    print("刷新了!!!")
    # mPlay.terminate() #关闭音频
    # playMusic() #重启音频
    muti_imgs() #重新加载图片
print("出错啦end!!!")
cv.destroyAllWindows()

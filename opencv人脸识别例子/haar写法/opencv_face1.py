# -*- coding: utf-8 -*
import cv2 as cv
# Argparse的作用就是为py文件封装好可以选择的参数，使他们更加灵活，丰富。
import argparse
# sys模块包含了与Python解释器和它的环境有关的函数。
import sys
# NumPy系统是Python的一种开源的数值计算扩展。这种工具可用来存储和处理大型矩阵
import numpy as np
import time
import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# face_cascade = cv.CascadeClassifier("/home/siiva/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_default.xml")
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")


# 初始人脸数量定为0
faceNum = 0
# 识别时间间隔
dt_z = 900
# 基准时间
t0 = time.time()
# 从摄像头获取画面
cap = cv.VideoCapture(1)

# 从视频获取画面
# videoPath = "/home/siiva/桌面/qwe.mp4"
# cap = cv.VideoCapture(videoPath)
# 改变视频分辨率
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

def face_function():
    faces = face_cascade.detectMultiScale(small_frame,1.1,5,25)
    global faceNum
    global dt_z
    # 图片里有人脸时
    if len(faces)>0:
        print("有人脸")
        for x, y, w, h in faces:
            x *= 4
            y *= 4
            w *= 4
            h *= 4
            # 给有人脸的帧画上线框
            cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        dt_z = 100
        faceNum += 1
    # 图片里没人脸时
    else:
        print("不要脸==============")
        dt_z = 900
        faceNum = 0
    if (faceNum >= 5):
        sys.exit()

while(True):
    print(dt_z)
    ret, frame = cap.read() # 逐帧采集视频流
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # 转灰度图
    small_frame = cv.resize(gray, (0, 0), fx=0.25, fy=0.25)
    # cv.namedWindow('window', 0)
    # cv.resizeWindow('window', 1920, 1080)
    # cv.moveWindow('window', 0, 0)
    # cv.imshow('window', frame)
    cv.waitKey(1)#设定毫秒后显示下一帧图像
    
    global t0
    t1 = time.time()
    dt_t = int(round((t1-t0)*1000))
    if(dt_t >= dt_z):
        t0 = t1
        face_function()
    cv.imshow('window', frame)
cap.release()  #释放摄像头
cv.destroyAllWindows()  #关闭所有窗口





    

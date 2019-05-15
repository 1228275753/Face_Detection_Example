# -*- coding: utf-8 -*
import cv2 as cv
import requests
# Argparse的作用就是为py文件封装好可以选择的参数，使他们更加灵活，丰富。
import argparse
# sys模块包含了与Python解释器和它的环境有关的函数。
import sys
# NumPy系统是Python的一种开源的数值计算扩展。这种工具可用来存储和处理大型矩阵
import numpy as np
import time
import datetime
import threading
from sh import gphoto2 as gp
import signal, os, subprocess

def load_file():
	# 获取当前文件路径
	current_path = os.path.abspath(__file__)
	# 获取当前文件的父目录
	father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
	# config.ini文件路径,获取当前目录的父目录的父目录与congig.ini拼接
	config_file_path=father_path + '/haarcascade_frontalface_default.xml'
	return config_file_path
url = load_file()
face_cascade = cv.CascadeClassifier(url)


# 初始人脸数量定为0
faceNum = 0
# 识别时间间隔
dt_z = 900
# 基准时间
t0 = time.time()
# 设置十秒
tenSeconds = 15
# 从摄像头获取画面
cap = cv.VideoCapture(0)

# 改变视频分辨率
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# 检测人脸的方法
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
        dt_z = 200
        faceNum += 1
    # 图片里没人脸时
    else:
        print("没有脸==============")
        dt_z = 900
        faceNum = 0
    if (faceNum >= 5):
        # 检测到人脸后,十秒内不再进行检测
        dt_z = 15000
        faceNum = 0
        # 调用倒计时
        seconds_close()
        r = requests.get("https://iva.siiva.com/activity/start_prompt?activity_id=1555057493ie")
        

# 10秒倒计时关闭py程序
def seconds_close():
    global tenSeconds
    tenSeconds -= 1
    if tenSeconds > 0:
        threading.Timer(1, seconds_close).start()
    print (tenSeconds)
while(True):
    # print(dt_z)
    # print(t0)
    if tenSeconds <= 0:
        sys.exit()
    ret, frame = cap.read() # 逐帧采集视频流
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # 转灰度图
    small_frame = cv.resize(gray, (0, 0), fx=0.25, fy=0.25)
    cv.namedWindow('window', 0)
    cv.resizeWindow('window', 1920, 1080)
    # cv.moveWindow('window', 0, 0)
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





    

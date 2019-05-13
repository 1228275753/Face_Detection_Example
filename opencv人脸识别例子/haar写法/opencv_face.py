import cv2 as cv
# Argparse的作用就是为py文件封装好可以选择的参数，使他们更加灵活，丰富。
import argparse
# sys模块包含了与Python解释器和它的环境有关的函数。
import sys
# NumPy系统是Python的一种开源的数值计算扩展。这种工具可用来存储和处理大型矩阵
import numpy as np
# 通过os模块调用系统命令
import os
# 调用随机的方法
import random
import time
import signal, subprocess
# face_cascade = cv.CascadeClassifier("/home/siiva/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_default.xml")
face_cascade = cv.CascadeClassifier("/home/siiva/桌面/haarcascade_frontalface_default.xml")


# 初始人脸数量定为0
faceNum = 0
# 选取roi框的初始值
roiX = 100
roiW = 300
roiY = 0
roiH = 300
# 从摄像头获取画面
cap = cv.VideoCapture(0)
# 视频
# videoSrc = '/home/siiva/桌面/qwe.mp4'
# cap = cv.VideoCapture(videoSrc)
while(True):
    ret, frame = cap.read() # 逐帧采集视频流
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # 转灰度图
    print(frame.shape)  #查看视频宽高
    # 取矩形目标区域（高：100-300；宽：100-400）
    frame_box_data = frame[roiY:roiY+roiH, roiX:roiX+roiW] 
    gray_box_data = gray[roiY:roiY+roiH, roiX:roiX+roiW] 
    # 在特定区域里面识别人脸
    faces = face_cascade.detectMultiScale(gray_box_data,1.1,5)
    global faceNum
    # 图片里有人脸时
    if len(faces)>0:
        for faceRect in faces:
            x,y,w,h = faceRect
            # 给有人脸的帧画上线框
            cv.rectangle(frame_box_data,(x,y),(x+w,y+h),(255,0,0),2)
            
        faceNum += 1
        # print(filepath)
        print('===================yes===============')
        # 连续五帧有人脸时：
        # 杀死检测程序
        if (faceNum >= 5):
            sys.exit(1)
        # 检测帧率设为10帧
        cv.waitKey(100)
    # 图片里没人脸时
    else:
        print('================NO==================')
        # 重置人脸数量
        faceNum = 0
        # 检测帧率为2帧
        cv.waitKey(200)


    # 在原图上画目标区域:两个对角点画出的矩形。
    # x: 右为正；y: 下为正
    cv.rectangle(frame, (roiX, roiY), (roiX+roiW, roiY+roiH), (0, 255, 0), 2)
    cv.imshow('window', frame) # 显示采集到的视频流
    cv.imshow('sum', frame_box_data)  # 显示画出的区域
    # cv.waitKey(0)






# # 初始人脸数量定为0
# faceNum = 0
# # 从摄像头获取画面
# cap = cv.VideoCapture(1)
# while(True):
    # 从画面中得到Frame
    # hasFrame, frame = cap.read()
    # # 设置灰度
    # gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray,1.1,5)
    # global faceNum
    # # 图片里有人脸时
    # if len(faces)>0:
    #     for faceRect in faces:
    #         x,y,w,h = faceRect
    #         cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    #         roi_gray = gray[y:y+h//2,x:x+w]
    #         roi_color = frame[y:y+h//2,x:x+w]
            
    #     faceNum += 1
    #     # print(filepath)
    #     print('===================yes===============')
    #     # 连续五帧有人脸时：
    #     # 杀死检测程序
    #     if (faceNum >= 100):
    #         sys.exit(1)
    #     # 检测帧率设为10帧
    #     cv.waitKey(100)
    # # 图片里没人脸时
    # else:
    #     print('================NO==================')
    #     # 重置人脸数量
    #     faceNum = 0
    #     # 检测帧率为2帧
    #     cv.waitKey(100)

    # cv.imshow("winName", frame)
    
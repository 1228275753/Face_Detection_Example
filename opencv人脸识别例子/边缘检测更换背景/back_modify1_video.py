# -*- coding: utf-8 -*-
# 基于二值化阀值边缘处理的视频背景切换
import cv2 as cv
import math
import numpy as np

cap = cv.VideoCapture('qwe.mp4')
img_back = cv.imread('bluesky.jpeg')
img_back = cv.resize(img_back,(640,480))

while True:
    ret,img = cap.read()
    img = cv.resize(img,(640,480))
    # convert color space from bgr to gray
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # threshold 固定阀值二值化函数
    # 图像中,大于阀值212的都为白色(255),小于212的都为黑色
    threshold,imgOtsu = cv.threshold(imgGray,212,255,cv.THRESH_BINARY)

    fan = cv.bitwise_not(imgOtsu)

    res1 = cv.bitwise_and(img_back,img_back,mask=imgOtsu)
    res2 = cv.bitwise_and(img,img,mask=fan)
    finallyImg = cv.addWeighted(res1,1,res2,1,0)

    cv.imshow('imgOtsu',imgOtsu)
    cv.imshow('finallyImg',finallyImg)
    cv.waitKey(10)
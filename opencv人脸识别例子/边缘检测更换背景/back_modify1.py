# -*- coding: utf-8 -*-
# 基于otsu/二值化阀值边缘处理的背景切换
import cv2 as cv
import math
import numpy as np

img = cv.imread('jingjiang.png')
img_back = cv.imread('bluesky.jpeg')
img = cv.resize(img,(1280,1000))
img_back = cv.resize(img_back,(1280,1000))

# convert color space from bgr to gray
imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# laplacian edge
imgLap = cv.Laplacian(imgGray,cv.CV_8U)

# threshold 固定阀值二值化函数
# otsu method
# threshold,imgOtsu = cv.threshold(imgGray,210,255,cv.THRESH_BINARY + cv.THRESH_OTSU)
# 这是我自己测试的
threshold,imgOtsu = cv.threshold(imgGray,210,255,cv.THRESH_BINARY)

# 高斯模糊处理
# imgOtsu = cv.GaussianBlur(imgOtsu, (3, 3), 0)

fan = cv.bitwise_not(imgOtsu)

# img_back的大小必须和imgOtsu的大小一致
# img_back为实际图片,imgOtsu为处理过(如转灰度,拉普拉斯等等)的版式
res1 = cv.bitwise_and(img_back,img_back,mask=imgOtsu)
res2 = cv.bitwise_and(img,img,mask=fan)
finallyImg = cv.addWeighted(res1,1,res2,1,0)
# finallyImg = cv.add(img,img_back)


# cv.imshow('img',img)
cv.imshow('imgGray',imgGray)
cv.imshow('imgOtsu',imgOtsu)
# cv.imshow('fan',fan)
# cv.imshow('res1',res1)
# cv.imshow('res2',res2)
cv.imshow('finallyImg',finallyImg)
# cv.imshow('gaosimohu',gaosimohu)
cv.waitKey(0)
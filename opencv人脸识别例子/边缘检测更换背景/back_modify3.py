# -*- coding: utf-8 -*-
# 基于Sobel边缘检测算子的图像背景切换(测试阶段)
import cv2 as cv
img = cv.imread('jingjiang.png')
img = cv.resize(img,(640,480))
x = cv.Sobel(img, cv.CV_16S, 1, 0)
y = cv.Sobel(img, cv.CV_16S, 0, 1)
# cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
# 可选参数alpha是伸缩系数，beta是加到结果上的一个值，结果返回uint类型的图像
Scale_absX = cv.convertScaleAbs(x)  # convert 转换  scale 缩放
Scale_absY = cv.convertScaleAbs(y)
result = cv.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)


# threshold 固定阀值二值化函数
# 图像中,大于阀值212的都为白色(255),小于212的都为黑色
# threshold,imgOtsu = cv.threshold(result,5,255,cv.THRESH_BINARY_INV)


cv.imshow('img', img)
cv.imshow('result', result)
# cv.imshow('imgOtsu', imgOtsu)
cv.waitKey(0)
cv.destroyAllWindows()
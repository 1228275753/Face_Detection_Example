#!/usr/bin/env python
# -*- coding: utf-8 -*
from __future__ import print_function
import cv2 as cv
import numpy as np
import time
import io
import logging
import os
import subprocess
import sys

from PIL import Image

import gphoto2 as gp


# 戴入人脸检测模型
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
callback_obj = gp.check_result(gp.use_python_logging())
# 获取摄像头
camera = gp.check_result(gp.gp_camera_new())
# 初始化摄像头
gp.check_result(gp.gp_camera_init(camera))

# required configuration will depend on camera type!
# 所需配置将取决于摄像头类型！
print('检查摄像头配置')

# get configuration tree
# 获取摄像头配置树
config = gp.check_result(gp.gp_camera_get_config(camera))


# find the image format config item
# 查找图像格式配置项
OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
if OK >= gp.GP_OK:
	# get current setting
	# 获取当前设置
	value = gp.check_result(gp.gp_widget_get_value(image_format))
	# make sure it's not raw
	#确保它不是未加工的
	if 'raw' in value.lower():
		print('无法预览原始图像')
	

print (" 查找捕获大小类配置项")
# need to set this on my Canon 350d to get preview to work at all
# 需要在我的佳能350D上设置这个才能让预览工作。
OK, capture_size_class = gp.gp_widget_get_child_by_name(config, 'capturesizeclass')

if OK >= gp.GP_OK:
	# set value
	# 创建一个值
	value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
	gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
	# set config
	# 创建配置
	gp.check_result(gp.gp_camera_set_config(camera, config))
else:
	print ("捕获大小类错误")

systime = int(time.time()) 
count = 0
while (True):
	# 获取摄像头预览图像
	camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
	#print(camera_file)
	# 获取图像数据
	file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
	# display image
	#data = memoryview(file_data)
	#print(type(data), len(data))
	#print(data[:10].tolist())
	# 将图像数据装换成图像
	image = Image.open(io.BytesIO(file_data))
	# 将每一张图像添加到数组中,变成图片
	img = np.array(image)
	img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	# print (img.shape[0],img.shape[1],img.shape[2])
	# newX,newY = img.shape[1]*0.5, img.shape[0]* 0.5
	# newimg = cv.resize(img,(int(newX),int(newY)))
	roi_color = img[100:300, 100:300]           # 计算彩色画面ROI       
	gray = cv.cvtColor(roi_color, cv.COLOR_BGR2GRAY)            # 图片转换成灰色
	# faces = face_cascade.detectMultiScale(gray, 1.1, 3)     # 先检测人脸
	# for (x,y,w,h) in faces:     # 如果检测到人脸，获得人脸外框坐标，画出边框，检测眼睛
	# 	cv.rectangle(gray,(x,y),(x+w,y+h),(0,0xff,0),5)  # 画蓝色框
	# 	hasface = True

	cv.imshow('img',img)
	cv.imshow('roi_color',roi_color)
	if cv.waitKey(1) & 0xFF==ord('q'):
		break

	# 系统时间秒数
	systime1 = int(time.time()) 
	count = count + 1
	if systime1 > systime:
		print(count)
		count = 0
		systime = systime1

gp.check_result(gp.gp_camera_exit(camera))



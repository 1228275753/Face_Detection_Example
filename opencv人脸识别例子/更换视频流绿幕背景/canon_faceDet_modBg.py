# -*- coding: utf-8 -*-
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
import signal, os, subprocess

import gphoto2 as gp
import io
import logging
from PIL import Image

def load_file():
	# 获取当前文件路径
	current_path = os.path.abspath(__file__)
	# 获取当前文件的父目录
	father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
	global config_file_path
	global back_path
	# config.ini文件路径,获取当前目录的父目录的父目录与congig.ini拼接
	config_file_path=father_path + '/haarcascade_frontalface_default.xml'
	back_path=father_path + '/back4.jpg'
	#return config_file_path
load_file()
face_cascade = cv.CascadeClassifier(config_file_path)


# 初始人脸数量定为0
faceNum = 0
# 识别时间间隔
dt_z = 1000
# 基准时间
t0 = time.time()
# 设置十秒
tenSeconds = 15

# 绿幕背景图片
img_back1=cv.imread(back_path)
# 改变背景图片分辨率
img_back1 = cv.resize(img_back1,(928,616))

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
            cv.rectangle(frameBg,(x,y),(x+w,y+h),(0,0,255),2)
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
        # r = requests.get("https://iva.siiva.com/activity/start_prompt?activity_id=1555057493ie")
        

# 10秒倒计时关闭py程序
def seconds_close():
    global tenSeconds
    tenSeconds -= 1
    if tenSeconds > 0:
        threading.Timer(1, seconds_close).start()
    print (tenSeconds)

# 将绿幕换成背景
def greenToBg():
    # 重置背景
    img_back = img_back1
    global frame
    global frameBg
   
    #转换hsv
    hsv=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    #获取mask,mask1将绿屏变为白色
    mask1 = cv.inRange(hsv,lower_green,upper_green)
    #腐蚀膨胀,erode和dilate步骤为完善润滑mask1
    mask1=cv.erode(mask1,None,iterations=1)
    mask1=cv.dilate(mask1,None,iterations=1)


    # 反转mask1,mask2将绿屏变为黑色
    mask2 = cv.bitwise_not(mask1)
    # 生成最终输出
    # res1,将绿屏变为背景,其余全是黑色(即用img_back填充白色区域)
    res1 = cv.bitwise_and(img_back,img_back,mask=mask1)
    # res2,将绿屏变为黑色,其余全是正常(即用img填充白色区域)
    res2 = cv.bitwise_and(frame,frame,mask=mask2)
    frameBg = cv.addWeighted(res1,1,res2,1,0)

# 设置hsv颜色范围,
lower_green=np.array([35,35,45])
# 35-77为绿色的范围
upper_green=np.array([77,255,255])
# 35-124为绿/青/蓝三色的范围
# upper_blue=np.array([124,255,255])

# gphoto的一堆东西=============
logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
callback_obj = gp.check_result(gp.use_python_logging())
camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera))

# required configuration will depend on camera type!
print('Checking camera config')

# get configuration tree
config = gp.check_result(gp.gp_camera_get_config(camera))


# find the image format config item
OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
if OK >= gp.GP_OK:
    # get current setting
    value = gp.check_result(gp.gp_widget_get_value(image_format))
    # make sure it's not raw
    if 'raw' in value.lower():
        print('Cannot preview raw images')
       

print (" find the capture size class config item")
# need to set this on my Canon 350d to get preview to work at all
OK, capture_size_class = gp.gp_widget_get_child_by_name(
    config, 'capturesizeclass')

if OK >= gp.GP_OK:
    # set value
    value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
    gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
    # set config
    gp.check_result(gp.gp_camera_set_config(camera, config))
else:
    print ("capture size class error")

systime = int(time.time()) 
count = 0
# gphoto的一堆东西结束=============
while(True):
    # 如果倒计时结束,将退出程序
    if tenSeconds <= 0:
        cv.imwrite("origin1.jpg",frame)
        cv.imwrite("finish1.jpg",frameBg)
        sys.exit()

    camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
    image = Image.open(io.BytesIO(file_data))
    frame = np.array(image)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # 调用更换绿幕背景
    greenToBg()

    gray = cv.cvtColor(frameBg, cv.COLOR_BGR2GRAY) # 转灰度图
    small_frame = cv.resize(gray, (0, 0), fx=0.25, fy=0.25)  
    
    global t0
    t1 = time.time()
    count = count + 1
    dt_t = int(round((t1-t0)*1000))
    if(dt_t >= dt_z):
        print(count)
        t0 = t1
        count = 0
        face_function()
    # cv.namedWindow('window', 0)
    # cv.resizeWindow('window', 1920, 1080)
    # cv.moveWindow('window', 0, 0)
    cv.imshow('window', frameBg)
    if cv.waitKey(1) & 0xFF==ord('q'):
        # cv.imwrite("testImg.jpg",frame)
        # cv.imwrite("smallImg.jpg",small_frame)
	    break
# 结束预览
gp.check_result(gp.gp_camera_exit(camera))

cv.destroyAllWindows()  #关闭所有窗口





    

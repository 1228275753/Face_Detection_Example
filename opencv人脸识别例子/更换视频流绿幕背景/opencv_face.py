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
import _thread
import signal, os, subprocess
import pygame
import gphoto2 as gp
from sh import gphoto2 as gpsh
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
# obtain handle to face data model
face_cascade = cv.CascadeClassifier(config_file_path)
# 初始人脸数量定为0
faceNum = 0
# 识别时间间隔
dt_z = 1000
# 设置十秒
curr = 10
# 绿幕背景图片
img_back1=cv.imread(back_path)
# 改变背景图片分辨率
img_back1 = cv.resize(img_back1,(640,424)) 

# 杀死gphoto程序
def Killgphoto2Process():
	p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
	out, err = p.communicate()
   
    # Search for the line that has the process
    # we want to kill
	for line in out.splitlines():
		if b'gvfsd-gphoto2' in line:
			# Kill the process!
			pid = int(line.split(None,1)[0])
			os.kill(pid, signal.SIGKILL)
Killgphoto2Process()

# 播放音频
def play_music(filename, loops=0, start=0.0, value=0.5):
    """
    :param filename: 
    :param loops: 
    :param start: 
    :param value: 
    :return:
    """
    global myflag
    myflag = False  
    pygame.mixer.init() 
    while 1:
        if myflag == 0:
            pygame.mixer.music.load(filename)
            # pygame.mixer.music.play(loops=0, start=0.0)
            pygame.mixer.music.play(loops=loops, start=start)
            pygame.mixer.music.set_volume(value) 
        if pygame.mixer.music.get_busy() == True:
            myflag = True
        else:
            if myflag:
                pygame.mixer.music.stop()
                break
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
        dt_z = 1000
        faceNum = 0

    if (faceNum >= 3):
        dt_z = 10000
        # 调用绘制倒计时
        second_repeat()
        # 调用音频
        play_music("audio.mp3")
        faceNum = 0
        # r = requests.get("https://iva.siiva.com/activity/start_prompt?activity_id=1558607850so&from=auto_detect")
        
# 全局变量的倒计时
def second_repeat():
    global curr
    curr = curr - 1
    if curr > 0:
        threading.Timer(1, second_repeat).start()
    print ("剩余秒数:",curr)

# global tenSeconds
# tenSeconds -= 1
# if tenSeconds > 0:
#     threading.Timer(1, seconds_close).start()
# print (tenSeconds)

#调用倒计时的图像绘制
def count_down():
    cv.putText(frameBg,str(curr),(250,250),cv.FONT_HERSHEY_COMPLEX,12,(0,0,255),15)


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
    # 反转mask1,mask2将绿屏变为黑色
    mask2 = cv.bitwise_not(mask1)
    # 生成最终输出
    # res1,将绿屏变为背景,其余全是黑色(即用img_back填充白色区域)
    res1 = cv.bitwise_and(img_back,img_back,mask=mask1)
    # res2,将绿屏变为黑色,其余全是正常(即用img填充白色区域)
    res2 = cv.bitwise_and(frame,frame,mask=mask2)
    frameBg = cv.addWeighted(res1,1,res2,1,0)


# 拍照方法
def capture_image():
    # 拍照
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
    print('file_path==',file_path)
    # 存照片路径
    global imgPath
    target = os.path.join('imgs', file_path.name)
    imgPath = target
    # 相机文件
    camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    print('camera_file==',camera_file)
    # 保存
    gp.check_result(gp.gp_file_save(camera_file, target))
    gp.check_result(gp.gp_camera_exit(camera))
    capture_and_resize_image()
    

# 修改相片大小
def capture_and_resize_image():
    infile = imgPath #读取照片的位置及其名字
    outfile = 'imgs/outImg.jpg' #修改后照片储存位置和名字
    pic = cv.imread(infile)
    h = pic.shape[0] #照片的高
    w = pic.shape[1] #照片的宽
    s_h = 2160 #标准的高
    s_w = w * s_h / h #标准的宽
    dis_w = s_w - 2880 #多余的宽的长度
    half_dis_w = dis_w / 2
    img = cv.resize(pic,(int(s_w),int(s_h))) #缩小后的图片
    s_img = img[0:int(s_h), int(half_dis_w):int(half_dis_w + 2880)] #完成切割后的标准图片
    cv.imwrite(outfile,s_img) #输出新照片保存

# 设置hsv颜色范围,
lower_green=np.array([35,35,40])
# 35-77为绿色的范围
upper_green=np.array([80,255,255])
# 35-124为绿/青/蓝三色的范围
# upper_blue=np.array([124,255,255])

# 初始化相机=============
global camera
camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera))


# 全屏窗口=============
# cv.namedWindow('window', 0)
# cv.resizeWindow('window', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) #画面全屏
# cv.setWindowProperty('window', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) #窗口全屏

# 初始化帧率
count = 0
# 基准时间
t0 = time.time()
flag = 0
while(True):
    # 获取预览照片
    camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
    image = Image.open(io.BytesIO(file_data))
    frame = np.array(image)
    frame = cv.flip(frame,1,dst=None)
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # 调用更换绿幕背景
    greenToBg()

    gray = cv.cvtColor(frameBg, cv.COLOR_BGR2GRAY) # 转灰度图
    small_frame = cv.resize(gray, (0, 0), fx=0.25, fy=0.25)
    
    t1 = time.time()
    count = count + 1
    dt_t = int(round((t1-t0)*1000))
    if(dt_t >= dt_z):
        print("当前帧率:",count)
        t0 = t1
        count = 0
        face_function()
	
    # 检测到人
    if(curr!=10):
        # 调用音频
        # play_music("audio.mp3")
        # 绘制倒计时
        cv.putText(frameBg,str(curr),(250,250),cv.FONT_HERSHEY_COMPLEX,12,(0,0,255),15)

    # 倒计时结束了
    if(curr <= 0):
        capture_image()
        curr = 10	
		
 
    cv.imshow('window', frameBg)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
# 结束预览
gp.check_result(gp.gp_camera_exit(camera))

cv.destroyAllWindows()  #关闭所有窗口





    

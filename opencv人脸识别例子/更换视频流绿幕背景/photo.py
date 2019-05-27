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
import gphoto2 as gp
from sh import gphoto2 as gpsh
import io
import logging
from PIL import Image, ImageDraw, ImageFont

DETECT_THRESHOLD =5              # 重复检测次数
PHOTO_PATH  = 'imgs/outImg.jpg'  # 储存照片的位置
FACE_MODEL_PATH = '/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'

def load_file():
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    global config_file_path
    global back_path
    # config.ini文件路径,获取当前目录的父目录的父目录与congig.ini拼接
    config_file_path= father_path + '/haarcascade_frontalface_default.xml'
    back_path= father_path + '/back4.jpg'

# 提供云服务相机在线状态
# todo [DON]
def isCameraOnline():
    return True

# 提供云服务相机预览图片
# todo [DON]
def getCameraPreview():
    return True

# 提供云服务相机直播预览流
# todo [DON]
def getCameraLiveStream():
    return True


# 杀死gphoto程序,同时确定相机连线。通知云服务如果无法连接
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

    # RESET 相机多次，直到相机不回复错误讯息
    # todo [DON]

    # 如果相机无法连线，通知云服务
    # todo [DON]

# 检测人脸的方法
def face_function(small_frame):
    global faceNum
    global face_cascade
    global scale_factor

    faces = face_cascade.detectMultiScale(small_frame,1.1,5)
    # 图片里有人脸时
    if len(faces)>0:
        print("有人脸")
        t0 = t1
        for x, y, w, h in faces:
            x = int (x/scale_factor)
            y = int (y/scale_factor)
            w = int (w/scale_factor)
            h = int (h/scale_factor)
            # 给有人脸的帧画上线框
            cv.rectangle(frameBg,(x,y),(x+w,y+h),(0,0,255),2)
        if countdown == 0:  # 没有在倒数的话才更新人脸检测次数
            faceNum += 1
        return True
    else:
#        print("没有脸==============")
        faceNum = 0
        return False

# 将绿幕换成背景
def greenToBg():
    # 重置背景
    global img_back1
    global frame
    global frameBg
    img_back = img_back1
    tframe = frame  # 不要改变原来摄像机获得的画面
    hsv=cv.cvtColor(tframe,cv.COLOR_BGR2HSV)      #转换hsv
    mask1 = cv.inRange(hsv,lower_green,upper_green)     #获取mask,mask1将绿屏变为白色
    mask2 = cv.bitwise_not(mask1)    # 反转mask1,mask2将绿屏变为黑色
    # res1,将绿屏变为背景,其余全是黑色(即用img_back填充白色区域)
    res1 = cv.bitwise_and(img_back,img_back,mask=mask1)
    # res2,将绿屏变为黑色,其余全是正常(即用img填充白色区域)
    res2 = cv.bitwise_and(tframe,tframe,mask=mask2)
    frameBg = cv.addWeighted(res1,1,res2,1,0)

# 删除照片
def remove_file(path_):
    try:
        os.remove(path_)
    except OSError:
        os.lchmod(path_, stat.S_IWRITE)
        os.remove(path_)

# 在屏幕上显示中文
def drawChinese(image_file,str):
    img_OpenCV = cv.imread(image_file)
    img_OpenCV = cv.flip(img_OpenCV,1,dst=None) #水平镜像
    print('draw chinese')
    # 图像从OpenCV格式转换成PIL格式
    img_PIL = Image.fromarray(cv.cvtColor(img_OpenCV, cv.COLOR_BGR2RGB))
    font = ImageFont.truetype('NotoSansCJK-Black.ttc', 100)
    fillColor = (255,0,0)
    position = (100,100)

    str.encode('utf-8').decode("unicode_escape")
    # if not isinstance(str, unicode):
    #     str = str.decode('utf8')
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, str, font=font, fill=fillColor)
    img = cv.cvtColor(np.asarray(img_PIL),cv.COLOR_RGB2BGR)
    return img

# 二维码生成中
def TransmitImage(image_file):
    global frameBg
    # 确定前面的mp3播放已经结束，再播放新的提示音频
    cv.waitKey(2000)
    # 播放第二个音频:二维码生成中
    subprocess.Popen(["python","mp3.py","audio_2.mp3"])
    img = drawChinese(image_file,'二维码生成中...')
    cv.imshow('上海金融中心', img)
    cv.waitKey(8000)

    # 显示二维码=============
    subprocess.Popen(["python","mp3.py","audio_3.mp3"])
    imH = img.shape[0] #获取img的高
    imW = img.shape[1]
    s_h = int(imH / 2) #定义一个二维码的宽高
    s_h2 = int(s_h / 2)
    s_w = int(imW / 2)
    s_w2 = s_w - s_h2
    print('二维码的宽:',s_h)
    # qrcodeImg = cv.imread('qrcode.jpg') #获取二维码
    img2 = cv.imread('qrcode.jpg') #获取二维码
    img2 = cv.resize(img2,(s_h,s_h)) #设置二维码尺寸
	# rows,cols,channels = img2.shape
    img[0:s_h, 0:s_h] = img2
    codeImgPath = 'imgs/code.jpg' #有二维码和人的图片
    cv.imwrite(codeImgPath,img)
    codeImg = Image.open(codeImgPath)
    for i in range (0,20):
        print('loop',i)
        img1 = np.array(codeImg)
        img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
        # 显示二维码消失的倒计时
        cv.putText(img1,str(20-i),(int(imW*0.8),int(imH*0.2)),cv.FONT_HERSHEY_PLAIN,20,(0,0,255),10)
        cv.imshow('上海金融中心', img1)
        cv.waitKey(1000)
    os.remove(codeImgPath)

    

# 显示二维码
# def scanQRCode(qrcode_file):
#     # 第三个音频:请扫描二维码
#     subprocess.Popen(["python","mp3.py","audio_3.mp3"])
#     print(qrcode_file)
#     print('scan qr code==========')
#     img_qrcode = Image.open(qrcode_file)
#     print('qr code file opened',img_qrcode, qrcode_file)
# #    img[100,100] = cv_img_qrcode
#     txt_x = int(image_width / 2) - 12
#     txt_y = int(image_height/ 2) + 12
#     print('enter loop')
#     for i in range (0,20):
#         print('loop',i)
#         img = np.array(img_qrcode)
#         # 显示二维码消失的倒计时
#         cv.putText(img,str(20-i),(0,50),cv.FONT_HERSHEY_PLAIN,4,(0,255,0),2)
#         cv.imshow('上海金融中心', img)
#         cv.waitKey(1000)
#         print('二维码扫吗中')
#     print('exit scanqr code')


# 拍照方法
def capture_image():
    # 拍照
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
    # 存照片路径
    global imgPath

    target = os.path.join('imgs', file_path.name)
    imgPath = target
    print(imgPath, file_path.folder, file_path.name)
    # 相机文件
    camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    # 保存
    gp.check_result(gp.gp_file_save(camera_file, target))
    capture_and_resize_image()

    # 用SOCKET将照片传回服务器（本地或云）
    print('transmite image')
    TransmitImage(PHOTO_PATH) #PHOTO_PATH:修剪过后的照片名字

    # 获取二维码后显示到屏幕一段时间，让用户拿出手机扫吗
    # scanQRCode('qrcode.jpg')

    # 删除照片
    remove_file(target)     # remove captured file
    remove_file(PHOTO_PATH) # remove resized file

# 修改相片大小
def capture_and_resize_image():
    infile = imgPath #读取照片的位置及其名字
    outfile = PHOTO_PATH  #修改后照片储存位置和名字
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

# 初始化相机=============
def initializecamera():
    global camera #相机
    global back_path #背景图路径
    global img_back1 #背景图
    global image_width #相机预览图的宽
    global image_height #相机预览图的高
    global scale_factor #获取图像缩小的倍数
    global screen_width, screen_height

    Killgphoto2Process() #先停止gphoto2 运行线程

    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    camera_file = gp.check_result(gp.gp_camera_capture_preview(camera))
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
    image = Image.open(io.BytesIO(file_data))
    frame = np.array(image)
    image_height, image_width = frame.shape[:2]     # 获得相机预览图片大小
    print('相机预览画面 宽/高=', image_width,'/', image_height)
    img_back1 = cv.imread(back_path)    # 绿幕背景图片
    img_back1 = cv.resize(img_back1,(image_width,image_height))  # 改变背景图片分辨率
    if image_width > 900:
        scale_factor = 0.5
    else:
        scale_factor = 1

    # 检测目前显示屏分辨率，根据分辨率再显示文字大小和位置
    #cmd = ['xrandr']
    #cmd2 = ['grep', '*']
    #p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    #p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    #p.stdout.close()

    #resolution_string, junk = p2.communicate()
    #resolution = resolution_string.split()[0]
    #swidth, sheight = resolution.split('x')
    #screen_width = int(swidth)
    #screen_height = int(sheight)
    #print (screen_width, screen_height)


#
# start main program here
#
# 调用背景图片和识别文件路径的方法
load_file()
# 初始化相机的方法
initializecamera()

# 引用人脸训练文件
face_cascade = cv.CascadeClassifier(config_file_path)
faceNum = 0  # 初始人脸数量定为0
curr = 0
countdown = 0  # 倒数计时counter

# 35-124为绿/青/蓝三色的范围
lower_green=np.array([35,35,40])   # 设置hsv颜色范围,
upper_green=np.array([80,255,255]) # 35-77为绿色的范围

# 全屏窗口=============
cv.namedWindow('上海金融中心', 0)
cv.resizeWindow('上海金融中心', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) #画面全屏
cv.setWindowProperty('上海金融中心', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) #窗口全屏

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
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # 转灰度图
    greenToBg()    # 调用更换合成绿幕背景
    if image_width > 900:
        # canon 600D 1050x704, 500D 928x616
        small_frame = cv.resize(gray, (0, 0), fx=scale_factor, fy=scale_factor)
    else:
        small_frame = gray

    # 计算当前的fps帧率
    t1 = int(time.time())
    # count:帧率
    count = count + 1
    # 如果60秒没检测到人脸
    if(t1 - t0 > 60):
        initializecamera()
        t0 = t1

    # 呼叫人脸检测函式，同时看是否在倒数
    if (countdown == 0) | (curr < 5):
        if face_function(small_frame) == True:
            # 检测到5帧有人脸时
            if faceNum >= DETECT_THRESHOLD:
                # 播放第一个音频
                ret1 = subprocess.Popen(["python","mp3.py","audio_1.mp3"])
                print("face detected, play count down")
                countdown = int(time.time())
                faceNum= 0

    # 在倒数
    if countdown > 0:
        currtime = int(time.time()) # 获取现在时间秒数
        curr = currtime-countdown   # 获取检测到人脸后经历的秒数
        # 显示倒数文字在屏幕中间
        fontsize = 12
        txt_x = int(image_width / 2) - fontsize
        txt_y = int(image_height/ 2) + fontsize
        # 当经历了10秒后,拍照
        if curr > 10:
            countdown = curr = facenum = 0
            capture_image()
        else:
            cv.putText(frameBg,str(10-curr),(txt_x,txt_y),cv.FONT_HERSHEY_PLAIN,fontsize,(0,0,255),7)

    cv.imshow('上海金融中心', frameBg)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

# 结束预览
gp.check_result(gp.gp_camera_exit(camera))
cv.destroyAllWindows()  #关闭所有窗口







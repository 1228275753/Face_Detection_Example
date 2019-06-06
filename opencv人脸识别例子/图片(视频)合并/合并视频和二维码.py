import cv2 as cv
import numpy as np
import os
import requests
import time

# 视频帧率为30帧
def muti_video():
    # 视频源地址
    videoPath1 = requests.get("https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1557886955xa/1557886955xa_1559298174359.mp4")
    videoPath2 = requests.get("https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1557886955xa/1557886955xa_1559297690876.mp4")
    videoPath3 = requests.get("https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/1557886955xa/1557886955xa_1559297504675.mp4")
    # 三个视频源
    cap1Data = videoPath1.content #读取文件字节
    cap2Data = videoPath2.content
    cap3Data = videoPath3.content
    # 写入视频
    global file_path1
    global file_path2
    global file_path3
    file_path1='{}'.format(os.getcwd()+"/inter1.mp4") #在当前路径给视频命名
    file_path2='{}'.format(os.getcwd()+"/inter2.mp4")
    file_path3='{}'.format(os.getcwd()+"/inter3.mp4")
    with open(file_path1,'wb') as f1, open(file_path2,'wb') as f2, open(file_path3,'wb') as f3: #打开文件,并定义权限为"读写"
        f1.write(cap1Data) #将视频字节写入文件
        f1.close() #关闭文件
        f2.write(cap2Data)
        f2.close() #关闭文件
        f3.write(cap3Data)
        f3.close() #关闭文件
    # 读取视频
    cap1 = cv.VideoCapture(file_path1)
    cap2 = cv.VideoCapture(file_path2)
    cap3 = cv.VideoCapture(file_path3)
    # 二维码地址
    ewmPath1 = requests.get("https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png")
    ewmPath2 = requests.get("https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png")
    ewmPath3 = requests.get("https://siiva-video.oss-cn-hangzhou.aliyuncs.com/qrcode/1555057493ie_1557470772627.png")
    # 三张二维码,解码成图片矩阵
    ewm1 = cv.imdecode(np.fromstring(ewmPath1.content, np.uint8), 1) #ewmPath1.content 是读取的远程文件的字节流
    ewm2 = cv.imdecode(np.fromstring(ewmPath2.content, np.uint8), 1)
    ewm3 = cv.imdecode(np.fromstring(ewmPath3.content, np.uint8), 1)
    # 全屏窗口,这样就可以自适应视频大小
    cv.namedWindow('imgWindow', cv.WINDOW_NORMAL) #获取窗口名字
    cv.resizeWindow('imgWindow', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) #画面全屏
    cv.setWindowProperty('imgWindow', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN) #窗口全屏
    
    time0 = time.time()
    while True:
        # 分别获取三个视频源的帧
        ret1,frame1 = cap1.read()
        ret2,frame2 = cap2.read()
        ret3,frame3 = cap3.read()
        #将读取图像逆时针旋转90度
        frame1 = np.rot90(frame1, 1) 
        frame2 = np.rot90(frame2, 1)
        frame3 = np.rot90(frame3, 1)
        # 分别给三个视频加上二维码
        frame1[1440:1870, 600:1030] = ewm1
        frame2[1440:1870, 600:1030] = ewm2
        frame3[1440:1870, 600:1030] = ewm3
        # 图集,合并三个视频的帧在一起
        frames = np.hstack([frame1,frame2,frame3])
        cv.imshow("imgWindow",frames)
        cv.waitKey(1)
        # 测试当前帧率
        time5 = time.time()
        t = time5-time0
        t = int(round(t*1000))
        zl = int(1000/t)
        print("当前帧率为:=====",zl)
        time0 = time5
    cap.release()
muti_video()
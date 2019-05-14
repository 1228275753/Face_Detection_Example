#-*-coding: utf-8 -*
import cv2
import  numpy as np
# 视频流
cap = cv2.VideoCapture(1)
# 绿幕背景图片
img_back1=cv2.imread('back.jpeg')
# 改变背景图片分辨率
img_back1 = cv2.resize(img_back1,(1280,720))
# 改变视频(摄像头)分辨率
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# 编辑输出视频的各种变量===============
# videoName = 'myTest0.avi'#视频名字
# print('视频名字:',videoName)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')#视频格式
# print('视频格式:',fourcc)
# fps = cap.get(cv2.CAP_PROP_FPS)# 获取视频帧率
# print('视频帧率:',fps)
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))# 查看视频size
# print('视频大小:',size)
# videoWrite = cv2.VideoWriter(videoName,fourcc,fps,size)

# 设置hsv颜色范围,
lower_green=np.array([35,43,46])
# 35-77为绿色的范围
upper_green=np.array([77,255,255])
# 35-124为绿/青/蓝三色的范围
# upper_blue=np.array([124,255,255])
while True:
    # global img_back
    img_back=img_back1
    
    # 获取视频的每一帧
    ret,img = cap.read()
    rows,cols,channels = img.shape#rows，cols最后一定要是前景图片的，后面遍历图片需要用到
    
    #转换hsv
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #获取mask,mask1将绿屏变为白色
    mask1 = cv2.inRange(hsv,lower_green,upper_green)
    #腐蚀膨胀,erode和dilate步骤为完善润滑mask1
    mask1=cv2.erode(mask1,None,iterations=1)
    mask1=cv2.dilate(mask1,None,iterations=1)


    # 反转mask1,mask2将绿屏变为黑色
    mask2 = cv2.bitwise_not(mask1)
    # 生成最终输出
    # res1,将绿屏变为背景,其余全是黑色(即用img_back填充白色区域)
    res1 = cv2.bitwise_and(img_back,img_back,mask=mask1)
    # res2,将绿屏变为黑色,其余全是正常(即用img填充白色区域)
    res2 = cv2.bitwise_and(img,img,mask=mask2)
    final_output = cv2.addWeighted(res1,1,res2,1,0)
    
    
    # cv2.namedWindow('window', 0)
    # cv2.resizeWindow('window', 1280, 720)
    # cv2.moveWindow('window', 0, 0)
    # 显示处理过后的视频
    cv2.imshow('window',final_output)
    # 输出视频
    # videoWrite.write(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # cv2.imwrite("testImg1.jpg",img_back)
        break
# cv2.release()
cv2.destroyAllWindows()

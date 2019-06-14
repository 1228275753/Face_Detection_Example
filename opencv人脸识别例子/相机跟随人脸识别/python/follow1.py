import cv2
import numpy as np
# pip install pyserial安装serial
import serial #python与arduino之间的通信
 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)
screenW = 640
halfW = int(screenW/2)
screenH = 320
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screenW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screenH)
# /dev/ttyUSB0: 这个名字在arduino工具-串口监视器查看
# 115200: 波特率,这是比较理想的波特率,不要改
ser = serial.Serial('/dev/ttyUSB0', 115200)
 
while True:
    ret, img = cap.read()
    # print("是否有画面:",ret)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 2, 5)
    if len(faces):
        # 目的是为了只识别一张人脸,方便追踪
        (x, y, w, h) = max(faces, key=lambda face: face[2]*face[3])
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        
        position = x + w/2.0 #脸的中间在x轴的位置
        print(position)
        wucha = 20 #设置一个偏离正中间的误差
        # 如果脸在左边,输出 a
        if position < halfW-wucha:
            ser.write(b'a')
        # 脸在右边,输出 b
        if position > halfW+wucha:
            ser.write(b'b')
         
    cv2.imshow('face', img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
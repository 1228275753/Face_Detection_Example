#-*-coding: utf-8 -*
import face_recognition
import cv2 as cv
import numpy as np

# 获取对网络摄像机的引用0（默认值）
cap = cv.VideoCapture(0)

# 初始化一些变量
face_locations = []
face_encodings = []
process_this_frame = True
faceNum = 0
while True:
    # 抓取一帧视频
    ret, frame = cap.read()
    # 将视频帧的大小调整为1/4，以便更快地进行人脸识别处理
    small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # 将图像从bgr颜色（opencv使用）转换为rgb颜色（人脸识别使用）
    rgb_small_frame = small_frame[:, :, ::-1]

    # 只处理其他每帧视频以节省时间
    if process_this_frame:
        # 查找当前视频帧中的所有face和face编码
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)    

    process_this_frame = not process_this_frame

    global faceNum
    # 如果有人脸
    if (len(face_locations)>0):
        faceNum += 1
        print (faceNum)
    else:
        faceNum = 0
    # 连续十帧有人脸,退出程序
    if (faceNum >= 10):
        break

    # 显示结果
    for top, right, bottom, left in face_locations:
        # 自我们检测到的帧被缩放到1/4大小后，将备份面位置缩放
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 在脸上画一个方框
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # 显示结果图像
    cv.imshow('Video', frame)
    # 点击键盘上的“Q”退出！
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

# 释放摄像头手柄
cap.release()
cv.destroyAllWindows()

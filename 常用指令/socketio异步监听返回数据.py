import cv2 as cv
from socketIO_client_nexus import SocketIO, LoggingNamespace
import _thread

cap = cv.VideoCapture(0)
# 接收socket返回
def receive_cmd(*args):
    print('receive_cmd', args)
    back_result = args[0]["param"]["action"]
    print(back_result)
    if(back_result):
        print("接收到拍照指令----------")
# 注册socket
def register_socket():
    print("进入注册")
    with SocketIO('101.37.151.52', 3000, LoggingNamespace) as socketIO:
        socketIO.emit('cmd_register',{ 'deviceId': '142857', 'from': '777'})
        socketIO.on('cmd', receive_cmd)
        socketIO.wait()
# 这个方法调用socket监听返回,不会影响其他程序运行
_thread.start_new_thread(register_socket,())

tt = 1
while True:
    if tt == 1:
        print("进来了")
        tt = 0
    ret,frame = cap.read()
    cv.imshow('frame',frame)
    cv.waitKey(1)

#-*-coding: utf-8 -*
import face_recognition
import cv2
import numpy as np

# 这是一个从你的网络摄像头实时视频运行人脸识别的演示。这比另一个例子要复杂一点，但它包括一些基本的性能调整，使事情运行得更快：
#   1. 以1/4分辨率处理每个视频帧（尽管仍以全分辨率显示）
#   2. 只检测其他视频帧中的人脸。
# 请注意：此示例要求只安装opencv（cv2库）以从网络摄像机中读取。使用人脸识别库时，不需要使用opencv。只有在您想运行这个特定的演示时才需要它。如果您在安装它时遇到问题，请尝试其他不需要它的演示。

# 获取对网络摄像机的引用0（默认值）
video_capture = cv2.VideoCapture(0)

#加载示例图片并学习如何识别它。
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# 加载第二个示例图片并学习如何识别它。
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# 创建已知人脸编码及其名称的数组
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

# 初始化一些变量
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # 抓取一帧视频
    ret, frame = video_capture.read()

    # 将视频帧的大小调整为1/4，以便更快地进行人脸识别处理
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # 将图像从bgr颜色（opencv使用）转换为rgb颜色（人脸识别使用）
    rgb_small_frame = small_frame[:, :, ::-1]

    # 只处理其他每帧视频以节省时间
    if process_this_frame:
        # 查找当前视频帧中的所有face和face编码
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 看看这张脸是否与已知的脸匹配(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # 如果在已知的面部编码中发现匹配，只需使用第一个。
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, 使用与新面距离最小的已知面
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # 显示结果
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # 自我们检测到的帧被缩放到1/4大小后，将备份面位置缩放
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 在脸上画一个方框
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 在面下绘制一个名称为的标签
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # 显示结果图像
    cv2.imshow('Video', frame)

    # 点击键盘上的“Q”退出！
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头手柄
video_capture.release()
cv2.destroyAllWindows()

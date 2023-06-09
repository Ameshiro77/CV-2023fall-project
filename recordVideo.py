"""
This .py is used to record video
"""

import cv2,os
from utils.calibrate import normal_undistort

from configs.Intrinsic_normal import cameraMatrix , distCoeff
cap = cv2.VideoCapture(0)  # 打开摄像头

fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 视频编解码器
fps = cap.get(cv2.CAP_PROP_FPS)  # 帧数
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 宽高
out = cv2.VideoWriter('result8.avi', fourcc, fps, (width, height))  # 写入视频

images_count = len(os.listdir("video"))  # num of current images
id = images_count  # don't +1 because id starts from 0

while cap.isOpened():
    ret, frame = cap.read()
    if ret == True:
        frame = normal_undistort(frame,cameraMatrix , distCoeff)
        cv2.imshow('frame', frame)
        out.write(frame)  # 写入帧
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):  # q退出
            break
        elif key == ord('c'):
            img_path = f'video/{id}.png'  # save into the folder
            cv2.imwrite(img_path, frame)
            print(f'captured at {img_path}')
            id += 1
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()


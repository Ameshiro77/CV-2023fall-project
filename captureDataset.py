"""
This .py is to capture images as datasets used for object-dececting.
本程序用于拍摄数据集。 
"""

import cv2
from configs.Intrinsic_normal import cameraMatrix, distCoeff
from utils.capture import Capture
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    print("width={}".format(cap.get(3)))
    print("height={}".format(cap.get(4)))
    print("exposure={}".format(cap.get(15)))

    cap.set(cv2.CAP_PROP_BRIGHTNESS, 120)  # 亮度
    cap.set(cv2.CAP_PROP_CONTRAST, 32)  # 对比度
    cap.set(cv2.CAP_PROP_SATURATION, 64)  # 饱和度 
    cap.set(cv2.CAP_PROP_HUE, 0)  # 色调 
    cap.set(cv2.CAP_PROP_EXPOSURE, -6.5)  # 曝光 

    Capture("./yolov7-detection/datasets/InstantNoodlesDataset/data/images",
            -1, cap, isUndistort=True, K=cameraMatrix, D=distCoeff, isPreClean=False)

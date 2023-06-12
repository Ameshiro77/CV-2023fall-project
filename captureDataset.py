"""
This .py is to capture images as datasets used for object-dececting.
本程序用于拍摄数据集。 
"""

import cv2
from configs.Intrinsic_normal import cameraMatrix, distCoeff
from utils.capture import Capture
if __name__ == '__main__':
    cap = cv2.VideoCapture("video/test.avi")
    Capture("./video",
            -1, cap, isUndistort=False, K=cameraMatrix, D=distCoeff, isPreClean=False)

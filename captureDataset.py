"""
This .py is to capture images as datasets used for object-dececting.
本程序用于拍摄数据集。 
"""

import cv2
from configs.Intrinsic_normal import cameraMatrix, distCoeff
from utils.capture import Capture
if __name__ == '__main__':
    cap = cv2.VideoCapture(1)

 

    Capture("./yolov7-detection/datasets/SpeedBumpDataset/data/images",
            -1, cap, isUndistort=True, K=cameraMatrix, D=distCoeff, isPreClean=False)

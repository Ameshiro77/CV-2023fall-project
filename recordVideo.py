import cv2
from utils.calibrate import Capture,normal_undistort
from configs.Intrinsic_normal import cameraMatrix , distCoeff
import os
import torch


if __name__ == "__main__":
    # load model
    model = torch.load("./yolov7-detection/weights/yolov7.pt")
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = normal_undistort(frame,cameraMatrix , distCoeff)

       
        

        #cv2.imshow('press c to capture , q to exit..', frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            break
    cv2.destroyAllWindows()

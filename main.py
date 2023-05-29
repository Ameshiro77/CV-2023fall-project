import cv2
from configs.Intrinsic_normal import cameraMatrix,distCoeff
from utils.calibrate import Capture
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    Capture("./groundImg",1,cap)
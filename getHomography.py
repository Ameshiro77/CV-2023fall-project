"""
This .py is to compute H between two planes:image plane and ground plane
(本程序实现：求解成像平面和大地平面的单应矩阵)
"""

import cv2
import numpy as np
from utils.calibrate import *
from utils.capture import Capture
from utils.opFile import writeHomographyToFile
from configs.Intrinsic_normal import cameraMatrix,distCoeff

imgps = []
objps = [[0,0],[100,100],[200,200],[300,300]]

# mouse callback function
def click_corner(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        print(x,y)
        if len(imgps) >= len(objps):
            print("nums of imgps points exceed!")
            return
        else:
            imgps.append([x,y])
        
if __name__ == '__main__':

    # capture a image
    cap = cv2.VideoCapture(0)

    # Capture("./groundImg",1,cap,True,cameraMatrix,distCoeff)
    img = cv2.imread("./groundImg/0.png")
    cv2.destroyAllWindows()

    # click the corner
    cv2.namedWindow("groundBoard")
    cv2.setMouseCallback("groundBoard",click_corner)
    
    while(1):
        cv2.imshow("groundBoard", img)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            imgps = np.array(imgps,dtype=np.float32)  # change type to np.ndarray
            objps = np.array(objps,dtype=np.float32)
            H , _ = cv2.findHomography(imgps,objps)
            writeHomographyToFile("./configs/homography.py",H)
            print(H,type(H))
            break

    
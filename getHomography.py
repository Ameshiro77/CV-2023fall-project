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
# 322,380 422,330 408,313 238,317
objps = [[2100,3200],[-2000.2,3200],[2100,9010],[-2000.2,9010]] 
# 一段长320cm
# 二段长320cm
# 三段长261cm
# 右宽 210cm
# 左宽 200.2cm

# mouse callback function
def click_corner(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        if len(imgps) >= len(objps):
            print("nums of imgps points exceed!")
            return
        else:
            print(x,y)
            imgps.append([x,y])
        
if __name__ == '__main__':

    # capture a image
    cap = cv2.VideoCapture(1)

    #Capture("./groundImg",1,cap,True,cameraMatrix,distCoeff)
    img = cv2.imread("./groundImg/0.png")
    cv2.destroyAllWindows()

    # click the corner
    cv2.namedWindow("groundBoard")
    cv2.setMouseCallback("groundBoard",click_corner)
    
    while(1):
        cv2.imshow("groundBoard", img)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            # imgps = [[322,380],[322,330],[ 408,313],[ 238,317]]
            imgps = np.array(imgps,dtype=np.float32)  # change type to np.ndarray
            objps = np.array(objps,dtype=np.float32)
            H , _ = cv2.findHomography(imgps,objps)

            dst = cv2.warpPerspective(img,H,(800,600))
            cv2.imshow("img",dst)
            cv2.waitKey(0)

            writeHomographyToFile("./configs/homography.py",H)
            print(H,type(H))
            break

    
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

imgps = [[319,349],[155,281],[320,284],[500,281],[224,260],[319,260],[443,260],[321,247],[320,227],[319,308],[449,310],[239,284]] #mm
objps = [[0,300],[-300,600],[0,600],[300,600],[-300,900],[0,900],[300,900],[0,1200],[0,5100],[0,450],[150,450],[-150,600]]  #mm

# 322,380 422,330 408,313 238,317
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
            print(x,y)
            return
        else:
            print(x,y)
            imgps.append([x,y])
        
if __name__ == '__main__':

    # capture a image
    cap = cv2.VideoCapture(0)

    #Capture("./groundImg",1,cap,True,cameraMatrix,distCoeff,False)
    img = cv2.imread("./groundImg/6.png")
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

            dst = cv2.warpPerspective(img,H,(3000,2000))
            dst = cv2.resize(dst,[800,600])
            # cv2.imwrite("result.png",dst)
            cv2.imshow("img",dst)
            cv2.waitKey(0)

            writeHomographyToFile("./configs/homography.py",H)
            print(H,type(H))
            break

    
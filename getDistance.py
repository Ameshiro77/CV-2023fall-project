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
from utils.measureDistance import getDistance

# mouse callback function
def click_corner(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        print(x,y)
        dist = round(getDistance(x,y),5)
        print("dist=",dist,"m")

        
if __name__ == '__main__':

    img = cv2.imread("./groundImg/61.png")
    cv2.destroyAllWindows()

    # click the corner
    cv2.namedWindow("groundBoard")
    cv2.setMouseCallback("groundBoard",click_corner)
    
    while(1):
        cv2.imshow("groundBoard", img)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            break

    
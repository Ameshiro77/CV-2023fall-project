import cv2
import numpy as np
import random

# mouse callback function
def click_corner(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        print(x,y,img[x,y])


if __name__ == "__main__":
    # cap = cv2.VideoCapture("video/result3.avi")
    img = cv2.imread("./video/80.png",cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow("1")
    #cv2.setMouseCallback("1",click_corner)
    while(1):
        # ret, img = cap.read()
        if 1 == True:
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            thre , dst = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
            # ret, frame = cap.read()
            cv2.imshow("dst",dst)
            key = cv2.waitKey(1) & 0xff
            if key == ord('q') or key == ord('Q'):
                break
        else:
            break

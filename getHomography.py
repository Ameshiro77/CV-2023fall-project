import cv2
from utils.calibrate import *
from configs.Intrinsic_normal import cameraMatrix,distCoeff

# mouse callback function
def click_corner(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 1, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0,0,0), thickness = 1)
        print(x,y)
        
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
            break

    
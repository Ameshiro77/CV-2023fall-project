import cv2

# this function is to draw corners
def drawCorners(img,w,h,corners):
    cv2.drawChessboardCorners(img,(w,h),corners,True)
    img = cv2.resize(img,(800,600))
    cv2.imshow('corners',img)
    cv2.waitKey(0)
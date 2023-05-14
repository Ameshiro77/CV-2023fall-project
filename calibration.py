"""
This .py is to do:
1. capture 
2. calibrate camera (normal or fisheye) using photos captured
3. undistort the image using K and D by calibrarion result 
"""
# ==========
import cv2
import numpy as np
from utils.drawing import drawCorners
from utils.opFile import writeIntriToFile,cleanFolder
from utils.calibrate import normal_undistort,Board,Calibrate
# ==========

"""
this function is to take photos to calibrate
parameters:
    folder: where the photos will be saved
    num: how many photos will take
return: none
"""
def Capture(folder:str,num: int, cap: cv2.VideoCapture) -> None:
    count = 0   # nums of photos captured
    while True:
        success, frame = cap.read()
        if not success or count >= num:
            break
        cv2.imshow('press c to capture , q to exit..', frame)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            break

        elif key == ord('c'):
            img_path = f'{folder}/{count}.png'  # save into the folder
            cv2.imwrite(img_path, frame)
            print(f'captured at {img_path}')
            count += 1

"""
this function is to undistort
"""
def undistort(img,cameraMatrix , distCoeff, mode = "normal"): # correct the image 
    if mode == "normal":
        dst = normal_undistort(img,cameraMatrix , distCoeff)
        print("dst shape:",dst.shape)
        cv2.imshow("img",dst)
        cv2.waitKey(0)  
        cv2.imwrite('calibresult.png', dst)
    
    else:
        img_undistorted = cv2.fisheye.undistortImage(img, cameraMatrix, distCoeff)
        cv2.imshow('Undistorted Image', img_undistorted)
        cv2.waitKey(0)

if __name__ == '__main__':
    print("please select the action...")
    print("[1]capture [2]calibrate [3]undistort")
    cameraMatrix,distCoeff = None,None
    selec = input()
    if selec == '1':
        # delete the formal photos
        cleanFolder("./caliImg")
        print("former photos have been cleaned up.taking new photos.")
        cap = cv2.VideoCapture(0)
        Capture("./caliImg",5,cap)
    
    elif selec == '2':
        board = Board(11,8,10) #col row width(mm)
        mode = input("choose your camera type: [1]normal [2]fisheye\n")
        if mode == '1':
            cameraMatrix,distCoeff = Calibrate("caliImg",board,mode="normal",out_file="./configs/Intrinsic_normal.py")
        elif mode == '2':
            cameraMatrix,distCoeff = Calibrate("caliImg",board,mode="fisheye",out_file="./configs/Intri_fisheye.py")  
        else:
            print("error input.exit.")

    elif selec == '3':
        img = cv2.imread("./caliImg/0.png")
        mode = input("choose your camera type: [1]normal [2]fisheye\n")
        if mode == '1':
            from configs.Intrinsic_normal import cameraMatrix,distCoeff
            undistort(img,cameraMatrix,distCoeff,mode = "normal")
        elif mode == '2':
            from configs.Intrinsic_fisheye import cameraMatrix,distCoeff
            undistort(img,cameraMatrix,distCoeff,mode = "fisheye")
        else:
            print("error input.exit.")

    else:
        print("illegal input.exit.")
  

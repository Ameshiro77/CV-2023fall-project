"""
This .py is to do:
1. capture 
2. calibrate camera (normal or fisheye) using photos captured
3. undistort the image using K and D by calibrarion result 
(本程序用来拍照标定板、标定、去畸变)
"""
# ==========
import cv2
from utils.calibrate import normal_undistort, Board, Calibrate
from utils.capture import Capture
# ==========

"""
this function is to undistort
"""


def undistort(img, cameraMatrix, distCoeff, mode="normal"):  # correct the image
    if mode == "normal":
        dst = normal_undistort(img, cameraMatrix, distCoeff)
        print("dst shape:", dst.shape)
        cv2.imshow("img", dst)
        cv2.waitKey(0)

    else:
        img_undistorted = cv2.fisheye.undistortImage(
            img, cameraMatrix, distCoeff)
        cv2.imshow('Undistorted Image', img_undistorted)
        cv2.waitKey(0)


if __name__ == '__main__':
    print("please select the action...")
    print("[1]capture [2]calibrate [3]undistort")
    cameraMatrix, distCoeff = None, None
    selec = input()
    if selec == '1':
        print("former photos have been cleaned up.taking new photos.")
        cap = cv2.VideoCapture(0)
        # clean the dst folder first
        Capture("./caliImg", 5, cap, isPreClean=True)

    elif selec == '2':
        board = Board(11, 8, 10)  # col row width(mm)
        mode = input("choose your camera type: [1]normal [2]fisheye\n")
        if mode == '1':
            cameraMatrix, distCoeff = Calibrate(
                "caliImg", board, mode="normal", out_file="./configs/Intrinsic_normal.py")
        elif mode == '2':
            cameraMatrix, distCoeff = Calibrate(
                "caliImg", board, mode="fisheye", out_file="./configs/Intri_fisheye.py")
        else:
            print("error input.exit.")

    elif selec == '3':
        img = cv2.imread("./caliImg/0.png")
        mode = input("choose your camera type: [1]normal [2]fisheye\n")
        if mode == '1':
            from configs.Intrinsic_normal import cameraMatrix, distCoeff
            undistort(img, cameraMatrix, distCoeff, mode="normal")
        elif mode == '2':
            from configs.Intrinsic_fisheye import cameraMatrix, distCoeff
            undistort(img, cameraMatrix, distCoeff, mode="fisheye")
        else:
            print("error input.exit.")

    else:
        print("illegal input.exit.")

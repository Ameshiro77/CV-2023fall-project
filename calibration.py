import cv2
import numpy as np
import glob
from utils.drawing import drawCorners
from utils.opFile import writeIntriToFile,cleanFolder
import os

"""
Board class: you need to preset the cols,rows and width of the board
    cols: nums of corners per row
    rows: nums of corners per col
    width: gap length between two neighbor corner
"""
class Board:
    def __init__(self,col,row,width) -> None:
        self.COL = col # num of corners' cols
        self.ROW = row # num of corners' rows
        self.width = width # length(mm) between rows/cols in real world
        pass

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
this function is to calibrate
and return K and distortion coefficience
parameters:
    board_folder: where the boards image lies , example: "./img"
    mode : normal or fisheye | defautl:normal
    out_file: where the result will output
return :
    cameraMatrix,distCoeff
"""
def Calibrate(board_folder:str,board:Board,mode="normal",out_file:str="./configs/intri.py"):
    objPoints = []  # 3D world's points
    imgPoints = []  # 2D corner points

    # get 3D points 
    objp = np.zeros((board.ROW*board.COL,1,3),np.float32)  #!!! (N,1,3)
    objp[:,0,:2] = np.mgrid[0:board.COL,0:board.ROW].T.reshape(-1,2)
    objp = objp * board.width # single board size length (mm)
    #print(objp)
    h, w = 0 , 0

    imageSets = glob.glob(board_folder+'/*.png') #images of boards captured
    for frame in imageSets:
        img = cv2.imread(frame)
        h,w,_ = img.shape  # !!!it is not (w,h) but (h,w)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # remove channels

        # append 3D points
        objPoints.append(objp)

        # get corners and append
        _, corners = cv2.findChessboardCorners(gray, (board.COL, board.ROW), None)  # corner: N,1,2
        imgPoints.append(corners)   

        print("objp:",objp,"\ncorners:",corners)
        #if no match 
        if len(objPoints[0]) != len(imgPoints[0]):
            print(f"no match in {frame}!")
            return
        
        # show photo
        drawCorners(img,board.COL, board.ROW,corners)

    if mode == "fisheye" :
        K = np.array(np.zeros((3, 3)))
        D = np.array(np.zeros((4, 1)))
        criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        rvecs = [np.zeros((1, 1, 3), dtype=np.float32) for i in range(len(imageSets))]
        tvecs = [np.zeros((1, 1, 3), dtype=np.float32) for i in range(len(imageSets))]
        ret, K, D, rvecs, tvecs = cv2.fisheye.calibrate(objPoints, imgPoints, (w,h), K, D, rvecs, tvecs,criteria=criteria)
        print(K,D)
        return K,D

    else:
        _ , cameraMatrix , distCoeff, rvec , tvec = cv2.calibrateCamera(objPoints,imgPoints,(w,h),None,None)
        print("====results of calibration====")
        print("error:",_,"num of boards :",len(rvec),len(tvec))
        print("K:",cameraMatrix , "\ndistcoeff:",distCoeff)
        writeIntriToFile(out_file,cameraMatrix,distCoeff)
        return cameraMatrix,distCoeff

"""
this function is to undistort
"""
def undistort(img,cameraMatrix , distCoeff, mode = "normal"): # correct the image 
    if mode == "normal":
        h,  w = img.shape[:2]
        # we set alpha = 0 : reserve black pixels
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeff, (w,h), 0, (w,h),centerPrincipalPoint=False)
        print('\nK,new_K,roi:\n','K:',cameraMatrix,'\nnew K:',newcameramtx,'\nroi:',roi)
        # undistort
        mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix,  distCoeff, None, cameraMatrix, (w,h), 5)
        dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        print(dst.shape)
        cv2.imshow("img",cv2.resize(dst,(640,480)))
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
        board = Board(11,8,1) #col row width(mm)
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
  

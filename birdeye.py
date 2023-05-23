from utils.calibrate import Board,normal_undistort
import cv2
import numpy as np

def getBirdEyeImage(board:Board,K,D,file="./caliImg/0.png"):
    # get board plane points 
    objp = np.zeros((board.ROW*board.COL,1,2),np.float32)  #!!! (N,1,2)
    objp[:,0,:2] = np.mgrid[0:board.COL,0:board.ROW].T.reshape(-1,2)
    objp = objp * board.width + 200 # single board size length (mm)

    img = cv2.imread(file)
    img = normal_undistort(img,K,D)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # remove channels

    # get corners
    _, corners = cv2.findChessboardCorners(gray, (board.COL, board.ROW), None)  # corner: N,1,2
    criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), criteria)
        
    H , _ = cv2.findHomography(corners,objp)
    print(H)
    dst = cv2.warpPerspective(img,H,(800,600))
    cv2.imshow("img",dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    board = Board(11,8,10) #col row width(mm)
    from configs.Intrinsic_normal import cameraMatrix,distCoeff
    getBirdEyeImage(board,cameraMatrix,distCoeff)
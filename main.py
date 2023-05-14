import cv2
from configs.Intrinsic_normal import cameraMatrix,distCoeff
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.fisheye.undistortImage(frame, cameraMatrix, distCoeff)
        cv2.imshow('camera',frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            break
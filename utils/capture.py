import cv2
import os
from utils.calibrate import normal_undistort
from utils.opFile import cleanFolder
"""
this function is to take images to calibrate
parameters:
    folder: where the photos will be saved
    num: how many photos will take. if num == -1,then there is no limit.
    isUndistort: whether to undistort the token image
    isPreClean: whether to clean the dst folder. if not,the id of the images will follow the current images.
return: none
"""


def Capture(folder: str, num: int, cap: cv2.VideoCapture, isUndistort=False, K=None, D=None, isPreClean=False) -> None:
    if isPreClean == True:
        cleanFolder(folder)

    count = 0   # nums of photos captured this time
    images_count = len(os.listdir(folder))  # num of current images
    id = images_count  # don't +1 because id starts from 0

    while True:
        success, frame = cap.read()
        if (num != -1) and (not success or count >= num):
            break

        if isUndistort == True:
            frame = normal_undistort(frame, K, D)

        cv2.imshow('press c to capture , q to exit..', frame)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            break

        elif key == ord('c'):
            img_path = f'{folder}/{id}.png'  # save into the folder
            cv2.imwrite(img_path, frame)
            print(f'captured at {img_path}')
            id += 1

import cv2

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        cv2.imshow('camera',frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q') or key == ord('Q'):
            break
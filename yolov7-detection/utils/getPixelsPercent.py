import cv2
THRESHOLD = 100 #二值化阈值

def getPixelsPercent(img , c1 , c2):
    # print("====")
    # print(img.shape)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thre , dst = cv2.threshold(img,THRESHOLD,255,cv2.THRESH_BINARY)
    x_tl = c1[0]  # bbox的 左上角xy 右下角xy 像素坐标
    y_tl = c1[1]
    x_rb = c2[0]
    y_rb = c2[1]
    # print(c1,c2)
    h = y_rb - y_tl
    w = x_rb - x_tl
    nums_of_lightBump = 0 # 减速带黄色的那部分 二值化出来
    for x in range(w):
        for y in range(h):
            pixel_value = dst[ y_tl + y  , x_tl + x ]
            # dst[ y_tl + y  , x_tl + x ] = 0
            if pixel_value < THRESHOLD:  #如果是白色的，就是说 是黄色的那部分
                nums_of_lightBump += 1
    nums_of_total = h * w  # 总bbox的像素数
    percent = nums_of_lightBump / nums_of_total 
    # while(1):
    #     cv2.imshow("1",dst)
    #     key = cv2.waitKey(1) & 0xff
    #     if key == ord('q') or key == ord('Q'):
    #         break
    return percent



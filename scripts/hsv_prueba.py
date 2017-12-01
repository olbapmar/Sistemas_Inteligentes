import cv2
import numpy as np
import glob

SIZE = 128

for file in glob.glob('./dataset/signals/samples/*'):
    img = cv2.imread(file)
    img = cv2.resize(img, (SIZE, SIZE))
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Limites de rojo
    low_red1 = np.array([0, 50, 50])
    up_red1 = np.array([15, 255, 255])
    low_red2 = np.array([240, 50, 50])
    up_red2 = np.array([255, 255, 255])

    mask1 = cv2.inRange(img_hsv, low_red1, up_red1)
    mask2 = cv2.inRange(img_hsv, low_red1, up_red1)

    end = cv2.bitwise_or(mask1, mask2)
    kernel = np.ones((3, 3), np.uint8)
    end = cv2.dilate(end, kernel)

    end2 = cv2.bitwise_and(img, img, mask=end)

    cv2.imshow('imagen', end2), cv2.waitKey(1000)
import cv2
import glob

surf = cv2.xfeatures2d.SURF_create(10000)

for file in glob.glob('./dataset/signals/*'):
    img = cv2.imread(file)
    kp, des = surf.detectAndCompute(img, None)
    img2 = cv2.drawKeypoints(img, kp, None, (255, 0, 0), 4)
    cv2.imshow("imagen", img2), cv2.waitKey(10000)

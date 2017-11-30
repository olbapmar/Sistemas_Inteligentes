import cv2
import glob

surf = cv2.xfeatures2d.SURF_create(10000)

descriptores = []
keypoints = []
images = []

for file in glob.glob('./dataset/signals/*.png'):
    img = cv2.imread(file)
    kp, des = surf.detectAndCompute(img, None)
    img2 = cv2.drawKeypoints(img, kp, None, (255, 0, 0), 4)
    cv2.imshow("imagen", img2), cv2.waitKey(500)
    descriptores.append(des)
    keypoints.append(kp)
    images.append(img)


img2 = cv2.imread('./dataset/signals/samples/120.PNG')
img2 = cv2.resize(img2, (img.shape[0] + 100, img.shape[1] + 100))
kp2, des2 = surf.detectAndCompute(img2, None)

bf = cv2.BFMatcher()

matches = bf.match(descriptores[1], des2)


img3 = cv2.drawMatches(images[1], keypoints[1], img2, kp2, matches, None)

print(sum(m.distance for m in matches) / len(matches))

cv2.imshow("imagen", img3), cv2.waitKey(0)
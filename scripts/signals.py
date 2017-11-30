import cv2
import json

SIZE = 128

surf = cv2.xfeatures2d.SURF_create(8000)

descriptores = []
keypoints = []
images = []
archivos = []
nombres = []

signals_data = json.load(open('./dataset/signals/signals.json'))
for s in signals_data:
    archivos.append(signals_data[s])
    nombres.append(s)

for file in archivos:   
    img = cv2.imread('./dataset/signals/' + file)
    img = cv2.resize(img, (SIZE, SIZE))
    kp, des = surf.detectAndCompute(img, None)
    descriptores.append(des)
    keypoints.append(kp)
    images.append(img)

img2 = cv2.imread('./dataset/signals/samples/Ceda.PNG')
img2 = cv2.resize(img2, (120, 120))
kp2, des2 = surf.detectAndCompute(img2, None)
bf = cv2.BFMatcher()
for i in range(len(images)):
    matches = bf.match(descriptores[i], des2)
    img3 = cv2.drawMatches(images[i], keypoints[i], img2, kp2, matches, None)
    print(nombres[i] + ": " + str(sum(m.distance for m in matches) / len(matches)))
    cv2.imshow("imagen", img3), cv2.waitKey(0)
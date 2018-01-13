import cv2
import numpy as np
import glob


def detectar_rojo(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Limites de rojo
    low_red1 = np.array([0, 50, 50])
    up_red1 = np.array([25, 255, 255])
    low_red2 = np.array([155, 50, 50])
    up_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(img_hsv, low_red1, up_red1)
    mask2 = cv2.inRange(img_hsv, low_red2, up_red2)

    end = cv2.bitwise_or(mask1, mask2)

    return end


for file in glob.glob('../dataset/real/prohibido_paso.jpg'):
    img = cv2.imread(file)
    
    mask = detectar_rojo(img)
    #end2 = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.GaussianBlur(mask, (9, 9), 2, 2)
    cv2.imshow('imagen', mask), cv2.waitKey(0)

    circulos = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20,  param2=30, minRadius=5, maxRadius=(int)(img.shape[0] / 4))

    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        regiones = []
        for i in circulos[0, :]:
            radio = i[2]
            esq = [i[0] - radio, i[1] - radio]
            aux = cv2.resize(img[esq[1]:(esq[1] + radio*2), esq[0]:(esq[0] + radio*2)], (500, 500))
            regiones.append(aux)

        surf = cv2.xfeatures2d.SURF_create(1000)
        bf = cv2.BFMatcher()
        for img in regiones:
            cv2.imshow('region', img), cv2.waitKey(0)
            kp1, des1 = surf.detectAndCompute(cv2.UMat(img), None)

            img2 = cv2.imread('../dataset/signals/80.png')
            kp2, des2 = surf.detectAndCompute(cv2.UMat(img2), None)

            matches = bf.match(des1, des2)
            img3 = cv2.drawMatches(img, kp1, img2, kp2, matches, None)
            cv2.imshow('a', img3), cv2.waitKey(0)
            print(str(sum(m.distance for m in matches) / len(matches)))
        #cv2.imshow('imagen', img), cv2.waitKey(0)
        
        

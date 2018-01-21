import cv2
import numpy as np
import math 


class Semaforo:

    def contornos(self, img):
        # Pasamos la imagen a blanco y negro
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        topHat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, np.ones((11, 11),
                                  np.uint8))
        
        topHat = cv2.GaussianBlur(topHat, (3, 3), 1, 1)
        _, topHat = cv2.threshold(topHat, 127, 255, cv2.THRESH_BINARY)
        _, contornos, herencia = cv2.findContours(topHat, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # contornos = contornos[0] if imutils.is_cv2() else contornos[1]
        herencia = herencia[0]
        cnts2 = []

        for i in range(0, len(contornos)):
            (x, y, w, h) = cv2.boundingRect(contornos[i])
            
            max = h
            min = w
            if (w > h):
                max = w
                min = h

            # cv2.isContourConvex(contornos[i]) and hierarchy[i][2] == -1
            if ((max / min < 1.8 and max < 20 and min > 2) and cv2.isContourConvex(contornos[i]) and herencia[i][2] == -1):
                cnts2.append(contornos[i])

        cnts3 = [] 

        for i in range(0, len(cnts2)):
            (x, y, w, h) = cv2.boundingRect(cnts2[i])
            
            mask_aux = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
            maskval = 255
            flags = 8 | ( maskval << 8 ) | cv2.FLOODFILL_MASK_ONLY
            _, __, ___, rect = cv2.floodFill(img, mask_aux, (x + int(w/2), y + int(h/2)), (255,0,255), (20,20,20), (20,20,20), flags)
            if (math.fabs(w - rect[2]) < 10 and math.fabs(h - rect[3]) < 10):
                cnts3.append(cnts2[i])

            #cv2.circle(img_gray, (x + int(w/2), y + int(h/2)), 2, (255,0,0), -1, 8, 0)
            cv2.imshow("", mask_aux)

        print(str(len(cnts2)) + " " + str(len(cnts3)))
        return cnts3




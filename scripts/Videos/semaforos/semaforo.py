import cv2
import numpy as np
import math 


class Semaforo:

    def contornos(self, img):
        # Pasamos la imagen a blanco y negro
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        topHat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, np.ones((11, 11),
                                  np.uint8))
        
        cv2.imshow("Top-Hat", topHat)
        cv2.waitKey(1)

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

        #img_copy = img.copy()
        #cv2.drawContours(img_copy, cnts2, -1, (0, 255, 0), 2)
        #cv2.imshow("Pre-floodfill",img_copy)
        #cv2.waitKey(1)

        cnts3 = []
        boundingRects = [] 

        for i in range(0, len(cnts2)):
            (x, y, w, h) = cv2.boundingRect(cnts2[i])
            
            mask_aux = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
            maskval = 255
            flags = 8 | (maskval << 8 ) | cv2.FLOODFILL_MASK_ONLY
            _, __, ___, rect = cv2.floodFill(img, mask_aux, (x + int(w/2), y + int(h/2)), (255,0,255), (20,20,20), (20,20,20), flags)
            
            max = rect[3]
            min = rect[2]
            if (w > h):
                max = rect[2]
                min = rect[3]

            if (math.fabs(w - rect[2]) < 10 and math.fabs(h - rect[3]) < 10
                 and (max / min) < 1.3):

                cnts3.append(cnts2[i])
                boundingRects.append([x, y, w, h])

            #cv2.circle(img_gray, (x + int(w/2), y + int(h/2)), 2, (255,0,0), -1, 8, 0)
            #cv2.imshow("", mask_aux)

        print(str(len(cnts2)) + " " + str(len(cnts3)))
        
        self.templateMatching(img, cnts3, boundingRects)

        return cnts3

    def templateMatching(self, img, contornos, boundingRects):

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        for i in range(0, len(contornos)):
            diametro = max(boundingRects[i][2], boundingRects[i][3])
            centro = (boundingRects[i][0] + int((boundingRects[i][2] / 2)),
                      boundingRects[i][1] + int((boundingRects[i][3] / 2)))
            
            width = int(1.5 * diametro)
            height = int(5 * diametro)

            x = centro[0] - int(width / 2)
            y = centro[1] - int((0.2 * height + diametro / 2))

            cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 255), 1)
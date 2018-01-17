from circularSignals import CircularSignals
from triangularSignals import TriangularSignals
from octogonalSignals import OctogonalSignals
from threading import Thread

import time
import cv2
import numpy as np
import imutils


class VideoHandler:

    def __init__(self):
        self.frame = None
        self.video = None
        self.noParar = True
        pass

    def calcularContornos(self, mask):
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        cnts2 = []
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        for c in cnts:
        
            (x, y, w, h) = cv2.boundingRect(c)
            # (x, y), radio = cv2.minEnclosingCircle(c)
            max = h
            min = w
            if (w > h):
                max = w
                min = h

            if ((max / min < 1.4) and (max < 200) and (min > 10)):
                cnts2.append(c)

        return cnts2

    def calcular_mascara(self, img):

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Limites de rojo
        low_red1 = np.array([0, 40, 40])
        up_red1 = np.array([20, 255, 255])
        low_red2 = np.array([160, 40, 40])
        up_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(img_hsv, low_red1, up_red1)
        mask2 = cv2.inRange(img_hsv, low_red2, up_red2)

        end = cv2.bitwise_or(mask1, mask2)
        # end = cv2.erode(end, np.ones((3, 3)))
        end = cv2.dilate(end, np.ones((3, 3)))
        end = cv2.GaussianBlur(end, (5, 5), 2, 2)

        return end

    def start(self, video):

        self.video = video

 
        Thread(target=self.updateVideo, args=()).start()
        

        triangulo = TriangularSignals()
        octogono = OctogonalSignals()
        circular = CircularSignals()

        while self.frame is not None:

            # start = time.time()

            img = self.frame
            mask = self.calcular_mascara(img)
            contorno = self.calcularContornos(mask)

            # Actualiza señales triangulares
            triangulo.actualizaImagen(img)
            triangulo.actualizaMascara(mask)
            triangulo.actualizaContorno(contorno)
            triangulo.findSignals()

            # Actualiza señales octogonales
            octogono.actualizaImagen(triangulo.img)
            octogono.actualizaMascara(mask)
            octogono.actualizaContorno(contorno)
            octogono.findSignals()

            # Actualizar señales circulares
            circular.actualizaImagen(octogono.img)
            circular.actualizaMascara(mask)
            circular.findSignals()
            
            cv2.imshow('imagen', octogono.img)
            cv2.imshow('mask', mask)    

            # print(int(1/24*1000) - (int)(start - end))
            cv2.waitKey(1)

    def updateVideo(self):

        vidFile = cv2.VideoCapture(self.video)
        #fps = vidFile.get(cv2.CV_CAP_PROP_FPS)
        ret, img = vidFile.read()
        self.frame = cv2.resize(img, (853, 480), interpolation = cv2.INTER_LINEAR)

        time.sleep(7)
        while ret and self.noParar:

            ret, img = vidFile.read()
            self.frame = cv2.resize(img, (853, 480), interpolation = cv2.INTER_LINEAR)
            time.sleep(1/25)





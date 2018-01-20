from circularSignals import CircularSignals
from triangularSignals import TriangularSignals
from octogonalSignals import OctogonalSignals
from threading import Thread
from threading import Event

import time
import cv2
import numpy as np
import imutils


class VideoHandler:

    def __init__(self):
        self.frame = None
        self.video = None
        self.noParar = True
        self.event = Event()
        pass

    def calcularContornos(self, mask):
        _, cnts, _ = cv2.findContours(mask, cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_SIMPLE)

        cnts2 = []
        # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        for c in cnts:
        
            (x, y, w, h) = cv2.boundingRect(c)
            # (x, y), radio = cv2.minEnclosingCircle(c)
            max = h
            min = w
            if (w > h):
                max = w
                min = h

            if ((max / min < 1.4) and (max < 200) and (min > 30)):
                cnts2.append(c)

        return cnts2

    def calcular_mascara(self, img):

        img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)

        # Limites de rojo
        # low_red1 = np.array([0, 30, 30])
        # up_red1 = np.array([20, 255, 255])
        # low_red2 = np.array([160, 30, 30])
        # up_red2 = np.array([180, 255, 255])

        # mask = cv2.inRange(img_hsv, low_red1, up_red1)
        # mask2 = cv2.inRange(img_hsv, low_red2, up_red2)
        # low = np.array([0,0,90])
        # up = np.array([80,80,255])
        # mask = cv2.inRange(img, low, up)

        lab_down = np.array([5, 150, 64])
        lab_up = np.array([240, 256, 191])

        mask = cv2.inRange(img_lab, lab_down, lab_up)

        # mask = cv2.bitwise_or(mask, mask2)
        # end = cv2.erode(mask, np.ones((3, 3)))
        end = cv2.dilate(mask, np.ones((3, 3)))
        end = cv2.GaussianBlur(mask, (3, 3), 1, 1)

        return end
    
     # Calcula la máscara usada para detectar los semáforos.
    
    def calcularMascaraSemaforo(self, img):

        # Pasamos la imagen a blanco y negro
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        topHat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, np.ones((11, 11),
                                  np.uint8))
        
        topHat = cv2.GaussianBlur(topHat, (3, 3), 1, 1)

        _, topHat = cv2.threshold(topHat, 127, 255, cv2.THRESH_BINARY)

        _, contornos, herencia = cv2.findContours(topHat, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow('topHat', topHat)

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
            if ((max / min < 1.8 and max < 20) and cv2.isContourConvex(contornos[i]) and herencia[i][2] == -1):
                cnts2.append(contornos[i])

        return cnts2

    def start(self, video):

        self.video = video
        Thread(target=self.updateVideo, args=()).start()
        
        self.event.wait()
        triangulo = TriangularSignals()
        octogono = OctogonalSignals()
        circular = CircularSignals()

        while self.frame is not None and self.noParar:

            # start = time.time()

            img = self.frame
            mask = self.calcular_mascara(img)
            #self.calcularMascaraSemaforo(img)
            cv2.drawContours(img, self.calcularMascaraSemaforo(img), -1, (0, 255, 0), 2)
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
            #cv2.imshow('mask Semaforo', maskSemaforo)  

            # print(int(1/24*1000) - (int)(start - end))
            cv2.waitKey(1)


    def updateVideo(self):

        vidFile = cv2.VideoCapture(self.video)
        # fps = vidFile.get(cv2.CV_CAP_PROP_FPS)
        ret, img = vidFile.read()
        self.frame = cv2.resize(img, (853, 480), interpolation = cv2.INTER_LINEAR)
        self.event.set()

        while ret and self.noParar:
            ret, img = vidFile.read()
            if ret:
                self.frame = cv2.resize(img, (853, 480), interpolation = cv2.INTER_LINEAR)
            time.sleep(1/25)

        self.noParar = False

    def parar(self):
        self.noParar = False

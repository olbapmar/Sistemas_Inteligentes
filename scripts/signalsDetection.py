from abc import ABCMeta, abstractmethod

import imutils
import cv2
import numpy as np


# Class that detects signals on an image.
class SignalsDetection:

    __metaclass__ = ABCMeta

    def __init__(self, img):
        
        self.img = img
        self.mask = self.detectar_rojo(self.img)
        self.detected = False  # True if a signal has been detected.
        self.numberSignals = 0  # Number of signals detected;
        # Shows binary image.
        cv2.imshow('imagen', self.mask), cv2.waitKey(0)

    def detectar_rojo(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Limites de rojo
        low_red1 = np.array([0, 50, 50])
        up_red1 = np.array([25, 255, 255])
        low_red2 = np.array([155, 50, 50])
        up_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(img_hsv, low_red1, up_red1)
        mask2 = cv2.inRange(img_hsv, low_red2, up_red2)

        end = cv2.bitwise_or(mask1, mask2)

        # end = cv2.erode(end, np.ones((8, 8)))
        # end = cv2.dilate(end, np.ones((9, 9)))
        end = cv2.GaussianBlur(end, (9, 9), 2, 2)

        return end
    
    # Returns the portions of the image that contain
    # signals.
    @abstractmethod
    def obtenerRegiones(self, detectedSignals):
        pass

    @abstractmethod
    def findSignals(self):
        pass

    def matchSignals(self, region):
        surf = cv2.xfeatures2d.SURF_create(1000)
        bf = cv2.BFMatcher()

        mejorResultado = 100
        signalType = ''

        cv2.imshow('region', region), cv2.waitKey(0)
        kp1, des1 = surf.detectAndCompute(cv2.UMat(region), None)

        for filename in self.signals:
            img2 = cv2.imread('../dataset/signals/' + filename + '.png')
            kp2, des2 = surf.detectAndCompute(cv2.UMat(img2), None)

            matches = bf.match(des1, des2)
            if (len(matches) != 0):
                img3 = cv2.drawMatches(region, kp1, img2, kp2, matches, None)
                cv2.imshow('a', img3), cv2.waitKey(0)
                resultadoActual = sum(m.distance for m in matches) / len(matches)
                if (resultadoActual < mejorResultado):
                    mejorResultado = resultadoActual
                    signalType = filename
        print(str(signalType) + ': ' + str(mejorResultado))


# Detects circular signals.
class CircularSignals(SignalsDetection):

    signals = ['30', '40', '50', '60', '70', '80', '100', '120',
               'no_adelantar', 'prohibido_paso']

    signalType = "circular"

    def findSignals(self):
        circulos = cv2.HoughCircles(self.mask, cv2.HOUGH_GRADIENT, 1, 20,
                                    param2=30, minRadius=5, maxRadius=(int)
                                    (self.img.shape[0] / 4))
        
        self.numberSignals = len(circulos[0])
        print("Detected " + str(self.numberSignals) + " " +
              self.signalType)
        
        if circulos is not None:
            circulos = np.uint16(np.around(circulos))
            regiones = self.obtenerRegiones(circulos)
            for img in regiones:
                self.matchSignals(img)

        # ccv2.imshow('imagen', img), cv2.waitKey(0)

    def obtenerRegiones(self, detectedSignals):
        regiones = []

        for i in detectedSignals[0, :]:
            radio = i[2]
            esq = [i[0] - radio, i[1] - radio]
            aux = cv2.resize(self.img[esq[1]:(esq[1] + radio*2), esq[0]:(
                esq[0] + radio*2)], (500, 500))

            regiones.append(aux)
        
        return regiones
    

# Detects triangular signals.
class NonCircularSignals(SignalsDetection):

    signals = []
    numberVertex = 0
    signalType = ''

    def findSignals(self):

        cnts = cv2.findContours(self.mask, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        triangulos = []

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if len(approx) == self.numberVertex:
                triangulos.append(c)

        self.numberSignals = len(triangulos)
        print("Detected " + str(self.numberSignals) + " " + self.signalType)

        if triangulos is not None:
            regiones = self.obtenerRegiones(triangulos)
            for img in regiones:
                self.matchSignals(img)
        
    def obtenerRegiones(self, detectedSignals):

        regiones = []

        for i in range(0, self.numberSignals):

            (x, y, w, h) = cv2.boundingRect(detectedSignals[i])
            aux = cv2.resize(self.img[y:(y + h), x:(x + w)], (500, 500))
            regiones.append(aux)

        return regiones


# Detects octogonal signals.
class OctogonalSignals(NonCircularSignals):

    signals = ['stop']
    numberVertex = 8
    signalType = "octogonal"


# Detects octogonal signals.
class TriangularSignals(NonCircularSignals):

    signals = ['ceda_paso']
    numberVertex = 3
    signalType = "triangular"


from signalsDetection import SignalsDetection
from region import Region
import cv2
import numpy as np


# Detects circular signals.
class CircularSignals(SignalsDetection):

    signals = ['30', '40', '50', '60', '70', '80', '100', '120',
               'no_adelantar', 'prohibido_paso']

    signalType = "circular"
    MINRADIOUS = 10
    MAXRADIOUS = 300

    def findSignals(self):
        circulos = cv2.HoughCircles(self.mask, cv2.HOUGH_GRADIENT, 1, 20,
                                    param2=30, minRadius=5, maxRadius=(int)
                                    (self.img.shape[0] / 4))
        
        print("Detected " + str(self.numberSignals) + " " +
              self.signalType)
        
        if circulos is not None:

            self.numberSignals = len(circulos[0])
            circulos = np.uint16(np.around(circulos))
            regiones = self.obtenerRegiones(circulos)
            if regiones is not None: 
                for img in regiones:
                    self.matchSignals(img)

        # ccv2.imshow('imagen', img), cv2.waitKey(0)

    def obtenerRegiones(self, detectedSignals):
        regiones = []

        for i in detectedSignals[0, :]:
            radio = i[2]

            if ((radio < self.MAXRADIOUS) and (radio > self.MINRADIOUS) and 
                  (i[0] - radio < 853) and (i[1] - radio < 480)):

                print(i[0] - radio)
                print(i[1] - radio)
                esq = [i[0] - radio, i[1] - radio]
               
                x = esq[0]
                y = esq[1]
                h = radio * 2
                w = h
                if ((y + h > 0) and (x + w > 0)):
                    aux = cv2.resize(self.img[y:(y + h), x:(x + w)], (500, 500))
                    regiones.append(Region(aux, x, y, w, h))
        
        return regiones

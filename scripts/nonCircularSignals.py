from signalsDetection import SignalsDetection
from region import Region
import cv2


# Detects non-circular signals.
class NonCircularSignals(SignalsDetection):

    signals = []
    numberVertex = 0
    signalType = ''

    def __init__(self):
        super().__init__()
        self.contorno = None

    def findSignals(self):
        cnts = self.contorno

        # cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        shape = []

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)
            if (self.signalType != 'circle'):
                if len(approx) == self.numberVertex:
                    shape.append(c)
            else:
                #print(len(approx))
                if len(approx) >= self.numberVertex:
                    shape.append(c)

        self.numberSignals = len(shape)
        # print("Detected " + str(self.numberSignals) + " " + self.signalType)

        if shape is not None:
            regiones = self.obtenerRegiones(shape)
            for img in regiones:
                self.matchSignals(img)
        
    def obtenerRegiones(self, detectedSignals):

        regiones = []

        for i in range(0, self.numberSignals):

            c = detectedSignals[i]
            (x, y, w, h) = cv2.boundingRect(c)
            aux = cv2.resize(self.img[y:(y + h), x:(x + w)], (500, 500))
            regiones.append(Region(aux, x, y, w, h))

        return regiones

    def actualizaContorno(self, contorno):
        self.contorno = contorno

from circularSignals import CircularSignals
from triangularSignals import TriangularSignals
from octogonalSignals import OctogonalSignals

import time
import cv2
import numpy as np
import imutils


def calcularContornos(mask):
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)

    cnts2 = []
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    for c in cnts:
       
        # (x, y, w, h) = cv2.boundingRect(c)
        (x, y), radio = cv2.minEnclosingCircle(c)
        if ((radio < 300) and (radio > 100)):
            cnts2.append(c)

    return cnts2


def calcular_mascara(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Limites de rojo
    low_red1 = np.array([0, 100, 100])
    up_red1 = np.array([25, 255, 255])
    low_red2 = np.array([155, 100, 100])
    up_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(img_hsv, low_red1, up_red1)
    mask2 = cv2.inRange(img_hsv, low_red2, up_red2)

    end = cv2.bitwise_or(mask1, mask2)

    # end = cv2.erode(end, np.ones((3, 3)))
    # end = cv2.dilate(end, np.ones((9, 9)))
    end = cv2.GaussianBlur(end, (9, 9), 2, 2)
    #cv2.imshow('imagen', end), cv2.waitKey(0)
    return end


#vidFile = cv2.VideoCapture(0)

#fps = 25

#ret, frame = vidFile.read() # read first frame, and the return code of the function.
#while ret:  # note that we don't have to use frame number here, we could read from a live written file.
    print("yes")
    #cv2.imshow("frameWindow", frame)
    #cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
    #ret, frame = vidFile.read()

    #img = frame

img = cv2.imread('../dataset/real/circulos.jpg')

img = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_LINEAR)
mask = calcular_mascara(img)
contorno = calcularContornos(mask)

triangulo = TriangularSignals(img, mask, contorno)

octogono = OctogonalSignals(img, mask, contorno)
# circulo2 = CircularSignals2(img, mask, contorno)
circular = CircularSignals(img, mask)

triangulo.findSignals()
octogono.img = triangulo.img
octogono.findSignals()
circular.img = octogono.img
start = time.time()
circular.findSignals()

end = time.time()
print(end - start)
cv2.imshow('imagen', circular.img), cv2.waitKey(0)



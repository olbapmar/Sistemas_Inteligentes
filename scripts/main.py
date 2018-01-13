from signalsDetection import *
import cv2

img = cv2.imread('../dataset/real/circulos.jpg')

triangulo = TriangularSignals(img)
octogono = OctogonalSignals(img)
circular = CircularSignals(img)


triangulo.findSignals()
octogono.findSignals()
circular.findSignals()


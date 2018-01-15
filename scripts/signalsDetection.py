from abc import ABCMeta, abstractmethod
from region import Region

import imutils
import cv2
import numpy as np


# Class that detects signals on an image.
class SignalsDetection:

    __metaclass__ = ABCMeta

    signalName = ''

    def __init__(self, img, mask):
        
        self.img = img
        self.mask = mask
        self.detected = False  # True if a signal has been detected.
        self.numberSignals = 0  # Number of signals detected;

        self.surf = cv2.xfeatures2d.SURF_create(1000)
        self.bf = cv2.BFMatcher()
        self.descriptorSignals = {}

        for filename in self.signals:
            
            self.img2= cv2.imread('../dataset/signals/' + filename + '.png')
            kp2, des2 = self.surf.detectAndCompute(cv2.UMat(self.img2), None)
            self.descriptorSignals[filename] = des2

        # Shows binary image.
        # cv2.imshow('imagen', self.mask), cv2.waitKey(0)
    
    # Returns the portions of the image that contain signals.
    @abstractmethod
    def obtenerRegiones(self, detectedSignals):
        pass

    # Finds signals on an image
    @abstractmethod
    def findSignals(self):
        pass

    # Given a region of an image, it calculates which signal matches best.
    def matchSignals(self, region):

        mejorResultado = 100
        kp1, des1 = self.surf.detectAndCompute(cv2.UMat(region.img), None)

        for key, value in self.descriptorSignals.items():
            matches = self.bf.match(des1, value)
            if (len(matches) != 0):
                resultadoActual = sum(m.distance for m in matches) / len(matches)
                if (resultadoActual < mejorResultado):
                    mejorResultado = resultadoActual
                    self.signalName = key

        print(str(self.signalName) + ': ' + str(mejorResultado))
        self.drawBoundingBox(region)

    # Draws the bounding box for the signal detected.
    def drawBoundingBox(self, region):

        cv2.rectangle(self.img, (region.x, region.y), (region.x + region.w,
                      region.y + region.h), (0, 255, 0), 2)

        cv2.putText(self.img, self.signalName, (region.x, region.y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)


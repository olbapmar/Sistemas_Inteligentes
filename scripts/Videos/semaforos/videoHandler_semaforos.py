from semaforo import Semaforo
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


    def start(self, video):
        self.video = video
        Thread(target=self.updateVideo, args=()).start()
        
        self.event.wait()
        semaforos = Semaforo()

        while self.frame is not None and self.noParar:
            img = self.frame

            #semaforos.contornos(img)
            contornos = semaforos.contornos(img)
            cv2.drawContours(img, contornos, -1, (0, 255, 0), 2)

            
            cv2.imshow('imagen', img)

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

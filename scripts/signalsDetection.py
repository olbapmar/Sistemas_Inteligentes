from abc import ABCMeta, abstractmethod
import cv2


# Class that detects signals on an image.
class SignalsDetection:

    __metaclass__ = ABCMeta

    descriptorSignals = {}

    signals = ['30', '40', '50', '60', '70', '80', '100', '120',
               'no_adelantar', 'prohibido_paso', 'ceda_paso', 'stop']

    def __init__(self):
        
        self.img = None
        self.signalName = ''
        self.mask = None
        self.detected = False  # True if a signal has been detected.
        self.numberSignals = 0  # Number of signals detected;
        self.surf = cv2.xfeatures2d.SURF_create(1000)
        self.bf = cv2.BFMatcher()
        self.threshold = 0.4

        for filename in SignalsDetection.signals:
            
            self.img2 = cv2.imread('../dataset/signals/' + filename + '.png')
            kp2, des2 = self.surf.detectAndCompute(cv2.UMat(self.img2), None)
            SignalsDetection.descriptorSignals[filename] = des2

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

        # for key, value in SignalsDetection.descriptorSignals.items():

        for sign in self.signals:
            matches = self.bf.match(des1, SignalsDetection.descriptorSignals[sign])
            if (len(matches) != 0):
                resultadoActual = sum(m.distance for m in matches) / len(matches)
                if (resultadoActual < mejorResultado and resultadoActual < self.threshold):
                    mejorResultado = resultadoActual
                    self.signalName = sign

        print(str(self.signalName) + ': ' + str(mejorResultado))
        if (mejorResultado < self.threshold):
            self.drawBoundingBox(region)

    # Draws the bounding box for the signal detected.
    def drawBoundingBox(self, region):

        cv2.rectangle(self.img, (region.x, region.y), (region.x + region.w,
                      region.y + region.h), (0, 255, 0), 2)

        cv2.putText(self.img, self.signalName, (region.x, region.y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    def actualizaImagen(self, img):
        self.img = img

    def actualizaMascara(self, mask):
        self.mask = mask
    
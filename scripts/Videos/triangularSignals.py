from nonCircularSignals import NonCircularSignals
import math
import numpy as np


# Detects triangular signals.
class TriangularSignals(NonCircularSignals):

    def __init__(self):
        self.signals = ['ceda_paso']
        self.numberVertex = 3
        self.signalType = "triangular"

        NonCircularSignals.__init__(self)

    def matchSignals(self, region, contorno, approx):

        diferenciaMax = 0.3
        # calculo del vértice más bajo.
        min = 1000

        for coordenada in approx:
            if coordenada[0, 1] < min:
                min = coordenada[0, 1]

        verticesParalelos = 0
        for coordenada in approx:
            if (math.fabs(coordenada[0, 1] - min) < (region.h * diferenciaMax)):
                verticesParalelos += 1
        
        if verticesParalelos == 2:
            self.signalName = 'Ceda el paso'
            print("Ceda")
        else:
            self.signalName = 'Peligro'
            print("Peligro")

        self.drawBoundingBox(region)
   

from nonCircularSignals import NonCircularSignals


# Detects octogonal signals.
class OctogonalSignals(NonCircularSignals):

    def __init__(self, img, mask, contorno):
        self.signals = ['stop']
        self.numberVertex = 8
        self.signalType = "octogonal"

        NonCircularSignals.__init__(self, img, mask, contorno)

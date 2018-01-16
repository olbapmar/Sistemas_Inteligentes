from nonCircularSignals import NonCircularSignals


# Detects triangular signals.
class TriangularSignals(NonCircularSignals):

    def __init__(self):
        self.signals = ['ceda_paso']
        self.numberVertex = 3
        self.signalType = "triangular"

        NonCircularSignals.__init__(self)



from nonCircularSignals import NonCircularSignals


# Detects triangular signals.
class TriangularSignals(NonCircularSignals):

    signals = ['ceda_paso']
    numberVertex = 3
    signalType = "triangular"

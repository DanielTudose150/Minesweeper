class Piece:
    def __init__(self, hasBomb):
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False
        self.number = 0

    def getHasBomb(self):
        return self.hasBomb

    def getClicked(self):
        return self.clicked

    def getFlagged(self):
        return self.flagged

    def setNumber(self, number):
        self.number = number

    def getNumber(self):
        return self.number

    def setFlag(self):
        self.flagged = not self.flagged

    def setClicked(self):
        self.clicked = True

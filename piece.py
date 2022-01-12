class Piece:
    """
    A class used to represent a block on the board and to keep information about respective block.

    Attributes
    ----------
        hasBomb : bool
            flag if block is a mine
        clicked : bool
            flag if block has been clicked
        flagged : bool
            flag if block has been flagged by the user
        number : int
            number of mines around piece if not mine

    Methods
    -------
        getHasBomb():
            Returns the flag hasBomb.
        getClicked():
            Returns the flag clicked.
        getFlagged():
            Returns the flag flagged.
        setNumber(number):
            Sets a new value up for number.
        getNumber():
            Returns the attribute number.
        setFlag():
            Flips the flag flagged.
        setClicked():
            Sets the flag clicked to True.
    """
    def __init__(self, hasBomb):
        """
        Initialises the necessary attributes.

        Parameters
        ----------
            hasBomb : bool
                flag if the piece is a mine
        """
        self.hasBomb = hasBomb
        self.clicked = False
        self.flagged = False
        self.number = 0

    def getHasBomb(self):
        """Returns the flag hasBomb."""
        return self.hasBomb

    def getClicked(self):
        """Returns the flag clicked."""
        return self.clicked

    def getFlagged(self):
        """Returns the flag flagged."""
        return self.flagged

    def setNumber(self, number):
        """Sets a new value up for number."""
        self.number = number

    def getNumber(self):
        """Returns the attribute number."""
        return self.number

    def setFlag(self):
        """Flips the flag flagged."""
        self.flagged = not self.flagged

    def setClicked(self):
        """Sets the flag clicked to True."""
        self.clicked = True

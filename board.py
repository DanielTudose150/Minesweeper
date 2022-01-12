from piece import Piece
from random import sample


class Board:
    """
    A class used to represent the board of the Minesweeper game.

    Attributes
    ----------
        lost : bool
            a check if the state of the board results in a lost game
        won : bool
            a check if the state of the board results in a won game
        board : list[list[Piece]
            a matrix representing the board
        size : (int, int)
            width and height of the board
        numberOfBombs : int
            number of bombs on the board
        spaces : int
            number of non-mines on the board
        clicked : int
            number of clicked blocks by the user

    Methods
    -------
        setBoard():
            Sets the board up if the size of board is not custom.
        getSize():
            Return the size of board
        getNumberOfBombs(size):
            Determines and returns the number of mines relative to the side of the board.
        getNoBombs():
            Returns the number of mines on the board
        getBombs(bombs):
            Returns a list of the coordinates of the mines
        getPiece(index):
            Returns the piece at the given index.
        setNumbers():
            Determines the values of the non-mines blocks.
        getNumber(index):
            Returns the number of mines around the Piece at the given index.
        outOfBounds(index):
            Checks if the given coordinates are outside the board.
        handleClick(piece, index, flag):
            Interprets the user click at a given position and updates the board accordingly.
        getWon():
            Checks if the win condition has been achieved.
        setWon(won):
            Sets the won stats to the parameter.
        getLost():
            Returns the status regarding the lost status.
        setLost(lost):
            Sets the won stats to the parameter.
        setBombs(bombs):
            Sets the number of mines to the parameters and generates bombs coordinates for the mines.
    """
    def __init__(self, size, custom):
        self.lost = False
        self.won = False
        self.board = None
        self.size = size
        self.numberOfBombs = self.getNumberOfBombs(self.size) if not custom else custom
        self.spaces = self.size[0] * self.size[1] - self.numberOfBombs
        self.clicked = 0
        if custom:
            self.setBombs(custom)
        else:
            self.setBoard()

    def setBoard(self):
        self.board = []
        bombs = self.getBombs(self.numberOfBombs)
        for row in range(self.size[0]):
            rowList = []
            for col in range(self.size[1]):
                piece = None
                if (row, col) in bombs:
                    piece = Piece(True)
                else:
                    piece = Piece(False)
                rowList.append(piece)
            self.board.append(rowList)
        self.setNumbers()

    def getSize(self):
        return self.size

    def getNumberOfBombs(self, size):
        if size == (9, 9):
            return 10
        if size == (16, 16):
            return 40
        if size == (30, 16) or size == (16, 30):
            return 99
        # size of board is custom, so the number of bombs will be 15% of the total number of blocks
        # 15/100 * blocks = bombs
        return int(0.15 * size[0] * size[1])

    def getNoBombs(self):
        return self.numberOfBombs

    def getBombs(self, bombs):
        bombList = sample(range(self.size[0] * self.size[1]), bombs)
        for i in range(len(bombList)):
            bombList[i] = (bombList[i] // self.size[1], bombList[i] % self.size[1])
        return bombList

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def setNumbers(self):
        """Determines the values of the non-mines blocks."""
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                index = (row, col)
                value = self.getNumber(index)
                self.getPiece(index).setNumber(value)

    def getNumber(self, index):
        """
        Returns the number of mines around the piece at the given index.

        Parameters
        ----------
            index : (int, int)
                coordinates of the piece

        Return
        ------
            value : int
                number of mines around the piece
        """
        move = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        value = 0
        for m in move:
            pos = (index[0] + m[0], index[1] + m[1])
            if not self.outOfBounds(pos):
                if self.getPiece(pos).getHasBomb():
                    value += 1
        return value

    def outOfBounds(self, index):
        """
        Checks if the given coordinates are outside the board.

        Parameters
        ----------
            index : (int, int)
                coordinates

        Return
        ------
            True or False
        """
        if index[0] < 0 or index[0] >= self.size[0]:
            return True
        if index[1] < 0 or index[1] >= self.size[1]:
            return True
        return False

    def handleClick(self, piece, index, flag):
        """
        Interprets the user click at a given position and updates the board accordingly.

        Parameters
        ----------
            piece : Piece
                the block on the board
            index : (int, int)
                coordinates of the piece
            flag : bool
                represents whether the click was right click or not

        Return
        ------
            -1 or 1 if the click was a right click
            0 elsewhere
        """
        if piece.getClicked() or (not flag and piece.getFlagged()):
            return 0
        if flag:
            piece.setFlag()
            return -1 if piece.getFlagged() else 1
        piece.setClicked()
        if piece.getHasBomb():
            self.lost = True
            return 0
        self.clicked += 1
        if piece.getNumber() != 0:
            return 0
        move = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        q = []
        q.append(index)
        while len(q) > 0:
            first = q.pop(0)
            for m in move:
                pos = first[0] + m[0], first[1] + m[1]
                if self.outOfBounds(pos):
                    continue
                piece2 = self.getPiece(pos)
                if piece2.getClicked() or piece2.getHasBomb() or piece2.getFlagged():
                    continue
                piece2.setClicked()
                self.clicked += 1
                if piece2.getNumber():
                    continue
                q.append(pos)
        return 0

    def getWon(self):
        """
        Checks if the win condition has been achieved.

        Return
        ------
            spaces == clicked
        """
        return self.spaces == self.clicked

    def setWon(self, won):
        """
        Sets the won stats to the parameter.

        Parameters
        ----------
            won : bool
                the new status regarding the won status
        """
        self.won = won

    def getLost(self):
        """Returns the status regarding the lost status."""
        return self.lost

    def setLost(self, lost):
        """Sets the won stats to the parameter."""
        self.lost = lost

    def setBombs(self, bombs):
        """Sets the number of mines to the parameters and generates bombs coordinates for the mines."""
        self.numberOfBombs = bombs
        mines = self.getBombs(bombs)
        self.board = []
        for row in range(self.size[0]):
            rowList = []
            for col in range(self.size[1]):
                piece = None
                if (row, col) in mines:
                    piece = Piece(True)
                else:
                    piece = Piece(False)
                rowList.append(piece)
            self.board.append(rowList)
        self.setNumbers()


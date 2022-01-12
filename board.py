from piece import Piece
from random import sample


class Board:
    def __init__(self, size, custom):
        self.lost = False
        self.won = False
        self.board = None
        self.size = size
        self.numberOfBombs = self.getNumberOfBombs(self.size)
        self.spaces = self.size[0] * self.size[1] - self.numberOfBombs
        self.clicked = 0
        self.setBoard() if not custom else self.setBombs(custom)

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
        # bombList.sort()
        for i in range(len(bombList)):
            bombList[i] = (bombList[i] // self.size[1], bombList[i] % self.size[1])
        return bombList

    def getPiece(self, index):
        return self.board[index[0]][index[1]]

    def setNumbers(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                index = (row, col)
                value = self.getNumber(index)
                self.getPiece(index).setNumber(value)

    def getNumber(self, index):
        move = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        value = 0
        for m in move:
            pos = (index[0] + m[0], index[1] + m[1])
            if not self.outOfBounds(pos):
                if self.getPiece(pos).getHasBomb():
                    value += 1
        return value

    def outOfBounds(self, index):
        if index[0] < 0 or index[0] >= self.size[0]:
            return True
        if index[1] < 0 or index[1] >= self.size[1]:
            return True
        return False

    def handleClick(self, piece, index, flag):
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
        for m in move:
            pos = index[0] + m[0], index[1] + m[1]
            if self.outOfBounds(pos):
                continue
            piece2 = self.getPiece(pos)
            if (not piece2.getHasBomb()) and (not piece2.getClicked()):
                self.handleClick(piece2, pos, False)
        return 0

    def getWon(self):
        return self.spaces == self.clicked

    def getLost(self):
        return self.lost

    def setBombs(self, bombs):
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


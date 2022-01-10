from piece import Piece
from random import sample

class Board:
    def __init__(self, size):
        self.board = None
        self.size = size
        self.numberOfBombs = self.getNumberOfBombs(self.size)
        self.setBoard()

    def setBoard(self):
        self.board = []
        bombs = self.getBombs(self.numberOfBombs)

        trues = 0
        falses = 0
        for i in bombs:
            print(i)
        print(f"bombs.length = {len(bombs)}")
        for row in range(self.size[0]):
            rowList = []
            for col in range(self.size[1]):
                piece = None
                if (row, col) in bombs:
                    piece = Piece(True)
                    trues = trues + 1
                else:
                    piece = Piece(False)
                    falses  = falses + 1
                rowList.append(piece)
            self.board.append(rowList)
        print(f"{trues}\n{falses}")

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

    def getBombs(self, bombs):
        bombList = sample(range(self.size[0] * self.size[1]), bombs)
        bombList.sort()
        for i in range(len(bombList)):
            bombList[i] = (bombList[i] // self.size[1], bombList[i] % self.size[1])

        print(self.size)
        return bombList

    def getPiece(self, piece):
        return self.board[piece[0]][piece[1]]

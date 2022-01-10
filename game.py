import pygame
import os


def setcwd():
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)


class Game:
    def __init__(self, board, screenSize):
        self.screen = None
        self.images = None
        self.board = board
        self.screenSize = screenSize
        #self.pieceSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        self.setPieceSize((self.screenSize[0], self.screenSize[1] - 100), self.board.getSize())
        setcwd()
        self.loadImages()


    def run(self):
        pygame.init()
        pygame.display.set_caption('Minesweeper')
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        topLeft = (0, 100)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = 0, topLeft[1] + self.pieceSize[1]

    def loadImages(self):
        self.images = {}
        for fileName in os.listdir("assets"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"assets\\" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def setPieceSize(self, screenSize, boardSize):
        maxi = max(boardSize[0], boardSize[1])
        self.pieceSize = screenSize[0] // maxi, screenSize[1] // maxi

    def getImage(self, piece):
        string = "mine-unclicked-block" if piece.getHasBomb() else "normal-block"
        return self.images[string]
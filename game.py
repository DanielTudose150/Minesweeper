import pygame
import os
from time import sleep


def setcwd():
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)


class Game:
    def __init__(self, board, screenSize, offset, timed):
        self.screen = None
        self.images = None
        self.headerImages = {}
        self.board = board
        self.screenSize = screenSize
        self.offset = offset
        self.timed = timed
        self.rects = []
        self.setPieceSize((self.screenSize[0], self.screenSize[1] - self.offset), self.board.getSize())
        setcwd()
        self.loadImages()
        self.loadHeaderImages()
        self.getRects()
        pygame.init()
        pygame.display.set_caption('Minesweeper')

    def run(self):
        self.screen = pygame.display.set_mode(self.screenSize)
        running = True
        frameRate = pygame.time.Clock()
        FPS = 60
        while running:
            frameRate.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                sound = pygame.mixer.Sound("sound\\win.mp3")
                sound.play()
                sleep(3)
                running = False
            if self.board.getLost():
                sound = pygame.mixer.Sound("sound\\lose.mp3")
                sound.play()
                sleep(3)
                running = False
        pygame.quit()

    def draw(self):
        topLeft = (0, self.offset)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = 0, topLeft[1] + self.pieceSize[1]

        self.drawHeader()

    def loadImages(self):
        self.images = {}
        for fileName in os.listdir("assets\\game"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"assets\\game\\" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def setPieceSize(self, screenSize, boardSize):
        maxi = max(boardSize[0], boardSize[1])
        self.pieceSize = screenSize[0] // maxi, screenSize[1] // maxi

    def getImage(self, piece):
        string = None
        if piece.getClicked():
            if piece.getHasBomb():
                string = "mine-clicked-block"
            else:
                if piece.getNumber() > 0:
                    string = str(piece.getNumber())
                else:
                    string = "empty-block"
        else:
            if piece.getFlagged():
                string = "flag-block"
            else:
                string = "normal-block"
        return self.images[string]

    def handleClick(self, position, rightClick):
        if self.board.getLost():
            return
        index = (position[1] - self.offset) // self.pieceSize[1], position[0] // self.pieceSize[0]
        if self.indexOutOfBounds(index):
            return
        piece = self.board.getPiece(index)
        self.board.handleClick(piece, index, rightClick)

    def indexOutOfBounds(self, index):
        if index[0] < 0 or index[0] >= self.board.getSize()[0]:
            return True
        if index[1] < 0 or index[1] >= self.board.getSize()[1]:
            return True
        return False

    def loadHeaderImages(self):
        self.headerImages["header"] = self.images["header"]
        self.headerImages["header"] = pygame.transform.scale(self.headerImages["header"], (1000, 100))

        self.headerImages["bg-block"] = self.images["bg-block"]
        self.headerImages["bg-block"] = pygame.transform.scale(self.headerImages["bg-block"], (100, 50))

        self.headerImages["exit"] = self.images["exit"]
        self.headerImages["exit"] = pygame.transform.scale(self.headerImages["exit"], (50, 50))

        self.headerImages["retry"] = self.images["retry"]
        self.headerImages["retry"] = pygame.transform.scale(self.headerImages["retry"], (50, 50))

    def drawHeader(self):
        topLeft = (0, 0)
        self.screen.blit(self.headerImages["header"], topLeft)

        topLeft = (100, 25)
        self.screen.blit(self.headerImages["bg-block"], topLeft)

        topLeft = (800, 25)
        self.screen.blit(self.headerImages["bg-block"], topLeft)

        topLeft = (400, 25)
        self.screen.blit(self.headerImages["retry"], topLeft)

        topLeft = (550, 25)
        self.screen.blit(self.headerImages["exit"], topLeft)

    def getRects(self):
        flags = pygame.Rect(100, 25, 100, 50)
        self.rects.append(flags)

        timer = pygame.Rect(800, 25, 100, 50)
        self.rects.append(timer)

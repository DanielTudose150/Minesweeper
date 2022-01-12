import pygame
import os
from time import sleep
from multiprocessing import Process
from multiprocessing.sharedctypes import Value


def setcwd():
    """Sets the current working directory to the directory of the script."""
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)


def runTimer(seconds):
    """
    Represents the timer function

    Parameters
    ----------
        seconds : multiprocessing.ctype
            represents the number of seconds for the timer to count down
    """
    finished = False
    while not finished:
        seconds.value -= 1
        sleep(1)
        if seconds.value <= 0:
            finished = not finished


class Game:
    """
    A class used to represent the game of Minesweeper.

    Attributes
    ----------
        pieceSize : (int, int)
            width and height of the blocks
        screen : pygame.Surface
            the game window
        images : dict
            key : str
                name of the image
            value : pygame.image
            Contains the assets for the game
        board : Board
            object representing the game board
        screenSize : (int, int)
            width and height of the window
        offset : int
            offset relative to the window origin
        timed : [bool, int]
            a list containing information about the timer of the game
            the first element represents if a timer will be used in the game
            the second element represents the number of seconds
        seconds : int
            the number of seconds for the timer
        sharedSeconds : multiprocessing.ctype
            the number of seconds for the timer
            this attribute is shared between the main process and the timer process
        timer : multiprocessing.Process
            the process handling the timer
        rects : list
            contains the rectangles in the header
        running : bool
            the game loop condition
        retry : bool
            represents if the user wants to reset the board
        retry2 : bool
            represents a check to not reinitialise the timer
        flags : int
            represents the number of bombs shown in the header
        font : str
            the location of the font used to write text
        firstClick : bool
            tracks whether the first click has been made or not

        Methods
        -------
            run():
                Represents the game loop.
            draw():
                Draws the board and the header.
            loadImages():
                Loads the image assets and fills the image dictionary.
            setPieceSize(screenSize, boardSize):
                Determines the size of the blocks relative to the window and board sizes.
            getImage(piece):
                Retrieves the image corresponding to the given piece relative to its state.
            handleClick(position, rightClick):
                Processes the click interaction from the user and whether that was a right click or not.
            indexOutOfBounds(index):
                Checks if a given index is outside of the board.
            loadHeaderImages():
                Loads the header assets and fills the header image dictionary.
            drawHeader():
                Draws the header on the window.
            getRects():
                Sets the header rectangles up.
            handleHeaderClick(position):
                Processes the click interaction on the header from the user and sets specific flags.
            drawBoard():
                Draws the board after the user clicks on a mine.
            drawFlags():
                Draws the number of unflagged mines left.
            drawTime():
                Draws the seconds from the timer.
            setupTimer():
                Initialises the shared variable and creates the timer process.
            startTimer():
                Starts the timer process.
            checkTimer():
                Checks if the given seconds have been elapsed.
    """
    def __init__(self, board, screenSize, offset, timed):
        """
        Initialises the necessary attributes. Updates the working directory. Loads necessary assets.

        Parameters
        ----------
            board : Board
                represents the board of the game
            screenSize : (int, int)
                width and height of the window
            offset : int
                the windows will be drawn offset pixels lower
            timed : [bool, int]
                the first value represents if the game will have a timer
                the second value represents the seconds
        """
        self.pieceSize = None
        self.screen = None
        self.images = None
        self.headerImages = {}
        self.board = board
        self.screenSize = screenSize
        self.offset = offset
        self.timed = timed
        self.seconds = timed[1]
        self.sharedSeconds = None
        self.timer = self.setupTimer()
        self.rects = []
        self.running = True
        self.retry = False
        self.retry2 = False
        self.flags = board.getNoBombs()
        self.font = "font\\mine-sweeper.ttf"
        self.firstClick = False
        self.setPieceSize((self.screenSize[0], self.screenSize[1] - self.offset), self.board.getSize())
        setcwd()
        self.loadImages()
        self.loadHeaderImages()
        self.getRects()

        pygame.init()
        pygame.display.set_caption('Minesweeper')

    def run(self):
        """Represents the main game loop."""
        self.screen = pygame.display.set_mode(self.screenSize)
        self.running = True
        frameRate = pygame.time.Clock()
        FPS = 60
        while self.running:
            frameRate.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    rightClick = pygame.mouse.get_pressed()[2]
                    self.handleClick(position, rightClick)
            self.draw()
            pygame.display.flip()
            if self.timed[0] and self.checkTimer():
                self.board.setLost(True)
            if self.board.getWon():
                sound = pygame.mixer.Sound("sound\\win.mp3")
                sound.play()
                sleep(3)
                self.running = False
            if self.board.getLost():
                self.drawBoard()
                pygame.display.flip()
                sound = pygame.mixer.Sound("sound\\lose.mp3")
                sound.play()
                sleep(3)
                self.running = False
        if self.retry:
            self.board.__init__(self.board.getSize(), self.board.getNoBombs())
            self.retry = False
            self.retry2 = True
            self.flags = self.board.getNoBombs()
            self.timed[1] = self.seconds
            self.sharedSeconds.value = self.timed[1]
            self.firstClick = False
            self.run()
        pygame.quit()

    def draw(self):
        """Draws the board and the header."""
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
        """Loads the board asserts and fills the board image dictionary."""
        self.images = {}
        for fileName in os.listdir("assets\\game"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"assets\\game\\" + fileName)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[fileName.split(".")[0]] = image

    def setPieceSize(self, screenSize, boardSize):
        """
        Determines the size of the blocks relative to the screen and board sizes

        Parameters
        ----------
            screenSize : (int, int)
                width and height of the windows
            boardSize : (int, int)
                width and height of the board
        """
        maxi = max(boardSize[0], boardSize[1])
        self.pieceSize = screenSize[0] // maxi, screenSize[1] // maxi

    def getImage(self, piece):
        """
        Retrieves the image corresponding to the given piece relative to its state.

        Parameters
        ----------
            piece : Piece
                object representing a piece from the board

        Return
        ------
            image : pygame.Image
        """
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
        """
        Processes the click interaction from the user and whether that was a right click or not.

        Parameters
        ----------
            position : (int, int)
                coordinates of where the user clicked on the window
            rightClick : bool
                represents whether the click was a right click or not
        """
        if self.board.getLost():
            return
        index = (position[1] - self.offset) // self.pieceSize[1], position[0] // self.pieceSize[0]
        if self.indexOutOfBounds(index):
            self.handleHeaderClick(position)
            return

        if not self.firstClick:
            self.firstClick = True
            if not self.retry2:
                self.startTimer(self.timer)

        piece = self.board.getPiece(index)
        self.flags += self.board.handleClick(piece, index, rightClick)

    def indexOutOfBounds(self, index):
        """
        Checks if a given index is outside of the board.

        Parameters
        ----------
            index : (int, int)
                coordinates

        Return
        ------
            True or False
        """
        if index[0] < 0 or index[0] >= self.board.getSize()[0]:
            return True
        if index[1] < 0 or index[1] >= self.board.getSize()[1]:
            return True
        return False

    def loadHeaderImages(self):
        """Loads the header assets and fills the header image dictionary."""
        self.headerImages["header"] = self.images["header"]
        self.headerImages["header"] = pygame.transform.scale(self.headerImages["header"], (1000, 100))

        self.headerImages["bg-block"] = self.images["bg-block"]
        self.headerImages["bg-block"] = pygame.transform.scale(self.headerImages["bg-block"], (100, 50))

        self.headerImages["exit"] = self.images["exit"]
        self.headerImages["exit"] = pygame.transform.scale(self.headerImages["exit"], (50, 50))

        self.headerImages["retry"] = self.images["retry"]
        self.headerImages["retry"] = pygame.transform.scale(self.headerImages["retry"], (50, 50))

    def drawHeader(self):
        """Draws the header on the window."""
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

        self.drawFlags()
        self.drawTime()

    def getRects(self):
        """Sets the header rectangles up."""
        flags = pygame.Rect(100, 25, 100, 50)
        self.rects.append(flags)

        timer = pygame.Rect(800, 25, 100, 50)
        self.rects.append(timer)

    def handleHeaderClick(self, position):
        """
        Processes the click interaction on the header from the user and sets specific flags.

        Parameters
        ----------
            position : (int, int)
                coordinates of where the user clicked on the window
        """
        index = position[0] // 50, position[1] // 25
        if index[0] == 8:
            if 1 <= index[1] <= 2:
                self.retry = True
                self.running = False
        elif index[0] == 11:
            if 1 <= index[1] <= 2:
                self.running = False

    def drawBoard(self):
        """Draws the board after the user clicks on a mine."""
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                if not piece.getHasBomb() and piece.getNumber() == 0:
                    continue
                piece.setClicked()
        self.draw()

    def drawFlags(self):
        """Draws the number of unflagged mines left."""
        RED = (255, 0, 0)
        font = pygame.font.Font(self.font, 20)
        text = font.render(str(self.flags), True, RED)
        textRect = text.get_rect()
        textRect.center = self.rects[0].center

        self.screen.blit(text, textRect)

    def drawTime(self):
        """Draws the seconds from the timer."""
        RED = (255, 0, 0)
        font = pygame.font.Font(self.font, 20)
        value = self.sharedSeconds.value
        text = font.render(str(value), True, RED)
        textRect = text.get_rect()
        textRect.center = self.rects[1].center

        self.screen.blit(text, textRect)

    def setupTimer(self):
        """
        Initialises the shared variable and creates the timer process.

        Return
        ------
            p : Process
                represents the timer process
        """
        self.sharedSeconds = Value('i', self.timed[1])
        p = Process(target=runTimer, args=[self.sharedSeconds])
        return p

    def startTimer(self, p):
        """Starts the timer process."""
        p.start()

    def checkTimer(self):
        """
        Checks if the given seconds have been elapsed.

        Return
        ------
            sharedSeconds.value <= 0
        """
        if self.timed[0]:
            with self.sharedSeconds:
                if self.sharedSeconds.value <= 0:
                    return True
        return False

import pygame
import os
from time import sleep


def setcwd():
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)


class Menu:

    def __init__(self, screenSize):
        setcwd()
        pygame.init()
        self.running = True
        self.images = {}
        self.screenSize = screenSize
        self.window = pygame.display.set_mode(self.screenSize)
        self.GREY = (192, 192, 192)
        self.RED = (255, 0, 0)
        self.buttonSize = (200, 100)
        self.time = [False, 0]
        self.font = "font\\mine-sweeper.ttf"
        self.loadImages()
        pygame.display.set_caption('Minesweeper')

    def run(self):
        value = [8, 0, 0, 0, self.time]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    value = self.handleClick(position)
            self.window.fill(self.GREY)
            self.draw()
            pygame.display.flip()
        if self.time[0] and value[0] != 8:
            value = self.handleTimedMenu(value)
        pygame.quit()
        return value

    def loadImages(self):
        for fileName in os.listdir("assets\\menu"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"assets\\menu\\" + fileName)
            image = pygame.transform.scale(image, self.buttonSize)
            self.images[fileName.split(".")[0]] = image

    def draw(self):
        topLeft = (400, 50)
        image = self.images["title"]
        image = pygame.transform.scale(image, (self.buttonSize[0] * 2, self.buttonSize[1] * 2))

        self.window.blit(image, (topLeft[0] - self.buttonSize[0] // 2, topLeft[1]))

        topLeft = topLeft[0], topLeft[1] + 250
        self.window.blit(self.images["beginner"], topLeft)

        topLeft = topLeft[0], topLeft[1] + 110
        self.window.blit(self.images["intermediate"], topLeft)

        topLeft = topLeft[0], topLeft[1] + 110
        self.window.blit(self.images["expert"], topLeft)

        topLeft = topLeft[0], topLeft[1] + 110
        self.window.blit(self.images["custom"], topLeft)

        topLeft = topLeft[0], topLeft[1] + 110
        self.window.blit(self.images["time-no" if not self.time[0] else "time-yes"], topLeft)

        topLeft = topLeft[0], topLeft[1] + 110
        self.window.blit(self.images["exit"], topLeft)

    def handleClick(self, position):
        index = position[0] // 100, position[1] // 100

        if not (4 <= index[0] < 6):
            return [0, 0, 0, 0, self.time]
        if index[1] == 7:
            self.time[0] = not self.time[0]
            return [7, 0, 0, 0, self.time]
        if index[1] == 3:
            self.running = False
            return [3, 9, 9, 10, self.time]
        if index[1] == 4:
            self.running = False
            return [4, 16, 16, 40, self.time]
        if index[1] == 5:
            self.running = False
            return [5, 16, 30, 99, self.time]
        if index[1] == 6:
            self.running = False
            return self.handleCustom()
        if index[1] == 8:
            self.running = False
            return [8, 0, 0, 0, self.time]

    def handleCustom(self):
        row = 9
        col = 9
        mines = 10

        running = True
        images = self.getCustomImages()
        display = pygame.Surface(self.screenSize)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    value = self.handleCustomClick(position, row, col, mines)
                    running = value[0]
                    row = value[1]
                    col = value[2]
                    mines = value[3]
            self.window.fill(self.GREY)
            display.fill(self.GREY)
            # display.blit(self.images["title"], (0, 0))
            display = self.drawCustomButtons(display, images)
            display = self.drawRectangles(display, row, col, mines)

            self.window.blit(display, (0, 0))
            pygame.display.flip()

        return (6, row, col, mines, self.time)

    def getCustomImages(self):
        images = {}
        for key in self.images.keys():
            if "plus" in key or "minus" in key:
                images[key] = self.images[key]

        for i in images.keys():
            images[i] = pygame.transform.scale(images[i], (100, 100))

        images["title"] = pygame.transform.scale(self.images["title"], (self.buttonSize[0] * 2, self.buttonSize[1] * 2))
        images["start"] = self.images["start"]

        return images

    def drawCustomButtons(self, display, images):
        topLeftLeft = (100, 300)
        topLeftCenter = (400, 300)
        topLeftRight = (700, 300)

        # row buttons
        topLeft = topLeftLeft
        display.blit(images["plus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["plus-10"], topLeft)

        topLeft = topLeftLeft[0], topLeftLeft[1] + 200
        display.blit(images["minus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["minus-10"], topLeft)

        # col buttons
        topLeft = topLeftCenter
        display.blit(images["plus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["plus-10"], topLeft)

        topLeft = topLeftCenter[0], topLeftCenter[1] + 200
        display.blit(images["minus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["minus-10"], topLeft)

        # bombs buttons
        topLeft = topLeftRight
        display.blit(images["plus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["plus-10"], topLeft)

        topLeft = topLeftRight[0], topLeftRight[1] + 200
        display.blit(images["minus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["minus-10"], topLeft)

        topLeft = (400, 50)
        display.blit(images["title"], (topLeft[0] - self.buttonSize[0] // 2, topLeft[1]))

        topLeft = (400, 800)
        display.blit(images["start"], topLeft)
        return display

    def drawRectangles(self, display, row, col, mines):
        rect1 = pygame.Rect(100, 400, 200, 100)
        rect2 = pygame.Rect(400, 400, 200, 100)
        rect3 = pygame.Rect(700, 400, 200, 100)

        pygame.draw.rect(display, (0, 0, 0), rect1)
        pygame.draw.rect(display, (0, 0, 0), rect2)
        pygame.draw.rect(display, (0, 0, 0), rect3)

        # rows counter
        font = pygame.font.Font(self.font, 20)
        text = font.render(str(row), True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect1.center

        display.blit(text, textRect)

        # row text
        text = font.render("ROWS", True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect1.center[0], rect1.center[1] + 200

        display.blit(text, textRect)

        # columns counter
        text = font.render(str(col), True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect2.center

        display.blit(text, textRect)

        # column text

        text = font.render("COLUMNS", True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect2.center[0], rect2.center[1] + 200

        display.blit(text, textRect)

        # mines counter
        text = font.render(str(mines), True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect3.center

        display.blit(text, textRect)

        # mine counter

        text = font.render("MINES", True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect3.center[0], rect3.center[1] + 200

        display.blit(text, textRect)

        return display

    def handleCustomClick(self, position, row, col, mines):
        running = True
        index = position[0] // 50, position[1] // 100

        if 2 <= index[0] <= 3:
            if index[1] == 3:
                row += 1
                if row > 99:
                    row = 99
            elif index[1] == 5:
                row -= 1
                if row < 5:
                    row = 5
        elif 4 <= index[0] <= 5:
            if index[1] == 3:
                row += 10
                if row > 99:
                    row = 99
            elif index[1] == 5:
                row -= 10
                if row < 5:
                    row = 5
        elif 8 <= index[0] <= 9:
            if index[1] == 3:
                col += 1
                if col > 99:
                    col = 99
            elif index[1] == 5:
                col -= 1
                if col < 5:
                    col = 5
            elif index[1] == 8:
                running = False
        elif 10 <= index[0] <= 11:
            if index[1] == 3:
                col += 10
                if col > 99:
                    col = 99
            elif index[1] == 5:
                col -= 10
                if col < 5:
                    col = 5
        elif 14 <= index[0] <= 15:
            if index[1] == 3:
                mines += 1
                if mines > row * col:
                    mines = row * col
            elif index[1] == 5:
                mines -= 1
                if mines < 3:
                    mines = 3
        elif 16 <= index[0] <= 17:
            if index[1] == 3:
                mines += 10
                if mines > row * col:
                    mines = row * col
            elif index[1] == 5:
                mines -= 10
                if mines < 3:
                    mines = 3

        return running, row, col, mines

    def handleTimedMenu(self, value):
        running = True
        images = self.getCustomImages()
        display = pygame.Surface(self.screenSize)
        value[4][1] = 100

        # value = [mode, row, col, mines, [timed, seconds]]

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    res = self.handleTimeClick(position, value)
                    running = res[0]
                    value = res[1]

            self.window.fill(self.GREY)
            display.fill(self.GREY)
            display = self.drawTimeMenu(display, images, value[4][1])

            self.window.blit(display, (0, 0))
            pygame.display.flip()

        return value

    def drawTimeMenu(self, display, images, seconds):
        topLeft = (400, 50)
        display.blit(images["title"], (topLeft[0] - self.buttonSize[0] // 2, topLeft[1]))

        topLeft = (400, 800)
        display.blit(images["start"], topLeft)

        # buttons
        topLeft = (400, 300)
        display.blit(images["plus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["plus-10"], topLeft)

        topLeft = 400, 500
        display.blit(images["minus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["minus-10"], topLeft)

        # seconds
        rect = pygame.Rect(400, 400, 200, 100)
        pygame.draw.rect(display, (0, 0, 0), rect)
        font = pygame.font.Font(self.font, 20)
        text = font.render(str(seconds), True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect.center

        display.blit(text, textRect)

        # seconds text
        text = font.render("SECONDS", True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect.center[0], rect.center[1] + 200

        display.blit(text, textRect)

        return display

    def handleTimeClick(self, position, value):
        running = True
        index = position[0] // 100, position[1] // 100

        if 4 <= index[0] <= 5:
            if index[1] == 8:
                running = False
        if index[0] == 4:
            if index[1] == 3:
                value[4][1] += 1
            elif index[1] == 5:
                value[4][1] -= 1
                if value[4][1] < 60:
                    value[4][1] = 60
        elif index[0] == 5:
            if index[1] == 3:
                value[4][1] += 10
            elif index[1] == 5:
                value[4][1] -= 10
                if value[4][1] < 60:
                    value[4][1] = 60

        return running, value

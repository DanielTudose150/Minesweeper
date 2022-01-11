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
        # self.display = pygame.Surface(self.screenSize)
        self.GREY = (192, 192, 192)
        self.RED = (255, 0, 0)
        self.buttonSize = (200, 100)
        self.time = False
        self.font = "font\\mine-sweeper.ttf"
        self.loadImages()
        pygame.display.set_caption('Minesweeper')

    def run(self):
        value = [8, 0, 0, self.time]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    value = self.handleClick(position)
            # self.display.fill(self.GREY)
            self.window.fill(self.GREY)
            # self.window.blit(self.display, (0, 0))
            self.draw()
            pygame.display.flip()
        pygame.quit()
        return value

    def drawText(self, text, size, pos):
        font = pygame.font.Font(self.font, size)
        textSurface = font.render(text, True, self.RED)
        textRect = textSurface.get_rect()
        textRect.center = pos
        self.display.blit(textSurface, textRect)

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
        self.window.blit(self.images["time-no" if not self.time else "time-yes"], topLeft)
        topLeft = topLeft[0], topLeft[1] + 110
        self.window.blit(self.images["exit"], topLeft)

    def handleClick(self, position):
        index = position[0] // 100, position[1] // 100

        if not (4 <= index[0] < 6):
            return [0, 0, 0, self.time]
        if index[1] == 7:
            self.time = not self.time
            return [7, 0, 0, self.time]
        if index[1] == 3:
            self.running = False
            return [3, 9, 9, self.time]
        if index[1] == 4:
            self.running = False
            return [4, 16, 16, self.time]
        if index[1] == 5:
            self.running = False
            return [5, 16, 30, self.time]
        if index[1] == 6:
            self.running = False
            return self.handleCustom()
        if index[1] == 8:
            self.running = False
            return [8, 0, 0, self.time]

    def handleCustom(self):
        row = 9
        col = 9

        running = True
        images = self.getCustomImages()
        display = pygame.Surface(self.screenSize)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    value = self.handleCustomClick(position, row, col)
                    running = value[0]
                    row = value[1]
                    col = value[2]
            self.window.fill(self.GREY)
            display.fill(self.GREY)
            # display.blit(self.images["title"], (0, 0))
            display = self.drawCustomButtons(display, images)
            display = self.drawRectangles(display, row, col)

            self.window.blit(display, (0, 0))
            pygame.display.flip()

        return (6, row, col, self.time)

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
        topLeftLeft = (200, 300)
        topLeftRight = (600, 300)
        topLeft = topLeftLeft
        display.blit(images["plus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["plus-10"], topLeft)

        topLeft = topLeftLeft[0], topLeftLeft[1] + 200
        display.blit(images["minus-1"], topLeft)

        topLeft = topLeft[0] + 100, topLeft[1]
        display.blit(images["minus-10"], topLeft)

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

    def drawRectangles(self, display, row, col):
        rect1 = pygame.Rect(200, 400, 200, 100)
        rect2 = pygame.Rect(600, 400, 200, 100)

        pygame.draw.rect(display, (0, 0, 0), rect1)
        pygame.draw.rect(display, (0, 0, 0), rect2)

        font = pygame.font.Font(self.font, 20)
        text = font.render(str(row), True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect1.center

        display.blit(text, textRect)

        text = font.render(str(col), True, self.RED)
        textRect = text.get_rect()
        textRect.center = rect2.center

        display.blit(text, textRect)
        return display

    def handleCustomClick(self, position, row, col):
        running = True
        index = position[0] // 50, position[1] // 100

        if 4 <= index[0] <= 5:
            if index[1] == 3:
                row += 1
                if row > 99:
                    row = 99
            elif index[1] == 5:
                row -= 1
                if row < 5:
                    row = 5
        elif 6 <= index[0] <= 7:
            if index[1] == 3:
                row += 10
                if row > 99:
                    row = 99
            elif index[1] == 5:
                row -= 10
                if row < 5:
                    row = 5
        elif 12 <= index[0] <= 13:
            if index[1] == 3:
                col += 1
                if col > 99:
                    col = 99
            elif index[1] == 5:
                col -= 1
                if col < 5:
                    col = 5
        elif 14 <= index[0] <= 15:
            if index[1] == 3:
                col += 10
                if col > 99:
                    col = 99
            elif index[1] == 5:
                col -= 10
                if col < 5:
                    col = 5
        elif 8 <= index[0] <= 11:
            if index[1] == 8:
                running = False

        return running, row, col

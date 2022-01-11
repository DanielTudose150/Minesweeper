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
        self.display = pygame.Surface(self.screenSize)
        self.GREY = (192, 192, 192)
        self.RED = (255, 0, 0)
        self.buttonSize = (200, 100)
        self.time = False
        self.font = "font\\mine-sweeper.ttf"
        self.loadImages()

    def run(self):
        value = [8, 0, 0]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    value = self.handleClick(position)
            self.display.fill(self.GREY)
            self.window.blit(self.display, (0, 0))
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
        for fileName in os.listdir("assets"):
            if not fileName.endswith(".png"):
                continue
            image = pygame.image.load(r"assets\\" + fileName)
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
            return [0, 0, 0]
        if index[1] == 7:
            self.time = not self.time
            return [7, 0, 0]
        if index[1] == 3:
            self.running = False
            return [3, 9, 9]
        if index[1] == 4:
            self.running = False
            return [4, 16, 16]
        if index[1] == 5:
            self.running = False
            return [5, 16, 30]
        if index[1] == 6:
            pass
        if index[1] == 8:
            self.running = False
            return [8, 0, 0]


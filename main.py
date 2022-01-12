import sys
from game import Game
from board import Board
from menu import Menu


def handleValue(value):
    if value[0] == 8:
        sys.exit()
    if 3 <= value[0] <= 6:
        return value[1], value[2], value[3], value[4]


offset = 100
screenSize = (1000, 1000)
menu = Menu(screenSize)
running = menu.run()

res = handleValue(running)

size = res[0], res[1]
mines = res[2]
timed = res[3]

boardSize = size


board = Board(boardSize, mines)
game = Game(board, screenSize, offset, timed)
game.run()

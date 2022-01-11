import sys
from game import Game
from board import Board
from menu import Menu


def handleValue(value):
    if value[0] == 8:
        sys.exit()
    if 3 <= value[0] <= 6:
        return (value[1], value[2], value[3])


offset = 100
screenSize = (1000, 1000)
menu = Menu(screenSize)
running = menu.run()

res = handleValue(running)

size = res[0], res[1]
timed = res[2]

boardSize = size


board = Board(boardSize)
game = Game(board, screenSize, offset, timed)
game.run()

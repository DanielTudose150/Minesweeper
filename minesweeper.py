import sys
from game import Game
from board import Board
from menu import Menu


def handleValue(value):
    """
    Interprets the response from the menu.

    Parameters
    ----------
        value : [int, int, int, int, [bool, int]]
            represents the list of the processed information of the user
                first value represents the option selected by the user
                second value represents the number of rows
                third value represents the number of columns
                fourth value represents the number of mines
                fifth value represents a pair regarding the timer:
                    first value represents if a timer will be used in the game
                    second value represents the number of seconds for the timer
    """
    if value[0] == 8:
        sys.exit()
    if 3 <= value[0] <= 6:
        return value[1], value[2], value[3], value[4]


if __name__ == '__main__':
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

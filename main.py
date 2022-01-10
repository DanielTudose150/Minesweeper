from game import Game
from board import Board

boardSize = (9, 9)
screenSize = (1000, 1000)

board = Board(boardSize)
game = Game(board, screenSize)
game.run()

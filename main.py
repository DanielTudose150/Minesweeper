from game import Game
from board import Board

boardSize = (16, 30)
screenSize = (1000, 1000)

board = Board(boardSize)
game = Game(board, screenSize)
game.run()

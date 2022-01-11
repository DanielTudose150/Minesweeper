from game import Game
from board import Board

boardSize = (9, 9)
screenSize = (800, 800)
offset = 100

board = Board(boardSize)
game = Game(board, screenSize, offset)
game.run()

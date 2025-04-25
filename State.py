import numpy as np

class State:
    def __init__(self, board = None):
        if board is not None:
            self.board = board
        else:
            self.board = self.init_board()
        self.end_of_game = 0

    def init_board (self):
        board = np.zeros((12, 8))
        for x in range(board.shape[0]):
            board[x, 2:6] = 1
        board[2, 2:5] = 2
        board[7, 3:6] = 2


        return board
  
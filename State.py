import numpy as np
import torch
import random

class State:
    def __init__(self, board = None):
        if board is not None:
            self.board = board
        else:
            self.board = self.init_board()
        self.end_of_game = 0

    def init_board (self):
        board = np.zeros((18, 12))
        for x in range(board.shape[0]):
            board[x, 2:6] = 1
        for x2 in range(8): # manual build of the board
            if x2 % 2 == 0:
                board[x2, random.randint(2,5)] = 2
        return board
    
    def tensorToState (state_tensor):
        board = state_tensor.reshape([18,12]).cpu().numpy()
        return State(board)
    
    def toTensor (self, device = torch.device('cpu')):
        tensor = torch.tensor(self.board, dtype=torch.float32, device=device)
        tensor = tensor.unsqueeze(0).unsqueeze(0)
        return tensor
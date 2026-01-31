import numpy as np
import torch
import random

class State:
    view_height = 12
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
    
    def toTensor(self, device=torch.device('cpu'), player=None):
        board = self.board

        if player is not None:
            row = player.row
            start = row
            end = row + self.view_height
            board = board[start:end, :]
            
            if board.shape[0] < self.view_height:
                pad = self.view_height - board.shape[0]
                board = np.pad(
                    board,
                    ((0, pad), (0, 0)),
                    constant_values=0
                )
            
            # add player position channel (one-hot encoded at the player's column in first row)
            player_channel = np.zeros_like(board)
            player_channel[0, player.col] = 1.0
            
            # stack board and player position channels
            board = np.stack([board, player_channel], axis=0)
            tensor = torch.tensor(board, dtype=torch.float32, device=device)
            return tensor.unsqueeze(0)
        else:
            tensor = torch.tensor(board, dtype=torch.float32, device=device)
            return tensor.unsqueeze(0).unsqueeze(0)
import random
from Player import Player

class Enviroment:
    def __init__(self, state, speed = 10):
        self.state = state
        self.player = Player()
        self.step = 0
        self.speed = speed

    def move (self, action):
        self.player.move(action)
        self.step += 1
        if self.step % self.speed == 0:
            self.roll()
            
    def add_spikes(self):
        offset = random.randint(0, 2)
        delay = random.randint(5, 30)
        if self.step % delay == 0:
            self.state.board[0, 2 + offset: 4 + offset] = 2


    def roll (self):

        # Scroll all rows one down
        self.state.board[1:] = self.state.board[:-1]

        # Set row 0 to zeros
        self.state.board[0] = 0
        self.state.board[0, 2:6] = 1
        self.add_spikes()


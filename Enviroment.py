import random
from Player import Player
from State import State

class Enviroment:
    def __init__(self, state, speed = 10):
        self.state : State = state
        self.player = Player()
        self.step = 0
        self.speed = speed
        self.wait = 2
        self.boost = False
        self.boost_counter = 0
        self.direction = random.choice([-1, 1])
        self.height_left = random.randint(2, 10)

        self.player.animation_speed = 8

    def move (self, action):
        self.player.move(action)
        self.hit()
        self.step += 1
        self.boost_counter += 1
        if (self.boost and self.boost_counter < 200):
            self.speed = 5
        else:
            self.speed = 10
            self.player.animation_speed = 8
        if self.step % self.speed == 0:
            self.roll()

    def hit (self):
        col = self.player.col
        row = self.player.row
        board = self.state.board

        if board[row, col] == 0:
            print("outside")
        elif board[row, col] == 2:
            print("spike")
        elif board[row, col] == 3:
            self.boost = True
            self.player.animation_speed = 3
            self.boost_counter = 0

    def add_spikes(self):
        delay = random.randint(5, 30)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 2
            
    def add_boost(self):
        delay = random.randint(5, 300)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 3

    def roll(self):

        # Scroll all rows one down
        self.state.board[1:] = self.state.board[:-1]
        # New row        
        self.state.board[0] = 0

        self.state.board[0, self.wait:self.wait + 4] = 1
        
        self.height_left -= 1

        if self.height_left == 0:
            new_wait = self.wait + self.direction

            if 0 <= new_wait <= 4:
               self.wait = new_wait
            else:
                self.direction *= -1

            self.height_left = random.randint(4, 10)

        self.add_spikes()
        self.add_boost()

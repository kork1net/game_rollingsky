import random
from Player import Player

class Enviroment:
    def __init__(self, state, speed = 10):
        self.state = state
        self.player = Player()
        self.step = 0
        self.speed = speed

        self.wait = 2
        self.direction = random.choice([-1, 1])
        self.height_left = random.randint(4, 10)

    def move (self, action):
        self.player.move(action)
        self.step += 1
        if self.step % self.speed == 0:
            self.roll()
            
    def add_spikes(self):
        delay = random.randint(5, 30)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 2
            
    def add_boost(self):
        delay = random.randint(5, 200)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 3

    def roll(self):
        print(self.step)

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

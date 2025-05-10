import random
import pygame
from Player import Player
from State import State

pygame.mixer.init()
boost_sound = pygame.mixer.Sound("sfx/start.mp3")
death = pygame.mixer.Sound("sfx/die.mp3")
bonus_sound = pygame.mixer.Sound("sfx/bonus.mp3")
slime_sound = pygame.mixer.Sound("sfx/slimes.mp3")
jump_sound = pygame.mixer.Sound("sfx/jumps.mp3")
start_sound = pygame.mixer.Sound("sfx/starts.mp3")

class Enviroment:
    def __init__(self, state, speed = 10):
        self.state : State = state
        self.player = Player()
        self.step = 0
        self.speed = speed
        self.wait = 2
        self.direction = random.choice([-1, 1])
        self.height_left = random.randint(2, 20)
        self.player.animation_speed = 8
        self.jump_speed = 0
        
        self.boost = False
        self.boost_counter = 0

        self.slow = False
        self.slow_counter = 0
        
        self.jumping = False
        self.jumping_counter = 0

        self.played_boost_sound = False
        self.played_spike_sound = False
        self.played_slime_sound = False
        self.played_jump_sound = False
        self.played_bonus_sound = False

        self.touched_boost = False
        self.touched_boost2 = False

        self.jumpduration = 35
        self.spike_frequency = 25 # lower -> more spikes

        self.score = 0
        self.score_speed = 10
        self.game_over = False
    
    def play_start_sound(self):
        start_sound.play()
        

    def move (self, action):
        self.player.move(action)
        self.hit()
        self.step += 1

        if (self.score < 500):
            self.spike_frequency = 25
        if (100 < self.score < 1000):
            self.spike_frequency = 20
        if (1000 < self.score < 2000):
            self.spike_frequency = 15
        if (2000 < self.score < 3000):
            self.spike_frequency = 10
        if (3000 < self.score):
            self.spike_frequency = 2
    

        self.boost_counter += 1
        self.slow_counter += 1
        if (self.jumping):
            
            self.jumping_counter += 1
            self.player.jumping = True

        if (self.jumping and self.jumping_counter >= self.jumpduration):
            self.jumping = False
            self.jumping_counter = 0
            self.player.jumping = False

        self.speed = 10
        self.jumpduration = 35
        self.score_speed = 10
        self.player.animation_speed = 8

        if (self.boost and self.boost_counter < 200):
            self.jumpduration = 20
            self.speed = 5
            self.score_speed = 5
            self.player.animation_speed = 3

        elif (self.slow and self.slow_counter < 200):
            self.jumpduration = 50
            self.speed = 30
            self.score_speed = 40
            self.player.animation_speed = 30

        if self.step % self.speed == 0:
            self.roll()

        if (self.step % self.score_speed == 0):
            self.score += 1 

    def hit(self):
        col = self.player.col
        row = self.player.row
        board = self.state.board
        self.play_sound(col, row, board)

        if board[row, col] == 0:
            if (not self.jumping):
                self.game_over = True # stop game
                self.player.broken = True

        elif board[row, col] == 2:
            if (not self.jumping):
                self.game_over = True # stop game
                self.player.broken = True

        elif board[row, col] == 3:
            if (not self.jumping):
                self.boost = True
                self.boost_counter = 0
                self.slow = False

        elif board[row, col] == 4:
            if (not self.jumping):
                self.slow = True
                self.slow_counter = 0
                self.boost = False

        elif board[row, col] == 5:
            self.jumping = True
            self.jumping_counter = 0

        elif board[row, col] == 100:
            if not self.jumping and not self.touched_boost:
                self.score += 200
            self.touched_boost = True

        elif board[row, col] == 101:
            if not self.jumping and not self.touched_boost2:
                self.score += 3000
            self.touched_boost2 = True

        else:
            self.touched_boost = False
            self.touched_boost2 = False

    def play_sound(self, col, row, board):
        if board[row, col] == 0 or board[row, col] == 2:
            if (not self.jumping):
                if not self.played_spike_sound:
                    death.play()
                self.played_spike_sound = True
        else:
            self.played_spike_sound = False

        if board[row, col] == 3: # boost
            if (not self.jumping):
                if not self.played_boost_sound:
                    boost_sound.play()
                self.played_boost_sound = True
        else:
            self.played_boost_sound = False
        
        if board[row, col] == 4: # slime
            if (not self.jumping):
                if not self.played_slime_sound:
                    slime_sound.play()
                self.played_slime_sound = True
        else:
            self.played_slime_sound = False

        if board[row, col] == 5: # jumper
            if not self.played_jump_sound:
                jump_sound.play()
            self.played_jump_sound = True
        else:
            self.played_jump_sound = False
        
        if board[row, col] == 100 or board[row, col] == 101: # bonus
            if (not self.jumping):
                if not self.played_bonus_sound:
                    bonus_sound.play()
                self.played_bonus_sound = True
        else:
            self.played_bonus_sound = False

    def _is_spike_safe(self, col):
        board = self.state.board

        if col - 2 >= self.wait:
            if board[1, col - 1] == 2 or board[2, col-2] == 2:
                return False

        if col + 2 <= self.wait + 3:
            if board[1, col + 1] == 2 or board[2, col+2] == 2:
                return False
        
        return True

    def add_spikes(self):
        delay = random.randint(1, self.spike_frequency)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            if self._is_spike_safe(col):
                self.state.board[0, col] = 2
            
    def add_boost(self):
        delay = random.randint(5, 300)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 3

    def add_slime(self):
        delay = random.randint(5, 200)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 4

    def add_bonus500(self):
        delay = random.randint(5, 1000)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 100

    def add_bonus3000(self):
        delay = random.randint(5, 30000)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 101

    def reset(self):
        self.__init__(self.state) 
        self.state.board = self.state.init_board()
        self.player.broken = False

    def roll(self):

        # Scroll all rows one down
        self.state.board[1:] = self.state.board[:-1]
        # New row        
        self.state.board[0] = 0

        hole = random.randint(1,8)

        self.state.board[0, self.wait:self.wait + 4] = 1
        
        self.height_left -= 1

        if self.height_left == 0:
            if(hole == 1):
                self.state.board[0, self.wait:self.wait + 4] = 0
                self.state.board[1, random.randint(self.wait, self.wait + 3)] = 5
            else:
                self.state.board[0, self.wait:self.wait + 4] = 1
                self.add_spikes()
                self.add_boost()
                self.add_slime()
                self.add_bonus500()
                self.add_bonus3000()

            new_wait = self.wait + self.direction

            if 0 <= new_wait <= 4:
               self.wait = new_wait
            else:
                self.direction *= -1

            self.height_left = random.randint(4, 10)
            
        else:
            self.add_spikes()
            self.add_boost()
            self.add_slime()
            self.add_bonus500()
            self.add_bonus3000()

        

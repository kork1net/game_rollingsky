import random
import pygame
from Player import Player
from State import State

pygame.mixer.init()
boost_sound = pygame.mixer.Sound("sfx/start.mp3")
death = pygame.mixer.Sound("sfx/die.mp3")
bonus_sound = pygame.mixer.Sound("sfx/bonus.mp3")

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
        self.height_left = random.randint(2, 20)
        self.player.animation_speed = 8

        self.played_boost_sound = False
        self.played_spike_sound = False
        self.played_bonus_sound = False

        self.touched_boost = False

        self.score = 0
        self.score_speed = 10
        self.game_over = False

    def move (self, action):
        self.player.move(action)
        self.hit()
        self.step += 1

        if (self.step % self.score_speed == 0):
            self.score += 1 
        self.boost_counter += 1
        if (self.boost and self.boost_counter < 200):
            self.speed = 5
            self.score_speed = 5
        else:
            self.speed = 10
            self.score_speed = 10
            self.player.animation_speed = 8
        if self.step % self.speed == 0:
            self.roll()

    def hit (self):
        col = self.player.col
        row = self.player.row
        board = self.state.board

        self.play_sound(col, row, board)

        if board[row, col] == 0:
            self.game_over = True # stop game
        elif board[row, col] == 2:
            self.game_over = True # stop game
        elif board[row, col] == 3:
            self.boost = True
            self.player.animation_speed = 3
            self.boost_counter = 0
        elif board[row, col] == 100:
            if not self.touched_boost:
                self.score += 200
            self.touched_boost = True
        else:
            self.touched_boost = False

    def play_sound(self, col, row, board):
        if board[row, col] == 0 or board[row, col] == 2:
            if not self.played_spike_sound:
                death.play()
            self.played_spike_sound = True
        else:
            self.played_spike_sound = False

        if board[row, col] == 3: # boost
            if not self.played_boost_sound:
                boost_sound.play()
            self.played_boost_sound = True
        else:
            self.played_boost_sound = False

        if board[row, col] == 100: # bonus
            if not self.played_bonus_sound:
                bonus_sound.play()
            self.played_bonus_sound = True
        else:
            self.played_bonus_sound = False

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

    def add_bonus(self):
        delay = random.randint(5, 2000)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 100

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
        self.add_bonus()

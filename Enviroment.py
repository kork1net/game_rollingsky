import random
import pygame
from Player import Player
from State import State

pygame.mixer.init()
boost_sound = pygame.mixer.Sound("sfx/start.mp3")
boost_sound.set_volume(0.2)
death = pygame.mixer.Sound("sfx/die.mp3")
bonus_sound = pygame.mixer.Sound("sfx/bonus.mp3")
slime_sound = pygame.mixer.Sound("sfx/slimes.mp3")
jump_sound = pygame.mixer.Sound("sfx/jumps.mp3")
start_sound = pygame.mixer.Sound("sfx/starts.mp3")

class Enviroment:
    def __init__(self, state, speed = 10):

        
        self.state : State = state
        self.player = Player()
        
        self.tile_size = 60
        self.scroll_offset = 0

        self.step = 0 # distance of the player
        self.speed = speed # speed of the player
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
        self.touched_boost3 = False

        self.jumpduration = 35
        self.spike_frequency = 25 # lower -> more spikes
        self.jumper_frequency = 8

        self.score = 0
        self.score_speed = 5 #############
        self.game_over = False
        self.pause = False
    
    def play_start_sound(self):
        start_sound.play()

    def move (self, action):
        self.player.move(action)
        self.hit()
        self.step += 1

        if (self.score < 500):
            self.spike_frequency = 15
        if (100 < self.score < 1000):
            self.spike_frequency = 11
        if (1000 < self.score < 2000):
            self.spike_frequency = 7
            self.jumper_frequency = 4
        if (2000 < self.score < 3000):
            self.spike_frequency = 3
            self.jumper_frequency = 3
        if (3000 < self.score):
            self.spike_frequency = 1
            self.jumper_frequency = 2
    

        self.boost_counter += 1
        self.slow_counter += 1
        if (self.jumping):
            
            self.jumping_counter += 1
            self.player.jumping = True

        if (self.jumping and self.jumping_counter >= self.jumpduration):
            self.jumping = False
            self.jumping_counter = 0
            self.player.jumping = False

        self.speed = 6
        self.jumpduration = 35
        self.score_speed = 5 ############
        self.player.animation_speed = 8

        if (self.boost and self.boost_counter < 200):
            self.jumpduration = 20
            self.speed = 10
            self.score_speed = 3
            self.player.animation_speed = 3

        elif (self.slow and self.slow_counter < 200):
            self.jumpduration = 50
            self.speed = 3
            self.score_speed = 40
            self.player.animation_speed = 30

        self.scroll_offset += self.speed   #######################################################

        if (self.scroll_offset >= self.tile_size):
            self.scroll_offset = 0
            self.roll()

        if (self.step % self.score_speed == 0):
            self.score += 1 


    def hit(self):
        board = self.state.board

        player_rect = self.player.rect

        tile_size = self.tile_size

        row = int((player_rect.centery - self.scroll_offset) // tile_size)
        col = self.player.col

        tile_id = board[row, col]

        self.play_sound(col, row, board)

        if tile_id == 0:
            if not self.jumping:
                self.game_over = True
                self.player.broken = True

        elif tile_id == 2:  # ספייק
            if not self.jumping:
                self.game_over = True
                self.player.broken = True

        elif tile_id == 3:  # בוסט
            if not self.jumping:
                self.boost = True
                self.boost_counter = 0
                self.slow = False

        elif tile_id == 4:  # סליים
            if not self.jumping:
                self.slow = True
                self.slow_counter = 0
                self.boost = False

        elif tile_id == 5:  # ג'אמפר
            self.jumping = True
            self.jumping_counter = 0

        elif tile_id == 6:
            if not self.jumping and not self.touched_boost:
                self.score += 200
            self.touched_boost = True

        elif tile_id == 7:
            if not self.jumping and not self.touched_boost2:
                self.score += 1000
            self.touched_boost2 = True
        
        elif tile_id == 8:
            if not self.jumping and not self.touched_boost3:
                self.score += 3000
            self.touched_boost3 = True

        else:
            self.touched_boost = False
            self.touched_boost2 = False
            self.touched_boost3 = False

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
        
        if board[row, col] == 6 or board[row, col] == 7 or board[row, col] == 8: # bonus
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

    def add_bonus200(self):
        delay = random.randint(5, 700)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 6

    def add_bonus1000(self):
        delay = random.randint(5, 15000)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 7

    def add_bonus3000(self):
        delay = random.randint(5, 36000)
        if self.step % delay == 0:
            col = random.randint(self.wait, self.wait + 3)
            self.state.board[0, col] = 8

    def reset(self):
        self.__init__(self.state) 
        self.state.board = self.state.init_board()
        self.player.broken = False
    

    def roll(self):

        # scroll all rows one down
        self.state.board[1:] = self.state.board[:-1]
    
        # new row        
        self.state.board[0] = 0

        hole = random.randint(1,self.jumper_frequency)
        self.state.board[0, self.wait:self.wait + 4] = 1
        
        self.height_left -= 1

        if self.height_left == 0:
            if(hole == 1):
                jumper_tile = random.randint(self.wait, self.wait + 3) 
                self.state.board[0, self.wait:self.wait + 4] = 0 # empty row
                self.state.board[1, jumper_tile] = 5 # place a jumper                
            else:
                self.state.board[0, self.wait:self.wait + 4] = 1
                self.add_all()

            new_wait = self.wait + self.direction

            if 0 <= new_wait <= 4:
               self.wait = new_wait
            else:
                self.direction *= -1

            self.height_left = random.randint(4, 10)

            # ensure there is not a spike before a jumper:
            if(hole == 1):
                if self.state.board[2, jumper_tile] == 2:
                    self.state.board[2, jumper_tile] = 1 
            
        else:
            self.add_all()

    def add_all(self):
        self.add_spikes()
        self.add_boost()
        self.add_slime()
        self.add_bonus200()
        self.add_bonus1000()
        self.add_bonus3000()
                

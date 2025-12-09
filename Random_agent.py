import pygame
import random
import time

class Random_agent:
    def __init__(self, action_interval=0.5):
        self.action_interval = action_interval
        self.last_action_time = time.time()
        self.possible_actions = [-1, 0, 1]  # left, no move, right
        self.current_action = 0
    
    def action(self, events):
        current_time = time.time()
        
        if current_time - self.last_action_time >= self.action_interval:
            self.current_action = random.choice(self.possible_actions)
            self.last_action_time = current_time
        
        return self.current_action


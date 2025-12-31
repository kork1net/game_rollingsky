import torch
import numpy as np
import math
import random
from Enviroment import Enviroment
from State import State
from DQN import DQN

class DQN_agent:
    def __init__(self, env=None, train = True) -> None:
        self.DQN = DQN()
        self.is_train = True
        self.step = 0
        self.train(train)
        self.env = env
    
    def train(self, train: bool):
        self.is_train = train
        if train:
            self.DQN.train()
        else:
            self.DQN.eval()
        
    def action(self, state: State, epoch = None, events= None, train = None):
        #actions = [1, -1]
        #return random.choice(actions)
        epoch = self.step
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actions = [1, 0, -1]

        if rnd < epsilon:# epsilon:
            self.step += 1
            return random.choice(actions)

        state_tensor = state.toTensor()

        with torch.no_grad():
            Q_values = self.DQN(state_tensor)
        max_index = torch.argmax(Q_values)

        self.step += 1

        return actions[max_index]
    
    def get_actions(self, states, dones):
        actions = []
        for i, state in enumerate(states):
            if dones[i].item():
                actions.append(0)
            else:
                actions.append(self.action(State.tensorToState(state), train=False))
        return torch.tensor(actions)
            

    def epsilon_greedy(self, epoch, start = 1.0, final=0.01, decay=170.0):
        if decay <= 0:
            return final
        eps = final + (start - final) * math.exp(-1.0 * float(epoch) / float(decay))
        print(float(max(final, min(start, eps))))
        return float(max(final, min(start, eps)))

            

import torch
import numpy as np
import math
import random
from Enviroment import Enviroment
from State import State
from DQN import DQN


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class DQN_agent:
    def __init__(self, env=None, train = True) -> None:
        self.DQN = DQN()
        self.is_train = True
        self.step = 0
        self.train(train)
        self.env = env
        self.executed = 0
   
    def train(self, train: bool):
        self.is_train = train
        if train:
            self.DQN.train()
        else:
            self.DQN.eval()
       
    def action(self, state: State, epoch = None, events= None, train = None):
        epoch = self.step
        
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actions = [-1, 0, 1]
        if rnd < epsilon:# epsilon:
            self.step += 1
            return random.choice(actions)
        
        self.executed += 1

        state_tensor = state.toTensor(device=device)    
        state_tensor = state_tensor.view(1, 1, 18, 12).to(device)


        with torch.no_grad():
            Q_values = self.DQN(state_tensor)
        max_index = torch.argmax(Q_values).item()
        
        inverse_action_mapping = [-1, 0, 1]
        chosen_action = inverse_action_mapping[max_index]

        q_vals = Q_values.cpu().numpy()[0]
        if (self.step % 100 == 0):
            print(f"Q-values: left={q_vals[0]:.4f}, center={q_vals[1]:.4f}, right={q_vals[2]:.4f} | max_index: {max_index} | Epoch: {epoch} | Executed {self.executed} actions")

        self.step += 1

        return chosen_action
   
    def get_actions(self, states, dones):
        actions = []
        for i, state in enumerate(states):
            if dones[i].item():
                actions.append(0)
            else:
                actions.append(self.action(State.tensorToState(state), train=False))
        return torch.tensor(actions)
           


    def epsilon_greedy(self, epoch, start = 1.0, final=0.01, decay=1500.0):
        if epoch > decay:
            return final
        eps = ((start - final) / -decay) * epoch + 1
        return eps

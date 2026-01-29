import torch
import torch.nn as nn
import math
import random


import torch
import torch.nn as nn


gamma = 0.99
MSELoss = nn.MSELoss()


class DQN(nn.Module):
    def __init__(self, num_actions=3):
        super().__init__()


        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU()
        )


        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 18 * 12, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)
        )


    def forward(self, x):
        # x = x.float()
        x = self.conv(x)
        return self.fc(x)
   
    def loss(self, Q_value, rewards, Q_next_Values, Dones):
        Q_new = rewards + gamma * Q_next_Values * (1- Dones)
        return MSELoss(Q_value, Q_new)
   
    def copy (self):
        new_DQN = DQN()
        new_DQN.load_state_dict(self.state_dict())
        return new_DQN

    def load_params(self, path):
        self.load_state_dict(torch.load(path))

    def save_params(self, path):
        torch.save(self.state_dict(), path)

    def __call__(self, states, actions=None):
        return self.forward(states)

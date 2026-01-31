from collections import deque
import random
import torch
import numpy as np
from State import State

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class ReplayBuffer:
    def __init__(self, capacity= 10000) -> None:
        self.buffer = deque(maxlen=capacity)

    def push_tensors (self, state_tensor, action_tensor, reward_tensor, next_state_tensor, done):
        self.buffer.append((state_tensor, action_tensor, reward_tensor, next_state_tensor, done))
            
    def sample(self, batch_size):
        batch_size = min(batch_size, len(self.buffer))
        states, actions, rewards, next_states, dones = zip(
            *random.sample(self.buffer, batch_size)
        )

        states = torch.cat(states, dim=0)       # [batch,1,12,12]
        next_states = torch.cat(next_states, dim=0)  # [batch,1,12,12]
        actions = torch.cat(actions, dim=0)     # [batch,1]
        rewards = torch.cat(rewards, dim=0)     # [batch,1]
        dones = torch.cat(dones, dim=0)         # [batch,1]

        if device is not None:
            states = states.to(device)
            next_states = next_states.to(device)
            actions = actions.to(device)
            rewards = rewards.to(device)
            dones = dones.to(device)

        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)
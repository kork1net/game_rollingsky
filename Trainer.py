
import pygame
from Graphics import *
from Enviroment import Enviroment
from State import State
from DQN_agent import DQN_agent
from DQN import DQN
from ReplayBuffer import ReplayBuffer
import torch
import os
import random

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = Enviroment(State())

text_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 30)
small_text_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 25)

def get_new_run_path(folder="data"):
    os.makedirs(folder, exist_ok=True)
    runs = [
        int(f.split("_")[1].split(".")[0])
        for f in os.listdir(folder)
        if f.startswith("run_") and f.endswith(".pth")
    ]
    if runs:
        run_id = max(runs) + 1
    else:
        run_id = 1
    return os.path.join(folder, f"run_{run_id:03d}.pth")


def main():
    
    #region initialization
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    epochs = 500000
    start_epoch = 0
    C = 2000
    batch = 32
    learning_rate = 5e-4
    gamma = 0.99

    env = Enviroment(State(), render=True)

    player = DQN_agent(env=env, train=True)
    player.DQN.to(device)
    player_hat = DQN_agent(env=env, train=False)
    player_hat.DQN.to(device)

    Q = player.DQN.to(device)
    Q_hat: DQN = Q.copy().to(device)
    Q_hat.eval()

    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)

    checkpoint_path = 'data/run_011.pth'
    print("saving training to:", checkpoint_path)
    
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']+1
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        Q_hat.load_state_dict(checkpoint['model_state_dict'])

    player_hat.DQN = Q_hat

    replay = ReplayBuffer()

    best_score = 0


    #endregion   

    #region train loop
    for epoch in range(start_epoch, epochs):

        state = env.reset()
        state_tensor = state.toTensor(device, env.player)
        state_tensor = state_tensor.float()
        
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            action = player.action(state=state, epoch=epoch)

            next_state, reward, done = env.move(action, True)

            next_state_tensor = next_state.toTensor(device, env.player)
            
            action_mapping = {-1: 0, 0: 1, 1: 2}
            action_idx = action_mapping[action]

            replay.push_tensors(
                state_tensor,
                torch.tensor([[action_idx]], device=device, dtype=torch.long),
                torch.tensor([[reward]], device=device, dtype=torch.float32),
                next_state_tensor,
                torch.tensor([[done]], device=device, dtype=torch.float32)
            )

            state = next_state
            state_tensor = next_state_tensor.float()

            if len(replay) >= batch:

                states, actions, rewards, next_states, dones = replay.sample(batch)

                states = states.to(device)
                next_states = next_states.to(device)
                rewards = rewards.to(device).view(-1)
                dones = dones.to(device).view(-1)
                q_values = Q(states)

                actions_idx = actions.view(-1, 1) 

                q_sa = q_values.gather(1, actions_idx).squeeze(1)
                
                with torch.no_grad():
                    q_next = Q_hat(next_states).max(1)[0]
                    target = rewards + gamma * q_next * (1 - dones)

                loss = torch.nn.functional.mse_loss(q_sa, target)

                optim.zero_grad()
                loss.backward()
                optim.step()
                
                if env.step % 100 == 0:
                    epsilon = player.epsilon_greedy(epoch)
                    print(f"Step: {env.step} | Loss: {loss.item():.4f} | Epsilon: {epsilon:.4f} | Avg Reward: {rewards.mean().item():.4f}")

            if env.step % C == 0:
                Q_hat.load_state_dict(Q.state_dict())
            
            if env.render:
                graphics(env)
                graphics.main_img_call(True)
                graphics.draw_text("SCORE:"+str(env.score), text_font, ('white'), 12, 18)
                graphics.draw_text("AI", small_text_font, ('black'), 10, 685)
                pygame.display.update()
                clock.tick(240)

        
        if (env.score > best_score):
            best_score = env.score
        if epoch % 20 == 0:
            torch.save({'epoch': epoch, 'model_state_dict': Q.state_dict(), 'optimizer_state_dict': optim.state_dict()}, checkpoint_path)
        if epoch % 10 == 0:
            print(f"Epoch: {epoch} | Score: {env.score} | Best Score: {best_score}")

    #endregion  


if __name__ == '__main__':
    main()
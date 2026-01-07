
import pygame
from Graphics import *
from Enviroment import Enviroment
from State import State
from DQN_agent import DQN_agent
from DQN import DQN
from ReplayBuffer import ReplayBuffer
import torch

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = Enviroment(State())

text_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 30)
death_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 45)
restart_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 25)


def main():
    
    #region initialization
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    epochs = 10000
    start_epoch = 0
    C = 500
    batch = 100
    learning_rate = 1e-3
    gamma = 0.99

    env = Enviroment(State())

    player = DQN_agent(env=env, train=True)
    player.DQN.to(device)
    player_hat = DQN_agent(env=env, train=False)
    player_hat.DQN.to(device)

    Q = player.DQN.to(device)
    Q_hat: DQN = Q.copy().to(device)
    Q_hat.eval()

    player_hat.DQN = Q_hat

    replay = ReplayBuffer()
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)


    #endregion  

    #region train loop
    for epoch in range(start_epoch, epochs):

        state = env.reset()
        state_tensor = state.toTensor(device)
        state_tensor = state_tensor.float()
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            action = player.action(state=state, epoch=epoch)

            next_state, reward, done = env.move(action)

            next_state_tensor = next_state.toTensor(device)

            replay.push_tensors(
                state_tensor,
                torch.tensor([[action]], device=device, dtype=torch.long),
                torch.tensor([[reward]], device=device, dtype=torch.float32),
                next_state_tensor,
                torch.tensor([[done]], device=device, dtype=torch.float32)
            )

            state = next_state

            if len(replay) >= batch:

                states, actions, rewards, next_states, dones = replay.sample(batch)

                states = states.to(device).view(batch, 1, 18, 12)
                next_states = next_states.to(device).view(batch, 1, 18, 12)
                rewards = rewards.to(device).view(-1)
                dones = dones.to(device).view(-1)
                q_values = Q(states)

                action_mapping = {-1: 0, 0: 1, 1: 2}
                actions_idx = torch.tensor([[action_mapping[a.item()]] for a in actions], device=device, dtype=torch.long)
                actions_idx = actions_idx.view(-1, 1) 

                q_sa = q_values.gather(1, actions_idx).squeeze(1)

                

                with torch.no_grad():
                    q_next = Q_hat(next_states).max(1)[0]
                    target = rewards + gamma * q_next * (1 - dones)

                loss = torch.nn.functional.mse_loss(q_sa, target)

                optim.zero_grad()
                loss.backward()
                optim.step()

            if env.step % C == 0:
                Q_hat.load_state_dict(Q.state_dict())
            
            graphics(env)
            graphics.main_img_call(True)
            graphics.draw_text("SCORE:"+str(env.score), text_font, ('white'), 12, 18)
            graphics.draw_text("AI", restart_font, ('black'), 10, 685)


            pygame.display.update()
            clock.tick(FPS)
        

        print(f"Epoch {epoch} | Score: {env.score}")
    #endregion  


if __name__ == '__main__':
    main()




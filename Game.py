import pygame
import torch
from Graphics import *
from Enviroment import Enviroment
from State import State
from Human_agent import Human_agent
from Random_agent import Random_agent
from DQN_agent import DQN_agent
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = Enviroment(State())

# player = Human_agent()
player = DQN_agent(env=env, train=False)

checkpoint_path = "data/run_001.pth"

if isinstance(player, DQN_agent):
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path, map_location=device)
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        print("Loaded trained model")
    else:
        print("No trained model found")

try:
    player.DQN.to(device)
except Exception:
    pass


text_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 30)
death_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 45)
restart_font = pygame.font.Font("fonts/pressstart2p-regular.ttf", 25)


pygame.mixer.music.load('sfx/background.mp3')
pygame.mixer.music.play(-1)


def main():
   
    start = False
    run = True


    while (run):
        pygame.event.pump()
        events = pygame.event.get()
        if not env.pause:
            graphics(env)
        for event in events:


            if event.type == pygame.QUIT:
                run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if graphics.sound_rect.collidepoint(mouse_pos): ## sound button pressed
                    graphics.sound_button_pressed()
                    if graphics.sound_state == 0:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
               


        if not start:
            graphics.main_img_call(False)
            graphics.draw_text("Press [space]", restart_font, ('black'), 75, 483)
            graphics.draw_text("Press [space]", restart_font, ('white'), 75, 480)
           
            for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            env.reset()
                            env.play_start_sound()
                            start = True
        if start:
            graphics.main_img_call(True)
           
            for event in events:
                    if event.type == pygame.KEYDOWN and not env.game_over:
                        if event.key == pygame.K_ESCAPE and env.pause == False:
                            env.pause = True
                            pygame.mixer.music.pause()
                            graphics.draw_text("paused", restart_font, ('white'), 170, 350)


                        elif event.key == pygame.K_ESCAPE and env.pause == True:
                            env.pause = False
                            pygame.mixer.music.unpause()


            if not env.game_over and not env.pause:
                action = player.action(state=env.state, events=events)
                print(action)
                env.move(action)
           
            if env.game_over:


                graphics.draw_text("Game Over!", death_font, ('red'), 20, 305)
                graphics.draw_text("Game Over!", death_font, ('white'), 20, 300)


                graphics.draw_text("[space] to restart", restart_font, ('red'), 10, 373)
                graphics.draw_text("[space] to restart", restart_font, ('white'), 10, 370)


                pygame.mixer.music.stop()


                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            env.reset()
                            if (graphics.sound_state == 0):
                                pygame.mixer.music.unpause()
                                pygame.mixer.music.play(-1)
                            env.play_start_sound()




            graphics.draw_text("SCORE:"+str(env.score), text_font, ('white'), 12, 18)
            graphics.draw_text("Player", restart_font, ('black'), 10, 685)


        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

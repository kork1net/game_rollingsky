import pygame
import torch
from Graphics import *
from Environment import Environment
from State import State
from Human_agent import Human_agent
from Random_agent import Random_agent
from DQN_agent import DQN_agent
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = Environment(State())

human_player = Human_agent()
ai_player = DQN_agent(env=env, train=False)

checkpoint_path = "data/run_048.pth"

if os.path.exists(checkpoint_path):
    checkpoint = torch.load(checkpoint_path, map_location=device)
    ai_player.DQN.load_state_dict(checkpoint['model_state_dict'])
    print("Loaded trained model")
else:
    print("No trained model found")

ai_player.DQN.to(device)

player = ai_player  # start with AI
current_player = 'ai'


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
            graphics.draw_text("[space] for Human", restart_font, ('black'), 25, 483)
            graphics.draw_text("[space] for Human", restart_font, ('white'), 25, 480)
            graphics.draw_text("[a] for AI", restart_font, ('black'), 110, 543)
            graphics.draw_text("[a] for AI", restart_font, ('white'), 110, 540)
           
            for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            env.reset()
                            env.play_start_sound()
                            start = True
                            player = human_player
                            humanEnv = False
                            current_player = 'human'
                        elif event.key == pygame.K_a:
                            env.reset()
                            env.play_start_sound()
                            start = True
                            player = ai_player
                            humanEnv = True
                            current_player = 'ai'
  

                            
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

                        elif event.key == pygame.K_SPACE:
                            player = human_player
                            humanEnv = False
                            current_player = 'human'
                        elif event.key == pygame.K_a:
                            player = ai_player
                            humanEnv = True
                            current_player = 'ai'


            if not env.game_over and not env.pause:
                action = player.action(state=env.state, events=events)
                env.move(action, humanEnv)
           
            if env.game_over:


                graphics.draw_text("Game Over!", death_font, ('red'), 20, 305)
                graphics.draw_text("Game Over!", death_font, ('white'), 20, 300)


                graphics.draw_text("[r] to restart", restart_font, ('red'), 54, 373)
                graphics.draw_text("[r] to restart", restart_font, ('white'), 54, 370)


                pygame.mixer.music.stop()


                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            env.reset()
                            if (graphics.sound_state == 0):
                                pygame.mixer.music.unpause()
                                pygame.mixer.music.play(-1)
                            env.play_start_sound()




            graphics.draw_text("SCORE:"+str(env.score), text_font, ('white'), 12, 18)
            graphics.draw_text(f"{current_player}", restart_font, ('white'), 5, 685)


        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

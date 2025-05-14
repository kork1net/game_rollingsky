import pygame
from Graphics import *
from Enviroment import Enviroment
from State import State
from Human_agent import Human_agent

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = Enviroment(State())
player = Human_agent()

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
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        graphics(env)

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
            if not env.game_over:
                action = player.action(events)
                env.move(action)
            if env.game_over:

                graphics.draw_text("Game Over!", death_font, ('red'), 20, 305)
                graphics.draw_text("Game Over!", death_font, ('white'), 20, 300)

                graphics.draw_text("Press r to restart", restart_font, ('red'), 20, 373)
                graphics.draw_text("Press r to restart", restart_font, ('white'), 20, 370)

                pygame.mixer.music.stop()

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            env.reset()
                            pygame.mixer.music.play(-1)
                            env.play_start_sound()
                
            
            graphics.draw_text(str(env.score), text_font, ('white'), 10, 10)
                
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

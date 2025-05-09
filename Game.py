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

text_font = pygame.font.SysFont("pressstart2pregular", 30)
death_font = pygame.font.SysFont("pressstart2pregular", 45)

pygame.mixer.music.load('sfx/background.mp3')
pygame.mixer.music.play(-1)

def main():
    
    run = True
    while (run):
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        if not env.game_over:
            action = player.action(events)
            env.move(action)

        graphics(env)
        if env.game_over:
            graphics.draw_text("Game Over!", death_font, ('red'), 20, 305)
            graphics.draw_text("Game Over!", death_font, ('white'), 20, 300)
            pygame.mixer.music.stop()
            

        graphics.draw_text(str(env.score), text_font, ('white'), 10, 10)
            
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

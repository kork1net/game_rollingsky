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
IntScore = 1
StringScore = str(IntScore)

text_font = pygame.font.SysFont("verdana", 90)

def main():
    run = True
    while (run):
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        action = player.action(events)
        env.move(action)
        graphics(env)

        graphics.draw_text(StringScore, text_font, ('white'), 20, 0)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

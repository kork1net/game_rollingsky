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

def main():
    run = True
    # comment
    while (run):
        pygame.event.pump()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        action = player.action(events)
        env.move(action)
        graphics(env)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

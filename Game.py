import pygame
from Graphics import *
from Enviroment import Enviroment
from State import State

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()
env = Enviroment(State())

def main():
    run = True
    global ball_x

    while (run):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        graphics(env.state)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ball_x -= speed
        if keys[pygame.K_RIGHT]:
            ball_x += speed

        graphics.screen.blit(ball_img, (ball_x, ball_y))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()

import pygame

class Human_agent:
    def __init__(self):
        pass

    def action (self, events=None, env=None):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return -1
                elif event.key == pygame.K_RIGHT:
                    return 1
        return 0                
import pygame

class Player (pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("img/Ball.png")
        self.image = pygame.transform.scale(self.image,(30, 30))
        self.rect = self.image.get_rect()
        self.col = 4
        self.row = 10
        self.x = 140
        self.tile = 40
            
    def move (self, action):
        self.col += action

    def draw (self, surface):
        y = self.tile * self.row + self.tile / 2
        self.x += ((self.tile * self.col + self.tile / 2) - self.x) * 0.4
        self.rect.center = (self.x, y)
        surface.blit(self.image, self.rect)

    def update(self, action): # for sprite Group
        self.move(action)
import pygame

class Player (pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
    
        
        self.images = [pygame.image.load("img/Ball.png"), pygame.image.load("img/Ball2.png"), pygame.image.load("img/Ball3.png"), pygame.image.load("img/Ball4.png")]
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],(45, 45))

        self.balls_index = 0

        self.rect = self.images[0].get_rect()
        self.col = 4
        self.row = 10
        self.x = 140
        self.tile = 60
        self.animation = 0
        self.animation_speed = 8
        self.jumping = False
            
    def move (self, action):
        self.col += action
        

    def draw (self, surface):
        y = self.tile * self.row + self.tile / 2
        self.x += ((self.tile * self.col + self.tile / 2) - self.x) * 0.6
        self.rect.center = (self.x, y)
        
        if self.jumping == True:
            image = pygame.transform.scale(self.images[self.balls_index], (70, 70))
            self.x -= 15
        else:
            image = self.images[self.balls_index]

        surface.blit(image, self.rect)

        self.animation += 1
        if self.animation >= self.animation_speed:
            self.balls_index += 1
            if self.balls_index == 4:
                self.balls_index = 0
            self.animation = 0

    
    def update(self, action): # for sprite Group
        self.move(action)

import pygame

class Player (pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
    
        broken_img = pygame.image.load("img/broken.png")

        self.images = [pygame.image.load("img/Ball.png"), pygame.image.load("img/Ball2.png"), pygame.image.load("img/Ball3.png"), pygame.image.load("img/Ball4.png"), broken_img]
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],(45, 45))
            if i==4:
                self.images[i] = pygame.transform.scale(broken_img,(55, 55))

        self.balls_index = 0

        self.rect = self.images[0].get_rect()
        self.col = 4
        self.row = 10
        self.x = 140
        self.tile = 60
        self.animation = 0
        self.animation_speed = 8
        self.jumping = False
        self.broken = False
            
    def move (self, action):
        if (action == -1 and self.col != 0):
            self.col += action
        if (action == 1 and self.col != 7):
            self.col += action
        
        

    def draw (self, surface):
        y = self.tile * self.row + self.tile / 2
        self.x += ((self.tile * self.col + self.tile / 2) - self.x) * 0.9
        self.rect.center = (self.x, y)
        
        if self.jumping == True:
            image = pygame.transform.scale(self.images[self.balls_index], (70, 70))
            self.x -= 15
        else:
            image = self.images[self.balls_index]

        surface.blit(image, self.rect)

        if (not self.broken):
            self.animation += 1
            if self.animation >= self.animation_speed:
                self.balls_index += 1
                if self.balls_index == 4:
                    self.balls_index = 0
                self.animation = 0
        else:
            self.balls_index = 4
            self.x -= 60
            y -= 60

        

    
    def update(self, action): # for sprite Group
        self.move(action)

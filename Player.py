import pygame

class Player (pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
    
        broken_img = pygame.image.load("img/broken.png")

        self.images = [pygame.image.load("img/Ball.png"), pygame.image.load("img/Ball2.png"), pygame.image.load("img/Ball3.png"), pygame.image.load("img/Ball4.png"), broken_img]
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],(45, 45))
            if i==4:
                self.images[i] = pygame.transform.scale(broken_img,(45, 45))

        self.balls_index = 0

        self.rect = self.images[0].get_rect()
        self.col = 4
        self.row = 10
        self.tile = 60
        self.x = self.tile * self.col + self.tile / 2
        self.animation = 0
        self.animation_speed = 8
        self.jumping = False
        self.broken = False

        self.jumping_offset = 1

        self.last_action = 0
    
    def move (self, action):
        if action == self.last_action:
            return

        self.last_action = action

        if (action == -1 and self.col != 0):
            self.col += action
        if (action == 1 and self.col != 7):
            self.col += action
        

    def draw (self, surface):

        y = self.tile * self.row + self.tile / 2
        self.x += ((self.tile * self.col + self.tile / 2) - self.x) * 0.4
        self.rect.center = (self.x, y)

        image = self.images[self.balls_index]
        
        if self.jumping == True:
            if self.jumping_offset < 1.5:
                self.jumping_offset += 0.08
        else:
            if self.jumping_offset > 1:
                self.jumping_offset -= 0.05

        
        image = pygame.transform.scale_by(self.images[self.balls_index], self.jumping_offset)
        rect = image.get_rect(center=self.rect.center)
        
        surface.blit(image, rect)

        if (not self.broken):
            self.animation += 1
            if self.animation >= self.animation_speed:
                self.balls_index += 1
                if self.balls_index == 4:
                    self.balls_index = 0
                self.animation = 0
        else:
            self.balls_index = 4

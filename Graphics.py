import pygame

ball_x = 137
speed = 3
ball_y = 400
FPS = 60
WIDTH, HEIGHT = 480, 720

tile_img = pygame.image.load("img/Tile.png")
tile_img = pygame.transform.scale(tile_img,(60, 60))

spike_img = pygame.image.load("img/Spike.png")
spike_img = pygame.transform.scale(spike_img,(60, 60))

boost_img = pygame.image.load("img/Boost.png")
boost_img = pygame.transform.scale(boost_img,(60, 60))

bonus200_img = pygame.image.load("img/Bonus500.png")
bonus200_img = pygame.transform.scale(bonus200_img,(60, 60))

bonus1000_img = pygame.image.load("img/Bonus1000.png")
bonus1000_img = pygame.transform.scale(bonus1000_img,(60, 60))

bonus3000_img = pygame.image.load("img/Bonus3000.png")
bonus3000_img = pygame.transform.scale(bonus3000_img,(60, 60))

star_img = pygame.image.load("img/Star.png")
star_img = pygame.transform.scale(star_img,(60, 60))

slime_img = pygame.image.load("img/Slime.png")
slime_img = pygame.transform.scale(slime_img,(60, 60))

jumper_img = pygame.image.load("img/jumper.png")
jumper_img = pygame.transform.scale(jumper_img,(60, 60))

ball_img = pygame.image.load("img/Ball.png")
ball_img = pygame.transform.scale(ball_img,(45, 45))

main_img = pygame.image.load("img/RollingLava.png")
main_img = pygame.transform.scale(main_img,(445, 292))

background_img = pygame.image.load("img/backgroundimg.png")
background_img = pygame.transform.scale(background_img,(480, 720))

class Graphics:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.main_surf = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption('Rolling Lava')

        self.main_scale = 1.0
        self.scale_direction = 1
        

    def draw(self, env):
        self.main_surf.blit(background_img, (0,0))
        self.draw_tiles(env.state)
        env.player.draw(self.main_surf)
        
        self.screen.blit(self.main_surf, (0, 0))

    def main_img_call(self, start):
       
        if not start:
            self.animate_main_img()
            img_w = int(445 * self.main_scale)
            img_h = int(292 * self.main_scale)

            scaled_img = pygame.transform.scale(main_img, (img_w, img_h))
            x = (WIDTH - img_w) // 2
            y = 150
            self.screen.blit(scaled_img, (x, y))


    def animate_main_img(self):
        speed = 0.002 
        max_scale = 1.05
        min_scale = 0.95

        self.main_scale += speed * self.scale_direction

        if self.main_scale >= max_scale or self.main_scale <= min_scale:
            self.scale_direction *= -1
    
    def draw_tiles(self, state):
        board = state.board
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row,col] != 0:
                    self.draw_tile((row, col), board[row, col])
        
    def draw_tile(self, row_col, current):
        x, y = self.calc_pos(row_col)
        
        if current == 1:
            self.main_surf.blit(tile_img, (x, y))
        if current == 2:
            self.main_surf.blit(tile_img, (x, y))
            self.main_surf.blit(spike_img, (x, y))
        if current == 3:
            self.main_surf.blit(boost_img, (x,y))
        if current == 4:
            self.main_surf.blit(slime_img, (x,y))
        if current == 5:
            self.main_surf.blit(jumper_img, (x,y))
        if current == 6:
            self.main_surf.blit(bonus200_img, (x,y))
        if current == 7:
            self.main_surf.blit(bonus1000_img, (x,y))
        if current == 8:
            self.main_surf.blit(bonus3000_img, (x,y))
        if current == 9: # easter egg
            self.main_surf.blit(tile_img, (x, y))
            self.main_surf.blit(star_img, (x,y))

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x,y))

    def calc_pos(self, row_col):
        row, col = row_col
        x = col * 60
        y = row * 60
        return x, y

        
    def __call__(self, env):
        self.draw(env)
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

bonus500_img = pygame.image.load("img/Bonus500.png")
bonus500_img = pygame.transform.scale(bonus500_img,(60, 60))

ball_img = pygame.image.load("img/Ball.png")
ball_img = pygame.transform.scale(ball_img,(45, 45))

background_img = pygame.image.load("img/backgroundimg.png")
background_img = pygame.transform.scale(background_img,(480, 720))

class Graphics:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.main_surf = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption('Rolling Lava')


    def draw(self, env):
        self.main_surf.blit(background_img, (0,0))
        self.draw_tiles(env.state)
        env.player.draw(self.main_surf)
        self.screen.blit(self.main_surf, (0, 0))
    
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
        if current == 100:
            self.main_surf.blit(bonus500_img, (x,y))

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
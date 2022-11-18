import pygame

class PoolTable:
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the table image and get its rect.
        self.table_img = pygame.image.load('images/Billiards/Pool_Table_Landscape.png')
        self.table_img = pygame.transform.smoothscale(self.table_img, (1000, 650))
        self.table_rect = self.table_img.get_rect()
        self.table_rect.center = self.screen_rect.center

    def blitme(self):
        self.screen.blit(self.table_img, self.table_rect)
import pygame


class CueStick():
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Billiards/cue_stick.png')
        self.image = pygame.transform.smoothscale(self.image, (400, 400))
        self.rot_image = self.image
        self.rect = self.image.get_rect()

        # Start each new shipp at the bottom center of the screen.
        self.rect.midleft = self.screen_rect.midleft
        # how much angle rotates with an arrow key
        self.step = 10
        self.theta = 0

    def update(self,direction):
        self.theta += direction * self.step

    def blitme(self):
        self.rot_image = pygame.transform.rotate(self.image,self.theta)
        self.rect = self.rot_image.get_rect()
        self.screen.blit(self.rot_image, self.rect)
import pygame


class CueStick():
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Billiards/cue_stick.png')
        self.image = pygame.transform.smoothscale(self.image, (400, 400))
        self.cue_stick = self.image.get_rect()

        # Start each new shipp at the bottom center of the screen.
        self.cue_stick.midleft = self.screen_rect.midleft

    def blitme(self):
        self.screen.blit(self.image, self.cue_stick)


import pygame

class Ball:
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/Billiards/cue_ball.png')
        self.image = pygame.transform.smoothscale(self.image, (30, 30))
        self.ball = self.image.get_rect()

        # Start each new shipp at the bottom center of the screen.
        self.ball.center = self.screen_rect.center

    def blitme(self):
        self.screen.blit(self.image, self.ball)

import pygame

class RedBall:
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the ball image and get its rect.
        self.image = pygame.image.load('images/Billiards/red_ball.png')
        self.image = pygame.transform.smoothscale(self.image, (35, 35))
        self.ball_rect = self.image.get_rect()

        self.ball_rect.midright = self.screen_rect.midright

        self.position = [800,250]

    def blitme(self):
        self.screen.blit(self.image, self.position)

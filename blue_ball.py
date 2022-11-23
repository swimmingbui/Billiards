import pygame

class BlueBall:
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the ball image and get its rect.
        self.image = pygame.image.load('images/Billiards/blue_ball.png')
        self.image = pygame.transform.smoothscale(self.image, (30, 30))
        self.ball_rect = self.image.get_rect()

        self.ball_rect.midright = self.screen_rect.midright

        self.position = [800,300]

    def blitme(self):
        self.screen.blit(self.image, self.position)

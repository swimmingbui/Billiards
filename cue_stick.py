import pygame
from ball import Ball

class CueStick:
    def __init__(self, bi_game):
        self.screen = bi_game.screen
        self.screen_rect = bi_game.screen.get_rect()

        # Load the cue stick image and get its rect.
        self.image = pygame.image.load('images/Billiards/cue_stick.png')
        self.image = pygame.transform.smoothscale(self.image, (400, 400))
        self.rot_image = self.image
        self.rect = self.image.get_rect()

        # Start each new cue stick at the left middle of the screen.
        #self.rect.midleft = self.screen_rect.midleft

        # how much an angle will be when rotating cue stick with an arrow key
        self.step = 5
        self.theta = 0
        self.ball = Ball(self)

    def update(self, direction):
        #determine angle to rotate image
        self.theta += direction * self.step

    def blitme(self):
        #rotating cue stick
        self.rot_image = pygame.transform.rotate(self.image, self.theta)
        self.rect.topright = self.ball.ball_rect.center
        self.screen.blit(self.rot_image, self.rect)

import sys

import pygame
from settings import Settings
from ball import Ball
from pool_table import PoolTable
from cue_stick import CueStick
from blue_ball import BlueBall
from red_ball import RedBall
from black_ball import BlackBall

class Billiards:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        #Set up game window
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Billiards")
        self.screen_rect = self.screen.get_rect()


        self.ball = Ball(self)
        self.cue_stick = CueStick(self)
        self.pool_table = PoolTable(self)
        self.blue_ball = BlueBall(self)
        self.red_ball = RedBall(self)
        self.black_ball = BlackBall(self)

    #draw pool table, ball, and cue stick
    def run_game(self):
        while True:
            self._check_events()
            self.screen.fill((0,0,0))
            self.pool_table.blitme()
            self.ball.blitme()
            self.blue_ball.blitme()
            self.red_ball.blitme()
            self.black_ball.blitme()
            self.cue_stick.blitme()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # press q to quit
                if event.key == pygame.K_q:
                    sys.exit()
                #press left arrow to move cue stick left
                if event.key == pygame.K_LEFT:
                    self.cue_stick.update(1)
                #press right arrow to move cue stick left
                if event.key == pygame.K_RIGHT:
                    self.cue_stick.update(-1)




        pygame.display.flip()

if __name__ == '__main__':
    bi = Billiards()
    bi.run_game()

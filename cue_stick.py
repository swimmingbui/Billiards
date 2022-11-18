import pygame
from pygame.sprite import Sprite
import math

class CueStick(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load('images/Billiards/cue_stick.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.theta = 0
        self.omega = 0


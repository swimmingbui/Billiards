import sys

import pygame

class Billiards:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1200,600))
        pygame.display.set_caption("Billiards")

        #draw pool table onto screen
        self.bg_img = pygame.image.load('images/Billiards/Pool_Table_Landscape.png').convert()
        self.bg_img = pygame.transform.smoothscale(self.bg_img, (800, 450))
        self.screen.blit(self.bg_img, [200, 125])

    def run_game(self):
        while True:
            self._check_events()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #press q to quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()


        pygame.display.flip()

if __name__ == '__main__':
    bi = Billiards()
    bi.run_game()

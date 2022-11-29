import pygame
#pymunk is a 2d physics library for rigid body physics
import pymunk
#link pygame and pymunk together
import pymunk.pygame_util

pygame.init()

#set dimensions for game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Billiards")

#pymunk space
space = pymunk.Space()
#draw shapes from pymunk onto game window
draw_options = pymunk.pygame_util.DrawOptions(screen)

#pymunk objects consist of body and shape
#function for creating balls
def create_ball(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = 5

    space.add(body, shape)
    return shape

new_ball = create_ball(25, (300, 100))

#game loop
run = True
while run:

    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # press ESC to quit
            if event.key == pygame.K_ESCAPE:
                run = False

    space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
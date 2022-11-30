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
#adds friction to the balls by adding them to the space's body
static_body = space.static_body

#draw shapes from pymunk onto game window
draw_options = pymunk.pygame_util.DrawOptions(screen)

#CLOCK
clock = pygame.time.Clock()
FPS = 120

#colors
BACKGROUND = (50,50,50)

#load images
table_image = pygame.image.load("images/table.png").convert_alpha()

#pymunk objects consist of body and shape
#function for creating balls
def create_ball(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    #link static object and the body created for the ball using pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
    #assigning variables to pivot
    pivot.max_bias = 0 #disable joint correction
    pivot.max_force = 1000 #imitate linear friction

    space.add(body, shape, pivot)
    return shape

new_ball = create_ball(25, (300, 300))

cue_ball = create_ball(25, (600, 310))

#game loop
run = True
while run:

    clock.tick(FPS)
    space.step(1 / FPS)

    #fill background
    screen.fill(BACKGROUND)

    #draw pool table
    screen.blit(table_image, (0,0))

    #check for events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            #pymunk checks for collisions
            cue_ball.body.apply_impulse_at_local_point((-1500, 0), (0,0))
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # press q to quit
            if event.key == pygame.K_q:
                run = False

    space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
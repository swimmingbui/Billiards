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

#game variables
diameter = 36

#colors
BACKGROUND = (50,50,50)

#load images
table_image = pygame.image.load("images/table.png").convert_alpha()
ball_images = []
for i in range(1,17):
    ball_image = pygame.image.load(f"images/ball_{i}.png").convert_alpha()
    ball_images.append(ball_image)

#pymunk objects consist of body and shape
#function for creating balls
def create_ball(radius, position):
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    #how much an object bounces
    shape.elasticity = 0.8
    #link static object and the body created for the ball using pivot joint to add friction
    pivot = pymunk.PivotJoint(static_body, body, (0,0), (0,0))
    #assigning variables to pivot
    pivot.max_bias = 0 #disable joint correction
    pivot.max_force = 1000 #imitate linear friction

    space.add(body, shape, pivot)
    return shape

#set up game balls that are in a triangle
balls = []
rows = 5
#potting balls (stripes and solids)
#making the balls in each column go from 5 down to 1
for column in range(5):
    for row in range(rows):
        position = (250 + (column * (diameter + 1)), 267 + (row * (diameter + 1)) + (column * diameter / 2))
        new_ball = create_ball(diameter / 2, position)
        balls.append(new_ball)
    rows -= 1
#find position to place cue ball
position = (888, SCREEN_HEIGHT / 2)
cue_ball = create_ball(diameter / 2, position)
balls.append(cue_ball)

#create pool table pockets
walls = [
    #coordinates for one pocket
    [(88,56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(89, 621), (110, 600),(556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

#function for creating pockets
#pymunk objects consist of body and shape
#polygon dimensions are the dimensions of the pocjet
def create_walls(polygon_dimensions):
    #create a static object instead of a moving object
    body = pymunk.Body(body_type= pymunk.Body.STATIC)
    body.position = ((0,0))
    shape = pymunk.Poly(body, polygon_dimensions)
    #how much an object bounces
    shape.elasticity = 0.8

    space.add(body, shape)

for wall in walls:
    create_walls(wall)

#game loop
run = True
while run:

    clock.tick(FPS)
    space.step(1 / FPS)

    #fill background
    screen.fill(BACKGROUND)

    #draw pool table
    screen.blit(table_image, (0,0))

    #draw pool balls
    for i, ball in enumerate(balls):
        screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

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

    #space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
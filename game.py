import pygame
#pymunk is a 2d physics library for rigid body physics
import pymunk
#link pygame and pymunk together
import pymunk.pygame_util
import math

pygame.init()

#set dimensions for game window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 678
BOTTOM_PANEL = 50

#game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + BOTTOM_PANEL))
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
lives = 3
diameter = 36
pocket_diameter = 66
force = 0
taking_shot = True
powering_up = False
cue_ball_potted = False
game_running = True
max_force = 10000
force_direction = 1
potted_balls = []

#colors
BACKGROUND = (50,50,50)
RED = (255, 0, 0)
GREEN = (0, 110, 24)
WHITE = (255, 255, 255)

#fonts
font = pygame.font.SysFont("Comic Sans MS", 30)
large_font = pygame.font.SysFont("Comic Sans MS", 60)


#load images
cue_stick_image = pygame.image.load("images/cue_stick.png").convert_alpha()
table_image = pygame.image.load("images/table.png").convert_alpha()
ball_images = []

#load each of the ball's images so stripes are stripes and solids are solids
for i in range(1,17):
    ball_image = pygame.image.load(f"images/ball_{i}.png").convert_alpha()
    ball_images.append(ball_image)

#function for drawing text onto the screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

#create six pockets on table
pockets = [
  (55, 63),
  (592, 48),
  (1134, 64),
  (55, 616),
  (592, 629),
  (1134, 616)
]

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

#create cue stick
class CueStick():
    def __init__(self, position):
        self.original_image = cue_stick_image
        self.theta = 0
        self.image = pygame.transform.rotate(self.original_image, self.theta)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self, theta):
        self.theta = theta

    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.theta)
        #the cue stick image is too long making wonky rotations
        #set the x and y coordinates at the tip of the cue stick
        surface.blit(self.image,
            (self.rect.centerx - self.image.get_width() / 2,
            self.rect.centery - self.image.get_height() / 2)
                     )

cue_stick = CueStick(balls[-1].body.position)

#create power bars to show how  hard cue ball will be hit
power_bar = pygame.Surface((10, 20))
power_bar.fill(RED)

#game loop
run = True
while run:
    Sound1 = pygame.mixer.Sound("sounds/collisions/Audio/impactBell_heavy_000.ogg")

    clock.tick(FPS)
    space.step(1 / FPS)

    #fill background
    screen.fill(BACKGROUND)

    #draw pool table
    screen.blit(table_image, (0,0))

    #check if any balls have been potted
    for i, ball in enumerate(balls):
        for pocket in pockets:
            ball_x_distance = abs(ball.body.position[0] - pocket[0])
            ball_y_distance = abs(ball.body.position[1] - pocket[1])
            #gives distance between center of ball and center of pocket
            ball_distance = math.sqrt((ball_x_distance ** 2) + (ball_y_distance ** 2))
            if ball_distance <= pocket_diameter / 2:
                #check if potted ball was the cue ball
                if i == len(balls) - 1:
                    lives -= 1
                    cue_ball_potted = True
                    ball.body.position = (-100, -100)
                    ball.body.velocity = (0.0, 0.0)
                else:
                    space.remove(ball.body)
                    balls.remove(ball)
                    potted_balls.append(ball_images[i])
                    ball_images.pop(i)




    #draw pool balls
    for i, ball in enumerate(balls):
        screen.blit(ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    #check if all balls have stopped moving
    taking_shot = True
    #balls is list of pymunk objects
    #makes cue stick disappear after each shot
    for ball in balls:
        #index 0 is x velocity index 1 is y velocity
        if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
            taking_shot = False

    #draw cue stick
    if taking_shot == True and game_running == True:
        #reposition cue ball if it is potted
        if cue_ball_potted == True:
            balls[-1].body.position = (888, SCREEN_HEIGHT / 2)
            cue_ball_potted = False
        #calculate cue stick angle through mouse position
        mouse_position = pygame.mouse.get_pos()
        #reposition cue stick with cue ball
        cue_stick.rect.center = balls[-1].body.position
        x_distance = balls[-1].body.position[0] - mouse_position[0]
        y_distance = -(balls[-1].body.position[1] - mouse_position[1]) # negative because pygame y coordinates increase down screen
        #find angle in radians which is converted to degrees with degrees function from math library
        cue_stick_angle = math.degrees(math.atan2(y_distance, x_distance))
        cue_stick.update(cue_stick_angle)
        cue_stick.draw(screen)

    #power up cue stick
    if powering_up == True and game_running == True:
        force += 100 * force_direction
        if force >= max_force or force <= 0:
            force_direction *= -1
        #draw power bars
        for bar in range(math.ceil(force / 2000)):
            screen.blit(power_bar,
                (balls[-1].body.position[0] - 30 + (bar * 15), balls[-1].body.position[1] + 30))
    elif powering_up == False and taking_shot == True:
        # finding angle to shoot the cue ball in x and y direction
        x_impulse = math.cos(math.radians(cue_stick_angle))
        y_impulse = math.sin(math.radians(cue_stick_angle))
        balls[-1].body.apply_impulse_at_local_point((force * -x_impulse, force * y_impulse), (0, 0))
        force = 0
        force_direction = 1

    #draw bottom panel
    pygame.draw.rect(screen, BACKGROUND, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
    draw_text("LIVES: " + str(lives), font, GREEN, SCREEN_WIDTH - 200, SCREEN_HEIGHT + 10)

    #draw potted balls in bottom panel
    for i, ball in enumerate(potted_balls):
        screen.blit(ball, (10 + ( i * 50), SCREEN_HEIGHT + 10 ))

    #check for game over
    if lives <= 0:
        screen.fill(RED)
        draw_text("GAME OVER", large_font, WHITE, SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 - 100)
        game_running = False

    #check if all balls are potted
    if len(balls) == 1:
        draw_text("YOU WIN! :)", large_font, WHITE, SCREEN_WIDTH / 2 - 160, SCREEN_HEIGHT / 2 - 100)
        game_running = False

    #check for events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
            powering_up = True
        #determine how hard to hit cue ball
        if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
            pygame.mixer.Sound.play(Sound1)
            powering_up = False

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # press q to quit
            if event.key == pygame.K_q:
                run = False

    #space.debug_draw(draw_options)
    pygame.display.update()

pygame.quit()
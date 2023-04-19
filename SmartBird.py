#---------------------------------------------------------------------------------------------------------
# importing libraries

# 1º - pip install pygame
# pygame version used: 2.3.0 
# one of the most used libraries for game creating in python
import pygame

# this module provides a simple way to use functionality that is operating system dependent. 
# we are gonna use it to work with the images.
import os 

# random numbers generation library 
import random
#---------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------
# defining constants - game settings

# screen dimensions

# screen width
SCREEN_WIDTH = 500
# screen height
SCREEN_HEIGHT = 800

# images

# pygame.transform.scale2x() -> to increase 2 times the dimensions
# pygame.image.load() -> to load the image
# os.pah.join() -> to define the path of the image

# pipe image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
# base image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
# background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
# birds images
BIRDS_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))
        ]
# there are 3 position to the bird

# score text

# initializing the text
pygame.font.init() 
# score font
SCORE_FONTE = pygame.font.SysFont('arial', 50)
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# creating game objects: what is in the game and what can move

# background - freeze
# bird - moves (y axis)
# pipe - moves (x axis)
# base - moves (x axis)

# we are gonna create the 3 objects, that moves, as a python class:

class Bird:
    
    # defining Bird constants
    
    # Bird images 
    IMGS = BIRDS_IMGS

    # rotation animations    
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    # defining Bird attributes

    def __init__(self, x, y):
        
        # (x , y) where the Bird is born
        self.x = x
        self.y = y

        self.height = self.y

        # angle of the Bird -> start horizontal
        self.angle = 0

        # velocity of the Bird on y axis -> start 0
        self.velocity = 0

        # time for the bird to jump and come back -> parabolic motion
        self.time = 0

        # this is going to be used to change the Bird image
        self.image_counter = 0

        # current Bird image
        self.image = self.IMGS[0]

    # Bird actions

    def jump(self):

        # y is positive downward and negative upward
        self.velocity = -10.5

        # when the bird start jumping, the time is zero
        self.time = 0

        self.height = self.y

    # This function is gonna to be run every frame
    def move(self):

        # calculate the displacement
        self.time += 1
        # S = S0 + v0.t + a.t²/2  ->  MUV space formula
        displacement =  (self.velocity)*(self.time) (1.5)*(self.time**2)
        
        # restrict displacement
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2 # increase the jump
        
        # displace the Bird     
        self.y += displacement

        # animate Bird angle
        # displacement < 0 -> jumping
        # self.y < (self.height + 50) -> start to turn after while
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
            else:
                if self.angle > -90:
                    self.angle -= self.ROTATION_VELOCITY

    # draw Bird in the screen
    def draw(self, screen):
        
        # define which Bird image that is going to be used
        # 5 in 5 frames - change the image - slap wings
        self.image_counter += 1 
        if self.image_counter < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_counter < (self.ANIMATION_TIME)*2:
            self.image = self.IMGS[1]
        elif self.image_counter < (self.ANIMATION_TIME)*3:
            self.image = self.IMGS[2]
        elif self.image_counter < (self.ANIMATION_TIME)*4:
            self.image = self.IMGS[1]
        elif self.image_counter < (self.ANIMATION_TIME)*4 + 1:
            self.image = self.IMGS[0]
            self.image_counter = 0

        # if the Bird is falling, it's is not to slap wings
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_counter = (self.ANIMATION_TIME)*2 # the next slap wings is to down

        # to draw the Bird image

        # the Bird is constantly drawn, and it must to be drawn in the right angle
        image_rotated = pygame.transform.rotate(self.image, self.angle)

        # the Bird is goint to be drawn in a rectangle
        image_center = self.image.get_rect(topleft = (self.x, self.y)).center
        rectangle = image_rotated.get_rect(center=image_center)

        # to draw
        screen.blit(image_rotated, rectangle.topleft)

    # it is going to be drawn a mask around the Bird to help the colision system
    def get_mask(self):
        pygame.mask.from_surface(self.image)

    # END Bird


class Pipe:
    
    # defining Pipe constants

    # distance between the pipes (one above, one below)
    DISTANCE =  200

    # the Pipes are going to move in the x axis
    VELOCITY = 5

    # the Pipes needs the x point to be drawn, but the "y" is randon
    def __init__(self, x):
        
        self.x = x

        # reference point to draw the pipes -- "y"
        self.height = 0 

        # positions of the "bases" of the pipes
        self.pos_top = 0
        self.pos_bot= 0

        # images - they are CONSTANT
        # the pipe image is flipped in the y axis ---------- (x,y)
        self.TOP_PIPE_IMG = pygame.transform.flip(PIPE_IMG, False, True)
        self.BOT_PIPE_IMG = PIPE_IMG

        # parameter
        # the bird has already passed by?
        self.passed = False

        # function call
        self.define_height()

    def define_height(self):

        # (50,450) --- to not to be impossible to the bird to pass by
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.TOP_PIPE_IMG.get_height()
        self.pos_bot = self.height + self.DISTANCE

    def move(self):

        # x axis is negative to the left
        self.x -= self.VELOCITY

    # draw Pipe in the screen
    def draw(self, screen):
        # the blit() method will draw the contents of a pygame object
        # (image, position)
        screen.blit(self.TOP_PIPE_IMG, (self.x, self.pos_top))
        screen.blit(self.BOT_PIPE_IMG, (self.x, self.pos_bot))

    # verify if the Pipe collides with the Bird
    def collide(self, bird):

        # getting the masks of the objects
        bird_mask = bird.get_mask()
        top_pipe_mask = pygame.mask.from_surface(self.TOP_PIPE_IMG)
        bot_pipe_mask = pygame.mask.from_surface(self.BOT_PIPE_IMG)

        # calculating the distances between the objects
        # round() is to round the number to an integer, because the bird can have a float one
        distance_top_pipe = (self.x - round(bird.x), self.pos_top - round(bird.y))
        distance_bot_pipe = (self.x - round(bird.x), self.pos_bot - round(bird.y))

        # verify the collision with mask
        # overlap() are there two equal pixel overlapping each other?
        top_collided = bird_mask.overlap(top_pipe_mask, distance_top_pipe) # boolean value
        bot_collided = bird_mask.overlap(bot_pipe_mask, distance_bot_pipe) # boolean value

        # There are collision
        if top_collided == True or bot_collided == True:
            return True
        else:
            return False
        
        # END Pipe


class Base:
    
    # defining Pipe constants

    # the Base are going to move in the x axis
    VELOCITY = 5

    # Base width - there are going to be needed two bases, because the screen cannot to be empty
    # when the Base moves. The second one is going to be created with the Base width as reference
    WIDTH = BASE_IMG.get_width()

    IMAGE = BASE_IMG

    # only the y is needed, because de x of the two Bases are going to be defined by this function
    def __init__(self, y):
        
        # height of the base
        self.y = y

        # initial position of the two bases
        self.x1 = 0
        self.x2 = self.x1 + self.WIDTH

    def move(self):

        # they moves to the left
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        # if the base 1 is off the screen
        if self.x1 + self.WIDTH < 0:
             # put the base 1 next to the base 2
             self.x1 = self.x2 + self.WIDTH

        # if the base 2 is off the screen
        if self.x2 + self.WIDTH < 0:
             # put the base 2 next to the base 1
             self.x2 = self.x1 + self.WIDTH

    # draw Base in the screen
    def draw(self, screen):
        # the blit() method will draw the contents of a pygame object
        # (image, initial position)
        screen.blit(self.IMAGE, (self.x1, self.Y))
        screen.blit(self.IMAGE, (self.x2, self.Y))

    # END Base
#---------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------
# function to draw the screen

def  draw_screen(screen, birds, pipes, base, score_points):

    # draw the background of the game
    screen.blit(BG_IMG, (0,0))

    # there are going to be several birds when the IA is running
    for bird in birds:
        bird.draw(screen)

    # there are going to be most the one pipe on the screen at the same time
    for pipe in pipes:
        pipe.draw(screen)

    # score text
    # render() is to render the message on the screen
    # 1 -> it is for the text to be round and not pixelated
    # (255,255,255) -> RGB color
    text = SCORE_FONTE.render(f"Pontuação: {score_points}", 1, (255,255,255))
    screen.blit(text, (SCREEN_WIDTH-10-text.get_width(), 10))

    base.draw(screen)

    # updating the screen
    pygame.display.update()
#---------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------
# game's main function

def main():

    # defining initial parameters

    # list of birds
    # by now, only one bird
    # (230, 350) - initial position of the bird
    birds = [Bird(230, 350)]

    # 730 -> remember: the y axis grows to down
    base = Base(730)

    # list of pipes
    # by now, only one pipe
    # 700 -> it appear behind of the screen (SCREEN_WIDTH = 500)
    pipes = [Pipe(700)]

    # create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    score_points = 0

    # how often do you refresh the screen? FPS -> frame per second
    clock = pygame.time.Clock()


    # starting the game
    # a game is an infinite looping

    # the game is running
    running = True

    while running:

        # time is ticking
        # 30 FPS
        clock.tick(30)

        # interaction with the game
        # pygame.event.get() return a list of events
        # example: press the space button is an event
        for event in pygame.event.get():

            # close screen clicking on the "x"
            if event.type == pygame.QUIT:
                running = False
                # close screen
                pygame.quit()
                # quit game (the code)
                quit()

            # press a keyboard key    
            if event.type == pygame.KEYDOWN:
                # the key is the space?
                if event.key == pygame.K_SPACE:
                    # jump, bird, jump
                    for bird in birds:
                        bird.jump()

        # draw the screen is the last thing you do
        draw_screen(screen, birds, pipes, base, score_points)

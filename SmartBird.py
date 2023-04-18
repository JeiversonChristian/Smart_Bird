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
SW = 500
# screen height
SH = 800

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
SF = pygame.font.SysFont('arial', 50)
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

    # draw bird in the screen
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
    pass

class Base:
    pass

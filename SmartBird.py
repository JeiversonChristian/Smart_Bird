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
    
    # images
    IMGS = BIRDS_IMGS

    # rotation animations

class Pipe:
    pass

class Base:
    pass

# HERE THE BIRD IS TRULY SMART

#---------------------------------------------------------------------------------------------------------
# importing libraries

# 1º - pip install neat-python
# neat version used: 0.92
# NEAT - Neural Evolution Augmenting Topology
import neat

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
# "Almost global variables"

# inform if the AI is playing
ai_playing = True

# number of current generation
generation = 0

# this will save the max score of the current generation and the max fitness
last_max_score = 0
last_max_fitness = 0
#---------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------
# defining constants - game settings

# screen dimensions

# screen width
SCREEN_WIDTH = 500
# screen height
SCREEN_HEIGHT = 700

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
SCORE_FONTE = pygame.font.SysFont('arial', 35)
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
    ROTATION_VELOCITY = 30
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
        displacement =  (self.velocity)*(self.time) + (1.5)*(self.time**2)
        
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
        if self.angle <= -100:
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
        return pygame.mask.from_surface(self.image)

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
        distance_top_pipe = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_bot_pipe = (self.x - bird.x, self.pos_bot - round(bird.y))

        # verify the collision with mask
        # overlap() are there two equal pixel overlapping each other?
        top_collided = bird_mask.overlap(top_pipe_mask, distance_top_pipe) # (x,y) of collision
        bot_collided = bird_mask.overlap(bot_pipe_mask, distance_bot_pipe) # (x,y) of collision
        # if there is no collision, then the overlap return 'none'

        # Are there collision?
        if ((top_collided is None) and (bot_collided is None)):
            return False
        if ((top_collided is not None) or (bot_collided is not None)):
            return True
        
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
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))

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

    # if AI is playing, show the number of current generation
    if ai_playing == True:
        text = SCORE_FONTE.render(f"Geração: {generation}", 1, (255,255,255))
        screen.blit(text, (10, 10))

    base.draw(screen)

    # updating the screen
    pygame.display.update()
#---------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------
# game's main function
# to the AI: It's the fitness function -> it says how good was the bird
# the following parameters are required by the NEAT library
# genomes: the neural networks settings 
# config: all config.txt settings
def main(genomes, config):

    # it's to python understand that generation is a global variable, created in the beginning of the code
    # this was needed because we are modifying its value
    global generation, last_max_score, weights_best_bird

    # Each time main() runs, it's because it is the next generation
    generation += 1
    print("-------------------------------------------")    
    print(f"Generation: {generation}")
    
    last_max_score = 0
    last_max_fitness = 0

    # defining initial parameters

     # if the AI is playing, we are going to need 100 birds
    if ai_playing == True:
        # the 'i' bird matches the 'i' genome that matches the 'i' neural_networks
        neural_networks = []
        genomes_list = [] # genomes are the settings to create the neural networks
        birds = []


        # why _ ?
        # genomes is not a regular list
        # genomes = [(IDGenome, Genome), (IDGenome, Genome), (IDGenome, Genome), ...]
        # we just need the "Genome"
        # _ will save the "IDGenome" to discard it later
        for _, genome in genomes:
            # nn -> neural network
            # FeedForward -> values goes from left to right in the network 
            neural_network = neat.nn.FeedForwardNetwork.create(genome, config)
            neural_networks.append(neural_network)

            # bird's "score" -> is the bird good or not?
            # not the game's score, because, two birds with the same game score can be different
            # who gets the farthest?
            genome.fitness = 0 
            
            genomes_list.append(genome)
            birds.append(Bird(230, 350))

    else:    
        # only one pipe
        # (230, 350) - initial position of the bird
        birds = [Bird(230, 350)]


    # 730 -> remember: the y axis grows to down
    base = Base(630)

    # list of pipes   
    # only one pipe
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
                print(f"Max score: {last_max_score}")
                print(f"Max fitness: {last_max_fitness}")
                print("-------------------------------------------")
                # quit game (the code)
                quit()
            # the space button is only for the human
            if ai_playing == False:
                # press a keyboard key    
                if event.type == pygame.KEYDOWN:
                    # the key is the space?
                    if event.key == pygame.K_SPACE:
                        # jump, bird, jump
                        for bird in birds:
                            bird.jump()
        
        # indice of the pipe that bird has to look out
        pipe_indice = 0
        # if there is some bird
        if len(birds)>0:
            # if there are 2 pipes at least
            # and the first bird (there is always be a first) has already passed by the pipe
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].TOP_PIPE_IMG.get_width()):
                pipe_indice = 1
        else:
            # end game
            running = False
            break

        # start move the game objects

        # bird, move!

        for i, bird in enumerate(birds): # we need the address (i) and the element (bird)
            bird.move()
            # increase the bird fitness
            genomes_list[i].fitness += 0.1
            # activate the neural network and it gives the output
            # based on 3 attributes: bird y position, absolute value of distance in y from the pipes
            # and 
            output = neural_networks[i].activate((bird.y, 
                                                  abs(bird.y - pipes[pipe_indice].pos_top), 
                                                  abs(bird.y - pipes[pipe_indice].pos_bot)))
            # [-1,+1] -> output > 0.5, so the bird jumps
            if output[0] > 0.5:
                bird.jump()

        # base, move!
        base.move()

        # pipe, move!

        # auxiliary variable
        # do we need to add a pipe?
        add_pipe = False
        # removed pipes
        removed_pippes = []

        for pipe in pipes:
            for i, bird in enumerate(birds): # we need the address (i) and the element (bird)
                # if bird collides with pipe
                if pipe.collide(bird) == True:
                    # remove that bird of list of birds
                    birds.pop(i)
                    if ai_playing == True:
                        # penalizing the bird
                        genomes_list[i].fitness -= 1
                        # remove that genome of list of genomes
                        genomes_list.pop(i)
                        # remove that neural _networks of the list
                        neural_networks.pop(i)
                # if the bird has not passed by the pipe yet, but the bird is the half way through
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move()
            # if the pipe has passed by the screen
            if pipe.x + pipe.TOP_PIPE_IMG.get_width() < 0:
                # add that pipe to the list of removed pipes
                removed_pippes.append(pipe)
        
        # when the verification of the entire list of pipes ends
        # we can change the list of pipes
        if add_pipe == True:
            score_points += 1
            last_max_score = score_points
            pipes.append(Pipe(600))
            # when we need to add a pipe, it's because the bird has passed by one
            for genome in genomes_list:
                genome.fitness += 5
        for pipe in removed_pippes:
            pipes.remove(pipe)

        # if the birds passes the base or the top of the screen
        for i, bird in enumerate(birds):  # we need the address (i) and the element (bird)
            if bird.y + bird.image.get_height() > base.y or bird.y < 0:
                # remove that bird of list of birds
                birds.pop(i)
                # here we are not penalizing the AI
                if ai_playing == True:
                    if genomes_list[i].fitness > last_max_fitness:
                        last_max_fitness = genomes_list[i].fitness
                    genomes_list.pop(i)
                    neural_networks.pop(i)

        # draw the screen is the last thing you do
        draw_screen(screen, birds, pipes, base, score_points)
    print(f"Max score: {last_max_score}")
    print(f"Max fitness: {last_max_fitness}")
    print("-------------------------------------------")
#---------------------------------------------------------------------------------------------------------

def run_it(config_path):
    # that variable will receive the data from the config file
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    
    # creating the birds population using the config
    birds_population = neat.Population(config)

    # show statistics on the terminal
    #birds_population.add_reporter(neat.StdOutReporter(True))
    #birds_population.add_reporter(neat.StatisticsReporter())

    if ai_playing == True:
        # run(fitness_function, number of generations)
        birds_population.run(main, 100)
    else:
        # if the AI is not playing, there is not a genomes and config
        main(None, None)


# only run when it runs from it self
if __name__ == '__main__':

    # this will get this file's path
    SmartBirdAI_path = os.path.dirname(__file__)

    # this will join the two paths
    config_path = os.path.join(SmartBirdAI_path, 'config.txt')
    # so we ensure that the run will find the path to the config file
    run_it(config_path)

# -*- coding: utf-8 -*-
from copy import deepcopy

import pygame
import time
from utils import *


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False in order to exit the main loop
                running = False
    pygame.quit()
    

def movingDrone(currentMap, path, energy, speed=1):
    # animation of a drone on a path
    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))
    drona = pygame.image.load("drona.png")

    # drone_brick = where the drone went
    drone_brick = pygame.Surface((20, 20))
    drone_brick.fill(GREEN)
    drone_brick.set_alpha(50)
    # surveilled square
    sighted_cell = pygame.Surface((20, 20))
    sighted_cell.fill(RED)
    sighted_cell.set_alpha(50)

    sensors = energy.keys()
        
    for i in range(len(path)):
        screen.blit(image(currentMap), (0, 0))
        
        for j in range(i+1):
            x = path[j][0]
            y = path[j][1]
            screen.blit(drone_brick, (y*20, x*20))

            if (x, y) in sensors:
                # draw sighted cells
                energy_value = energy[(x, y)]
                for direction in DIRECTION_DICT.values():  # UP, DOWN, RIGHT, LEFT
                    aux_x, aux_y = x, y
                    for _ in range(energy_value):
                        aux_x += direction[0]
                        aux_y += direction[1]
                        if currentMap.check_if_pos_valid(aux_x, aux_y):
                            screen.blit(sighted_cell, (aux_y*20, aux_x*20))
                        else:
                            break

        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()
        time.sleep(0.5 * speed)            
    closePyGame()


def image(currentMap, colour=BLUE, background=WHITE):
    # creates the image of a map
    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20, 20))
    sensor = pygame.Surface((20, 20))
    sensor.fill(RED)
    brick.fill(colour)
    imagine.fill(background)

    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (j * 20, i * 20))
            if currentMap.surface[i][j] == 2:
                imagine.blit(sensor, (j * 20, i * 20))
                
    return imagine        

# import the pygame module, so you can use it
from random import randint

import pygame
import time
from pygame.locals import *
from common.global_variables import *
from domain.Map import Map
from domain.Drone import Drone
from service.service import Service


def dummysearch():
    # example of some path in test1.map from [5,7] to [7,11]
    return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]


def displayWithPath(service, index, path, destination):
    # choose color path and window caption for current algorithm
    colours = [GREEN, RED, PINK, GOLD]
    color = colours[index]
    captions = [f'Greedy algorithm: {len(path)} steps', f'A* algorithm: {len(path)} steps',
                f'Simulated annealing algorithm: {len(path)} steps']
    pygame.display.set_caption(captions[index])

    mark = pygame.Surface((20, 20))
    mark.fill(color)

    # reset the image to the initial one to erase old path
    image = service.getMap().image()

    # draw new path
    for move in path:
        image.blit(mark, (move[1] * 20, move[0] * 20))

    # draw the drone and destination
    image = service.getDrone().mapDroneAndEndPoint(image, destination)

    return image


def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("../logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we create the map
    m = Map(NR_LINES, NR_COLUMNS)
    m.randomMap()

    # we create the drone
    d = Drone()

    # create service and generate good coords for drone
    service = Service(d, m)
    new_coordinates = service.generate_coordinates()
    d.modify_coordinates(new_coordinates[0], new_coordinates[1])

    # create a surface on screen that has the size of N*20 X N*20
    screen = pygame.display.set_mode((NR_LINES * 20, NR_COLUMNS * 20))
    screen.fill(WHITE)

    # define a variable to control the main loop
    running = True

    # generate destination
    destination = service.generate_coordinates()

    # show elements on screen (walls, drone, destination)
    initial_image = m.image()
    screen.blit(d.mapDroneAndEndPoint(initial_image, destination), (0, 0))
    index = 0
    path = []

    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            
            if event.type == KEYDOWN:
                # everytime a key is pressed you show next algorithm's path
                if index == 0:
                    startTime = time.time()
                    path = service.GreedyAlgorithm(destination)
                    endTime = time.time()
                    print("Greedy took: ", endTime - startTime, "sec")
                    print(path)

                if index == 1:
                    startTime = time.time()
                    path = service.AStarAlgorithm(destination)
                    endTime = time.time()
                    print("A* took: ", endTime - startTime, "sec")
                    print(path)

                if index == 2:
                    startTime = time.time()
                    path = service.SimulatedAnnealingAlgorithm(destination, 1000)
                    endTime = time.time()
                    print("Simulated annealing took: ", endTime - startTime, "sec")
                    print(path)

                if index <= 2:
                    screen.blit(
                        displayWithPath(
                            service,
                            index,
                            path,
                            destination,
                        ),
                        (0, 0)
                    )

                    index = index+1
                else:  # show again the paths (you have to press one more time before it updates)
                    index = 0
                # d.move(m)  # this call will be erased

        pygame.display.flip()  # idk what this does but it works

    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()

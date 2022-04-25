import pygame

import numpy as np

from Global_variables import *


class DMap:
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = -1

    def markDetectedWalls(self, e, x, y):
        """
        Based on the environment, we use the sensors to read nr of available squares (until we hit a wall).

        We update the drone's map with what we receive from the "readUDMSensors" function like this:
        - we use an auxiliary coordinate, "i", which will take the values x-1(for UP), x+1(for DOWN)
        - we use an auxiliary coordinate, "j", which will take the values y+1(for LEFT), y-1(for RIGHT)
        - we paint the free surface by marking it with "0", and the wall by marking it with "1"
        - we decrement the auxiliary coord (i/j) and mark the surface with 0 until:
            - we are either at the border: UP(i >= 0), DOWN(i < self.__n), LEFT(j < self.__m), RIGHT(j >= 0)
            - or we hit a a wall (so the squares after the wall will not be painted)
        - after we painted the free space, if we did not reach a border, we also paint the wall
        :param e: Environment instance
        :param x: x-coordinate of drone
        :param y: y-coordinate of drone
        :return: nothing
        """
        if x is None or y is None:
            return None
        # mark on this map the walls that you detect (nr of squares in a certain direction until you hit the wall)
        walls = e.readUDMSensors(x, y)

        i = x - 1
        if walls[UP] > 0:
            while (i >= 0) and (i >= x - walls[UP]):
                self.surface[i][y] = 0
                i = i - 1
        if i >= 0:
            self.surface[i][y] = 1

        i = x + 1
        if walls[DOWN] > 0:
            while (i < self.__n) and (i <= x + walls[DOWN]):
                self.surface[i][y] = 0
                i = i + 1
        if i < self.__n:
            self.surface[i][y] = 1

        j = y + 1 # auxiliary coord
        if walls[LEFT] > 0:
            while (j < self.__m) and (j <= y + walls[LEFT]):
                self.surface[x][j] = 0
                j = j + 1
        if j < self.__m:
            self.surface[x][j] = 1

        j = y - 1
        if walls[RIGHT] > 0:
            while (j >= 0) and (j >= y - walls[RIGHT]):
                self.surface[x][j] = 0
                j = j - 1
        if j >= 0:
            self.surface[x][j] = 1

        return None

    def image(self, x, y):
        """
        The right image
        :param x:
        :param y:
        :return:
        """
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(LIGHT_PURPLE)
        brick.fill(PURPLE)
        imagine.fill(GRAYBLUE)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 0:
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine

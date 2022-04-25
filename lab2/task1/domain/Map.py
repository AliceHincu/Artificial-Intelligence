import pickle
from random import random
import numpy as np
import pygame
from common.global_variables import *


class Map:
    def __init__(self, n=NR_LINES, m=NR_COLUMNS):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="../maps/test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((NR_LINES*20, NR_COLUMNS*20))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def is_position_valid(self, x, y):
        """
        Check if the given position is valid meaning:
        - drone is still in the map
        - drone is not over a brick
        :param x: x-coordinate of drone
        :param y: y-coordinate of drone
        :return:
        """
        if x < 0 or y < 0 or x >= self.n or y >= self.m:  # out of bounds
            return False
        if self.surface[x][y] == 1:  # over a brick
            return False
        return True

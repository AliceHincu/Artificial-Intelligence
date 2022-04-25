import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from common.global_variables import *


class Drone:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def modify_coordinates(self, newX, newY):
        self.x = newX
        self.y = newY

    def get_coordinates(self):
        return self.x, self.y

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < NR_LINES:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < NR_COLUMNS:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("../drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))

        return mapImage

    def mapDroneAndEndPoint(self, mapImage, endPointCoords):
        drona = pygame.image.load("../drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        destination = pygame.image.load("../destination.png")
        destination = pygame.transform.scale(destination, (20, 20))
        mapImage.blit(destination, (endPointCoords[1] * 20, endPointCoords[0] * 20))

        return mapImage

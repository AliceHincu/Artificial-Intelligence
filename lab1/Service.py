from Environment import Environment
from Drone import Drone
from DroneMap import DMap
from random import randint


class Service:
    def __init__(self):
        self.__environment = Environment()
        self.__droneMap = DMap()
        self.__drone = Drone(randint(0, 19), randint(0, 19))

        self.__environment.loadEnvironment("test2.map")

    def getEnvironmentImage(self):
        return self.__environment.image()

    def droneCanMove(self):
        return self.__drone.canStillMove()

    def getDroneMapImage(self):
        return self.__droneMap.image(self.__drone.x, self.__drone.y)

    def markDetectedWalls(self):
        self.__droneMap.markDetectedWalls(self.__environment, self.__drone.x, self.__drone.y)

    def moveDrone(self):
        return self.__drone.moveDFS(self.__droneMap)

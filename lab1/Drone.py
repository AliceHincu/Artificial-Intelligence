import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.__visited = {}  # 0 for not visited, 1 for visited, the key are the coords of squares
        for i in range(0, 20):
            for j in range(0, 20):
                self.__visited[(i, j)] = 0
        self.__lastVisitedStack = [(x, y)] # the last visited position is the initial position

    def canStillMove(self):
        return not (self.x is None or self.y is None)

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def getNeighbours(self, detectedMap):
        """
        Get the neighbours of the drone
        :param detectedMap: the map that the drone detected until now
        :return: list of neighbours
        """
        neighbours = []
        if self.x > 0 and detectedMap.surface[self.x - 1][self.y] == 0:
            neighbours.append((self.x - 1, self.y))  # up neighbour
        if self.x < 19 and detectedMap.surface[self.x + 1][self.y] == 0:
            neighbours.append((self.x + 1, self.y))  # down neighbour
        if self.y > 0 and detectedMap.surface[self.x][self.y - 1] == 0:
            neighbours.append((self.x, self.y - 1))  # left neighbour
        if self.y < 19 and detectedMap.surface[self.x][self.y + 1] == 0:
            neighbours.append((self.x, self.y + 1))  # right neighbour

        return neighbours

    def moveDFS(self, detectedMap):
        """
        Get the neighbours.
        - If all of them are visited:
            - try to go to the square where you came from, because you still have unvisited positions. Basically
            backtrack from where you came until you reach an unvisited neighbour.
            - if self.__lastVisitedStack is empty, it means we are done
        - If at least one of the neighbours is unvisited:
            - add your current position to the stack
            - move to the new unvisited position
        :param detectedMap: the map that the drone detected until now
        :return: True if we are not done, false if we are.
        """
        # TO DO!
        # rewrite this function in such a way that you perform an automatic
        # mapping with DFS
        neighbours = self.getNeighbours(detectedMap)
        unvisited = [n for n in neighbours if self.__visited[n] == 0]  # horse
        if not unvisited:  # list is empty
            if not self.__lastVisitedStack:
                self.x, self.y = None, None
                return False
            self.x, self.y = self.__lastVisitedStack.pop()
        else:
            self.__lastVisitedStack.append((self.x, self.y))
            self.x, self.y = unvisited.pop()
            self.__visited[(self.x, self.y)] += 1

        return True


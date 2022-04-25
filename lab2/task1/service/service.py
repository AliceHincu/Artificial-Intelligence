import math
import random
from math import sqrt
from random import randint
from common.global_variables import *
import queue


class Service:
    def __init__(self, drone, droneMap):
        self._drone = drone
        self._map = droneMap

    @staticmethod
    def euclidean_distance(coord1, coord2):
        """
        WE USE IT AS THE COST FUNCTION FOR G AND H

        In mathematics, the Euclidean distance between two points is the length of
        a line segment between the two points.

        Basically you use the Pythagorean theorem: a^2 + b^2 = c^2 where:
        * a = (coord2.x - coord1.x)
        * b = (coord2.y - coord1.y)
        * c = the distance between coord1 and coord2

        :return: Euclidean distance
        """
        return sqrt((coord2[0] - coord1[0]) * (coord2[0] - coord1[0]) + (coord2[1] - coord1[1]) * (coord2[1] - coord1[1]))

    def evaluation_function_a_star(self, end, n, cost_dict):
        """
        f(n) = g(n) + h(n) where:
        * f(n) is the evaluation function
        * g(n) is the cost function from the initial state to the current state n
        * h(n) is the cost heuristic function from the current state to the final state

        :param end: end coordinates
        :param n: current coordinates
        :param cost_dict: for g function, the cost until now
        :return: f(n)
        """
        g = cost_dict[n]
        h = self.euclidean_distance(n, end)  # heuristic function = smart guess
        return g + h

    def evaluation_function_greedy(self, end, n):
        """
        only h(n) is considered:
        * h(n) is the cost heuristic function from the current state to the final state

        :param end: end coordinates
        :param n: current coordinate
        :return: f(n)
        """
        h = self.euclidean_distance(n, end)  # heuristic function = smart guess
        return h

    def bestFirstSearch(self, start, destination, f):
        """
        Get the shortest path
        :param start: start coordinates
        :param destination: coordinates
        :param f: function for priority queue
        :return: boolean(if it was foun or not) + the predecessors' dictionary.
        """
        found = False
        predecessor = {start: -1}  # save predecessors to recreate the path if it exists
        cost_dict = {start: 0}  # for g function

        visited = []
        toVisit = queue.PriorityQueue()  # FIFO sorted list (priority queue)
        toVisit.put((f(start, cost_dict), start))

        while not toVisit.empty() and not found:
            if toVisit.empty():  # ask this: why is it here if we have the while ????
                return False, []
            node = toVisit.get(block=False)[1]  # do not block until an item is available

            if node not in visited:
                visited.append(node)
            else:
                continue

            if node == destination:
                found = True
            else:
                neighbours = self.getNeighbours(node)
                for neighbour in neighbours:
                    if neighbour not in visited:
                        cost_dict[neighbour] = cost_dict[node] + 1  # update cost
                        toVisit.put((f(neighbour, cost_dict), neighbour))
                        predecessor[neighbour] = node

        return found, predecessor

    def AStarAlgorithm(self, destination):
        """
        There are generally three approximation heuristics to calculate h:
        - manhattan distance
            - When to use: When we are allowed to move only in four directions only (right, left, top, bottom)
        - diagonal distance
            - When to use: When we are allowed to move in eight directions only
        - euclidean distance
            - When to use: When we are allowed to move in any directions
        :param destination: coordinates
        :return:
        """
        start = self._drone.get_coordinates()
        path = self.bestFirstSearch(
            start, destination,
            lambda current, cost_dict: self.evaluation_function_a_star(destination, current, cost_dict)  # f function
        )

        if not path[0]:
            return []
        else:
            return self.computePath(path[1], destination)

    def GreedyAlgorithm(self, destination):
        start = self._drone.get_coordinates()
        path = self.bestFirstSearch(
            start, destination,
            lambda current, cost_dict: self.evaluation_function_greedy(destination, current)  # f function
        )

        if not path[0]:
            return []
        else:
            return self.computePath(path[1], destination)

    def SimulatedAnnealingAlgorithm(self, end, temperature):
        start = self._drone.get_coordinates()
        current_pos = start
        step_count = 0
        path = []
        while current_pos != end:
            path.append(current_pos)
            step_count += 1
            currentTemperature = temperature / step_count
            neighbours = self.getNeighbours(current_pos)
            neigh = neighbours[random.randint(0, len(neighbours) - 1)]
            if self.euclidean_distance(neigh, end) < self.euclidean_distance(current_pos, end):
                current_pos = neigh
            else:
                r = random.uniform(0, 1)
                # p = e^(delta(E)/T): Depends on difference (energy): delta(E), Is modelled by a temperature parameter T
                p = math.exp(-abs(self.euclidean_distance(neigh, end) - self.euclidean_distance(current_pos, end)) / currentTemperature)
                if r < p:
                    current_pos = neigh

        path.append(end)
        return path

    # =============== HELPER FUNCTIONS ===============
    @staticmethod
    def computePath(predecessors, end):
        """From the dict of predecessors, compute the shortest path from start to destination"""
        path = []
        while end != -1:
            path.append(end)
            end = predecessors[end]
        path.reverse()
        return path

    def getNeighbours(self, node):
        """Get neighbours of node that are valid"""
        neighbours = [(node[0] + dist_coord[0], node[1] + dist_coord[1]) for dist_coord in pos]  # get all 4 neighbours
        neighbours = [node for node in neighbours if self._map.is_position_valid(node[0], node[1])]  # check if neighbours are valid
        return neighbours

    def generate_coordinates(self):
        """Generate random and valid coordinates for start and destination"""
        x = randint(0, NR_LINES - 1)
        y = randint(0, NR_COLUMNS - 1)
        while not self._map.is_position_valid(x, y):
            x = randint(0, NR_LINES - 1)
            y = randint(0, NR_COLUMNS - 1)
        return x, y

    def getMap(self):
        return self._map

    def getDrone(self):
        return self._drone

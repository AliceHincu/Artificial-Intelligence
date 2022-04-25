import queue
from collections import deque
from copy import deepcopy
from math import sqrt
from random import randint

from a_star_algo import AStarAlgorithm
from ant import Ant
from domain.info_graph import InfoGraph
from map import Map
from utils import *


class Controller:
    def __init__(self):
        self.map = Map()
        self.drone_coordinates = INITIAL_POSITION
        self.n = self.map.n
        self.m = self.map.m
        self.info_graph = None

        self.solution = {
            "drone_path": {},  # key: tuple of src and dest coordinates, value: the drone path ... determined by A*
            "best_sensor_path": [],  # determined by ACO
            "sensor_number": {}  # key: tuple with coordinates, value: the sensor number
        }

        self.init_env()

    def check_initial_pos(self):
        while not self.map.check_if_pos_valid(self.drone_coordinates[0], self.drone_coordinates[1]):
            new_x = randint(0, self.n)
            new_y = randint(0, self.m)
            self.drone_coordinates = [new_x, new_y]

    def init_env(self):
        self.map.load_map("myMap.map")
        self.check_initial_pos()

    def get_map(self):
        return self.map

    # ---- STEP 1 ----
    def get_seen_squares_per_value(self, x, y):
        """
        Return an array representing how many new squares we can see at each step
        Example: [0, 3, 2, 1, 1, 1]
        - if the drone gives 0 energy to the sensor, the sensor sees 0 squares
        - 1 energy: the sensor sees 3 new squares
        - 2 energy: the sensor sees 2 new squares (so 3+2 = 5 in total)
        :param x:
        :param y:
        :return:
        """
        seen_squares_per_value = [0, 0, 0, 0, 0, 0]
        seen_squares_coords = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
        for direction in DIRECTION_DICT.values():  # UP, DOWN, RIGHT, LEFT
            aux_x, aux_y = x, y
            energy = 0
            while energy < MAX_SENSOR_CAPACITY:
                aux_x += direction[0]
                aux_y += direction[1]
                energy += 1
                if self.map.check_if_pos_valid(aux_x, aux_y):
                    seen_squares_per_value[energy] += 1
                    seen_squares_coords[energy].append((aux_x, aux_y))
                else:
                    break

        return seen_squares_per_value, seen_squares_coords

    def sensor_seen_squares(self):
        """
        Return an array representing how many squares we can see at each energy
        Example: if the seen_squares_per_value = [0, 3, 2, 1, 1, 1]
        - if the drone gives 0 energy it means we can see a total of 0 squares with the sensor
        - 1 energy: 0+3= 3 squares
        - 2 energy: 0+3+2= 5 squares
        and so on
        :return:
        """
        sensors = self.map.get_sensors()
        updated_sensors = []

        for sensor in sensors:
            x_sensor = sensor[0]
            y_sensor = sensor[1]
            s, seen_squares_coords = self.get_seen_squares_per_value(x_sensor, y_sensor)
            seen_squares = [sum(s[0:i + 1]) for i in range(len(s))]
            updated_sensors.append([x_sensor, y_sensor, seen_squares, seen_squares_coords])

        return updated_sensors

    # ---- STEP 2 ----
    def get_sensor_min_distance(self, sensors):
        """
        Get the minimum distance from sensor to sensor and from drone to sensor using A* algorithm
        :param sensors:
        :return:
        """
        min_distance = {}

        # get minimum distance from sensor to sensor
        for i in range(len(sensors) - 1):
            for j in range(i+1, len(sensors)):
                start = (sensors[i][0], sensors[i][1])
                dest = (sensors[j][0], sensors[j][1])
                path = AStarAlgorithm(start, dest, lambda x, y: self.map.check_if_pos_valid(x, y))
                self.solution["drone_path"][(start, dest)] = path
                self.solution["drone_path"][(dest, start)] = path[::-1]
                min_distance[(start, dest)] = len(path) - 1

        # get minimum distance from starting position to each sensor
        start = (self.drone_coordinates[0], self.drone_coordinates[1])
        for sensor in sensors:
            dest = (sensor[0], sensor[1])
            path = AStarAlgorithm(start, dest, lambda x, y: self.map.check_if_pos_valid(x, y))
            self.solution["drone_path"][(start, dest)] = path
            self.solution["drone_path"][(dest, start)] = path[::-1]
            min_distance[(start, dest)] = len(path) - 1

        return min_distance

    # ---- STEP 3+4 ----
    def epoch(self, noAnts, size, trace, alpha, beta, q0, rho):
        antSet = [Ant(size, deepcopy(self.info_graph)) for _ in range(noAnts)]
        for _ in range(size):
            # the maximum nr of iterations in an era is the length of the solution
            for ant in antSet:
                ant.addMove(q0, trace, alpha, beta)
        # for _ in range(size):
        #     antSet[0].addMove(q0, trace, alpha, beta)

        # update the trace with the pheromones left by all ants
        dTrace = [1.0 / antSet[i].fitness() for i in range(len(antSet))]
        for i in range(size):
            for j in range(size):
                trace[i][j] = (1 - rho) * trace[i][j]
        for i in range(len(antSet)):
            for j in range(len(antSet[i].path) - 1):
                x = antSet[i].path[j]
                y = antSet[i].path[j + 1]
                trace[x][y] = trace[x][y] + dTrace[i]
        # return best ant
        f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
        f = max(f)
        best_ant = antSet[f[1]]
        return [best_ant.path, best_ant.seen_squares, best_ant.spent_energy]

    def ACO(self):
        print("Program is running...")

        # Step 1: Determine for each sensor the number of squares that can be seen for each value from 0 to 5
        sensors = self.sensor_seen_squares()

        # Step 2: Determine the minimum distance between each pair of sensors
        min_distance = self.get_sensor_min_distance(sensors)

        # Step 3+4:
        # 3. Determine using ACO the shortest path between the sensors
        # 4. Determine using any method the quantity of energy that is left there (careful about
        # the energy spent and the remaining one after moving between points)
        self.info_graph = InfoGraph(sensors, min_distance, self.drone_coordinates)
        print(self.info_graph)
        size = len(sensors)+1

        solution = None
        bestSol = [[], 0, []]
        trace = [[1 for _ in range(size)] for _ in range(size)]

        print("Epochs: ", end=" ")
        for i in range(NUMBER_OF_EPOCHS):
            print(i, end=" ")
            solution = self.epoch(NUMBER_OF_ANTS, size, trace, ALPHA, BETA, Q0, RHO).copy()
            path = solution[0].copy()
            seen_squares = solution[1]
            spent_energy = solution[2]
            if seen_squares > bestSol[1]:
                bestSol = [path, seen_squares, spent_energy]

        self.solution["best_sensor_path"] = {"path": bestSol[0], "seen_squares": bestSol[1], "spent_energy": bestSol[2]}
        self.solution["sensor_coordinates"] = self.info_graph.sensor_coordinates
        print("", end="\n")
        print("Number of surveilled squares: ", bestSol[1])
        return self.solution

import pickle
from random import *
import numpy as np
from utils import *


class Map:
    def __init__(self, n=N, m=M):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def random_map(self, fill=0.2):
        # clear old map
        self.surface = np.zeros((self.n, self.m))

        # Generate walls
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

        # Generate sensors
        for _ in range(NUMBER_OF_SENSORS):
            sensor_x = randint(0, self.n - 1)
            sensor_y = randint(0, self.m - 1)
            while self.surface[sensor_x][sensor_y] == 1:  # generate until valid position
                sensor_x = randint(0, self.n - 1)
                sensor_y = randint(0, self.m - 1)
            self.surface[sensor_x][sensor_y] = 2

    def get_sensors(self):
        sensors = []

        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 2:
                    # in sensors we will save the coordinates and a list with the number of squares that can be seen for
                    # each value from 0 to 5...initially the number of squares will be 0 for each value
                    sensors.append([i, j, [0, 0, 0, 0, 0, 0]])

        return sensors

    def save_map(self, file_name="myMap.map"):
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def load_map(self, file_name):
        with open(file_name, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def check_if_pos_valid(self, x, y):
        """
        Check if the coordinates are in the map / in a wall
        """
        if x < 0 or y < 0 or x >= self.n or y >= self.m or self.surface[x][y] == 1:
            return False
        return True

    def check_if_sensor(self, x, y):
        """
        Check if the coordinates are of a sensor
        """
        return self.surface[x][y] == 2

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

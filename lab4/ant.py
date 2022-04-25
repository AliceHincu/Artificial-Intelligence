import math
from random import randint, random, choice
from utils import *


class Ant:
    def __init__(self, size, info_graph):
        self.size = size
        self.info_graph = info_graph

        self.battery_left = BATTERY_CAPACITY
        self.path = [0]
        self.spent_energy = {}
        self.seen_squares = 0

    def calculate_energy_spent(self):
        dest = self.path[-1]

        possible_squares = self.info_graph.seen_squares[dest]
        index_max_squares_surveilled = max([[possible_squares[i], i] for i in range(len(possible_squares))])[1]
        energy = min(index_max_squares_surveilled, self.battery_left)
        seen_squares = possible_squares[energy]

        return energy, seen_squares

    def remove_seen_squares(self, energy):
        """
        Dumb function but it works.
        :param energy:
        :return:
        """
        dest = self.path[-1]
        dest_coords = self.info_graph.sensor_coordinates[dest]

        seen_squares = []

        for sensor in self.info_graph.unseen_squares_coords:
            if sensor[0] == dest_coords[0] and sensor[1] == dest_coords[1]:
                for i in range(1, energy+1):
                    unseen_squares = sensor[3][i]
                    seen_squares += unseen_squares

        for sensor in self.info_graph.unseen_squares_coords:
            for e_val in sensor[3].keys():
                l = len(sensor[3][e_val])
                new = []
                for i in range(l):
                    if sensor[3][e_val][i] not in seen_squares:
                        new.append(sensor[3][e_val][i])
                sensor[3][e_val] = new

        # update how many squares you can see now
        for sensor in self.info_graph.unseen_squares_coords:
            a = [len(sensor[3][key]) for key in sensor[3].keys()]
            sensor[2] = [sum(a[0:i + 1]) for i in range(len(a))]
            sensor_nr = self.info_graph.sensor_number[(sensor[0], sensor[1])]
            self.info_graph.seen_squares[sensor_nr] = sensor[2]

    def distMove(self, current_sensor, next_sensor):
        """
        Return the empiric distance given by the distance between current_sensor and next_sensor
        :param next_sensor: a possible new sensor to visit
        :return: the empiric distance
        """
        return self.info_graph.cost[(current_sensor, next_sensor)]

    def nextMoves(self, src):
        """
        Return a list of possible correct movements from the given position
        :param src:
        :return:
        """
        new = []

        # start looking for the valid positions of the next move
        possible_destinations = self.info_graph.next_dest[src]
        for dest in possible_destinations:
            if dest not in self.path:
                new.append(dest)

        return new.copy()

    def addMove(self, q0, trace, alpha, beta):
        """
        Add a new position to the ant's solution if it's possible
        :param q0:
        :param trace:
        :param alpha:
        :param beta:
        :return:
        """
        # positions that are not valid are marked with 0
        p = [math.inf for _ in range(self.size)]

        # determine the next valid sensors in the variable nextSteps
        current_sensor = self.path[-1]
        nextSteps = self.nextMoves(current_sensor).copy()

        # if we don't have valid positions then we get out
        if len(nextSteps) == 0 or self.battery_left <= 0:
            return False

        # we put on the valid positions the value of the empiric distance
        for next_sensor in nextSteps:
            p[next_sensor] = self.distMove(current_sensor, next_sensor)

        # calculate the product between visibility^beta and trace^alpha
        # we put here "minus" so we can leave the max(p, key=..), since we need the minimum distance
        p = [(p[i] ** -beta) * (trace[current_sensor][i] ** alpha) for i in range(len(p))]

        if random() < q0:
            # add best possible move
            p = [[i, p[i]] for i in range(len(p))]
            p = max(p, key=lambda a: a[1])
            self.path.append(p[0])
        else:
            # add by probability
            s = sum(p)
            if s == 0:
                return choice(nextSteps)
            p = [p[i] / s for i in range(len(p))]
            p = [sum(p[0:i + 1]) for i in range(len(p))]
            r = random()
            i = 0
            while r > p[i]:
                i = i + 1
            self.path.append(i)

        energy, seen_squares = self.calculate_energy_spent()
        self.spent_energy[self.info_graph.sensor_coordinates[self.path[-1]]] = energy
        self.seen_squares += seen_squares
        self.battery_left -= energy
        self.remove_seen_squares(energy)
        return True

    def fitness(self):
        """
        The more seen squares the better. We need to get the maxim total area surveilled surrounding the sensors
        :return:
        """
        if self.seen_squares == 0:
            print("Here")
        return self.seen_squares
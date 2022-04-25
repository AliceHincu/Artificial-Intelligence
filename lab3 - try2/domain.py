# -*- coding: utf-8 -*-
import copy
import pickle
from math import sqrt
from random import *
from utils import *
import numpy as np


class Gene:
    def __init__(self):
        self.val = randint(0, 3)  # the 4 directions

    def __int__(self):
        return self.val

    def __str__(self):
        return str(self.val)


class Individual:
    """
    An individual = Possible solution (where the drone can move)
    """
    def __init__(self, size=0):
        self.__size = size  # how many genes
        self.__genes = [Gene() for _ in range(self.__size)]
        self.fitness_lvl = -1  # Quality => how good is the solution

    def fitness_lvl_check(self, x, y, seen, map):
        """
        We call this function for every step
        Check how many new squares the drone can see
        If the position is not valid, we return false so we can stop in the fitness function
        """
        if not map.check_if_pos_valid(x, y):
            return False

        for direction in DIRECTION_DICT.values():
            aux_x, aux_y = x, y
            while map.check_if_pos_valid(aux_x, aux_y):
                if (aux_x, aux_y) not in seen:
                    self.fitness_lvl += 0.1
                    seen.add((aux_x, aux_y))
                aux_x += direction[0]
                aux_y += direction[1]

        return True

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

    def fitness(self, drone_coordinates, map_):
        """
        FITNESS FUNCTION used: we count the number of seen squares from the map at every step until we either:
        - hit a wall
        - go outside the map
        - we remain without genes
        """
        # TODO complete
        # compute the fitness for the individual
        # and save it in self.fitness_lvl
        self.fitness_lvl = 0
        seen = set()
        x, y = drone_coordinates

        # check initial coords
        if not self.fitness_lvl_check(x, y, seen, map_):
            return

        for gene in self.__genes:
            # the gene indicates which way we move: up/down/left/right, and for each gene we build the drone path
            x += DIRECTION_DICT[int(gene)][0]
            y += DIRECTION_DICT[int(gene)][1]
            if not self.fitness_lvl_check(x, y, seen, map_):
                return

        distance = self.euclidean_distance((x, y), drone_coordinates) + 1  # in case of 0
        self.fitness_lvl += self.__size/distance  # for bonus points

    def mutate(self, mutateProbability=0.04):
        """
        Type: Random resetting
        The value of a gene is changed (by probability pm) into another value (from the definition domain)
        Basically: choose randomly a gene and reset it.
        """
        # TODO complete
        if random() < mutateProbability:
            self.__genes[randint(0, self.__size - 1)] = Gene()

    def crossover(self, otherParent, crossoverProbability=0.8):
        """
        Uniform crossover
        Each gene of an offspring comes from a randomly and uniform selected parent:
            - For each gene a uniform random number r is generated
            - If r < probability p (usually, p=0.5), c1 will inherit that gene from p1 and c2 from p2,
            - otherwise, c1 will inherit p2 and c2 will inherit p1
        """
        # TODO complete
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        for index in range(self.__size):
            gene1 = self.__genes[index]
            gene2 = otherParent.__genes[index]

            if random() >= crossoverProbability:
                gene1, gene2 = gene2, gene1

            offspring1.__genes[index] = gene1
            offspring2.__genes[index] = gene2

        return offspring1, offspring2

    def get_path(self):
        return self.__genes


class Population:
    """
    Set of possible solutions...
    P.S: here we save future offsprings
    """
    def __init__(self, populationSize=0, individualSize=0):
        self.__individuals = [Individual(individualSize) for _ in range(populationSize)]

    def __len__(self):
        return len(self.__individuals)

    def evaluate(self, drone, map_):
        # evaluates the population
        for individual in self.__individuals:
            individual.fitness(drone, map_)  # set the fitness level for each individual

    def get_avg(self):
        individuals_fitness = [individual.fitness_lvl for individual in self.__individuals]
        return np.average(individuals_fitness)

    def selection(self, k=0):
        """
        Rank-based selection:
            - Sort the entire population based on fitness
            - Each individual receives a rank
            - Best individual has rank niu
            - Worst individual has rank 1 (reversed in code)
        :param k:
        :return: best k individuals
        """
        # perform a selection of k individuals from the population
        # and returns that selection
        # TODO complete
        pop_copy = copy.deepcopy(self.__individuals)
        pop_copy.sort(key=lambda x: x.fitness_lvl, reverse=True)  # from the best to the worst
        return pop_copy[:k]

    def add_individual(self, individual):
        self.__individuals.append(individual)

    def get_best_path(self, drone):
        """
        We get the genes of the best individual, where genes <=> best path for drone
        :param drone:
        :return:
        """
        x, y = drone[0], drone[1]
        path = [(x, y)]
        path_as_genes = self.selection(1)[0].get_path()  # get the genes of the best individuals

        for gene in path_as_genes:
            i, j = DIRECTION_DICT[gene.val]
            x += i
            y += j
            path.append((x, y))
        return path


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def random_map(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

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

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    
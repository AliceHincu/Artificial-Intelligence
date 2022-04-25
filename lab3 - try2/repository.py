# -*- coding: utf-8 -*-
import json
from domain import *


class Repository:
    def __init__(self, drone_pos=[10, 10], steps=20, no_of_iterations=100, pop_size=100,
                 mutation_prob=0.05, crossover_prob=0.8, no_of_seeds=5):
        self.__populations = []
        self.cmap = Map()

        self.ea_params = {
            "drone_pos": drone_pos,  # drone position
            "steps": steps,  # battery of drone
            "no_of_iterations": no_of_iterations,
            "pop_size": pop_size,  # how many individuals in the population
            "mutation_prob": mutation_prob,
            "crossover_prob": crossover_prob,
            "no_of_seeds": no_of_seeds
        }

        self.current_iteration = 0

    def check_initial_pos(self):
        while not self.cmap.check_if_pos_valid(self.ea_params["drone_pos"][0], self.ea_params["drone_pos"][1]):
            new_x = randint(0, self.cmap.n)
            new_y = randint(0, self.cmap.m)
            self.ea_params["drone_pos"] = [new_x, new_y]

    def createPopulation(self, *args):
        # args = [populationSize, individualSize] -- you can add more args
        # TODO complete
        pop_size, individual_size = args
        return Population(pop_size, individual_size)

    def add_population(self, population):
        self.__populations.append(population)

    def get_latest_population(self):
        return self.__populations[-1]

    def get_pop_amount(self):
        return len(self.__populations)

    def get_repo_params(self):
        return self.ea_params

    # -- SETTERS --
    def set_steps(self, new_value):
        self.ea_params["steps"] = new_value

    def set_max_iterations(self, new_value):
        self.ea_params["no_of_iterations"] = new_value

    def set_population_size(self, new_value):
        self.ea_params["pop_size"] = new_value

    def set_no_of_seeds(self, new_value):
        self.ea_params["no_of_seeds"] = new_value

# -*- coding: utf-8 -*-
from random import randint

import map


class Repository:
    def __init__(self, drone_pos=[10, 10], steps=20, no_of_iterations=100, pop_size=100,
                 mutation_prob=0.05, crossover_prob=0.8, no_of_seeds=5):
        self.cmap = map.Map()

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
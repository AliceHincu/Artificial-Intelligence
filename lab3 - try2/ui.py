# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *
from domain import *
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class UI:
    def __init__(self, repo, controller):
        self.repo = repo
        self.controller = controller
        self.commands = {
            "0": self.quit,
            "1": self.create_random_map,
            "2": self.load_map,
            "3": self.save_map,
            "4": self.view_map,
            "5": self.parameter_setup,
            "6": self.run_solver,
            "7": self.visualise_statistics,
            "8": self.view_drone,
        }
        self.best_path = []
        self.stats = None
        self.std_dev = 0
        self.avg = 0

    @staticmethod
    def print_menu():
        print("0. Exit")
        print("--- Map options")
        print("1. Create a random map")
        print("2. Load a map")
        print("3. Save map")
        print("4. Visualise map")
        print("--- EA Options")
        print("5. Parameters setup")
        print("6. Run solver")
        print("7. Visualise statistics")
        print("8. View the drone moving on a path")

    @staticmethod
    def print_parameter_menu():
        print("0. Exit")
        print("1. Battery capacity")  # steps / nr of genes
        print("2. Max iterations")  # no_of_iterations
        print("3. Population size")  # pop_size=100
        print("4. Nr of seeds")  # no_of_seeds=30

    def create_random_map(self):
        self.controller.get_map().random_map()

    def load_map(self):
        file = input("file: ")
        self.controller.get_map().load_map(file)

    def save_map(self):
        file = input("file: ")
        self.controller.get_map().save_map(file)

    def view_map(self):
        print(self.repo.cmap)
        movingDrone(self.repo.cmap, [[-1, -1]])

    def parameter_setup(self):
        while True:
            self.print_parameter_menu()
            command = int(input(">>>"))
            if command == 0:
                break
            elif command == 1:
                value = int(input("How many steps: "))
                self.repo.set_steps(value)
            elif command == 2:
                value = int(input("How many max_iterations: "))
                self.repo.set_max_iterations(value)
            elif command == 3:
                value = int(input("New population size: "))
                self.repo.set_population_size(value)
            elif command == 4:
                value = int(input("New nr of seeds: "))
                self.repo.set_no_of_seeds(value)
        print("Repo params: ", self.repo.get_repo_params())

    def run_solver(self):
        self.controller.init_env()
        self.best_path, self.stats, self.std_dev, self.avg = self.controller.solver()

    def visualise_statistics(self):
        print(pd.DataFrame(self.stats))
        print("std dev: ", self.std_dev)
        print("avg: ", self.avg)

        stats = np.array(self.stats)

        plt.plot(stats[:, 0], stats[:, 1], "-b", label="avg fitness")
        plt.legend(loc="upper left")
        plt.show()
        plt.close()

    def view_drone(self):
        movingDrone(self.repo.cmap, self.best_path)

    def quit(self):
        exit(0)

    def show(self):
        while True:
            self.print_menu()
            command = input(">")
            if command in self.commands:
                self.commands[command]()


if __name__ == "__main__":
    repo_ = Repository()
    controller_ = Controller(repo_)
    ui = UI(repo_, controller_)
    ui.show()


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, mark seen)
#              ATTENTION! the function doesn't check if the path passes through walls

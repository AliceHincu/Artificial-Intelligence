# -*- coding: utf-8 -*-


# imports
from gui import *
from controller import *
from repository import *


class UI:
    def __init__(self, controller):
        self.controller = controller
        self.commands = {
            "0": self.quit,
            "1": self.create_random_map,
            "2": self.load_map,
            "3": self.save_map,
            "4": self.view_map,
            "5": self.run,
            "6": self.view_drone,
        }
        self.best_path = []
        self.spent_energy = []

    @staticmethod
    def print_menu():
        print("0. Exit")
        print("--- Map options")
        print("1. Create a random map")
        print("2. Load a map")
        print("3. Save map")
        print("4. Visualise map")
        print("--- AOC Options")
        print("5. Run setup")
        print("6. View the drone moving on a path")

    def create_random_map(self):
        self.controller.get_map().random_map()

    def load_map(self):
        file = input("file: ")
        self.controller.get_map().load_map(file)
        self.controller.check_initial_pos()

    def save_map(self):
        file = input("file: ")
        self.controller.get_map().save_map(file)

    def view_map(self):
        print(self.controller.get_map())
        movingDrone(self.controller.get_map(), [[-1, -1]], {})

    def run(self):
        solution = self.controller.ACO()

        # create the full path
        full_path = [tuple(self.controller.drone_coordinates)]
        sensor_path = solution["best_sensor_path"]["path"]
        number_to_coords = solution["sensor_coordinates"]
        for i in range(len(sensor_path)-1):
            src = number_to_coords[sensor_path[i]]
            dest = number_to_coords[sensor_path[i+1]]
            path = solution["drone_path"][(src, dest)]
            full_path += path[1:]

        self.best_path = full_path
        self.spent_energy = solution["best_sensor_path"]["spent_energy"]

    def view_drone(self):
        movingDrone(self.controller.get_map(), self.best_path, self.spent_energy)

    def quit(self):
        exit(0)

    def show(self):
        while True:
            self.print_menu()
            command = input(">")
            if command in self.commands:
                self.commands[command]()


if __name__ == "__main__":
    controller_ = Controller()
    ui = UI(controller_)
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

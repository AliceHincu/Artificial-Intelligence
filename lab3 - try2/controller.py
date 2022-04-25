import time

import numpy as np

from repository import *


class Controller:
    def __init__(self, repo):
        self.repo = repo
        self.statistics = []
        self.standard_deviation = -1

    def get_map(self):
        return self.repo.cmap

    def init_env(self):
        self.repo.check_initial_pos()

    def create_offsprings(self, first_parent, second_parent):
        first_offspring, second_offspring = first_parent.crossover(second_parent, self.repo.ea_params["crossover_prob"])
        first_offspring.mutate(self.repo.ea_params["mutation_prob"])
        second_offspring.mutate(self.repo.ea_params["mutation_prob"])
        return first_offspring, second_offspring

    def iteration(self):
        """
        Generational EA:
            - Each generation creates μ offspring
            - Each individual survives a generation only
            - Set of parents is totally replaced by set of offspring
        """
        # TODO complete

        # selection of the parents
        population = self.repo.get_latest_population()
        population.evaluate(self.repo.ea_params["drone_pos"], self.repo.cmap)  # call fitness func
        selection = population.selection(len(population) // 2)  # take superior half of parents and make children

        # create offsprings by crossover of the parents + apply some mutations
        offsprings = Population()
        is_couple = set()
        while len(offsprings) < len(population):
            # take 2 parents from superior half
            first_parent = selection[randint(0, len(selection) - 1)]
            second_parent = selection[randint(0, len(selection) - 1)]
            if (first_parent, second_parent) not in is_couple and not first_parent == second_parent:
                is_couple.add((first_parent, second_parent))
                offspring1, offspring2 = self.create_offsprings(first_parent, second_parent)
                offsprings.add_individual(offspring1)
                offsprings.add_individual(offspring2)

        # selection of the survivors
        self.repo.add_population(offsprings)
        
    def run(self, *args):
        """
        Return best individual
        :param args:
        :return:
        """
        seed_index, seed_ = args
        # TODO complete
        # args - list of parameters needed in order to run the algorithm
        # until stop condition
        #    perform an iteration
        #    save the information need it for the statistics

        for i in range(0, self.repo.ea_params["no_of_iterations"]):
            if seed_index == self.repo.ea_params["no_of_seeds"] - 1:  # if you are at the last run -> statistics
                population = self.repo.get_latest_population()
                population.evaluate(self.repo.ea_params["drone_pos"], self.repo.cmap)  # find fitness
                avg_fitness = population.get_avg()
                self.statistics.append([i, avg_fitness])
            self.iteration()

        population = self.repo.get_latest_population()
        population.evaluate(self.repo.ea_params["drone_pos"], self.repo.cmap)  # find fitness
        return population.selection(1)[0]

    def solver(self, *args):
        # TODO complete
        # args - list of parameters needed in order to run the solver
        # create the population,
        # run the algorithm
        # return the results and the statistics

        start_time = time.time()

        best_fitnesses = []
        for i in range(self.repo.ea_params["no_of_seeds"]):
            seed_ = randint(0, 100)
            seed(seed_)
            population = self.repo.createPopulation(self.repo.ea_params["pop_size"], self.repo.ea_params["steps"])
            self.repo.add_population(population)
            best_individual = self.run(i, seed_)
            best_fitnesses.append(best_individual.fitness_lvl)
            print(f">Seed nr {i} finished")

        print(f"--- {time.time() - start_time} seconds ---")
        return self.repo.get_latest_population().get_best_path(self.repo.ea_params["drone_pos"]), self.statistics, \
               np.std(best_fitnesses), np.average(best_fitnesses)

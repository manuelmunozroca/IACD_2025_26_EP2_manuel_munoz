import numpy as np
import random
from Generation import Individual, Generation
from Cities import Data

def genetic_algorithm(data: Data, population_size = 100, generations = 500, mutation_rate = 0.05, parents_num=10) -> Individual:
    actual_generation = Generation.generate_random_generation(data, population_size)
    for individual in actual_generation.population:
        individual.evaluate(data)
    for generation in range(generations - 1):
        if generation % 5 == 0:
            print("Generation " + str(generation))
        new_generation = list()
        parents = actual_generation.select_best_parents(parents_num)
        new_generation.extend(parents)
        while len(new_generation) < population_size:
            mother, father = random.choice(parents), random.choice(parents)
            son = mother.reproduce(father)
            son.mutate(mutation_rate)
            new_generation.append(son)
        actual_generation = Generation(new_generation)
        for individual in actual_generation.population:
            individual.evaluate(data)
        if actual_generation.get_best_individual().path == data.solution:
            return actual_generation.get_best_individual()
    return actual_generation.get_best_individual()



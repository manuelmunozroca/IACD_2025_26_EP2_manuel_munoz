import numpy as np
import random
from Generation import Individual, Generation
from Cities import Data

def genetic_algorithm(data: Data, population_size = 100, generations = 500, mutation_rate = 0.05, parents_num=10) -> Individual:
    actual_generation = Generation.generate_random_generation(data, population_size)
    for generation in range(generations - 1):
        for individual in actual_generation:
            individual.evaluate(data)
        new_generation = list()
        parents = actual_generation.select_best_parents(parents_num)
        new_generation.extend(parents)
        while len(new_generation) < population_size:
            mother, father = random.choice(parents), random.choice(parents)
            son = mother.reproduce(father)
            new_generation.append(son.mutate(mutation_rate))
        actual_generation = Generation(new_generation)
    return actual_generation.get_best_individual()



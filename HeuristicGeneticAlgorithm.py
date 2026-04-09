import random
from Generation import Individual, Generation
from Cities import Data
from typing import List


def heuristic_genetic_algorithm(data: Data, population_size=100, max_generations=3000, mutation_rate=0.05):
    actual_generation = Generation.generate_random_generation(data, population_size)
    history = []
    generation = 0

    for individual in actual_generation.population:
        individual.evaluate(data)

    while actual_generation.get_best_individual().distance > 35000 and generation < max_generations:
        if generation % 100 == 0:
            print("Generation " + str(generation))

        new_generation = list()

        parents = actual_generation.select_best_parents(int(population_size * 0.25))

        best = actual_generation.get_best_individual()
        new_generation.append(best)

        while len(new_generation) < population_size:
            mother, father = random.choice(parents), random.choice(parents)

            son = mother.reproduce_heuristic(father, data)
            son.mutate_inversion(mutation_rate)

            new_generation.append(son)

        actual_generation = Generation(new_generation)

        for individual in actual_generation.population:
            individual.evaluate(data)

        best_in_generation = actual_generation.get_best_individual()
        history.append(best_in_generation.distance)

        if is_same_route(data.solution, best_in_generation.path):
            break

        generation += 1

    return actual_generation.get_best_individual(), history, generation


def is_same_route(path1: List[int], path2: List[int]) -> bool:
    p1 = path1[:-1]
    p2 = path2[:-1]

    if len(p1) != len(p2):
        return False

    try:
        start_idx = p2.index(p1[0])
    except ValueError:
        return False
    size = len(p1)
    is_forward = all(p1[i] == p2[(start_idx + i) % size] for i in range(size))
    is_reverse = all(p1[i] == p2[(start_idx - i) % size] for i in range(size))
    return is_forward or is_reverse
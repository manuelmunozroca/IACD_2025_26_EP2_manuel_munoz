import random
from Generation import Individual, Generation
from Cities import Data


def heuristic_genetic_algorithm(data: Data, population_size=100, max_generations=1500, mutation_rate=0.05):
    actual_generation = Generation.generate_random_generation(data, population_size)
    history = []
    generation = 0

    for individual in actual_generation.population:
        individual.evaluate(data)

    while actual_generation.get_best_individual().distance >= 35000 and generation < max_generations:
        if generation % 100 == 0:
            print(f"Generation {generation} {actual_generation.get_best_individual().distance}")

        new_generation = list()

        parents = actual_generation.select_best_parents(int(population_size * 0.75))

        bests = []
        ordered_population = sorted(actual_generation.population, key=lambda x: x.distance)

        for ind in ordered_population:
            if not any(abs(ind.distance - other.distance) < 0.1 for other in bests):
                bests.append(ind)
            if len(bests) == 5:
                break

        new_generation.extend(bests)

        while len(new_generation) < population_size:
            limite_hijos = int(population_size * 0.8)
            while len(new_generation) < limite_hijos:
                mother, father = random.choice(parents), random.choice(parents)
                son = mother.reproduce_heuristic(father, data)
                son.mutate_inversion(mutation_rate, actual_generation.get_best_individual().distance)
                new_generation.append(son)

            ciudades_base = list(data.cities.keys())
            while len(new_generation) < population_size:
                ruta_aleatoria = ciudades_base.copy()
                random.shuffle(ruta_aleatoria)
                ruta_aleatoria.append(ruta_aleatoria[0])
                inmigrante = Individual(ruta_aleatoria)
                new_generation.append(inmigrante)

        actual_generation = Generation(new_generation)

        for individual in actual_generation.population:
            individual.evaluate(data)

        best_in_generation = actual_generation.get_best_individual()
        history.append(best_in_generation.distance)

        generation += 1

    return actual_generation.get_best_individual(), history, generation

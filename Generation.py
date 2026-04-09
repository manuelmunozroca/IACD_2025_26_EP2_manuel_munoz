from Cities import City, Data
import numpy as np
from typing import List

class Individual:
    def __init__(self, path: List[int]):
        self.path = path
        self.distance = 0.0

    def evaluate(self, data: 'Data') -> float:
        if self.distance == 0.0:
            distance = 0.0
            size = len(self.path)
            for i in range(size - 1):
                from_city = data.cities[self.path[i]]
                to_city = data.cities[self.path[i+1]]
                distance += from_city.distance_to(to_city)
            self.distance = distance
        return self.distance

    def mutate(self, mutation_rate: float) -> None:
        size = len(self.path)
        for i in range(size - 1):
            if np.random.rand() < mutation_rate:
                mutation = np.random.randint(1, size - 1)
                self.path[i], self.path[mutation] = self.path[mutation], self.path[i]
        if self.path[0] != self.path[-1]:
            self.path[-1] = self.path[0]

    def reproduce(self, father: 'Individual') -> 'Individual':
        size = len(self.path)
        mother_path, father_path = self.path.copy(), father.path.copy()
        start = np.random.randint(1, size - 2)
        end = np.random.randint(start + 1, size - 1)
        child_path = [-1] * size
        child_path[start:end] = mother_path[start:end]
        child_index, father_index = 0, 0
        while child_index != size - 1:
            if child_path[child_index] == -1:
                while father_path[father_index] in child_path:
                    father_index += 1
                child_path[child_index] = father_path[father_index]
            child_index += 1
        child_path[-1] = child_path[0]
        return Individual(child_path)

class Generation:
    def __init__(self, individuals: List[Individual]):
        self.population = individuals
        self.size = len(individuals)

    def get_best_individual(self):
        return min(self.population, key = lambda individual: individual.distance)

    def select_best_parents(self, parent_size: int) -> List[Individual]:
        sorted_population = sorted(self.population, key = lambda individual: individual.distance)
        return sorted_population[:parent_size]

    @classmethod
    def generate_random_generation(cls, data: 'Data', size: int) -> 'Generation':
        population = list()
        num_cities = len(data.cities.keys())
        for individual in range(size):
            path = list()
            while len(path) < num_cities:
                city = np.random.randint(1, num_cities + 1)
                if city not in path:
                    path.append(city)
            path.append(path[0])
            population.append(Individual(path))
        return Generation(population)



import Cities
import numpy as np
from typing import List

class Individual:
    def __init__(self, path = List[int]):
        self.path = path
        self.distance = 0.0

    def evaluate(self, data: 'Data') -> float:
        if self.distance == 0.0:
            distance = 0.0
            size = len(self.path)
            for i in range(size):
                from_city = data.cities[self.path[i]]
                to_city = data.cities[self.path[i+1]]
                distance += from_city.distance(to_city)
            self.distance = distance
            return self.distance

    def mutate(self, mutation_rate: float) -> None:
        size = len(self.path)
        for i in range(size):
            if np.random.rand() < mutation_rate:
                mutation = np.random.randint(size)
                self.path[i], self.path[mutation] = self.path[mutation], self.path[i]

class Generation:
    def __init__(self, individuals: List[Individual]):
        self.population = individuals

    def get_best_distance(self):
        return max(self.individuals, key = lambda individual: individual.distance)

    def select_best_parents(self, parent_size: int) -> List[Individual]:
        sorted_population = sorted(self.population, key = lambda individual: individual.distance)
        return sorted_population[:parent_size]

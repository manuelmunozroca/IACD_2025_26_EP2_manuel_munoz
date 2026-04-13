from Cities import City, Data
import numpy as np
from typing import List
import random

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

    def mutate_inversion(self, mutation_rate: float, current_best_distance) -> None:
        import random
        if random.random() < mutation_rate:
            route_length = len(self.path)
            num_inversions = 1 if current_best_distance < 35500 else 3
            for _ in range(num_inversions):
                start = random.randint(1, route_length - 4)
                end = random.randint(start + 2, route_length - 2)
                self.path[start:end] = self.path[start:end][::-1]

    def reproduce_heuristic(self, father: 'Individual', data: 'Data') -> 'Individual':
        import random
        route_length = len(self.path)
        starting_city = self.path[0]
        child_route = [starting_city]

        unvisited_cities = set(self.path[:-1])
        unvisited_cities.remove(starting_city)

        current_reference_city = starting_city

        while unvisited_cities:
            mother_city_index = self.path.index(current_reference_city)
            mother_next_city = self.path[(mother_city_index + 1) % (route_length - 1)]

            father_city_index = father.path.index(current_reference_city)
            father_next_city = father.path[(father_city_index + 1) % (route_length - 1)]

            current_city_node = data.cities[current_reference_city]
            mother_path_distance = current_city_node.distance_to(data.cities[mother_next_city])
            father_path_distance = current_city_node.distance_to(data.cities[father_next_city])

            selected_next_city = None

            if mother_next_city in unvisited_cities and father_next_city in unvisited_cities:
                if mother_path_distance < father_path_distance:
                    selected_next_city = mother_next_city
                else:
                    selected_next_city = father_next_city
            elif mother_next_city in unvisited_cities:
                selected_next_city = mother_next_city
            elif father_next_city in unvisited_cities:
                selected_next_city = father_next_city
            else:
                selected_next_city = random.choice(list(unvisited_cities))

            child_route.append(selected_next_city)
            unvisited_cities.remove(selected_next_city)
            current_reference_city = selected_next_city

        child_route.append(child_route[0])
        return Individual(child_route)

class Generation:
    def __init__(self, individuals: List[Individual]):
        self.population = individuals
        self.size = len(individuals)

    def get_best_individual(self):
        return min(self.population, key = lambda individual: individual.distance)

    def select_best_parents(self, parent_size: int) -> List[Individual]:
        return [self.tournament(5) for _ in range(parent_size)]

    def tournament(self, size = 5):
        fighters = random.sample(self.population, size)
        winner = min(fighters, key = lambda fighter: fighter.distance)
        return winner

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



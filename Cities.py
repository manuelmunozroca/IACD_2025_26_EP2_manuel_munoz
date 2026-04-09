import math
from typing import Dict, List

class City:
    def __init__(self, x: int, y: int):
        self._coordinates = (x,y)

    def distance_to(self, other: 'City'):
        x, y = self._coordinates
        return math.hypot(x -other._coordinates[0], y -other._coordinates[1])

class Data:
    def __init__(self, cities: Dict[int, City], solution: List[int]):
        self.cities = cities
        self.solution = solution

    def get_solution_distance(self):
        distance = 0.0
        size = len(self.solution)
        for i in range(size - 1):
            from_city = self.cities[self.solution[i]]
            to_city = self.cities[self.solution[i + 1]]
            distance += from_city.distance_to(to_city)
        return distance

class DataLoader:
    @staticmethod
    def parse_cities(filepath: str) -> Dict[int, City]:
        cities = dict()
        with open(filepath) as file:
            next(file)
            for line in file:
                city_id, x, y = line.strip().split()
                cities[int(city_id)] = City(int(x), int(y))
        return cities

    @staticmethod
    def parse_solution(filepath: str) -> List[int]:
        solution = list()
        with open(filepath) as file:
            for line in file:
                solution.append(int(line.strip()))
        return solution

    @classmethod
    def load_data(cls, cities_path: str, solution_path: str) -> Data:
        cities = cls.parse_cities(cities_path)
        solution = cls.parse_solution(solution_path)
        return Data(cities, solution)

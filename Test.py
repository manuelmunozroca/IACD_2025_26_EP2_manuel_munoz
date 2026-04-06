from GeneticAlgorithm import genetic_algorithm
from Cities import *

if __name__ == "__main__":
    print("Empezando experimento con 500 generaciones de 100 individuos")
    data = DataLoader.load_data("coordinates.txt", "solution.txt")
    best = genetic_algorithm(data, 500, 1000, 0.05, 10)
    print(f'Best path found: {best.path}')
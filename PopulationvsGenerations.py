import itertools
import numpy as np
import matplotlib.pyplot as plt
from GeneticAlgorithmNonStop import genetic_algorithm
from Cities import DataLoader

if __name__ == "__main__":
    data = DataLoader.load_data("coordinates.txt", "solution.txt")

    population_sizes = [100, 250, 500, 1000]
    mutation_rates = [0.01, 0.03, 0.05, 0.1, 0.15]

    tests = list(itertools.product(population_sizes, mutation_rates))
    results = {pop: [] for pop in population_sizes}

    for pop, mut in tests:
        print(f"Ejecutando Test -> Población: {pop} | Mutación: {mut}")
        best, history, gen = genetic_algorithm(data, population_size=pop, mutation_rate=mut)
        results[pop].append(gen)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=100)

    x = np.arange(len(population_sizes))
    width = 0.15
    offsets = [-2 * width, -width, 0, width, 2 * width]
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for i, mut in enumerate(mutation_rates):
        generations_list = [results[pop][i] for pop in population_sizes]
        ax.bar(x + offsets[i], generations_list, width, label=f'Mutación: {mut}', color=colores[i], edgecolor='black')

    ax.set_title('Algoritmo genético: generaciones vs tamaño_población y tasa de mutación', fontsize=16,
                 fontweight='bold', pad=20)
    ax.set_xlabel('Tamaño de Población', fontsize=13)
    ax.set_ylabel('Generaciones para alcanzar < 35000', fontsize=13)

    ax.set_xticks(x)
    ax.set_xticklabels(population_sizes)

    ax.legend(title='Tasas de Mutación', fontsize=11, title_fontsize=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7, color='gray')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()
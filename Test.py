from GeneticAlgorithm import genetic_algorithm
from Cities import *
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    print("Empezando experimento con 1500 generaciones de 500 individuos")
    generations, population_num = 1000, 500
    tests = [(0.03, 150), (0.03,50), (0.05, 150), (0.05, 50), (0.1, 150), (0.1,50), (0.15,150), (0.15,50)]
    data = DataLoader.load_data("coordinates.txt", "solution.txt")
    print(f"Mejor distancia es {data.get_solution_distance():.2f}")
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10), dpi=100)
    fig.suptitle('Comparativa de Hiperparámetros (1000 Gen, 500 Indiv)', fontsize=20, fontweight='bold')
    axes = axes.flatten()
    for i, test in enumerate(tests):
        mutation_rate, parent_num = test
        print(f"Ejecutando test {i} de 8. \n Parámetros:\nMutation rate: {mutation_rate}\nParent number: {parent_num}")
        best, history = genetic_algorithm(data, population_num, generations, mutation_rate, parent_num)
        print(f'Mejor distancia: {best.distance}')
        # Seleccionamos el subplot específico para este test
        ax = axes[i]

        # 3. PINTAR EN EL SUBPLOT
        ax.plot(history, color='#2ca02c', linewidth=2, alpha=0.8)

        ultimo_gen = len(history) - 1
        ultima_dist = history[-1]
        ax.scatter(ultimo_gen, ultima_dist, color='red', s=50, edgecolor='black', zorder=5)

        ax.set_title(f'Mut: {mutation_rate} | Padres: {parent_num}', fontsize=12, fontweight='bold')

        if i % 4 == 0:
            ax.set_ylabel('Mejor Distancia', fontsize=10)

        if i >= 4:
            ax.set_xlabel('Generación', fontsize=10)

        ax.grid(True, linestyle='--', alpha=0.5, color='gray')

        ax.annotate(f'{ultima_dist:.0f}',
                    xy=(ultimo_gen, ultima_dist),
                    xytext=(ultimo_gen - 50, ultima_dist + (ultima_dist * 0.1)),
                    ha='right', va='bottom', fontsize=10, color='red')
    plt.tight_layout()
    fig.subplots_adjust(top=0.90)
    plt.show()

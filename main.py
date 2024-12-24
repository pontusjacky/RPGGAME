import os
import random
from map import genrate_map
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--times', type=int, help='Some argument')
args = parser.parse_args()
i = str(args.times)
os.makedirs("output" + i, exist_ok=True)

population_size = 200
generations = 1000

population = [genrate_map(size=50) for _ in range(population_size)]

for generation in range(generations):
    
    fitness_scores = [landscape.fitness() for landscape in population]
    
    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
    population = sorted_population[:population_size // 2]
    
    while len(population) < population_size:
        parent = random.choice(population)
        child = genrate_map(size=50)
        child.map = parent.map.copy()
        child.mutate()
        population.append(child)

    best_landscape = population[0]
    best_landscape.to_image(f"output{i}/generation_{generation + 1}.png")
    print(f"Generation {generation + 1}: Best fitness = {fitness_scores[0]:.4f}")

print("Evolution Complete! Check the 'output' folder for generated map.")

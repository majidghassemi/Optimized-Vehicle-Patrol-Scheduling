import matplotlib.pyplot as plt
import numpy as np
import random

np.random.seed(42)
random.seed(42)

locations = np.random.rand(10, 2) * 100  # 10 random locations

initial_population = [np.random.permutation(10) for _ in range(5)]

def compute_fitness(route):
    unique_locations = len(set(route))
    total_distance = sum(np.linalg.norm(locations[route[i]] - locations[route[i+1]]) for i in range(len(route) - 1))
    # Normalize fitness to be between 80 and 90
    fitness = 80 + 10 * ((unique_locations - (total_distance / 100)) / 10)
    return fitness

fitness_scores = [compute_fitness(route) for route in initial_population]

# 1. Initial Population
plt.figure(figsize=(10, 5))
plt.scatter(locations[:, 0], locations[:, 1], c='red')
for i, loc in enumerate(locations):
    plt.text(loc[0], loc[1], f'{i}', fontsize=12, ha='right')
for route in initial_population:
    plt.plot(locations[route, 0], locations[route, 1], alpha=0.5)
plt.title("1. Initial Population")
plt.xlabel("Locations")
plt.ylabel(" ")
plt.show()

# 2. Fitness Computation
plt.figure(figsize=(10, 5))
plt.bar(range(len(initial_population)), fitness_scores, color='blue')
plt.title("2. Fitness Computation")
plt.xlabel("Individual")
plt.ylabel("Fitness Score")
plt.ylim(80, 90)
plt.show()

# 3. Tournament Selection
tournament_size = 3
tournament_individuals = random.sample(range(len(initial_population)), tournament_size)
tournament_fitness = [fitness_scores[i] for i in tournament_individuals]
best_tournament_individual = tournament_individuals[np.argmax(tournament_fitness)]

plt.figure(figsize=(10, 5))
plt.bar(tournament_individuals, tournament_fitness, color='green')
plt.title("3. Tournament Selection")
plt.xlabel("Tournament Individuals")
plt.ylabel("Fitness Score")
plt.bar(best_tournament_individual, fitness_scores[best_tournament_individual], color='red')
plt.ylim(80, 90)
plt.show()

# 4. Crossover
parent1 = initial_population[tournament_individuals[0]]
parent2 = initial_population[tournament_individuals[1]]
crossover_point = len(parent1) // 2
child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))

plt.figure(figsize=(10, 5))
plt.plot(range(len(parent1)), parent1, label='Parent 1', linestyle='--')
plt.plot(range(len(parent2)), parent2, label='Parent 2', linestyle='--')
plt.plot(range(len(child1)), child1, label='Child 1', color='blue')
plt.plot(range(len(child2)), child2, label='Child 2', color='green')
plt.title("4. Crossover")
plt.xlabel("Location Index")
plt.ylabel("Location")
plt.legend()
plt.show()

# 5. Mutation
mutated_child = child1.copy()
mutate_idx1, mutate_idx2 = random.sample(range(len(mutated_child)), 2)
mutated_child[mutate_idx1], mutated_child[mutate_idx2] = mutated_child[mutate_idx2], mutated_child[mutate_idx1]

plt.figure(figsize=(10, 5))
plt.plot(range(len(child1)), child1, label='Original Child', color='blue')
plt.plot(range(len(mutated_child)), mutated_child, label='Mutated Child', color='red')
plt.title("5. Mutation")
plt.xlabel("Location Index")
plt.ylabel("Location")
plt.legend()
plt.show()

# 6. Selection and Elitism
elite_size = 2
sorted_population = [x for _, x in sorted(zip(fitness_scores, initial_population), reverse=True)]
elites = sorted_population[:elite_size]
new_population = elites + [mutated_child, child2] + [initial_population[best_tournament_individual]]

new_fitness_scores = [compute_fitness(route) for route in new_population]

plt.figure(figsize=(10, 5))
plt.bar(range(len(new_population)), new_fitness_scores, color='gray')
for i in range(elite_size):
    plt.bar(i, new_fitness_scores[i], color='red', label='Elite' if i == 0 else "")
plt.title("6. Selection and Elitism")
plt.xlabel("New Population Individuals")
plt.ylabel("Fitness Score")
plt.ylim(80, 90)
plt.legend()
plt.show()

# 7. Termination Conditions
generations = 50
fitness_over_generations = [max([compute_fitness(np.random.permutation(10)) for _ in range(5)]) for _ in range(generations)]
termination_condition_met = generations - 1
no_improvement_threshold = 10

for i in range(no_improvement_threshold, generations):
    if all(fitness_over_generations[j] <= fitness_over_generations[j-1] for j in range(i-no_improvement_threshold+1, i+1)):
        termination_condition_met = i
        break

plt.figure(figsize=(10, 5))
plt.plot(range(generations), fitness_over_generations, label='Fitness')
plt.axvline(x=termination_condition_met, color='red', linestyle='--', label='Termination')
plt.title("7. Termination Conditions")
plt.xlabel("Generations")
plt.ylabel("Fitness Score")
plt.ylim(80, 90)
plt.legend()
plt.show()

# 8. Output
best_route = new_population[0]

plt.figure(figsize=(10, 5))
plt.scatter(locations[:, 0], locations[:, 1], c='red')
plt.plot(locations[best_route, 0], locations[best_route, 1], color='blue', label='Best Route')
for i, loc in enumerate(locations):
    plt.text(loc[0], loc[1], f'{i}', fontsize=12, ha='right')
plt.title("8. Output")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.legend()
plt.show()

import random
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

class GeneticAlgorithm:
    def __init__(self, vehicles, locations, shifts, population_size=400, generations=300, rest_period=10, patrol_time=5):
        self.vehicles = vehicles
        self.locations = locations + 2
        self.shifts = shifts
        self.population_size = population_size
        self.generations = generations
        self.patrol_time = patrol_time
        self.rest_period = rest_period
        self.shift_lengths = [119] * self.shifts
        self.distance_matrix = self.generate_distance_matrix()
        self.mutation_rate = 0.1
        self.elite_size = int(0.05 * self.population_size)
        self.tournament_size = 5
        self.population = self.initialize_population()
        self.fitness_cache = {}

    def generate_distance_matrix(self):
        return np.random.randint(10, 20, size=(102, 102))

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = {}
            for shift in range(self.shifts):
                shift_routes = {vehicle: [] for vehicle in range(self.vehicles)}
                individual[shift] = {vehicle: self.create_feasible_route(shift, shift_routes) for vehicle in range(self.vehicles)}
                for vehicle in range(self.vehicles):
                    shift_routes[vehicle] = individual[shift][vehicle][1]
            population.append(individual)
        return population

    def create_feasible_route(self, shift, shift_routes):
        route = [0]
        current_location = 0
        current_time = 0
        route_timings = [(current_location, current_time)]
        visited_times = {0: current_time}

        while current_time < self.shift_lengths[shift]:
            next_location = random.randint(1, 100)
            travel_time = self.distance_matrix[current_location][next_location]
            arrival_time = current_time + travel_time + self.patrol_time

            if any(arrival_time == other_time for other_route in shift_routes.values() for loc, other_time in other_route if loc == next_location):
                continue

            if next_location in visited_times and arrival_time - visited_times[next_location] <= 30:
                continue

            if arrival_time + self.distance_matrix[next_location][100] > self.shift_lengths[shift]:
                break

            route.append(next_location)
            route_timings.append((next_location, arrival_time))
            visited_times[next_location] = arrival_time
            current_location = next_location
            current_time = arrival_time

        if current_location != 100 and current_time + self.distance_matrix[current_location][100] <= self.shift_lengths[shift]:
            route.append(100)
            current_time += self.distance_matrix[current_location][100]
            route_timings.append((100, current_time))

        return (route, route_timings)

    def evaluate_fitness(self, individual):
        ind_str = str(individual)
        if ind_str in self.fitness_cache:
            return self.fitness_cache[ind_str]
        
        unique_locations = set()
        total_distance = 0
        for shift in individual:
            for vehicle in individual[shift]:
                route, _ = individual[shift][vehicle]
                unique_locations.update(route)
                for i in range(len(route) - 1):
                    total_distance += self.distance_matrix[route[i]][route[i+1]]
        fitness = len(unique_locations) - (total_distance / 1000)
        self.fitness_cache[ind_str] = fitness
        return fitness

    def crossover(self, parent1, parent2):
        child = {shift: {vehicle: None for vehicle in range(self.vehicles)} for shift in range(self.shifts)}
        for shift in range(self.shifts):
            for vehicle in range(self.vehicles):
                if random.random() > 0.5:
                    child[shift][vehicle] = parent1[shift][vehicle]
                else:
                    child[shift][vehicle] = parent2[shift][vehicle]
        return child

    def mutate(self, individual):
        for shift in individual.values():
            for vehicle_data in shift.values():
                route, timings = vehicle_data
                if random.random() < self.mutation_rate:
                    if len(route) > 3:
                        idx1, idx2 = random.sample(range(1, len(route) - 2), 2)
                        route[idx1], route[idx2] = route[idx2], route[idx1]

    def select_parents(self):
        return self.tournament_selection(), self.tournament_selection()

    def tournament_selection(self):
        tournament = random.sample(self.population, self.tournament_size)
        fittest = max(tournament, key=self.evaluate_fitness)
        return fittest

    def run(self):
        best_fitnesses = []
        best_solution = None
        best_fitness = float('-inf')

        for generation in range(self.generations):
            new_population = []
            elite_individuals = sorted(self.population, key=self.evaluate_fitness, reverse=True)[:self.elite_size]
            new_population.extend(elite_individuals)

            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.create_offspring) for _ in range((self.population_size - self.elite_size) // 2)]
                for future in futures:
                    child1, child2 = future.result()
                    new_population.extend([child1, child2])

            self.population = sorted(new_population, key=self.evaluate_fitness, reverse=True)[:self.population_size]

            current_best_fitness = self.evaluate_fitness(self.population[0])
            best_fitnesses.append(current_best_fitness)
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = self.population[0]

            if generation > 0 and best_fitnesses[-1] == best_fitnesses[-2]:
                self.mutation_rate = min(1.0, self.mutation_rate + 0.01)
            else:
                self.mutation_rate = max(0.1, self.mutation_rate - 0.01)

        return best_solution, best_fitness, best_fitnesses

    def create_offspring(self):
        parent1, parent2 = self.select_parents()
        child1 = self.crossover(parent1, parent2)
        child2 = self.crossover(parent2, parent1)
        self.mutate(child1)
        self.mutate(child2)
        return child1, child2

best_overall_solution = None
best_overall_fitness = 0
best_fitness_per_iteration = []
average_fitness_per_iteration = []
max_fitness_so_far = float('-inf')

for i in range(100):
    ga = GeneticAlgorithm(vehicles=4, locations=99, shifts=4)
    best_solution, fitness, best_fitnesses = ga.run()
    if fitness > max_fitness_so_far:
        max_fitness_so_far = fitness
    best_fitness_per_iteration.append(max_fitness_so_far)
    average_fitness_per_iteration.append(sum(best_fitness_per_iteration) / len(best_fitness_per_iteration))
    if fitness > best_overall_fitness:
        best_overall_fitness = fitness
        best_overall_solution = best_solution

plt.figure(figsize=(12, 6))
plt.plot(best_fitness_per_iteration, label='Best Distinct Locations Visited Up to Each Iteration', color='blue')
plt.plot(average_fitness_per_iteration, label='Average Distinct Locations Visited', color='red', linestyle='--')
plt.xlabel('Iteration')
plt.ylabel('Distinct Locations Visited')
plt.title('Distinct Locations Visited per Iteration: GDVPS')
plt.legend()
plt.grid(True)
plt.show()

print(f"Best Iteration - Total distinct locations visited: {best_overall_fitness}")
for shift in best_overall_solution:
    for vehicle in best_overall_solution[shift]:
        route, timings = best_overall_solution[shift][vehicle]
        print(f"Vehicle {vehicle}, Shift {shift}:")
        print(f"  Route: {route}")
        print("  Timing:")
        for loc, time in timings:
            print(f"    Location {loc} at time {time} minutes")

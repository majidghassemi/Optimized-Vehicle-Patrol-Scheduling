import random
import numpy as np
import re
from datetime import datetime
import time

class GDVPS:
    def __init__(self, vehicles, locations, shifts=6, population_size=400, generations=500, rest_period=10, patrol_time=5, heuristic_file='/home/majidghasemi/Optimized-Vehicle-Patrol-Scheduling/large_instances/AHBPS_large.txt'):
        self.vehicles = vehicles
        self.locations = locations + 1
        self.shifts = shifts
        self.population_size = population_size
        self.generations = generations
        self.patrol_time = patrol_time
        self.rest_period = rest_period
        self.shift_lengths = [119] * self.shifts
        self.base_distance_matrix = self.generate_distance_matrix()
        self.distance_matrix = self.base_distance_matrix.copy()
        self.mutation_rate = 0.1
        self.elite_size = int(0.1 * self.population_size)
        self.tournament_size = max(2, int(0.05 * self.locations))
        self.heuristic_solutions = self.load_heuristic_solutions(heuristic_file)
        self.population = self.initialize_population()
        self.fitness_cache = {}

    def generate_distance_matrix(self):
        matrix = np.random.normal(mu=15, scale=5, size=(self.locations, self.locations))
        
        matrix = (matrix + matrix.T) // 2
        
        np.fill_diagonal(matrix, 0)

        for i in range(self.locations):
            for j in range(i + 1, self.locations):
                if random.random() < 0.3:
                    matrix[i][j] = matrix[j][i] = np.inf

        return matrix

    def fluctuate_travel_times(self):
        for i in range(self.locations):
            for j in range(i + 1, self.locations):
                if self.base_distance_matrix[i][j] != np.inf:
                    fluctuation = random.choice([-2, 2])
                    self.distance_matrix[i][j] = self.base_distance_matrix[i][j] + fluctuation
                    self.distance_matrix[j][i] = self.distance_matrix[i][j]

    def load_heuristic_solutions(self, heuristic_file):
        heuristic_solutions = {}
        with open(heuristic_file, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 2):
                match = re.search(r'(\d+) vehicles, (\d+) shifts, (\d+) locations', lines[i])
                if match:
                    vehicles = int(match.group(1))
                    locations = int(match.group(3))
                    key = (vehicles, locations)
                    avg_unique_locations = float(re.search(r'Average Unique Locations Visited: (\d+\.?\d*)', lines[i]).group(1))
                    heuristic_solutions[key] = avg_unique_locations
        return heuristic_solutions

    def initialize_population(self):
        population = []
        heuristic_key = (self.vehicles, self.locations - 1)
        if (self.vehicles, self.locations - 1) in self.heuristic_solutions:
            for _ in range(min(10, self.population_size)):
                individual = {}
                for shift in range(self.shifts):
                    shift_routes = {vehicle: [] for vehicle in range(self.vehicles)}
                    for vehicle in range(self.vehicles):
                        num_locations = int(self.heuristic_solutions[heuristic_key])
                        route = [0] + random.sample(range(1, self.locations), num_locations) + [0]
                        timings = [(loc, 0) for loc in route]
                        individual[shift] = {vehicle: (route, timings)}
                population.append(individual)

        remaining_population_size = self.population_size - len(population)
        for _ in range(remaining_population_size):
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
            next_location = random.randint(1, self.locations - 1)
            travel_time = self.distance_matrix[current_location][next_location]
            arrival_time = current_time + travel_time + self.patrol_time

            if any(arrival_time == other_time for other_route in shift_routes.values() for loc, other_time in other_route if loc == next_location):
                continue

            if next_location in visited_times and arrival_time - visited_times[next_location] <= 30:
                continue

            if arrival_time + self.distance_matrix[next_location][0] > self.shift_lengths[shift]:
                break

            route.append(next_location)
            route_timings.append((next_location, arrival_time))
            visited_times[next_location] = arrival_time
            current_location = next_location
            current_time = arrival_time

        if current_location != 0 and current_time + self.distance_matrix[current_location][0] <= self.shift_lengths[shift]:
            route.append(0)
            current_time += self.distance_matrix[current_location][0]
            route_timings.append((0, current_time))

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
                total_distance += sum(self.distance_matrix[route[i]][route[i+1]] for i in range(len(route) - 1))
        fitness = len(unique_locations)
        self.fitness_cache[ind_str] = fitness
        return fitness

    def crossover(self, parent1, parent2):
        child = {}
        for shift in range(self.shifts):
            child[shift] = {}
            for vehicle in range(self.vehicles):
                if random.random() > 0.5:
                    if vehicle in parent1[shift]:
                        child[shift][vehicle] = parent1[shift][vehicle]
                else:
                    if vehicle in parent2[shift]:
                        child[shift][vehicle] = parent2[shift][vehicle]
            for vehicle in range(self.vehicles):
                if vehicle not in child[shift]:
                    child[shift][vehicle] = self.create_feasible_route(shift, {})
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
        return max(tournament, key=self.evaluate_fitness)

    def run(self):
        best_fitnesses = []
        best_solution = None
        best_fitness = float('-inf')
        stagnation_count = 0

        for generation in range(self.generations):
            self.distance_matrix = self.base_distance_matrix.copy()

            if random.random() < 0.5:
                print("Fluctuating travel times for this run.")
                self.fluctuate_travel_times()
            else:
                print("Keeping travel times constant for this run.")

            new_population = []
            elite_individuals = sorted(self.population, key=self.evaluate_fitness, reverse=True)[:self.elite_size]
            new_population.extend(elite_individuals)

            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                self.mutate(child1)
                self.mutate(child2)
                new_population.append(child1)
                new_population.append(child2)

            self.population = sorted(new_population, key=self.evaluate_fitness, reverse=True)[:self.population_size]

            current_best_fitness = self.evaluate_fitness(self.population[0])
            best_fitnesses.append(current_best_fitness)

            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_solution = self.population[0]
                stagnation_count = 0
            else:
                stagnation_count += 1

            print(f"Generation {generation + 1}, Best Fitness: {current_best_fitness}, Stagnation Count: {stagnation_count}")

            if stagnation_count >= 25:
                print(f"Terminating early at generation {generation + 1} due to lack of improvement.")
                break

        return best_solution, best_fitness, best_fitnesses

    def write_results_to_file(self, filename, vehicles, locations, shifts, best_fitness, average_fitness, execution_time=None):
        with open(filename, 'a') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"{vehicles} vehicles, {shifts} shifts, {locations} locations => Best fitness (distinct locations visited): {best_fitness}, Average fitness: {average_fitness}\n")
            if execution_time is not None:
                file.write(f"Execution Time: {execution_time:.2f} seconds\n")
            file.write("-----\n")

    def print_travel_details(self, solution):
        for shift in solution:
            print(f"Shift {shift + 1}:")
            for vehicle, (route, timings) in solution[shift].items():
                print(f"  Vehicle {vehicle + 1}:")
                for loc, time in timings:
                    print(f"    Location {loc}, Time {time}")
                print("")


results_filename = 'GDVPS_Run_Time_Large_Instance_Vehicles_Changes_v2.txt'

VALID_PAIRS = [(15, 1000)]

for vehicles, locations in VALID_PAIRS:
    shifts = 6
    best_overall_solution = None
    best_overall_fitness = 0
    total_fitness_across_iterations = 0
    max_fitness_so_far = float('-inf')

    start_time = time.time()

    for i in range(1):
        ga = GDVPS(vehicles=vehicles, locations=locations, shifts=shifts)
        best_solution, fitness, best_fitnesses = ga.run()
        if fitness > max_fitness_so_far:
            max_fitness_so_far = fitness

        total_fitness_across_iterations += fitness

        if fitness > best_overall_fitness:
            best_overall_fitness = fitness
            best_overall_solution = best_solution

    average_fitness_across_iterations = total_fitness_across_iterations / 1

    end_time = time.time()
    execution_time = end_time - start_time

    ga.write_results_to_file(results_filename, vehicles, locations, shifts, best_overall_fitness, average_fitness_across_iterations, execution_time)

    print(f"Details for {vehicles} vehicles and {locations} locations:")
    ga.print_travel_details(best_overall_solution)
    print("\n" + "-"*50 + "\n")

print("Automated Genetic Algorithm tests for all valid pairs completed. Results saved to file.")

import random
import numpy as np
import re
from datetime import datetime

# Define the number of locations
NUM_LOCATIONS = 100

class GeneticAlgorithm:
    def __init__(self, vehicles, locations, shifts, population_size=200, generations=150, rest_period=10, patrol_time=5):
        self.vehicles = vehicles
        self.locations = locations + 2  # Adding start and end locations
        self.shifts = shifts
        self.population_size = population_size
        self.generations = generations
        self.patrol_time = patrol_time
        self.rest_period = rest_period
        self.shift_lengths = [119] * self.shifts
        self.distance_matrix = self.generate_distance_matrix()
        self.mutation_rate = 0.1
        self.elite_size = int(0.1 * self.population_size)
        self.tournament_size = 5
        self.population = self.initialize_population()
        self.fitness_cache = {}

    def generate_distance_matrix(self):
        return np.random.randint(10, 20, size=(self.locations, self.locations))

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
        route = [0]  # Starting point
        current_location = 0
        current_time = 0
        route_timings = [(current_location, current_time)]
        visited_times = {0: current_time}

        while current_time < self.shift_lengths[shift]:
            next_location = random.randint(1, self.locations - 2)  # Ensure it's within the valid range
            travel_time = self.distance_matrix[current_location][next_location]
            arrival_time = current_time + travel_time + self.patrol_time

            if any(arrival_time == other_time for other_route in shift_routes.values() for loc, other_time in other_route if loc == next_location):
                continue

            if next_location in visited_times and arrival_time - visited_times[next_location] <= 30:
                continue

            if arrival_time + self.distance_matrix[next_location][self.locations - 1] > self.shift_lengths[shift]:
                break

            route.append(next_location)
            route_timings.append((next_location, arrival_time))
            visited_times[next_location] = arrival_time
            current_location = next_location
            current_time = arrival_time

        # Add the end location
        if current_location != self.locations - 1 and current_time + self.distance_matrix[current_location][self.locations - 1] <= self.shift_lengths[shift]:
            route.append(self.locations - 1)
            current_time += self.distance_matrix[current_location][self.locations - 1]
            route_timings.append((self.locations - 1, current_time))

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
        fitness = len(unique_locations) - (total_distance / 1000)
        self.fitness_cache[ind_str] = fitness
        return fitness

    def crossover(self, parent1, parent2):
        child = {}
        for shift in range(self.shifts):
            child[shift] = {vehicle: (None, None) for vehicle in range(self.vehicles)}
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
        return max(tournament, key=self.evaluate_fitness)

    def run(self):
        best_fitnesses = []
        best_solution = None
        best_fitness = float('-inf')
        stagnation_count = 0  # Track how long the solution has not improved

        for generation in range(self.generations):
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
                stagnation_count = 0  # Reset stagnation counter if there's an improvement
            else:
                stagnation_count += 1

            if stagnation_count >= 10:  # Early termination if no improvement for 10 generations
                print(f"Terminating early at generation {generation} due to lack of improvement.")
                break

            if generation > 0 and best_fitnesses[-1] == best_fitnesses[-2]:
                self.mutation_rate = min(1.0, self.mutation_rate + 0.01)
            else:
                self.mutation_rate = max(0.1, self.mutation_rate - 0.01)

        return best_solution, best_fitness, best_fitnesses

    def write_results_to_file(self, filename, vehicles, locations, shifts, best_fitness, average_fitness):
        with open(filename, 'a') as file:  # Open in append mode
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"{vehicles} vehicles, {shifts} shifts, {locations} locations => Best fitness (distinct locations visited): {best_fitness}, Average fitness: {average_fitness}\n")
            file.write("-----\n")

# Function to parse the text file and extract parameters
def parse_file(file_path):
    instances = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r"(\d+) cars?, (\d+) shifts?, (\d+) locations?,", line)
            if match:
                cars = int(match.group(1))
                shifts = int(match.group(2))
                locations = int(match.group(3))
                instances.append((cars, shifts, locations))
    return instances

# Path to the text file containing the instances
file_path = './results.txt'

# Parse the file to get the instances
instances = parse_file(file_path)

# File to save all the results
results_filename = 'ga_results_automated_from_file.txt'

# Iterate over all instances and run the algorithm
for cars, shifts, locations in instances:
    best_overall_solution = None
    best_overall_fitness = 0
    total_fitness_across_iterations = 0
    max_fitness_so_far = float('-inf')

    for i in range(100):
        ga = GeneticAlgorithm(vehicles=cars, locations=locations, shifts=shifts)
        best_solution, fitness, best_fitnesses = ga.run()

        # Update the maximum fitness so far
        if fitness > max_fitness_so_far:
            max_fitness_so_far = fitness

        # Accumulate the fitness across iterations
        total_fitness_across_iterations += fitness

        # Update the best overall solution if this iteration's fitness is the best seen so far
        if fitness > best_overall_fitness:
            best_overall_fitness = fitness
            best_overall_solution = best_solution

    # Calculate the average fitness across all 100 iterations
    average_fitness_across_iterations = total_fitness_across_iterations / 100

    # Write the results for this configuration to the file
    ga.write_results_to_file(results_filename, cars, locations, shifts, best_overall_fitness, average_fitness_across_iterations)

# Inform user that the process is complete
print("Automated Genetic Algorithm tests completed. Results saved to file.")
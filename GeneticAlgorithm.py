import random
import numpy as np
import re
from datetime import datetime

# Define the number of locations
# NUM_LOCATIONS = 100

class GeneticAlgorithm:
    def __init__(self, vehicles, locations, shifts=1, population_size=200, generations=150, rest_period=10, patrol_time=5):
        self.vehicles = vehicles
        self.locations = locations + 1  # Adding depot location
        self.shifts = shifts
        self.population_size = population_size
        self.generations = generations
        self.patrol_time = patrol_time
        self.rest_period = rest_period
        self.shift_lengths = [720]  # Single shift with 720 minutes
        self.edge_probability = 0.099  # Edge probability for the random network
        self.distance_matrix = self.generate_distance_matrix()
        self.mutation_rate = 0.1
        self.elite_size = int(0.1 * self.population_size)
        self.tournament_size = 5
        self.population = self.initialize_population()
        self.fitness_cache = {}

    def generate_distance_matrix(self):
        # Create an adjacency matrix with the specified edge probability
        adjacency_matrix = np.random.rand(self.locations, self.locations) < self.edge_probability
        
        # Make the matrix symmetric and remove self-loops
        adjacency_matrix = np.triu(adjacency_matrix, 1)
        adjacency_matrix += adjacency_matrix.T
        
        # Generate the distance matrix with random distances only where an edge exists
        distance_matrix = np.zeros((self.locations, self.locations))
        distance_matrix[adjacency_matrix] = np.random.randint(10, 20, size=np.count_nonzero(adjacency_matrix))
        
        # Set distances to a high value (infinity) where no edge exists to represent no direct path
        distance_matrix[distance_matrix == 0] = np.inf
        
        # Ensure that the diagonal is zero (no self-distance)
        np.fill_diagonal(distance_matrix, 0)
        
        return distance_matrix

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = {}
            shift_routes = {vehicle: [] for vehicle in range(self.vehicles)}
            individual[0] = {vehicle: self.create_feasible_route(0, shift_routes) for vehicle in range(self.vehicles)}
            for vehicle in range(self.vehicles):
                shift_routes[vehicle] = individual[0][vehicle][1]
            population.append(individual)
        return population

    def create_feasible_route(self, shift, shift_routes):
        depot = 0  # Start and end location is the depot
        route = [depot]  # Starting at the depot
        current_location = depot
        current_time = 0
        route_timings = [(current_location, current_time)]
        visited_times = {depot: [current_time]}  # Store visit times as a list to track multiple visits

        took_rest = False  # Track if the vehicle has taken a rest

        while current_time < self.shift_lengths[shift]:
            possible_locations = [loc for loc in range(1, self.locations) if self.distance_matrix[current_location][loc] < np.inf]
            if not possible_locations:
                break
            
            next_location = random.choice(possible_locations)
            travel_time = self.distance_matrix[current_location][next_location]
            arrival_time = current_time + travel_time + self.patrol_time

            # Check revisit condition: no more than 10 times and with a gap of at least 30 minutes
            if next_location in visited_times:
                if len(visited_times[next_location]) >= 10:
                    continue
                if any(arrival_time - prev_time < 30 for prev_time in visited_times[next_location]):
                    continue

            # Check if returning to depot for a mandatory rest
            if not took_rest and arrival_time + self.distance_matrix[next_location][depot] <= self.shift_lengths[shift] - 10:
                rest_time = random.randint(10, 30)
                route.append(next_location)
                route_timings.append((next_location, arrival_time))
                current_time = arrival_time + rest_time + self.distance_matrix[next_location][depot]
                route.append(depot)
                route_timings.append((depot, current_time))
                visited_times[next_location] = [arrival_time]
                current_location = depot
                took_rest = True
                continue

            if arrival_time + self.distance_matrix[next_location][depot] > self.shift_lengths[shift]:
                break

            route.append(next_location)
            route_timings.append((next_location, arrival_time))
            if next_location in visited_times:
                visited_times[next_location].append(arrival_time)
            else:
                visited_times[next_location] = [arrival_time]
            current_location = next_location
            current_time = arrival_time

        # Ensure the vehicle returns to the depot if time allows
        if current_location != depot and current_time + self.distance_matrix[current_location][depot] <= self.shift_lengths[shift]:
            route.append(depot)
            current_time += self.distance_matrix[current_location][depot]
            route_timings.append((depot, current_time))

        return (route, route_timings)

    def evaluate_fitness(self, individual):
        ind_str = str(individual)
        if ind_str in self.fitness_cache:
            return self.fitness_cache[ind_str]
        
        unique_locations = set()
        for shift in individual:
            for vehicle in individual[shift]:
                route, _ = individual[shift][vehicle]
                unique_locations.update(route)
        fitness = len(unique_locations)
        self.fitness_cache[ind_str] = fitness
        return fitness

    def crossover(self, parent1, parent2):
        child = {}
        child[0] = {vehicle: (None, None) for vehicle in range(self.vehicles)}
        for vehicle in range(self.vehicles):
            if random.random() > 0.5:
                child[0][vehicle] = parent1[0][vehicle]
            else:
                child[0][vehicle] = parent2[0][vehicle]
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

            if stagnation_count >= 20:  # Early termination if no improvement for 10 generations
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

# Define the valid pairs of vehicles and locations
valid_pairs = [
    (1, 4), (1, 10), (1, 20), (2, 4), (2, 10), (2, 20), (2, 30), (3,10), (3, 20), (3, 30), (3, 50), (3, 75), (3, 100), (4, 20), (4,30),
    (4, 50), (4, 75), (4, 100), (4, 125), (4, 150), (5, 50), (5, 75), (5, 100), (5, 125), (5, 150), (5, 175), (5, 200), (10, 100), (10, 150), (10, 200), (10, 250), (10, 300), 
    (10, 400), (15, 150), (15, 200), (15, 300), (15, 400), (15, 500), (20, 200), (20, 300), (20, 400), (20, 500), (20, 750), (25, 500), (25, 750), (25, 1000), 
    (30, 500), (30, 750), (30, 1000)
]

# File to save all the results
results_filename = 'ga_results_automated_from_file.txt'

# Iterate over all valid pairs and run the algorithm
for cars, locations in valid_pairs:
    best_overall_solution = None
    best_overall_fitness = 0
    total_fitness_across_iterations = 0
    max_fitness_so_far = float('-inf')

    for i in range(50):
        ga = GeneticAlgorithm(vehicles=cars, locations=locations, shifts=1)
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
    average_fitness_across_iterations = total_fitness_across_iterations / 50

    # Write the results for this configuration to the file
    ga.write_results_to_file(results_filename, cars, locations, 1, best_overall_fitness, average_fitness_across_iterations)

# Inform user that the process is complete
print("Automated Genetic Algorithm tests completed. Results saved to file.")
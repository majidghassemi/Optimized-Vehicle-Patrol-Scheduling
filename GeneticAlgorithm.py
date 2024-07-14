import random
import matplotlib.pyplot as plt

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
        self.population = self.initialize_population()
        self.mutation_rate = 0.1 

    def generate_distance_matrix(self):
        return [[random.randint(10, 20) for _ in range(102)] for _ in range(102)]

    def initialize_population(self):
        return [{shift: {vehicle: self.create_feasible_route(shift) for vehicle in range(self.vehicles)} for shift in range(self.shifts)} for _ in range(self.population_size)]

    def create_feasible_route(self, shift):
        route = [0]
        current_location = 0
        current_time = 0
        route_timings = [(current_location, current_time)]

        while current_time < self.shift_lengths[shift]:
            next_location = random.randint(1, 100)
            travel_time = self.distance_matrix[current_location][next_location]
            arrival_time = current_time + travel_time + self.patrol_time

            if arrival_time + self.distance_matrix[next_location][100] > self.shift_lengths[shift]:
                break

            route.append(next_location)
            route_timings.append((next_location, arrival_time))
            current_location = next_location
            current_time = arrival_time

        if current_location != 100 and current_time + self.distance_matrix[current_location][100] <= self.shift_lengths[shift]:
            route.append(100)
            current_time += self.distance_matrix[current_location][100]
            route_timings.append((100, current_time))

        return (route, route_timings)

    def evaluate_fitness(self, individual):
        unique_locations = set()
        for shift in individual:
            for vehicle in individual[shift]:
                route, _ = individual[shift][vehicle]
                unique_locations.update(route)
        return len(unique_locations)

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
        parents = random.sample(self.population, 2)
        return parents[0], parents[1]

    def run(self):
        best_fitnesses = []
        best_solution = None
        best_fitness = 0

        for generation in range(self.generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1, parent2 = self.select_parents()
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                self.mutate(child1)
                self.mutate(child2)
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

best_overall_solution = None
best_overall_fitness = 0
best_fitness_per_iteration = []
average_fitness_per_iteration = []
max_fitness_so_far = 0

for i in range(100):
    ga = GeneticAlgorithm(vehicles=5, locations=99, shifts=4)
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
plt.title('Best and Average Performance Over 100 Iterations for Genetic Algorithm')
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



# Genetic Dynamic VPS (GDVPS)
import random
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class HVSP:
    def __init__(self, vehicles, total_locations, shift_duration=720, patrol_time=5, max_rest_time=30, edge_probability=0.1, iterations=30):
        # Validate parameters
        assert vehicles > 0, "Number of vehicles must be positive"
        assert total_locations > 1, "Number of locations must be greater than 1"
        assert shift_duration > 0, "Shift duration must be positive"
        assert patrol_time > 0, "Patrol time must be positive"
        assert max_rest_time >= 0, "Max rest time must be non-negative"
        
        self.vehicles = vehicles
        self.total_locations = total_locations
        self.depot = 0  # Single depot, acting as both start and end point
        self.shift_duration = shift_duration  # Single 12-hour shift (720 minutes)
        self.patrol_time = patrol_time
        self.max_rest_time = max_rest_time
        self.iterations = iterations
        self.edge_probability = edge_probability
        self.distance_matrix = self.generate_random_network()
        self.vehicle_rest_time = {}  # Track when each vehicle takes its rest

    def generate_random_network(self):
        """
        Generate a random network (distance matrix) with a given probability for an edge to exist.
        """
        distance_matrix = np.full((self.total_locations + 1, self.total_locations + 1), np.inf)

        for i in range(self.total_locations + 1):
            for j in range(i + 1, self.total_locations + 1):
                if random.random() < self.edge_probability:
                    travel_time = random.randint(10, 20)
                    distance_matrix[i][j] = travel_time
                    distance_matrix[j][i] = travel_time  # Undirected graph

        # Ensure the depot is connected to some locations
        for i in range(1, self.total_locations + 1):
            if distance_matrix[self.depot][i] == np.inf:
                travel_time = random.randint(10, 20)
                distance_matrix[self.depot][i] = travel_time
                distance_matrix[i][self.depot] = travel_time

        return distance_matrix

    def needs_revisiting(self, current_time, location, last_visit_times, location_locks):
        # Check if exactly 30 minutes have passed since the last visit and no lock exists on the location
        return (current_time - last_visit_times[location]) >= 30 and (location_locks[location] is None or location_locks[location] <= current_time)

    def initialize_simulation(self):
        # Initialize structures to store routes, timings, and visits
        routes = {vehicle: [] for vehicle in range(self.vehicles)}
        timing_info = {vehicle: [] for vehicle in range(self.vehicles)}
        location_visits = {loc: [] for loc in range(1, self.total_locations + 1)}
        self.vehicle_rest_time = {vehicle: None for vehicle in range(self.vehicles)}  # Reset rest time tracking
        
        return routes, timing_info, location_visits

    def simulate_shift(self, vehicle, last_visit_times, location_locks, timing_info, routes, location_visits):
        current_time = 0
        rest_taken = False

        route = [self.depot]
        visited_this_shift = set()
        timing_info[vehicle].append((self.depot, current_time))
        
        while current_time + self.patrol_time <= self.shift_duration:
            # Check if the vehicle needs to take a rest
            if not rest_taken:
                # Ensure no other vehicle is resting
                if all(rest_time is None or rest_time <= current_time for v, rest_time in self.vehicle_rest_time.items() if v != vehicle):
                    rest_time = random.randint(10, self.max_rest_time)
                    current_time += rest_time
                    self.vehicle_rest_time[vehicle] = current_time  # Record when the vehicle rested
                    rest_taken = True

            # Select possible locations to visit
            possible_locations = [
                loc for loc in range(1, self.total_locations + 1)
                if loc not in visited_this_shift
                and self.distance_matrix[route[-1]][loc] != np.inf
                and self.needs_revisiting(current_time, loc, last_visit_times, location_locks)
            ]
            if not possible_locations:
                break

            random.shuffle(possible_locations)
            for loc in possible_locations:
                travel_time_to_next = self.distance_matrix[route[-1]][loc]
                stay_at_next = current_time + travel_time_to_next + self.patrol_time

                if stay_at_next + travel_time_to_next > self.shift_duration:
                    continue

                route.append(loc)
                visited_this_shift.add(loc)
                current_time = stay_at_next
                timing_info[vehicle].append((loc, current_time))
                last_visit_times[loc] = current_time
                location_locks[loc] = current_time + self.patrol_time
                location_visits[loc].append((vehicle, current_time))
                break

        # Add return to depot if time allows
        if current_time + self.distance_matrix[route[-1]][self.depot] <= self.shift_duration:
            current_time += self.distance_matrix[route[-1]][self.depot]
        route.append(self.depot)
        timing_info[vehicle].append((self.depot, current_time))
        routes[vehicle] = route

        return last_visit_times, location_locks

    def evaluate_solution(self, location_visits):
        return len([loc for loc in location_visits if location_visits[loc]])

    def run_simulation(self, last_visit_times, location_locks, is_detailed=False):
        routes, timing_info, location_visits = self.initialize_simulation()

        # Initialize with a random solution
        for vehicle in range(self.vehicles):
            last_visit_times, location_locks = self.simulate_shift(vehicle, last_visit_times, location_locks, timing_info,
                                                                   routes, location_visits)

        current_solution = routes
        current_score = self.evaluate_solution(location_visits)

        total_unique_locations_visited = current_score

        if is_detailed:
            self.print_detailed_info(total_unique_locations_visited, current_solution, timing_info)

        return total_unique_locations_visited

    def print_detailed_info(self, total_unique_locations_visited, routes, timing_info):
        print(f"Total distinct locations visited (excluding depot): {total_unique_locations_visited}")
        for vehicle in range(self.vehicles):
            print(f"Vehicle {vehicle}:")
            route = routes[vehicle]
            print(f"  Route: {route}")
            print("  Timing:")
            for loc, time in timing_info[vehicle]:
                loc_name = f"Location {loc}" if loc != self.depot else "Depot"
                print(f"      {loc_name} at time {time} minutes")

    def write_results_to_file(self, filename, vehicles, locations, rest_time, average_locations_visited):
        with open(filename, 'a') as file:  # Open in append mode
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"{vehicles} cars, {locations} locations, {rest_time} rest time => {average_locations_visited} locations were visited on average.\n")
            file.write("-----\n")

    def main(self):
        # Define ranges for vehicles and locations
        vehicle_options = [1, 2, 3, 4, 5, 7, 10, 12, 15, 20, 25, 30]
        location_options = [4, 10, 20, 30, 50, 75, 100, 150, 200, 250, 500, 1000]

        # Loop over all instances, filtering out cases where vehicles exceed a third of the locations
        for vehicles in vehicle_options:
            for locations in location_options:
                if vehicles <= locations // 3:  # Ensure vehicles do not exceed one-third of the locations
                    hvsp = HVSP(vehicles=vehicles, total_locations=locations)
                    results = []
                    for _ in range(hvsp.iterations):
                        last_visit_times = {loc: float('-inf') for loc in range(1, locations + 1)}
                        location_locks = {loc: None for loc in range(1, locations + 1)}
                        results.append(hvsp.run_simulation(last_visit_times, location_locks))

                    # Compute the average results
                    average_locations_visited = sum(results) / len(results)

                    # Write results to file (appending)
                    hvsp.write_results_to_file('results_automated.txt', vehicles, locations, hvsp.max_rest_time, average_locations_visited)

# Run the main function
if __name__ == "__main__":
    hvsp = HVSP(vehicles=2, total_locations=10)  # Initial values to start the automation loop
    hvsp.main()

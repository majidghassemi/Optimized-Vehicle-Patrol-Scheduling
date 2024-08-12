import random
import numpy as np
from datetime import datetime

class HVSP:
    def __init__(self, vehicles, total_locations, shift_duration=720, patrol_time=5, max_rest_time=20, edge_probability=0.099, iterations=30):
        assert vehicles > 0, "Number of vehicles must be positive"
        assert total_locations > 1, "Number of locations must be greater than 1"
        assert shift_duration > 0, "Shift duration must be positive"
        assert patrol_time > 0, "Patrol time must be positive"
        assert max_rest_time >= 0, "Max rest time must be non-negative"
        
        self.vehicles = vehicles
        self.total_locations = total_locations
        self.depot = 0  # Single depot
        self.shift_duration = shift_duration
        self.patrol_time = patrol_time
        self.max_rest_time = max_rest_time
        self.iterations = iterations
        self.edge_probability = edge_probability
        self.distance_matrix = self.generate_random_network()
        self.vehicle_rest_time = {}  # Track when each vehicle takes its rest
        self.max_revisits = 10  # Maximum revisits allowed per location

    def generate_random_network(self):
        distance_matrix = np.full((self.total_locations + 1, self.total_locations + 1), np.inf)
        for i in range(self.total_locations + 1):
            for j in range(i + 1, self.total_locations + 1):
                if random.random() < self.edge_probability:
                    travel_time = random.randint(10, 20)
                    distance_matrix[i][j] = travel_time
                    distance_matrix[j][i] = travel_time
        for i in range(1, self.total_locations + 1):
            if distance_matrix[self.depot][i] == np.inf:
                travel_time = random.randint(10, 20)
                distance_matrix[self.depot][i] = travel_time
                distance_matrix[i][self.depot] = travel_time
        return distance_matrix

    def needs_revisiting(self, current_time, location, last_visit_times, location_locks, visit_counts):
        # Check if exactly 30 minutes have passed since the last visit, 
        # no lock exists on the location, and the location has been visited fewer than 10 times
        return (current_time - last_visit_times[location]) >= 30 and \
               (location_locks[location] is None or location_locks[location] <= current_time) and \
               visit_counts[location] < self.max_revisits

    def initialize_simulation(self):
        routes = {vehicle: [] for vehicle in range(self.vehicles)}
        timing_info = {vehicle: [] for vehicle in range(self.vehicles)}
        location_visits = {loc: [] for loc in range(1, self.total_locations + 1)}
        visit_counts = {loc: 0 for loc in range(1, self.total_locations + 1)}
        self.vehicle_rest_time = {vehicle: None for vehicle in range(self.vehicles)}
        return routes, timing_info, location_visits, visit_counts

    def simulate_shift(self, vehicle, last_visit_times, location_locks, timing_info, routes, location_visits, visit_counts):
        current_time = 0
        rest_taken = False

        route = [self.depot]
        visited_this_shift = set()
        timing_info[vehicle].append((self.depot, current_time))
        
        print(f"[Vehicle {vehicle}] Starting shift with initial time {current_time}.")

        while current_time + self.patrol_time <= self.shift_duration:
            if not rest_taken and all(rest_time is None or rest_time <= current_time for v, rest_time in self.vehicle_rest_time.items() if v != vehicle):
                rest_time = random.randint(10, self.max_rest_time)
                current_time += rest_time
                self.vehicle_rest_time[vehicle] = current_time
                rest_taken = True
                print(f"[Vehicle {vehicle}] Taking rest for {rest_time} minutes. Current time: {current_time}.")

            possible_locations = [
                loc for loc in range(1, self.total_locations + 1)
                if self.distance_matrix[route[-1]][loc] != np.inf
                and self.needs_revisiting(current_time, loc, last_visit_times, location_locks, visit_counts)
            ]

            if not possible_locations:
                print(f"[Vehicle {vehicle}] No more valid locations to visit.")
                break

            closest_location = min(possible_locations, key=lambda loc: self.distance_matrix[route[-1]][loc])
            travel_time_to_next = self.distance_matrix[route[-1]][closest_location]
            stay_at_next = current_time + travel_time_to_next + self.patrol_time

            if stay_at_next + travel_time_to_next > self.shift_duration:
                print(f"[Vehicle {vehicle}] Not enough time to visit the next location. Ending shift.")
                break

            route.append(closest_location)
            visited_this_shift.add(closest_location)
            current_time = stay_at_next
            timing_info[vehicle].append((closest_location, current_time))
            last_visit_times[closest_location] = current_time
            location_locks[closest_location] = current_time + self.patrol_time
            location_visits[closest_location].append((vehicle, current_time))
            visit_counts[closest_location] += 1

            print(f"[Vehicle {vehicle}] Visited location {closest_location} at time {current_time}.")

        if current_time + self.distance_matrix[route[-1]][self.depot] <= self.shift_duration:
            current_time += self.distance_matrix[route[-1]][self.depot]
        route.append(self.depot)
        timing_info[vehicle].append((self.depot, current_time))
        routes[vehicle] = route

        print(f"[Vehicle {vehicle}] Returning to depot at time {current_time}.")

        return last_visit_times, location_locks, visit_counts

    def evaluate_solution(self, visit_counts):
        return sum(visit_counts.values())

    def run_simulation(self, last_visit_times, location_locks, is_detailed=False):
        routes, timing_info, location_visits, visit_counts = self.initialize_simulation()
        for vehicle in range(self.vehicles):
            print(f"--- Running simulation for vehicle {vehicle} ---")
            last_visit_times, location_locks, visit_counts = self.simulate_shift(vehicle, last_visit_times, location_locks, timing_info,
                                                                                routes, location_visits, visit_counts)

        current_score = self.evaluate_solution(visit_counts)

        if is_detailed:
            self.print_detailed_info(current_score, routes, timing_info)

        print(f"Simulation complete. Total visits: {current_score}")
        return current_score, routes, timing_info

    def print_detailed_info(self, total_visits, routes, timing_info):
        print(f"Total visits (including revisits): {total_visits}")
        for vehicle in range(self.vehicles):
            print(f"Vehicle {vehicle}:")
            route = routes[vehicle]
            print(f"  Route: {route}")
            print("  Timing:")
            for loc, time in timing_info[vehicle]:
                loc_name = f"Location {loc}" if loc != self.depot else "Depot"
                print(f"      {loc_name} at time {time} minutes")

    def write_results_to_file(self, filename, vehicles, locations, rest_time, average_visits, routes, timing_info):
        with open(filename, 'a') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"{vehicles} cars, {locations} locations, {rest_time} rest time => {average_visits} visits on average.\n")
            file.write("-----\n")
            file.write(f"Detailed travel logs:\n")
            for vehicle in range(vehicles):
                file.write(f"Vehicle {vehicle}:\n")
                route = routes[vehicle]
                file.write(f"  Route: {route}\n")
                file.write("  Timing:\n")
                for loc, time in timing_info[vehicle]:
                    loc_name = f"Location {loc}" if loc != self.depot else "Depot"
                    file.write(f"      {loc_name} at time {time} minutes\n")
                file.write("-----\n")
        print(f"Results written to file for {vehicles} vehicles and {locations}.")

    def main(self):
        valid_pairs = [
            (1, 4), (1, 10), (1, 20), (2, 4), (2, 10), (2, 20), (2, 30), (3,10), (3, 20), (3, 30), (3, 50), (3, 75), (3, 100), (4, 20), (4,30),
            (4, 50), (4, 75), (4, 100), (4, 125), (4, 150), (5, 50), (5, 75), (5, 100), (5, 125), (5, 150), (5, 175), (5, 200), (10, 100), (10, 150), (10, 200), (10, 250), (10, 300), 
            (10, 400), (15, 150), (15, 200), (15, 300), (15, 400), (15, 500), (20, 200), (20, 300), (20, 400), (20, 500), (20, 750), (25, 500), (25, 750), (25, 1000), 
            (30, 500), (30, 750), (30, 1000)
        ]

        for vehicles, locations in valid_pairs:
            print(f"Starting simulation for {vehicles} vehicles and {locations} locations.")
            hvsp = HVSP(vehicles=vehicles, total_locations=locations)
            results = []
            for _ in range(hvsp.iterations):
                result, routes, timing_info = hvsp.run_simulation(
                    {loc: float('-inf') for loc in range(1, locations + 1)},
                    {loc: None for loc in range(1, locations + 1)}
                )
                results.append(result)

            average_visits = sum(results) / len(results)
            hvsp.write_results_to_file('AHBPS_large_instances_results_automated.txt', vehicles, locations, hvsp.max_rest_time, average_visits, routes, timing_info)
            print(f"Finished simulation for {vehicles} vehicles and {locations} locations.")

# Run the main function
if __name__ == "__main__":
    hvsp = HVSP(vehicles=1, total_locations=4)
    hvsp.main()

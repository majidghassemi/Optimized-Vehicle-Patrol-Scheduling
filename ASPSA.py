import random
from datetime import datetime

class HVSP:
    def __init__(self, vehicles=1, total_locations=10, shifts=6, patrol_time=5, rest_period=10, shift_lengths=None, iterations=100):
        # Validate parameters
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
        timing_info[shift][vehicle].append((self.first_depot, current_time))
        
        travel_time_to_next = 0  # Initialize the variable

        while current_time + self.patrol_time <= end_time:
            # Select possible locations to visit
            possible_locations = [loc for loc in range(1, self.last_depot)
                                  if self.needs_revisiting(current_time, loc, last_visit_times, location_locks) and loc not in visited_this_shift]
            if not possible_locations:
                print(f"[Vehicle {vehicle}] No more valid locations to visit.")
                break

            closest_location = min(possible_locations, key=lambda loc: self.distance_matrix[route[-1]][loc])
            travel_time_to_next = self.distance_matrix[route[-1]][closest_location]
            stay_at_next = current_time + travel_time_to_next + self.patrol_time

            if stay_at_next + travel_time_to_next > self.shift_duration:
                print(f"[Vehicle {vehicle}] Not enough time to visit the next location. Ending shift.")
                break

            # Shuffle and select the next location to visit
            random.shuffle(possible_locations)
            for loc in possible_locations:
                travel_to_next = current_time + travel_time_to_next
                stay_at_next = travel_to_next + self.patrol_time
                if stay_at_next + travel_time_to_next <= end_time:
                    route.append(loc)
                    visited_this_shift.add(loc)
                    current_time = stay_at_next
                    timing_info[shift][vehicle].append((loc, current_time))
                    last_visit_times[loc] = current_time
                    location_locks[loc] = current_time + self.patrol_time
                    location_visits[loc].append((shift, vehicle, current_time))
                    break

        # Add return to depot if time allows
        if current_time + travel_time_to_next <= end_time:
            current_time += travel_time_to_next
        route.append(self.last_depot)
        timing_info[shift][vehicle].append((self.last_depot, current_time))
        routes[shift][vehicle] = route

        return last_visit_times, location_locks

    def evaluate_solution(self, location_visits):
        unique_visits = len({loc for loc, visits in location_visits.items() if visits})
        total_visits = sum(len(visits) for visits in location_visits.values())
        return unique_visits, total_visits

    def run_simulation(self, last_visit_times, location_locks, is_detailed=False):
        routes, timing_info, location_visits, shift_start_time, shift_end_time = self.initialize_simulation()

        # Initialize with a random solution
        for shift in range(self.shifts):
            for vehicle in range(self.vehicles):
                last_visit_times, location_locks = self.simulate_shift(shift, vehicle, last_visit_times, location_locks,
                                                                       shift_start_time, shift_end_time, timing_info,
                                                                       routes, location_visits)

        unique_locations_visited, total_visits = self.evaluate_solution(location_visits)

        if is_detailed:
            self.print_detailed_info(unique_locations_visited, total_visits, routes, timing_info)

        return unique_locations_visited, total_visits

    def print_detailed_info(self, unique_locations_visited, total_visits, routes, timing_info):
        print(f"Total distinct locations visited (excluding depots): {unique_locations_visited}")
        print(f"Total visits (including revisits): {total_visits}")
        for vehicle in range(self.vehicles):
            print(f"Vehicle {vehicle}:")
            route = routes[vehicle]
            print(f"  Route: {route}")
            print("  Timing:")
            for loc, time in timing_info[vehicle]:
                loc_name = f"Location {loc}" if loc != self.depot else "Depot"
                print(f"      {loc_name} at time {time} minutes")

    def write_results_to_file(self, filename, vehicles, shifts, locations, rest_time, average_unique, average_total):
        with open(filename, 'a') as file:  # Open in append mode
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"{vehicles} vehicles, {shifts} shifts, {locations} locations, {rest_time} rest time => "
                       f"Average Unique Locations Visited: {average_unique}, Average Total Visits: {average_total}.\n")
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
        # List of (vehicles, locations) pairs to test
        test_cases = [
            (5, 100), (5, 200), (5, 300), (8, 100), (8, 200), (8, 300), (8, 400), (8, 500), (10, 100), (10, 200), (10, 300), (10, 400), (10, 500), 
            (10, 750), (10, 1000), (12, 100), (12, 200), (12, 300), (12, 400), (12, 500), 
            (12, 750), (12, 1000), (15, 200),(15, 300),(15, 400), (15, 500), 
            (15, 750), (15, 1000), (20, 500), (20, 750), (20, 1000)
]

        for vehicles, locations in test_cases:
            self.vehicles = vehicles
            self.total_locations = locations
            self.last_depot = locations

            # Multiple simulation runs for statistics
            unique_results = []
            total_results = []
            for _ in range(self.iterations):
                last_visit_times = {loc: float('-inf') for loc in range(1, self.total_locations)}
                location_locks = {loc: None for loc in range(1, self.total_locations)}
                unique, total = self.run_simulation(last_visit_times, location_locks)
                unique_results.append(unique)
                total_results.append(total)

            # Compute and write results to file (appending)
            average_unique = sum(unique_results) / len(unique_results)
            average_total = sum(total_results) / len(total_results)
            self.write_results_to_file('results.txt', self.vehicles, self.shifts, self.total_locations, self.rest_period, average_unique, average_total)

        # Detailed simulation run for the final test case
        last_visit_times_detailed = {loc: float('-inf') for loc in range(1, self.total_locations)}
        location_locks_detailed = {loc: None for loc in range(1, self.total_locations)}

        unique_locations_visited, total_visits = self.run_simulation(last_visit_times_detailed, location_locks_detailed, is_detailed=True)

# Run the main function
if __name__ == "__main__":
    hvsp = HVSP(vehicles=1, total_locations=4)
    hvsp.main()

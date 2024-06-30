import random
import matplotlib.pyplot as plt

class HVSP:
    def __init__(self, vehicles=5, total_locations=100, shifts=4, patrol_time=5, rest_period=10, shift_lengths=None, iterations=100):
        # Validate parameters
        assert vehicles > 0, "Number of vehicles must be positive"
        assert total_locations > 1, "Number of locations must be greater than 1"
        assert shifts > 0, "Number of shifts must be positive"
        assert patrol_time > 0, "Patrol time must be positive"
        assert rest_period >= 0, "Rest period must be non-negative"
        
        self.vehicles = vehicles
        self.total_locations = total_locations
        self.first_depot = 0
        self.last_depot = total_locations
        self.shifts = shifts
        self.patrol_time = patrol_time
        self.rest_period = rest_period
        self.shift_lengths = shift_lengths if shift_lengths else [120] * shifts
        self.iterations = iterations

    def needs_revisiting(self, current_time, location, last_visit_times, location_locks):
        return (current_time - last_visit_times[location]) >= 30 and (location_locks[location] is None or location_locks[location] <= current_time)

    def initialize_simulation(self):
        # Initialize structures to store routes, timings, and visits
        routes = {shift: {vehicle: [] for vehicle in range(self.vehicles)} for shift in range(self.shifts)}
        timing_info = {shift: {vehicle: [] for vehicle in range(self.vehicles)} for shift in range(self.shifts)}
        location_visits = {loc: [] for loc in range(1, self.total_locations)}
        shift_start_time = {vehicle: [0] for vehicle in range(self.vehicles)}
        shift_end_time = {vehicle: [0] for vehicle in range(self.vehicles)}
        
        # Set the initial start and end times for the first shift
        for vehicle in range(self.vehicles):
            shift_start_time[vehicle][0] = 0
            shift_end_time[vehicle][0] = self.shift_lengths[0]
        
        return routes, timing_info, location_visits, shift_start_time, shift_end_time

    def simulate_shift(self, shift, vehicle, last_visit_times, location_locks, shift_start_time, shift_end_time, timing_info, routes, location_visits):
        # Update shift start and end times for shifts beyond the first
        if shift > 0:
            previous_end_time = timing_info[shift - 1][vehicle][-1][1]
            shift_start_time[vehicle].append(previous_end_time + self.rest_period)
            shift_end_time[vehicle].append(shift_start_time[vehicle][shift] + self.shift_lengths[shift])
        
        current_time = shift_start_time[vehicle][shift]
        end_time = shift_end_time[vehicle][shift]

        route = [self.first_depot]
        visited_this_shift = set()
        timing_info[shift][vehicle].append((self.first_depot, current_time))
        
        while current_time + self.patrol_time <= end_time:
            # Select possible locations to visit
            possible_locations = [loc for loc in range(1, self.last_depot)
                                  if self.needs_revisiting(current_time, loc, last_visit_times, location_locks) and loc not in visited_this_shift]
            if not possible_locations:
                break

            travel_time_to_next = random.randint(10, 20)
            next_possible_time = current_time + travel_time_to_next + self.patrol_time

            if next_possible_time + travel_time_to_next > end_time:
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
        return len({loc for loc, visits in location_visits.items() if visits})

    def get_neighbors(self, solution):
        # Generate neighbors by slightly modifying the current solution
        neighbors = []
        for shift in range(self.shifts):
            for vehicle in range(self.vehicles):
                for i in range(1, len(solution[shift][vehicle]) - 1):
                    for j in range(i + 1, len(solution[shift][vehicle]) - 1):
                        neighbor = {s: {v: list(solution[s][v]) for v in solution[s]} for s in solution}
                        neighbor[shift][vehicle][i], neighbor[shift][vehicle][j] = neighbor[shift][vehicle][j], neighbor[shift][vehicle][i]
                        neighbors.append(neighbor)
        return neighbors

    def run_simulation(self, last_visit_times, location_locks, is_detailed=False):
        routes, timing_info, location_visits, shift_start_time, shift_end_time = self.initialize_simulation()

        # Initialize with a random solution
        for shift in range(self.shifts):
            for vehicle in range(self.vehicles):
                last_visit_times, location_locks = self.simulate_shift(shift, vehicle, last_visit_times, location_locks,
                                                                       shift_start_time, shift_end_time, timing_info,
                                                                       routes, location_visits)

        current_solution = routes
        current_score = self.evaluate_solution(location_visits)

        # Hill climbing process
        while True:
            neighbors = self.get_neighbors(current_solution)
            best_neighbor = None
            best_score = current_score

            for neighbor in neighbors:
                neighbor_score = self.evaluate_solution(location_visits)
                if neighbor_score > best_score:
                    best_neighbor = neighbor
                    best_score = neighbor_score

            if best_score <= current_score:
                break

            current_solution = best_neighbor
            current_score = best_score

        total_unique_locations_visited = current_score

        if is_detailed:
            self.print_detailed_info(total_unique_locations_visited, current_solution, timing_info)

        return total_unique_locations_visited

    def print_detailed_info(self, total_unique_locations_visited, routes, timing_info):
        print(f"Total distinct locations visited (excluding depots): {total_unique_locations_visited}")
        for vehicle in range(self.vehicles):
            print(f"Vehicle {vehicle}:")
            for shift in range(self.shifts):
                route = routes[shift][vehicle]
                print(f"  Shift {shift}:")
                print(f"    Route: {route}")
                print("    Timing:")
                for loc, time in timing_info[shift][vehicle]:
                    loc_name = f"Location {loc}" if loc != self.first_depot and loc != self.last_depot else f"Depot {loc}"
                    print(f"      {loc_name} at time {time} minutes")

    def main(self):
        # Initialize detailed simulation state
        last_visit_times_detailed = {loc: float('-inf') for loc in range(1, self.total_locations)}
        location_locks_detailed = {loc: None for loc in range(1, self.total_locations)}

        # Detailed simulation run
        self.run_simulation(last_visit_times_detailed, location_locks_detailed, is_detailed=True)

        # Multiple simulation runs for plotting
        results = []
        for _ in range(self.iterations):
            last_visit_times = {loc: float('-inf') for loc in range(1, self.total_locations)}
            location_locks = {loc: None for loc in range(1, self.total_locations)}
            results.append(self.run_simulation(last_visit_times, location_locks))

        # Compute the best and mean results
        best_results = []
        current_best = 0
        mean_results = []
        cumulative_sum = 0

        for i, result in enumerate(results):
            if result > current_best:
                current_best = result
            best_results.append(current_best)
            cumulative_sum += result
            mean_results.append(cumulative_sum / (i + 1))

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, self.iterations + 1), results, linestyle='-', color='b', label='Distinct Locations Visited')
        plt.plot(range(1, self.iterations + 1), best_results, linestyle='--', color='g', label='Best So Far')
        plt.plot(range(1, self.iterations + 1), mean_results, linestyle=':', color='r', label='Mean')
        plt.title('Distinct Locations Visited per Iteration')
        plt.xlabel('Iteration')
        plt.ylabel('Distinct Locations Visited')
        plt.grid(True)
        plt.legend()
        plt.show()

# Run the main function
if __name__ == "__main__":
    hvsp = HVSP()
    hvsp.main()

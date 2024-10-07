import random
import numpy as np
from datetime import datetime
import time

class HVSP:
    def __init__(self, vehicles=1, total_locations=10, shifts=6, patrol_time=5, rest_period=10, shift_lengths=None, iterations=1):
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

        self.base_travel_times = self.generate_travel_times()

        self.travel_times = self.base_travel_times.copy()

    def generate_travel_times(self):
        travel_times = {}
        for i in range(self.total_locations):
            for j in range(i + 1, self.total_locations):
                time = np.random.normal(loc=15, scale=2.5)
                time = max(10, min(20, time)) 
                travel_times[(i, j)] = time
                travel_times[(j, i)] = time
        return travel_times

    def fluctuate_travel_times(self):
        for (i, j) in self.base_travel_times:
            fluctuation = random.choice([-2, 2])
            self.travel_times[(i, j)] = self.base_travel_times[(i, j)] + fluctuation
            self.travel_times[(j, i)] = self.travel_times[(i, j)]  # Keep symmetry

    def needs_revisiting(self, current_time, location, last_visit_times, location_locks):
        return (current_time - last_visit_times[location]) >= 30 and (location_locks[location] is None or location_locks[location] <= current_time)

    def initialize_simulation(self):
        routes = {shift: {vehicle: [] for vehicle in range(self.vehicles)} for shift in range(self.shifts)}
        timing_info = {shift: {vehicle: [] for vehicle in range(self.vehicles)} for shift in range(self.shifts)}
        location_visits = {loc: [] for loc in range(1, self.total_locations)}
        shift_start_time = {vehicle: [0] for vehicle in range(self.vehicles)}
        shift_end_time = {vehicle: [0] for vehicle in range(self.vehicles)}
        
        for vehicle in range(self.vehicles):
            shift_start_time[vehicle][0] = 0
            shift_end_time[vehicle][0] = self.shift_lengths[0]
        
        return routes, timing_info, location_visits, shift_start_time, shift_end_time

    def simulate_shift(self, shift, vehicle, last_visit_times, location_locks, shift_start_time, shift_end_time, timing_info, routes, location_visits):
        if shift > 0:
            previous_end_time = timing_info[shift - 1][vehicle][-1][1]
            shift_start_time[vehicle].append(previous_end_time + self.rest_period)
            shift_end_time[vehicle].append(shift_start_time[vehicle][shift] + self.shift_lengths[shift])
        
        current_time = shift_start_time[vehicle][shift]
        end_time = shift_end_time[vehicle][shift]

        route = [self.first_depot]
        visited_this_shift = set()
        timing_info[shift][vehicle].append((self.first_depot, current_time))
        
        travel_time_to_next = 0

        while current_time + self.patrol_time <= end_time:
            possible_locations = [loc for loc in range(1, self.last_depot)
                                  if self.needs_revisiting(current_time, loc, last_visit_times, location_locks) and loc not in visited_this_shift]
            if not possible_locations:
                break

            next_location = min(possible_locations, key=lambda loc: self.travel_times[(self.first_depot, loc)])

            travel_time_to_next = self.travel_times[(self.first_depot, next_location)]
            next_possible_time = current_time + travel_time_to_next + self.patrol_time

            if next_possible_time + travel_time_to_next > end_time:
                break

            route.append(next_location)
            visited_this_shift.add(next_location)
            current_time = next_possible_time
            timing_info[shift][vehicle].append((next_location, current_time))
            last_visit_times[next_location] = current_time
            location_locks[next_location] = current_time + self.patrol_time
            location_visits[next_location].append((shift, vehicle, current_time))

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

        if random.random() < 0.25:
            print("Fluctuating travel times for this run.")
            self.fluctuate_travel_times()
        else:
            print("Keeping travel times constant for this run.")
            self.travel_times = self.base_travel_times.copy()

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
            for shift in range(self.shifts):
                route = routes[shift][vehicle]
                print(f"  Shift {shift}:")
                print(f"    Route: {route}")
                print("    Timing:")
                for loc, time in timing_info[shift][vehicle]:
                    loc_name = f"Location {loc}" if loc != self.first_depot and loc != self.last_depot else f"Depot {loc}"
                    print(f"      {loc_name} at time {time} minutes")

    def write_results_to_file(self, filename, vehicles, shifts, locations, rest_time, average_unique, average_total, execution_time=None):
        with open(filename, 'a') as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"{vehicles} vehicles, {shifts} shifts, {locations} locations, {rest_time} rest time => "
                       f"Average Unique Locations Visited: {average_unique}, Average Total Visits: {average_total}.\n")
            if execution_time is not None:
                file.write(f"Execution Time: {execution_time:.2f} seconds\n")
            file.write("-----\n")

    def main(self):
        test_cases = [
            # The used test cases in the paper
        ]

        for vehicles, locations in test_cases:
            self.vehicles = vehicles
            self.total_locations = locations
            self.last_depot = locations

            start_time = time.time()

            unique_results = []
            total_results = []
            for _ in range(self.iterations):
                last_visit_times = {loc: float('-inf') for loc in range(1, self.total_locations)}
                location_locks = {loc: None for loc in range(1, self.total_locations)}
                unique, total = self.run_simulation(last_visit_times, location_locks)
                unique_results.append(unique)
                total_results.append(total)

            average_unique = sum(unique_results) / len(unique_results)
            average_total = sum(total_results) / len(total_results)

            end_time = time.time()
            execution_time = end_time - start_time

            self.write_results_to_file('AHBPS_Run_Time_Large_Instance_Nodes_Changes.txt', self.vehicles, self.shifts, self.total_locations, self.rest_period, average_unique, average_total, execution_time)

        last_visit_times_detailed = {loc: float('-inf') for loc in range(1, self.total_locations)}
        location_locks_detailed = {loc: None for loc in range(1, self.total_locations)}

        unique_locations_visited, total_visits = self.run_simulation(last_visit_times_detailed, location_locks_detailed, is_detailed=True)

if __name__ == "__main__":
    hvsp = HVSP()
    hvsp.main()

import pandas as pd
import matplotlib.pyplot as plt

gdvps_file = './large_instances/GDVPS_large.txt'
ahbps_file = './large_instances/AHBPS_large.txt'

gdvps_data = []
with open(gdvps_file, 'r') as file:
    for line in file:
        if "Best fitness" in line:
            parts = line.strip().split(' => ')
            conditions = parts[0]
            best_fitness = float(parts[1].split(',')[0].split(': ')[1])
            gdvps_data.append([conditions, best_fitness])

ahbps_data = []
with open(ahbps_file, 'r') as file:
    for line in file:
        if "Average Unique Locations Visited" in line:
            parts = line.strip().split(' => ')
            conditions = parts[0]
            unique_locations = float(parts[1].split(',')[0].split(': ')[1])
            ahbps_data.append([conditions, unique_locations])

gdvps_df = pd.DataFrame(gdvps_data, columns=['Conditions', 'Best Fitness'])
ahbps_df = pd.DataFrame(ahbps_data, columns=['Conditions', 'Average Unique Locations Visited'])

merged_df = pd.merge(gdvps_df, ahbps_df, on='Conditions')

# Plotting the data
plt.figure(figsize=(12, 8))
plt.plot(merged_df['Conditions'], merged_df['Best Fitness'], marker='o', label='GDVPS - Best Fitness')
plt.plot(merged_df['Conditions'], merged_df['Average Unique Locations Visited'], marker='s', label='AHBPS - Avg. Unique Locations Visited')
plt.xlabel('Conditions (Vehicles, Shifts, Locations)')
plt.ylabel('Value')
plt.title('Comparison of Best Fitness and Average Unique Locations Visited')
plt.xticks(rotation=90)
plt.legend()
plt.grid(True)
plt.tight_layout()

plot_file = '/comparison_plot.png'
plt.savefig(plot_file)
plt.show()

plot_file

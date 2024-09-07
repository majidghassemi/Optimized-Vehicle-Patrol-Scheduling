import matplotlib.pyplot as plt
import numpy as np

# Updated scenarios to include vehicles and locations
scenarios = [
    '10 V, 500 L', '10 V, 750 L', '10 V, 1000 L',
    '12 V, 500 L', '12 V, 750 L', '12 V, 1000 L',
    '15 V, 500 L', '15 V, 750 L', '15 V, 1000 L',
    '20 V, 500 L', '20 V, 750 L', '20 V, 1000 L',
]

# AHBPS (Average Unique Locations Visited)
ahbps_values = [0.07, 0.11, 0.15, 0.09, 0.14, 0.18, 0.11, 0.17, 0.23, 0.14, 0.22, 0.30]

# GDVPS (Average fitness)
gdvps_values = [33.66, 38.46, 107.31, 40.33, 46.03, 127.98, 62.43, 83.95, 119.92, 83.89, 70.19, 134.18]

# Group GDVPS values by the number of vehicles
vehicle_groups = {
    '10 V': gdvps_values[:3],
    '12 V': gdvps_values[3:6],
    '15 V': gdvps_values[6:9],
    '20 V': gdvps_values[9:]
}

# Calculate the average GDVPS runtime for each vehicle group
gdvps_averages = {vehicles: np.mean(times) for vehicles, times in vehicle_groups.items()}

# X-axis positions for vehicle groups (just indexes for the line plot)
x_positions = [1.5, 4.5, 7.5, 10.5]  # Middle of each vehicle group

# Extract the average values in the same order as x_positions
avg_gdvps_values = [gdvps_averages['10 V'], gdvps_averages['12 V'], gdvps_averages['15 V'], gdvps_averages['20 V']]

# Creating the plot
fig, ax = plt.subplots()

# Plotting all points together for GDVPS (black with dashes)
ax.plot(np.arange(len(scenarios)), gdvps_values, color='black', linestyle='--', marker='s', linewidth=2, label='GDVPS')

# Plotting all points together for AHBPS (Dark Yellow)
ax.plot(np.arange(len(scenarios)), ahbps_values, color='#FFD700', linestyle=':', marker='^', linewidth=2, label='AHBPS')

# Plot a line connecting the average GDVPS values for each vehicle group
ax.plot(x_positions, avg_gdvps_values, color='purple', linestyle='-', marker='o', linewidth=2, label='GDVPS Averages')

# Set the tick labels for the x-axis
ax.set_xticks(np.arange(len(scenarios)))
ax.set_xticklabels(scenarios, rotation=45, ha="right", fontsize=12)

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=14)
ax.set_ylabel('Execution Time (seconds)', fontsize=14)
ax.set_title('Execution Time Comparison between AHBPS and GDVPS', fontsize=14)

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=17)

# Add the legend
ax.legend(fontsize=12)

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('execution_time_comparison_ahbps_gdvps_with_group_avg_runtime_line.png', dpi=600)

# Show the plot
plt.show()

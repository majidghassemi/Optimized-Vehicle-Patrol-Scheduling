import matplotlib.pyplot as plt
import numpy as np

# Updated scenarios to include vehicles and locations
scenarios = [
    '1 V, 5 L', '1 V, 10 L', '1 V, 15 L',
    '2 V, 5 L', '2 V, 10 L', '2 V, 15 L',
    '3 V, 5 L', '3 V, 10 L', '3 V, 15 L',
    '4 V, 5 L', '4 V, 10 L', '4 V, 15 L',
]

# AHBPS (Average Unique Locations Visited)
ahbps_values = [4.0, 8.0, 13.0, 4.5, 9.0, 14.0, 5.0, 9.5, 14.8, 5.5, 9.75, 15.25]

# GDVPS (Average fitness)
gdvps_values = [6.0, 11.0, 15.0, 6.5, 11.5, 16.0, 7, 12, 17.0, 7.25, 12.5, 18]

# OPL (Optimal) values
opl_values = [7.0, 12.0, 17.0, 7.5, 13.0, 19.0, 8.0, 13.75, 19.99, 9.0, 15.0, 21.0]

# X-axis positions (just indexes for the line plot)
x = np.arange(len(scenarios))

# Creating the plot
fig, ax = plt.subplots()

# Grouping by the number of vehicles
vehicle_groups = [x[:3], x[3:6], x[6:9], x[9:]]  # Grouped by '1 V', '2 V', '3 V', '4 V'

# Plotting lines for each vehicle group without adding labels multiple times
# OPL line
for group in vehicle_groups:
    ax.plot(group, [opl_values[i] for i in group], color='limegreen', linestyle='-', marker='o', linewidth=2)

# GDVPS line
for group in vehicle_groups:
    ax.plot(group, [gdvps_values[i] for i in group], color='black', linestyle='--', marker='s', linewidth=2)

# AHBPS line (Dark Yellow)
for group in vehicle_groups:
    ax.plot(group, [ahbps_values[i] for i in group], color='#FFD700', linestyle=':', marker='^', linewidth=2)

# Finding the maximum values for each vehicle group
top_achieved_values_opl = [
    max([opl_values[i]]) for i in [2, 5, 8, 11]
]  # Index 2, 5, 8, 11 correspond to '15 locations' for each vehicle group (1V, 2V, 3V, 4V)
top_achieved_values_ahbps = [
    max([ahbps_values[i]]) for i in [2, 5, 8, 11]
]  
top_achieved_values_gdvps = [
    max([gdvps_values[i]]) for i in [2, 5, 8, 11]
]  

# Corresponding x positions for these top results
top_x_positions = [2, 5, 8, 11]  # Corresponding to '1 V, 15 L', '2 V, 15 L', '3 V, 15 L', '4 V, 15 L'

# Plotting the line connecting top results
ax.plot(top_x_positions, top_achieved_values_opl, color='purple', linestyle='-', marker='*', linewidth=2, label='OPL Top Achieved')
ax.plot(top_x_positions, top_achieved_values_gdvps, color='red', linestyle='-', marker='^', linewidth=2, label='GDVPS Top Achieved')
ax.plot(top_x_positions, top_achieved_values_ahbps, color='cyan', linestyle='-', marker='+', linewidth=2, label='AHBPS Top Achieved')
# ax.plot(top_x_positions, top_achieved_values, color='purple', linestyle='-', marker='*', linewidth=2)

# Add a single label for each plot in the legend
ax.plot([], [], color='limegreen', linestyle='-', marker='o', label='OPL', linewidth=2)
ax.plot([], [], color='black', linestyle='--', marker='s', label='GDVPS', linewidth=2)
ax.plot([], [], color='#FFD700', linestyle=':', marker='^', label='AHBPS', linewidth=2)

# Set the tick labels for the x-axis
ax.set_xticks(x)
ax.set_xticklabels(scenarios, rotation=45, ha="right", fontsize=16)

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=15)
ax.set_ylabel('Visited Locations', fontsize=15)
ax.set_title('Performance Comparison (OPL, AHBPS, GDVPS)', fontsize=15)

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=18)

# Add the legend with only OPL, GDVPS, AHBPS, and Top Achieved Results
ax.legend(fontsize=8, loc='best')

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('comparison_opl_ahbps_gdvps_top_results.png', dpi=300)

# Show the plot
plt.show()

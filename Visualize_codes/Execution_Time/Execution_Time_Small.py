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
ahbps_values = [0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001]

# GDVPS (Average fitness)
gdvps_values = [0.15, 0.16, 0.16, 0.30, 0.31, 0.31, 0.70 , 0.54, 0.55, 0.79, 0.71, 0.65]

# OPL (Optimal) values
opl_values = [250, 850, 2100, 265, 960, 2680, 305, 1000, 3719, 450, 1279, 4200]

# X-axis positions (just indexes for the line plot)
x = np.arange(len(scenarios))

# Creating the plot
fig, ax = plt.subplots()

# Grouping by the number of vehicles
vehicle_groups = [x[:3], x[3:6], x[6:9], x[9:]]  # Grouped by '1 V', '2 V', '3 V', '4 V'

# Plot OPL (limegreen with solid line), only connecting within each vehicle group
for i, group in enumerate(vehicle_groups):
    ax.plot(group, [opl_values[j] for j in group], color='limegreen', linestyle='-', marker='o', linewidth=2, label='OPL' if i == 0 else "")

# Plot GDVPS (black with dashed line), only connecting within each vehicle group
for i, group in enumerate(vehicle_groups):
    ax.plot(group, [gdvps_values[j] for j in group], color='black', linestyle='--', marker='s', linewidth=2, label='GDVPS' if i == 0 else "")

# Plot AHBPS (dark yellow with dotted line), only connecting within each vehicle group
for i, group in enumerate(vehicle_groups):
    ax.plot(group, [ahbps_values[j] for j in group], color='#FFD700', linestyle=':', marker='^', linewidth=2, label='AHBPS' if i == 0 else "")

# Find the top result in each group (max value from OPL, GDVPS, AHBPS)
top_values = []
top_x_positions = []

for group in vehicle_groups:
    max_value = max([opl_values[j] for j in group] + [gdvps_values[j] for j in group] + [ahbps_values[j] for j in group])
    top_values.append(max_value)
    top_x_positions.append(group[np.argmax([opl_values[j] for j in group] + [gdvps_values[j] for j in group] + [ahbps_values[j] for j in group])])

# Plot a purple line connecting the top results
# ax.plot(top_x_positions, top_values, color='purple', linestyle='-', marker='*', linewidth=2, label='Top Results')
ax.plot(top_x_positions, top_values, color='purple', linestyle='-', marker='*', linewidth=2)

# Set the tick labels for the x-axis
ax.set_xticks(x)
ax.set_xticklabels(scenarios, rotation=45, ha="right", fontsize=16)

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=15)
ax.set_ylabel('Execution Time (seconds)', fontsize=15)
ax.set_title('Execution Time Comparison (OPL, AHBPS, GDVPS)', fontsize=15)

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=18)

# Add the legend
ax.legend(fontsize=10, loc='best')

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('execution_time_comparison_opl_ahbps_gdvps_top_results.png', dpi=600)

# Show the plot
plt.show()

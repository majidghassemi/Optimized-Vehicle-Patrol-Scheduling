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
ahbps_values = [4.0, 8.0, 13.0, 4.0, 9.0, 14.0, 5.0, 9.0, 14.0, 5.0, 9.0, 14.0]

# GDVPS (Average fitness)
gdvps_values = [6.0, 11.0, 15.0, 6.0, 11.0, 16.0, 6.0, 10.0, 16.0, 6.0, 11.0, 17.0]

# OPL (Optimal) values
opl_values = [7.0, 12.0, 17.0, 8.0, 13.0, 19.0, 9.0, 13.0, 17.0, 10.0, 15.0, 21.0]

# Find the maximum value across all sets
max_value = max(max(ahbps_values), max(gdvps_values), max(opl_values))

# Normalize the values between 0 and 100
ahbps_values_normalized = [(val / max_value) * 100 for val in ahbps_values]
gdvps_values_normalized = [(val / max_value) * 100 for val in gdvps_values]
opl_values_normalized = [(val / max_value) * 100 for val in opl_values]

# X-axis positions
x = np.arange(len(scenarios))

# Creating the plot
fig, ax = plt.subplots()

# Plot each vehicle group separately without connecting the instances
# Group 1V
ax.plot(x[0:3], opl_values_normalized[0:3], color='limegreen', marker='o', linestyle='-', linewidth=2, label="OPL")
ax.plot(x[0:3], gdvps_values_normalized[0:3], color='black', marker='s', linestyle='--', linewidth=2, label="GDVPS")
ax.plot(x[0:3], ahbps_values_normalized[0:3], color='#FFD700', marker='^', linestyle=':', linewidth=2, label="AHBPS")

# Group 2V
ax.plot(x[3:6], opl_values_normalized[3:6], color='limegreen', marker='o', linestyle='-', linewidth=2)
ax.plot(x[3:6], gdvps_values_normalized[3:6], color='black', marker='s', linestyle='--', linewidth=2)
ax.plot(x[3:6], ahbps_values_normalized[3:6], color='#FFD700', marker='^', linestyle=':', linewidth=2)

# Group 3V
ax.plot(x[6:9], opl_values_normalized[6:9], color='limegreen', marker='o', linestyle='-', linewidth=2)
ax.plot(x[6:9], gdvps_values_normalized[6:9], color='black', marker='s', linestyle='--', linewidth=2)
ax.plot(x[6:9], ahbps_values_normalized[6:9], color='#FFD700', marker='^', linestyle=':', linewidth=2)

# Group 4V
ax.plot(x[9:12], opl_values_normalized[9:12], color='limegreen', marker='o', linestyle='-', linewidth=2)
ax.plot(x[9:12], gdvps_values_normalized[9:12], color='black', marker='s', linestyle='--', linewidth=2)
ax.plot(x[9:12], ahbps_values_normalized[9:12], color='#FFD700', marker='^', linestyle=':', linewidth=2)

# Finding the maximum normalized values for each vehicle group
top_achieved_values_normalized = [
    max([opl_values_normalized[i], gdvps_values_normalized[i], ahbps_values_normalized[i]]) 
    for i in [2, 5, 8, 11]  # Index 2, 5, 8, 11 correspond to '15 locations' for each vehicle group (1V, 2V, 3V, 4V)
]

# Corresponding x positions for these top results
top_x_positions = [x[2], x[5], x[8], x[11]]  # Corresponding to '1 V, 15 L', '2 V, 15 L', '3 V, 15 L', '4 V, 15 L'

# Plotting the line connecting top results
# ax.plot(top_x_positions, top_achieved_values_normalized, color='purple', linestyle='-', marker='*', linewidth=2, label='Top Achieved')
ax.plot(top_x_positions, top_achieved_values_normalized, color='purple', linestyle='-', marker='*', linewidth=2)

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=14)
ax.set_ylabel('Visited Locations (Normalized)', fontsize=14)
ax.set_title('Performance Comparison between OPL, AHBPS, and GDVPS', fontsize=13)

# Set the tick labels for the x-axis with increased font size
ax.set_xticks(x)
ax.set_xticklabels(scenarios, rotation=45, ha="right", fontsize=16)

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=16)

# Increase the font size of the legend
ax.legend(fontsize=12)

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('comparison_opl_ahbps_gdvps_with_top_line_normalized.png', dpi=600)

# Show the plot
plt.show()

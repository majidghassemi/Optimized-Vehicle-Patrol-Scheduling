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
opl_values = [7.0, 12.0, 17.0, 7.0, 13.0, 19.0, 8.0, 13.0, 17.0, 9.0, 15.0, 21.0]

# X-axis positions
x = np.arange(len(scenarios)) * 1.5

# Bar width
bar_width = 0.35  # Slightly smaller to fit three bars side by side

# Creating the plot
fig, ax = plt.subplots()

# Bar for OPL (summer green with horizontal hatch) on the far left
bars_opl = ax.bar(x - bar_width, opl_values, bar_width, label='OPL', color='limegreen', 
                  hatch='-', edgecolor='darkgreen')

# Bar for GDVPS (black with stripes) in the middle
bars_gdvps = ax.bar(x, gdvps_values, bar_width, label='GDVPS', color='white', 
                    hatch='//', edgecolor='black')

# Bar for AHBPS (pale yellow with dots) on the right
bars_ahbps = ax.bar(x + bar_width, ahbps_values, bar_width, label='AHBPS', color='#FFFF99', 
                    hatch='.', edgecolor='red')

# Finding the maximum values for each vehicle group
top_achieved_values = [
    max([opl_values[i], gdvps_values[i], ahbps_values[i]]) for i in [2, 5, 8, 11]
]  # Index 2, 5, 8, 11 correspond to '15 locations' for each vehicle group (1V, 2V, 3V, 4V)

# Corresponding x positions for these top results (use mid-bar positions for each group)
top_x_positions = [x[2], x[5], x[8], x[11]]  # Corresponding to '1 V, 15 L', '2 V, 15 L', '3 V, 15 L', '4 V, 15 L'

# Plotting the line connecting top results
# ax.plot(top_x_positions, top_achieved_values, color='red', linestyle='-', marker='*', linewidth=2, label='Top Achieved')
ax.plot(top_x_positions, top_achieved_values, color='red', linestyle='-', marker='*', linewidth=2)

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=14)
ax.set_ylabel('Visited Locations', fontsize=14)
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
plt.savefig('comparison_opl_ahbps_gdvps_with_top_line.png', dpi=600)

# Show the plot
plt.show()

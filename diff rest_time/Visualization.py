import matplotlib.pyplot as plt
import numpy as np

# Updated scenarios to include vehicles and locations (12 scenarios)
scenarios = ['5 Mins', '10 Mins', '15 Mins']

# AHBPS (Average Unique Locations Visited)
ahbps_values = [254.71, 205.01, 168.23]

# GDVPS (Average fitness)
gdvps_values = [298, 236.715, 188.537]

# Find the maximum value from both lists
max_value = max(max(ahbps_values), max(gdvps_values))

# Normalize the values between 0 and 100
ahbps_values_normalized = [(val / max_value) * 100 for val in ahbps_values]
gdvps_values_normalized = [(val / max_value) * 100 for val in gdvps_values]

# X-axis positions
x = np.arange(len(scenarios)) * 1.5

# Bar width
bar_width = 0.55

# Creating the plot
fig, ax = plt.subplots()

# Bar for GDVPS (black with stripes) on the left
bars_gdvps = ax.bar(x - bar_width/2, gdvps_values_normalized, bar_width, label='GDVPS', color='white', 
                    hatch='//', edgecolor='black')

# Bar for AHBPS (pale yellow with dots) on the right
bars_ahbps = ax.bar(x + bar_width/2, ahbps_values_normalized, bar_width, label='AHBPS', color='#FFFF99', 
                    hatch='.', edgecolor='red')

# Find the best (highest) normalized bar between AHBPS and GDVPS for each scenario
best_values_normalized = [max(ahbps_values_normalized[i], gdvps_values_normalized[i]) for i in range(len(scenarios))]
best_x_positions = [(x[i] - bar_width/2 + x[i] + bar_width/2)/2.0355 for i in range(len(scenarios))]

# Plot the line connecting the best normalized bars
ax.plot(best_x_positions, best_values_normalized, color='purple', linestyle='-', marker='*', linewidth=2)

# Labels and title with increased font size
ax.set_xlabel('Rest Time (10 V, 1000 L)', fontsize=14)
ax.set_ylabel('Visited Locations (Normalized)', fontsize=14)
ax.set_title('Performance Comparison by varying Rest Time', fontsize=13)

# Set the tick labels for the x-axis with decreased font size
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=13)

# Get the tick labels and set the one for "15 V, 1000 L" to bold
xtick_labels = ax.get_xticklabels()
for label in xtick_labels:
    if label.get_text() == '15 V, 1000 L':
        label.set_fontweight('bold')

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=17)

# Move the legend to the left of the figure
ax.legend(fontsize=12, loc='center left', bbox_to_anchor=(0.75, 0.9))

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('comparison_ahbps_gdvps_with_best_line_diff_rest_v2.png', dpi=600)

# Show the plot
plt.show()

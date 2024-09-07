import matplotlib.pyplot as plt
import numpy as np

# Updated scenarios to include vehicles and locations (12 scenarios)
scenarios = [
    '10 V, 500 L', '10 V, 750 L', '10 V, 1000 L',
    '12 V, 500 L', '12 V, 750 L', '12 V, 1000 L',
    '15 V, 500 L', '15 V, 750 L', '15 V, 1000 L',
    '20 V, 500 L', '20 V, 750 L', '20 V, 1000 L',
]

# AHBPS (Average Unique Locations Visited)
ahbps_values = [
    226,  # 10 V, 500 L
    245,  # 10 V, 750 L
    255,  # 10 V, 1000 L
    259,  # 12 V, 500 L
    285,  # 12 V, 750 L
    298,  # 12 V, 1000 L
    302,  # 15 V, 500 L
    338,  # 15 V, 750 L
    359,  # 15 V, 1000 L
    360,  # 20 V, 500 L
    418,  # 20 V, 750 L
    453   # 20 V, 1000 L
]

# GDVPS (Average fitness)
gdvps_values = [
    273,  # 10 V, 500 L
    288,  # 10 V, 750 L
    298,  # 10 V, 1000 L
    310,  # 12 V, 500 L
    334,  # 12 V, 750 L
    349,  # 12 V, 1000 L
    349,  # 15 V, 500 L
    564,  # 15 V, 750 L
    953,  # 15 V, 1000 L
    426,  # 20 V, 500 L
    712,  # 20 V, 750 L
    785   # 20 V, 1000 L
]

# X-axis positions
x = np.arange(len(scenarios)) * 1.5

# Bar width
bar_width = 0.55  # Slightly smaller to fit two bars side by side

# Creating the plot
fig, ax = plt.subplots()

# Bar for GDVPS (black with stripes) on the left
bars_gdvps = ax.bar(x - bar_width/2, gdvps_values, bar_width, label='GDVPS', color='white', 
                    hatch='//', edgecolor='black')

# Bar for AHBPS (pale yellow with dots) on the right
bars_ahbps = ax.bar(x + bar_width/2, ahbps_values, bar_width, label='AHBPS', color='#FFFF99', 
                    hatch='.', edgecolor='red')

# Find the best (highest) bar between AHBPS and GDVPS for each scenario
best_values = [max(ahbps_values[i], gdvps_values[i]) for i in range(len(scenarios))]
best_x_positions = [(x[i] - bar_width/2 + x[i] + bar_width/2)/2.0355 for i in range(len(scenarios))]  # Center of the bars

# Plot the line connecting the best bars
# ax.plot(best_x_positions, best_values, color='purple', linestyle='-', marker='*', linewidth=2, label='Best Values')
ax.plot(best_x_positions, best_values, color='purple', linestyle='-', marker='*', linewidth=2,)

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=14)
ax.set_ylabel('Visited Locations', fontsize=14)
ax.set_title('Performance Comparison between AHBPS and GDVPS', fontsize=13)

# Set the tick labels for the x-axis with decreased font size
ax.set_xticks(x)
ax.set_xticklabels(scenarios, rotation=45, ha="right", fontsize=13)

# Get the tick labels and set the one for "15 V, 1000 L" to bold
xtick_labels = ax.get_xticklabels()
for label in xtick_labels:
    if label.get_text() == '15 V, 1000 L':
        label.set_fontweight('bold')

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=17)

# Increase the font size of the legend
ax.legend(fontsize=12)

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('comparison_ahbps_gdvps_with_best_line.png', dpi=600)

# Show the plot
plt.show()

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
    365,  # 15 V, 500 L
    564,  # 15 V, 750 L
    602,  # 15 V, 1000 L
    426,  # 20 V, 500 L
    595,  # 20 V, 750 L
    701   # 20 V, 1000 L
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

# Plot lines connecting the best results for each vehicle group
# 10 V: Connecting the best results for '10 V, 500 L', '10 V, 750 L', '10 V, 1000 L'
best_10v = [max(ahbps_values[i], gdvps_values[i]) for i in range(3)]
ax.plot(x[0:3], best_10v, color='purple', linestyle='-', marker='*', linewidth=2, label='10 V Best')

# 12 V: Connecting the best results for '12 V, 500 L', '12 V, 750 L', '12 V, 1000 L'
best_12v = [max(ahbps_values[i], gdvps_values[i]) for i in range(3, 6)]
ax.plot(x[3:6], best_12v, color='orange', linestyle='-', marker='*', linewidth=2, label='12 V Best')

# 15 V: Connecting the best results for '15 V, 500 L', '15 V, 750 L', '15 V, 1000 L'
best_15v = [max(ahbps_values[i], gdvps_values[i]) for i in range(6, 9)]
ax.plot(x[6:9], best_15v, color='green', linestyle='-', marker='*', linewidth=2, label='15 V Best')

# 20 V: Connecting the best results for '20 V, 500 L', '20 V, 750 L', '20 V, 1000 L'
best_20v = [max(ahbps_values[i], gdvps_values[i]) for i in range(9, 12)]
ax.plot(x[9:12], best_20v, color='blue', linestyle='-', marker='*', linewidth=2, label='20 V Best')

# Labels and title with increased font size
ax.set_xlabel('Different Scenarios', fontsize=14)
ax.set_ylabel('Visited Locations', fontsize=14)
ax.set_title('Performance Comparison between AHBPS and GDVPS', fontsize=13)

# Set the tick labels for the x-axis with decreased font size
ax.set_xticks(x)
ax.set_xticklabels(scenarios, rotation=45, ha="right", fontsize=13)

# Increase the font size of the numbers on the y-axis
ax.tick_params(axis='y', labelsize=17)

# Move the legend to the left of the figure
ax.legend(fontsize=9, loc='best')

# Adjust layout
plt.tight_layout()

# Save the plot locally
plt.savefig('comparison_ahbps_gdvps_best_results_by_vehicle.png', dpi=600)

# Show the plot
plt.show()

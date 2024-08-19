import pandas as pd
import matplotlib.pyplot as plt

# Data from the files
scenarios = [
    '1 vehicle, 4 locations', '1 vehicle, 5 locations', '1 vehicle, 6 locations', '1 vehicle, 7 locations', 
    '1 vehicle, 8 locations', '1 vehicle, 10 locations', '1 vehicle, 12 locations', '1 vehicle, 15 locations',
    '2 vehicles, 4 locations', '2 vehicles, 5 locations', '2 vehicles, 6 locations', '2 vehicles, 7 locations', 
    '2 vehicles, 8 locations', '2 vehicles, 10 locations', '2 vehicles, 12 locations', '2 vehicles, 15 locations',
    '3 vehicles, 6 locations', '3 vehicles, 7 locations', '3 vehicles, 8 locations', '3 vehicles, 10 locations', 
    '3 vehicles, 12 locations', 
    '4 vehicles, 8 locations', '4 vehicles, 10 locations', '4 vehicles, 12 locations', '4 vehicles, 15 locations',
    '5 vehicles, 8 locations', '5 vehicles, 10 locations', '5 vehicles, 12 locations', '5 vehicles, 15 locations'
]

opl_values = [
    6, 7, 8, 9, 10, 12, 14, 17,
    9, 9, 10, 11, 12, 14, 16, 19,
    11, 12, 13, 15, 17,
    14, 16, 18, 20,
    15, 17, 19, 21
]

ahbps_values = [
    3, 4, 5, 6, 7, 9, 9, 13,
    3, 4, 5, 6, 7, 9, 11, 14,
    5, 6, 7, 9, 11,
    7, 9, 11, 14,
    7, 9, 11, 14
]

gdvps_values = [
    5, 6, 7, 8, 9, 11, 13, 15,
    5, 6, 7, 8, 9, 10, 13, 17,
    10, 9, 10, 14, 14,
    11, 12, 14, 17,
    11, 13, 15, 16
]

# Convert the data to DataFrames
df = pd.DataFrame({
    'Scenario': scenarios,
    'Optimal': opl_values,
    'AHBPS': ahbps_values,
    'GDVPS': gdvps_values
})

# Normalize the data based on the best achieved result (highest value)
df_normalized = df.copy()
max_value = df[['Optimal', 'AHBPS', 'GDVPS']].values.max()
df_normalized[['Optimal', 'AHBPS', 'GDVPS']] = df[['Optimal', 'AHBPS', 'GDVPS']] / max_value

# Plotting the normalized data
plt.figure(figsize=(14, 8))
bar_width = 0.25

# Set positions of bars on the x-axis
r1 = range(len(df_normalized))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]

# Create bars
plt.bar(r1, df_normalized['Optimal'], color='black', width=bar_width, label='Optimal')
plt.bar(r2, df_normalized['AHBPS'], color='red', width=bar_width, label='AHBPS')
plt.bar(r3, df_normalized['GDVPS'], color='blue', width=bar_width, label='GDVPS')

# Add xticks on the middle of the group bars
plt.xlabel('Different Scenarios')
plt.ylabel('Normalized Locations Visited')
plt.title('Normalized Performance evaluation between the Optimal solution, AHBPS, and GDVPS')
plt.xticks([r + bar_width for r in range(len(df_normalized))], df['Scenario'], rotation=90)

# Create legend & title
plt.legend()
plt.tight_layout()

# Save the plot to a file
plt.savefig('./normalized_performance_evaluation_optimal_AHBPS_GDVPS.png')

# Show the plot
plt.show()

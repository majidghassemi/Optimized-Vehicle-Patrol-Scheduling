import matplotlib.pyplot as plt

# Data from the files
scenarios = [
    '5 vehicles, 100 locations', '5 vehicles, 200 locations', '5 vehicles, 300 locations',
    '8 vehicles, 100 locations', '8 vehicles, 200 locations', '8 vehicles, 300 locations', '8 vehicles, 400 locations', '8 vehicles, 500 locations',
    '10 vehicles, 100 locations', '10 vehicles, 200 locations', '10 vehicles, 300 locations', '10 vehicles, 400 locations', '10 vehicles, 500 locations',
    '10 vehicles, 750 locations', '10 vehicles, 1000 locations',
    '12 vehicles, 100 locations', '12 vehicles, 200 locations', '12 vehicles, 300 locations', '12 vehicles, 400 locations', '12 vehicles, 500 locations',
    '12 vehicles, 750 locations', '12 vehicles, 1000 locations',
    '15 vehicles, 200 locations', '15 vehicles, 300 locations', '15 vehicles, 400 locations', '15 vehicles, 500 locations', 
    '15 vehicles, 750 locations', '15 vehicles, 1000 locations',
    '20 vehicles, 500 locations', '20 vehicles, 750 locations', '20 vehicles, 1000 locations'
]

gdvps_execution_time = [
    5.76, 8.06, 11.00,
    11.08, 16.71, 19.66, 25.18, 22.97,
    12.83, 18.37, 32.25, 35.90, 33.66,
    38.46, 107.31,
    25.97, 24.43, 36.13, 34.99, 40.33,
    46.03, 127.98,
    33.92, 44.82, 49.14, 62.43,
    83.95, 119.92,
    83.89, 70.19, 134.18
]

ahbps_execution_time = [
    0.01, 0.01, 0.02,
    0.01, 0.02, 0.03, 0.04, 0.06,
    0.01, 0.02, 0.04, 0.06, 0.07,
    0.11, 0.15,
    0.01, 0.03, 0.05, 0.07, 0.09,
    0.14, 0.18,
    0.04, 0.06, 0.08, 0.11,
    0.17, 0.23,
    0.14, 0.22, 0.30
]

# Plotting the data
plt.figure(figsize=(14, 8))
plt.plot(scenarios, gdvps_execution_time, color='blue', marker='o', label='GDVPS')
plt.plot(scenarios, ahbps_execution_time, color='red', marker='o', label='AHBPS')

plt.xlabel('Different Scenarios')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time comparison between AHBPS and GDVPS')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()

# Save the plot to a file
plt.savefig('/mnt/data/execution_time_comparison_AHBPS_GDVPS.png')

# Show the plot
plt.show()

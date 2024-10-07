import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# Data from the AHBPS and GDVPS files
scenarios = [
    '5 vehicles, 200 locations', '10 vehicles, 500 locations', '10 vehicles, 1000 locations',
    '15 vehicles, 750 locations', '15 vehicles, 1000 locations'
]

shifts = ['1 shift', '2 shifts', '3 shifts', '4 shifts', '5 shifts']

ahbps_data = {
    '5 vehicles, 200 locations': [23.81, 44.81, 62.98, 79.93, 93.83],
    '10 vehicles, 500 locations': [47.83, 90.92, 130.31, 165.3, 196.4],
    '10 vehicles, 1000 locations': [47.7, 93.04, 136.85, 177.87, 218.14],
    '15 vehicles, 750 locations': [71.47, 136.17, 194.5, 247.84, 295.7],
    '15 vehicles, 1000 locations': [71.57, 138.18, 199.74, 257.1, 310.86]
}

gdvps_data = {
    '5 vehicles, 200 locations': [29.563, 56.131, 75.735, 99.326, 112.857],
    '10 vehicles, 500 locations': [58.142, 105.296, 153.402, 191.6, 230.682],
    '10 vehicles, 1000 locations': [58.09, 105.285, 156.391, 200.55, 250.689],
    '15 vehicles, 750 locations': [82.647, 156.383, 215.151, 283.859, 340.587],
    '15 vehicles, 1000 locations': [83.663, 154.425, 229.138, 292.845, 352.497]
}

# Plotting the data
bar_width = 0.35
index = np.arange(len(shifts))

fig, ax = plt.subplots(figsize=(16, 8))

hatches = ['/', '\\', '|', '-', '+']
color_ahbps = '#FF3333'  # Red for AHBPS
color_gdvps = '#3399FF'  # Blue for GDVPS

for i, scenario in enumerate(scenarios):
    plt.bar(index + i * bar_width, ahbps_data[scenario], bar_width/2, color=color_ahbps, hatch=hatches[i], edgecolor='black', label=f'AHBPS - {scenario}')
    plt.bar(index + i * bar_width + bar_width/2, gdvps_data[scenario], bar_width/2, color=color_gdvps, hatch=hatches[i], edgecolor='black', label=f'GDVPS - {scenario}')

plt.xlabel('Number of Shifts')
plt.ylabel('Number of Visited Locations')
plt.title('AHBPS and GDVPS Evaluation by varying the number of shifts')

plt.xticks(index + bar_width, shifts)

# Custom legend for AHBPS and GDVPS
handles_ahbps = [mpatches.Patch(facecolor=color_ahbps, edgecolor='black', hatch=h, label=f'AHBPS - {scenarios[i]}') for i, h in enumerate(hatches)]
handles_gdvps = [mpatches.Patch(facecolor=color_gdvps, edgecolor='black', hatch=h, label=f'GDVPS - {scenarios[i]}') for i, h in enumerate(hatches)]
plt.legend(handles=handles_ahbps + handles_gdvps, loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.savefig('final_ahbps_gdvps_evaluation_shifts.png')
plt.show()

import matplotlib.pyplot as plt
import pandas as pd
import os

# === Setup directories ===
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# === Load dataset ===
file_path = os.path.join(ma_dir, "data", "final", "graph_data.xlsx")
df = pd.read_excel(file_path).rename(columns={"CAR_10_wins": "[-10, 10]"})

# Select event window columns
event_window_cols = ['[-10, 10]', '[-7, 7]', '[-5, 5]', '[-3, 3]', '[-1, 1]']

# Plot histograms and KDEs
for col in event_window_cols:
    plt.figure()
    df[col].plot(kind='hist', bins=30, density=True, alpha=0.6, label='Histogram')
    df[col].plot(kind='kde', label='KDE')
    plt.title(f'Distribution of CAR for Event Window {col}')
    plt.xlabel('CAR (%)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.show()

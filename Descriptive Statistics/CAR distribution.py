import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from scipy.stats import norm

# === Setup directories ===
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# === Load dataset ===
file_path = os.path.join(ma_dir, "data", "final", "graph_data.xlsx")
df = pd.read_excel(file_path).rename(columns={"CAR_10_wins": "[-10, 10]"})

# === Create output folder for plots ===
output_dir = os.path.join(current_dir, "car_distributions")
os.makedirs(output_dir, exist_ok=True)

# === Select event window columns ===
event_window_cols = ['[-10, 10]', '[-7, 7]', '[-5, 5]', '[-3, 3]', '[-1, 1]']

# === Plot histograms and KDEs, save to file ===
for col in event_window_cols:
    plt.figure()
    
    # Plot histogram and KDE
    df[col].plot(kind='hist', bins=30, density=True, alpha=0.6, label='Histogram')
    df[col].plot(kind='kde', label='KDE')
    
    # Plot normal distribution
    mean = df[col].mean()
    std = df[col].std()
    x_vals = np.linspace(df[col].min(), df[col].max(), 200)
    plt.plot(x_vals, norm.pdf(x_vals, loc=mean, scale=std), color='red', linestyle='--', label='Normal PDF')

    # Final touches
    plt.title(f'Distribution of CAR for Event Window {col}')
    plt.xlabel('CAR (%)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)

    # Save the plot
    safe_col_name = col.replace('[', '').replace(']', '').replace(',', '_').replace(' ', '')
    plot_path = os.path.join(output_dir, f"car_distribution_{safe_col_name}.png")
    plt.savefig(plot_path)
    plt.close()


from scipy.stats import shapiro, normaltest, jarque_bera

for col in event_window_cols:
    print(f"{col}:")
    print("  Shapiro-Wilk:", shapiro(df[col].dropna()))
    print("  Jarque-Bera:", jarque_bera(df[col].dropna()))
    print("  D’Agostino-Pearson:", normaltest(df[col].dropna()))

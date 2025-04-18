import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew, kurtosis

# === Setup directories ===
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# === Load the dataset ===
file_path = os.path.join(ma_dir, "data", "processed", "CAR_v5_extra_vars_cleaned.xlsx")
df = pd.read_excel(file_path)

# === Define the variable ===
deal_col = 'Total Transaction Value (€EURmm, Historical rate)'
deal_values = df[deal_col].dropna()

# === Create output directory ===
output_dir = os.path.join(ma_dir, "Descriptive Statistics", "Distribution Plots")
os.makedirs(output_dir, exist_ok=True)

# === 1. Raw Distribution (Histogram) ===
plt.figure(figsize=(10, 6))
plt.hist(deal_values, bins=30, color='skyblue', edgecolor='black')
plt.title("Distribution of Deal Values (EUR million)")
plt.xlabel("Deal Value (€ million)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "deal_value_distribution.png"))
plt.close()

# === 2. Log-Transformed Distribution ===
plt.figure(figsize=(10, 6))
plt.hist(np.log1p(deal_values), bins=30, color='steelblue', edgecolor='black')
plt.title("Log-Transformed Distribution of Deal Values")
plt.xlabel("Log(1 + Deal Value in € million)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "deal_value_log_distribution.png"))
plt.close()

# === 3. Skewness and Kurtosis ===
deal_skewness = skew(deal_values)
deal_kurtosis = kurtosis(deal_values)

print("📊 Deal Value Distribution Statistics")
print("-------------------------------------")
print(f"Observations: {len(deal_values)}")
print(f"Mean: {deal_values.mean():,.2f}")
print(f"Median: {deal_values.median():,.2f}")
print(f"Min: {deal_values.min():,.2f}")
print(f"Max: {deal_values.max():,.2f}")
print(f"Skewness: {deal_skewness:.2f}")
print(f"Kurtosis: {deal_kurtosis:.2f}")
print("\nHistograms saved to:", output_dir)

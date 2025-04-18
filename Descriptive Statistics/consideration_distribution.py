import os
import pandas as pd
import matplotlib.pyplot as plt

# === Setup directories ===
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# === Load dataset ===
file_path = os.path.join(ma_dir, "data", "processed", "CAR_v5_extra_vars_cleaned.xlsx")
df = pd.read_excel(file_path)

# === Clean and map "Consideration Offered" ===
def map_payment_type(value):
    if not isinstance(value, str):
        return None
    val = value.strip()

    if val == "Cash":
        return "Cash"
    elif val == "Common Equity":
        return "Stock"
    elif "Cash" in val:
        return "Mixed"
    else:
        return None  # Exclude Unknown, Combinations, etc.

df["Consideration Category"] = df["Consideration Offered"].apply(map_payment_type)
cleaned = df.dropna(subset=["Consideration Category"])

# === Count and plot ===
counts = cleaned["Consideration Category"].value_counts()

plt.figure(figsize=(8, 6))
counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Distribution of Consideration Types")
plt.xlabel("Payment Type")
plt.ylabel("Count")
plt.xticks(rotation=0)
plt.tight_layout()

# === Save plot ===
output_dir = os.path.join(ma_dir, "Descriptive Statistics")
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, "consideration_type_distribution.png"))
plt.close()

print("✅ Consideration type plot saved to:", output_dir)

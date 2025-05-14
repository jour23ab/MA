import matplotlib.pyplot as plt
import pandas as pd
import configparser
from collections import Counter
import numpy as np

# === Load config and event data ===
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

file1 = config["FINAL_FILES"]["abnormal_returns"]
event_values_dict = pd.read_excel(file1, sheet_name=None)  # All sheets loaded

# === Load characteristics dataset ===
char_file = config["FINAL_FILES"]["cars_analysis"]
char_df = pd.read_excel(char_file)

# === Classify mergers based on payment method ===
def classify_consideration(value):
    if isinstance(value, str) and 'cash' in value.lower():
        return 'cash'
    else:
        return 'non-cash'

char_df['group'] = char_df['Consideration Offered'].apply(classify_consideration)
group_mapping = dict(zip(char_df['Sheet Name'], char_df['group']))

# === Print group sizes ===
counts = Counter(group_mapping.values())
print("\nGroup sizes:")
for group, count in counts.items():
    print(f"{group}: {count} mergers")

# === Define event window ===
start_offset, end_offset = -10, 10
days = list(range(start_offset, end_offset + 1))

# === Collect all abnormal returns to compute percentiles ===
all_abnormal_returns = []
for values_df in event_values_dict.values():
    if "Abnormal Return" in values_df.columns:
        all_abnormal_returns.extend(values_df["Abnormal Return"].dropna().tolist())

lower_bound = np.percentile(all_abnormal_returns, 1)
upper_bound = np.percentile(all_abnormal_returns, 99)

print(f"\nRemoving outliers outside the 1st and 99th percentiles:")
print(f"Lower bound (1%): {lower_bound:.5f}, Upper bound (99%): {upper_bound:.5f}")

# === Prepare AAR and CAAR calculations ===
groups = ['cash', 'non-cash']
group_aar_dict = {g: [] for g in groups}
outlier_counts = {g: 0 for g in groups}

for day_offset in days:
    group_abnormal_returns = {g: [] for g in groups}

    for sheet_name, values_df in event_values_dict.items():
        if sheet_name not in group_mapping:
            continue

        group = group_mapping[sheet_name]

        if all(col in values_df.columns for col in ["M&A Announced Date", "Abnormal Return", "Buyers/Investors", "Ticker"]):
            values_df["Date"] = pd.to_datetime(values_df["Date"]).dt.date
            values_df["M&A Announced Date"] = pd.to_datetime(values_df["M&A Announced Date"]).dt.date
            announce_date = values_df["M&A Announced Date"].iloc[0]

            if announce_date in values_df["Date"].values:
                announce_idx = values_df[values_df["Date"] == announce_date].index[0]
                day_idx = announce_idx + day_offset

                if 0 <= day_idx < len(values_df):
                    abnormal_return = values_df.loc[day_idx, "Abnormal Return"]

                    # Remove outliers based on percentile bounds
                    if abnormal_return < lower_bound or abnormal_return > upper_bound:
                        outlier_counts[group] += 1
                        continue

                    group_abnormal_returns[group].append(abnormal_return)

    for g in groups:
        aar = sum(group_abnormal_returns[g]) / len(group_abnormal_returns[g]) if group_abnormal_returns[g] else None
        group_aar_dict[g].append(aar)

# Print number of removed outliers
print("\nOutliers removed per group:")
for g in groups:
    print(f"{g}: {outlier_counts[g]} observations removed")

# === Print AARs ===
print("\nAARs per group:")
for g in groups:
    print(f"\nGroup: {g}")
    for day, aar in zip(days, group_aar_dict[g]):
        print(f"Day {day}: AAR = {aar:.5f}" if aar is not None else f"Day {day}: AAR = None")

# === Calculate CAAR ===
group_caar_dict = {g: pd.Series(group_aar_dict[g]).cumsum().tolist() for g in groups}

# === Plot CAAR ===
plt.figure(figsize=(10, 6))
colors = {'cash': 'green', 'non-cash': 'blue'}

for g in groups:
    plt.plot(days, group_caar_dict[g], label=f"CAAR ({g})", linestyle='--', marker='x', color=colors[g])

plt.title("CAAR Comparison for Event Window [-10, 10]", fontsize=14)
plt.xlabel("Days Relative to Announcement Date", fontsize=12)
plt.ylabel("Cumulative Abnormal Return", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

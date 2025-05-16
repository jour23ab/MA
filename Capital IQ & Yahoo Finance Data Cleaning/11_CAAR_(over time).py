# Final integrated script for CAAR calculation and plotting with winsorize/trim toggle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import configparser
from scipy import stats
from openpyxl import load_workbook
import os

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the config file
config_path = os.path.join(base_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

# Load all sheets from abnormal_returns.xlsx
file1 = os.path.join(base_dir, config["FINAL_FILES"]["abnormal_returns"])
event_values_dict = pd.read_excel(file1, sheet_name=None)

# Go one level up to reach the GitHub/MA/data/final folder
project_root = os.path.dirname(base_dir)  # This goes one level up

# Define full path to the CAR dataframe
car_path = os.path.join(project_root, "data", "final", "df_trimmed_characteristics.xlsx")
car_df = pd.read_excel(car_path).rename(columns={"CAR_10_wins": "[-10, 10]"})
car_df = car_df.dropna(subset=["[-10, 10]"])

# Toggle outlier handling method: 'winsorize', 'trim', or 'none'
outlier_handling_mode = "none"  # Options: "winsorize", "trim", "none"

# Define event windows
event_windows = ["[-10, 10]", "[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]"]

# Dictionary to store processed car_df per window
car_df_dict = {}

for window in event_windows:
    if window in car_df.columns:
        temp_df = car_df[["Sheet Name", window]].dropna(subset=[window]).copy()

        if outlier_handling_mode == "winsorize":
            low, high = temp_df[window].quantile([0.01, 0.99])
            temp_df[window] = temp_df[window].clip(lower=low, upper=high)

        elif outlier_handling_mode == "trim":
            low, high = temp_df[window].quantile([0.01, 0.99])
            temp_df = temp_df[(temp_df[window] >= low) & (temp_df[window] <= high)]

        # If "none", keep values as-is
        car_df_dict[window] = temp_df


# Create a version of event_values_dict for each event window
event_values_dicts = {}

for window, df in car_df_dict.items():
    valid_sheets = set(df["Sheet Name"].dropna().astype(str))
    filtered_dict = {k: v for k, v in event_values_dict.items() if k in valid_sheets}
    event_values_dicts[window] = filtered_dict


# Define event windows
event_windows = {
    '[-10, 10]': (-10, 10),
    '[-7, 7]': (-7, 7),
    '[-5, 5]': (-5, 5),
    '[-3, 3]': (-3, 3),
    '[-1, 1]': (-1, 1)
}

event_window_dfs = {}
for window_name, (start_offset, end_offset) in event_windows.items():
    # Use the filtered event_values_dict for this specific window
    current_event_dict = event_values_dicts.get(window_name, {})

    days = list(range(start_offset, end_offset + 1))
    aar_list = []

    for day_offset in days:
        daily_returns = []

        for sheet, df in current_event_dict.items():
            if all(col in df.columns for col in ["M&A Announced Date", "Abnormal Return", "Date"]):
                df["Date"] = pd.to_datetime(df["Date"]).dt.date
                df["M&A Announced Date"] = pd.to_datetime(df["M&A Announced Date"]).dt.date
                announce_date = df["M&A Announced Date"].iloc[0]

                if announce_date in df["Date"].values:
                    announce_idx = df[df["Date"] == announce_date].index[0]
                    day_idx = announce_idx + day_offset

                    if 0 <= day_idx < len(df):
                        ar = df.loc[day_idx, "Abnormal Return"]
                        daily_returns.append(ar)

        aar = np.mean(daily_returns) if daily_returns else None
        aar_list.append(aar)

    caar_list = pd.Series(aar_list).cumsum().tolist()
    event_window_dfs[window_name] = pd.DataFrame({"Day": days, "AAR": aar_list, "CAAR": caar_list})

# Plotting
for window_name, df in event_window_dfs.items():
    plt.figure(figsize=(10, 6))
    plt.plot(df["Day"], df["CAAR"], label="CAAR", linestyle="--", marker="x")
    mode_label = {
        "winsorize": "Winsorized",
        "trim": "Trimmed",
        "none": "Trimming Based on Acquirer Characteristics"
    }[outlier_handling_mode]

    plt.title(f"CAAR for Event Window {window_name} ({mode_label})")

    plt.xlabel("Days Relative to Announcement")
    plt.ylabel("Cumulative Abnormal Return")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()




# Compute CAAR statistics based on trimmed/winsorized CAR values for each window
caar_summary = {
    "Metric": ["CAAR", "Std Dev", "T-Statistic", "P-Value (2-sided)"]
}

for window, df in car_df_dict.items():
    values = df[window].dropna().values
    n = len(values)

    if n > 1:
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        t_stat = mean / (std / np.sqrt(n))
        p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=n - 1))
    else:
        mean, std, t_stat, p_val = [np.nan] * 4

    caar_summary[window] = [mean, std, t_stat, p_val]

# Create summary DataFrame
caar_DF = pd.DataFrame(caar_summary)

print(f"Results based on CAR method ({mode_label})")
print(caar_DF)
print("CAAR statistics successfully calculated")



""" 
# Load CAR DataFrame from Excel file
cars_df = car_df

# Identify event window columns
event_windows = ["[-10, 10]", "[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]"]

# Keep only rows where the main 21-day event window is not NaN
car_values = cars_df.dropna(subset=["[-10, 10]"])

# Initialize CAAR summary dictionary
caar_summary = {
    "Metric": ["CAAR", "Std Dev", "T-Statistic", "P-Value (2-sided)"]
}

# Loop through each event window column and calculate statistics using the filtered rows
for window in event_windows:
    values = car_values[window].values
    n = len(values)

    if n > 1:
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        t_stat = mean / (std / np.sqrt(n))
        p_val = 2 * (1 - stats.t.cdf(np.abs(t_stat), df=n - 1))
    else:
        mean, std, t_stat, p_val = [np.nan] * 4

    caar_summary[window] = [mean, std, t_stat, p_val]

# Create summary DataFrame
caar_DF = pd.DataFrame(caar_summary)

print("results based on CAR method")
print(caar_DF)
print("CAAR statistics successfully calculated")
 """
import pandas as pd
import requests
import matplotlib.pyplot as plt
from setuptools.config.expand import read_files

# Define the URL for the VSTOXX data
url = "https://www.stoxx.com/document/Indices/Current/HistoricalData/h_v2tx.txt"

# Download the file content
response = requests.get(url)
data = response.text

# Save it as a text file locally
file_path = "VSTOXX_data.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(data)

# Load the data
df = pd.read_csv(file_path, sep=";", skiprows=4)
df.to_excel("VSTOXX_data.xlsx", index=False)
df.to_csv("VSTOXX_data.csv", index=False)

# Load dataset from saved CSV
file_path = "C:/Users/johan/Documents/Documents/Universitet/5. år MSc/Repository/Thesis/VSTOXX_data.csv"
colnames = ["Date", "Ticker", "Index"]
df = pd.read_csv(file_path, names=colnames, parse_dates=["Date"])
df.set_index("Date", inplace=True)
df.index = pd.to_datetime(df.index, format="%d.%m.%Y")
df_reformatted = df[df.index >= "2005-01-01"].copy()


def calculate_ema(data, column="Index", days=7, smoothing=2):
    """
    Calculate the Exponential Moving Average (EMA) for a given DataFrame column.
    """
    multiplier = smoothing / (1 + days)
    ema_values = [data[column].iloc[0]]

    for i in range(1, len(data)):
        ema_today = (data[column].iloc[i] * multiplier) + (ema_values[i - 1] * (1 - multiplier))
        ema_values.append(ema_today)

    data["EMA"] = ema_values
    return data


def identify_crisis_periods(data, ema_days=100, threshold=25, gap_days=31, min_crisis_length=31):
    """
    Identify periods where EMA of VSTOXX exceeds a given threshold, allowing short gaps
    within a crisis and filtering out very short above-threshold periods.

    Parameters:
        data: Input time series with 'Index' column and datetime index.
        ema_days (int): EMA smoothing window length.
        threshold: EMA threshold to define high volatility.
        gap_days: Max days allowed between above-threshold dates within a single crisis period.
        min_crisis_length: Minimum number of days that a crisis period must last to be retained.

    Returns:
        intervals (DataFrame): Crisis periods (start and end dates).
        data (DataFrame): Original data with EMA column added.
    """
    data = calculate_ema(data.copy(), column="Index", days=ema_days, smoothing=2)
    breach_dates = data[data["EMA"] > threshold].index.sort_values()

    if breach_dates.empty:
        return pd.DataFrame(columns=["Start", "End"]), data

    breach_series = pd.Series(breach_dates)
    day_diff = breach_series.diff().dt.days.fillna(0)
    group_id = (day_diff > gap_days).cumsum()
    intervals = breach_series.groupby(group_id).agg(['min', 'max'])
    intervals.columns = ['Start', 'End']

    # Filter out short-lived spikes (crisis periods with duration < min_crisis_length)
    intervals['Duration'] = (intervals['End'] - intervals['Start']).dt.days + 1
    intervals = intervals[intervals['Duration'] >= min_crisis_length]
    intervals = intervals.drop(columns='Duration')

    return intervals, data

### Sensitivity analysis with different specifications
# Define parameter sets for testing
specifications = {
    "Baseline (EMA 100, T=25)": {"ema_days": 100, "threshold": 25},
    "Model A (EMA 100, T=23)": {"ema_days": 100, "threshold": 23},
    "Model B (EMA 100, T=24)": {"ema_days": 100, "threshold": 24},
    "Model C (EMA 100, T=26)": {"ema_days": 100, "threshold": 26},
    "Model D (EMA 100, T=27)": {"ema_days": 100, "threshold": 27},
    "Model E (EMA 50, T=25)": {"ema_days": 50, "threshold": 25},
    "Model F (EMA 75, T=25)": {"ema_days": 75, "threshold": 25},
    "Model G (EMA 125, T=25)": {"ema_days": 125, "threshold": 25},
    "Model H (EMA 150, T=25)": {"ema_days": 150, "threshold": 25},
}

# Loop through and plot each configuration
for label, params in specifications.items():
    ema_days = params["ema_days"]
    threshold = params["threshold"]

    intervals, df_with_ema = identify_crisis_periods(df_reformatted, ema_days=ema_days, threshold=threshold)

    plt.figure(figsize=(12, 6))
    plt.plot(df_with_ema.index, df_with_ema["Index"], label="VSTOXX Daily", color="blue", linewidth=2)
    plt.plot(df_with_ema.index, df_with_ema["EMA"], label=f"{ema_days}-day EMA", color="red", linestyle="dashed", linewidth=2)
    plt.axhline(y=threshold, color='green', label=f"Threshold = {threshold}", linestyle='-')
    plt.title(f"VSTOXX & EMA – {label}", fontsize=14)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Index Value", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f"\n{label} — Crisis Periods Identified:")
    print(intervals)

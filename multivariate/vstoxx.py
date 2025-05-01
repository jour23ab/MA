import pandas as pd
import requests
import matplotlib.pyplot as plt
from setuptools.config.expand import read_files

#Define the URL for the VSTOXX data
url = "https://www.stoxx.com/document/Indices/Current/HistoricalData/h_v2tx.txt"

# Download the file content
response = requests.get(url)
data = response.text  # Read the content as text

# Save it as a text file locally
file_path = "VSTOXX_data.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(data)

# Load the data into a Pandas DataFrame
df = pd.read_csv(file_path, sep=";", skiprows=4)  # Adjust separator and skip initial rows if needed

# Save it as an Excel file
df.to_excel("VSTOXX_data.xlsx", index=False)

# Save it as a CSV file
df.to_csv("VSTOXX_data.csv", index=False)

print("Data successfully downloaded and saved as Excel and CSV!")

# Load dataset
file_path = "C:/Users/johan/Documents/Documents/Universitet/5. år MSc/Repository/Thesis/VSTOXX_data.csv"
colnames=["Date", "Ticker", "Index"]
df = pd.read_csv(file_path, names=colnames, parse_dates=["Date"])  # Ensure Date is recognized as datetime

# Set Date as the index
df.set_index("Date", inplace=True)
df.index = pd.to_datetime(df.index, format="%d.%m.%Y")  # Adjust format to match day.month.year
#df_reformatted= df.resample("ME").last()
df_reformatted = df


# Define function to calculate EMA using the given formula
def calculate_ema(data, column="Index", days=7, smoothing=2):
    """
    Calculate the Exponential Moving Average (EMA) for a given DataFrame column.

    Parameters:
    - data: Pandas DataFrame with a datetime index
    - column: Name of the column for which EMA is calculated
    - days: The period over which EMA is computed
    - smoothing: Smoothing factor (default is 2)

    Returns:
    - DataFrame with EMA values
    This function is manually computed, but is the same as pandas' built-in function pd.Series.ewm().
    """
    # Calculate the smoothing multiplier
    multiplier = smoothing / (1 + days)

    # Initialize EMA series
    ema_values = []

    # Set the first EMA value as the first actual data point (initialization)
    ema_values.append(data[column].iloc[0])

    # Compute EMA using the formula iteratively
    for i in range(1, len(data)):
        ema_today = (data[column].iloc[i] * multiplier) + (ema_values[i - 1] * (1 - multiplier))
        ema_values.append(ema_today)

    # Assign calculated EMA values to a new column in DataFrame
    data["EMA"] = ema_values

    return data


# Apply the EMA function to the monthly VSTOXX data
df_reformatted = calculate_ema(df_reformatted, column="Index", days=100, smoothing=2)

df_reformatted = df_reformatted[df_reformatted.index >= "2005-01-01"]

threshold = 25

# Plot the EMA alongside the original data
plt.figure(figsize=(12, 6))
plt.plot(df_reformatted.index, df_reformatted["Index"], label="VSTOXX Daily", color="blue", linewidth=2)
plt.plot(df_reformatted.index, df_reformatted["EMA"], label="100-day EMA", color="red", linestyle="dashed", linewidth=2)
plt.axhline(y=threshold, color='g', label="Threshold", linestyle='-')
# Formatting the plot
plt.title("VSTOXX & EMA", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Index Value", fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

print(df_reformatted)

breach_dates = df_reformatted[df_reformatted["EMA"] > threshold].index
print("Dates when VSTOXX breached the threshold of 25:", breach_dates)

# Example: breach_dates is your list of dates (DatetimeIndex or Series)
# Ensure the dates are sorted
breach_dates = breach_dates.sort_values()

# Convert to Series to calculate differences
breach_series = pd.Series(breach_dates)

# Identify breaks in consecutive months and new group if the gap is more than 31 days
month_diff = breach_series.diff().dt.days.fillna(0)
group_id = (month_diff > 31).cumsum()

# Group by these break points and extract intervals
intervals = breach_series.groupby(group_id).agg(['min', 'max'])

# Rename
intervals.columns = ['Start', 'End']

# Display
print(intervals)

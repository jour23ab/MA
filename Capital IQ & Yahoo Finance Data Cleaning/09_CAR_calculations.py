import pandas as pd
import configparser
import joblib

# THis code calculates the CAR values for each event window for each merger based on the abnormal returns calculated in the previous file.


# Load config file
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")


file1 = config["FINAL_FILES"]["abnormal_returns"]

# Load all sheets into dictionaries
event_values_dict = pd.read_excel(file1, sheet_name=None)  # Loads all sheets into a dictionary


""" file1 = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/abnormal_returns.pkl"
event_values_dict = joblib.load(file1) """


# Keep track of original number of DataFrames
original_count = len(event_values_dict)

# Remove sheets if they don't have the expected return or abnormal return for some reason.
event_values_dict = {
    key: df for key, df in event_values_dict.items()
    if {"Expected Return", "Abnormal Return"}.issubset(df.columns)
}

# Calculate how many were removed
removed_count = original_count - len(event_values_dict)

print(f"Removed {removed_count} DataFrames.")


# Define the event windows (in terms of days before and after the announcement date)
event_windows = {
    '[-10, 10]': (-10, 10),
    '[-7, 7]': (-7, 7),
    '[-5, 5]': (-5, 5),
    '[-3, 3]': (-3, 3),
    '[-1, 1]': (-1, 1)
}

# Initialize an empty list to store the rows for the CARs_DF DataFrame
car_data = []

# Loop through each merger's dataframe in event_values_dict
for sheet_name, values_df in event_values_dict.items():
    if all(col in values_df.columns for col in ["M&A Announced Date", "Abnormal Return", "Buyers/Investors", "Ticker"]):
        
        # Ensure date columns are in datetime format
        values_df["Date"] = pd.to_datetime(values_df["Date"]).dt.date
        values_df["M&A Announced Date"] = pd.to_datetime(values_df["M&A Announced Date"]).dt.date

        # Extract first occurrence of M&A Announced Date, Buyers/Investors, and Ticker
        announce_date = values_df["M&A Announced Date"].iloc[0]
        acquirer_name = values_df["Buyers/Investors"].iloc[0]
        ticker = values_df["Ticker"].iloc[0]

        # Create a list to store the CAR values for this merger
        car_values = [sheet_name, announce_date, acquirer_name, ticker]  

        # Find the index of the row where the date matches the announcement date
        if announce_date in values_df["Date"].values:
            announcement_idx = values_df[values_df["Date"] == announce_date].index[0]
            
            # Loop through event windows and calculate CAR for each
            for _, (start_offset, end_offset) in event_windows.items():
                start_idx = announcement_idx + start_offset
                end_idx = announcement_idx + end_offset
                
                # Ensure indices are within DataFrame bounds
                if 0 <= start_idx < len(values_df) and 0 <= end_idx < len(values_df):
                    car_value = values_df.loc[start_idx:end_idx, "Abnormal Return"].sum()
                else:
                    car_value = None  # Handle cases where event window exceeds data range
                
                car_values.append(car_value)  

            car_data.append(car_values)

        else:
            print(f"No match found for the announcement date: {announce_date}, {acquirer_name}")

# Convert to DataFrame
columns = ["Sheet Name", "M&A Announced Date", "Buyers/Investors", "Ticker"] + list(event_windows.keys())
cars_DF = pd.DataFrame(car_data, columns=columns)

print(cars_DF)

# Save to Excel
output_path = config["FINAL_FILES"]["car_values"]
cars_DF.to_excel(output_path, index=False)

print(f"Length of cars_DF: {len(cars_DF)}")

print("CARs DataFrame successfully created and saved!")

import pandas as pd
import numpy as np
from scipy import stats
from openpyxl import load_workbook

# Load CAR DataFrame from Excel file
cars_DF = pd.read_excel(output_path)

# Identify event window columns
event_windows = ["[-10, 10]", "[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]"]

# Keep only rows where the main 21-day event window is not NaN
car_values = cars_DF.dropna(subset=["[-10, 10]"])

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

print(caar_DF)
print("CAAR statistics successfully calculated")

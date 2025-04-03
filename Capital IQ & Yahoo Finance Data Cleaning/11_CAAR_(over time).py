import matplotlib.pyplot as plt
import pandas as pd
import configparser

# Load config file
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

file1 = config["FINAL_FILES"]["abnormal_returns"]

# Load all sheets into dictionaries
event_values_dict = pd.read_excel(file1, sheet_name=None)  # Loads all sheets into a dictionary

# Define the event windows (in terms of days before and after the announcement date)
event_windows = {
    '[-10, 10]': (-10, 10),
    '[-7, 7]': (-7, 7),
    '[-5, 5]': (-5, 5),
    '[-3, 3]': (-3, 3),
    '[-1, 1]': (-1, 1)
}

# Dictionary to store DataFrames for each event window
event_window_dfs = {}

# Loop through each event window first
for window_name, (start_offset, end_offset) in event_windows.items():
    print(f"Processing event window: {window_name} (from {start_offset} to {end_offset})")
    
    aar_list = []  # Stores AARs for each day in the event window
    days = list(range(start_offset, end_offset + 1))  # List of days in the event window
    
    # Loop through each day in the event window
    for day_offset in days:
        print(f"  Processing day {day_offset} relative to announcement date")
        
        abnormal_returns = []  # List to store abnormal returns for this day across mergers
        
        # Loop through each merger's dataframe
        for sheet_name, values_df in event_values_dict.items():
            if all(col in values_df.columns for col in ["M&A Announced Date", "Abnormal Return", "Buyers/Investors", "Ticker"]):
                
                # Ensure date columns are in datetime format
                values_df["Date"] = pd.to_datetime(values_df["Date"]).dt.date
                values_df["M&A Announced Date"] = pd.to_datetime(values_df["M&A Announced Date"]).dt.date

                # Get announcement date
                announce_date = values_df["M&A Announced Date"].iloc[0]

                # Find index of announcement date
                if announce_date in values_df["Date"].values:
                    announcement_idx = values_df[values_df["Date"] == announce_date].index[0]
                    day_idx = announcement_idx + day_offset  # Adjust index for this day
                    
                    # Ensure index is within bounds
                    if 0 <= day_idx < len(values_df):
                        abnormal_return = values_df.loc[day_idx, "Abnormal Return"]
                        abnormal_returns.append(abnormal_return)  # Store abnormal return
                    else:
                        print(f"    Warning: Day index {day_idx} out of bounds for merger {sheet_name}")
        
        # Compute AAR for this day (average across all mergers)
        if abnormal_returns:
            aar_value = sum(abnormal_returns) / len(abnormal_returns)
            aar_list.append(aar_value)  # Store AAR for this day
        else:
            print(f"    No abnormal returns found for day {day_offset} in event window {window_name}")
            aar_list.append(None)  # Handle case where no returns were found

    # Compute CAAR (cumulative sum of AARs over time)
    caar_list = pd.Series(aar_list).cumsum().tolist()

    # Create a DataFrame for this event window
    event_window_df = pd.DataFrame({
        "Day": days,
        "AAR": aar_list,
        "CAAR": caar_list
    })

    # Store the DataFrame in the dictionary
    event_window_dfs[window_name] = event_window_df
    print(f"  Finished processing {window_name} event window.")

# Final check to see the results
print("Completed processing all event windows. DataFrames stored in event_window_dfs:")
for window_name, df in event_window_dfs.items():
    print(f"{window_name}:")
    print(df)  # Display first few rows of each event window DataFrame




# Loop through each event window and plot
for window_name, df in event_window_dfs.items():
    print(f"Plotting {window_name} event window...")
    
    # Create a new figure
    plt.figure(figsize=(10, 6))
    
    # Plot CAAR on the same graph
    plt.plot(df["Day"], df["CAAR"], label="CAAR", color="red", marker='x', linestyle='--', linewidth=2)
    
    # Adding titles and labels
    plt.title(f"CAAR for Event Window {window_name}", fontsize=14)
    plt.xlabel("Days Relative to Announcement Date", fontsize=12)
    plt.ylabel("Returns", fontsize=12)
    
    # Adding a legend to distinguish between AAR and CAAR
    plt.legend()
    
    # Show grid for better readability
    plt.grid(True)
    
    # Display the plot
    plt.show()

    print(f"Finished plotting {window_name} event window.\n")

import pandas as pd
import ast
import re
import configparser
import joblib


# Indlæs config fil
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

# Read the Excel file containing stock data
filsti = config["STOCK_FILES"]["adj_estimation_prices"]
df = pd.read_excel(filsti)

# Ensure column is treated as a string
df["Closing Prices"] = df["Closing Prices"].astype(str)
initial_length = len(df)

# Read the market returns dataset
filsti = r"C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/market_data.xlsx"
market_returns_df = pd.read_excel(filsti)
market_returns_df["Date"] = pd.to_datetime(market_returns_df["Date"]).dt.date  # Ensure datetime format
market_returns_df = market_returns_df[["Date", "Market Simple Return"]]
#print(market_returns_df)

# Read the risk free rate dataset
filsti = r"C:/Users/b407939/Desktop/Speciale/Capital IQ/Raw/Cleaned_ECB_Yield.xlsx"
risk_free_yield = pd.read_excel(filsti)
risk_free_yield["Date"] = pd.to_datetime(risk_free_yield["Date"]).dt.date  # Ensure datetime format
risk_free_yield["Yield Curve Spot Rate"] = risk_free_yield["Yield Curve Spot Rate"] / 100  # Turn from percentage into decimal
#print(risk_free_yield)

# Read the eu fama french factors for SMB and HML values
filsti = r"C:/Users/b407939/Desktop/Speciale/Capital IQ/Raw/Europe_3_Factors_Daily.csv"
fama_french_df = pd.read_csv(filsti, encoding="utf-8")
fama_french_df["Date"] = pd.to_datetime(fama_french_df["Date"], format='%Y%m%d').dt.date  # Ensure datetime format
fama_french_df = fama_french_df[["Date", "SMB", "HML"]]
#print(fama_french_df)

# Function to convert string to dictionary safely
def parse_price_dict(price_str):
    cleaned_str = re.sub(r"Timestamp\('([^']+)'\)", r"'\1'", price_str)
    return ast.literal_eval(cleaned_str)  # Convert to dictionary

# Create a dictionary to store separate DataFrames
separate_tables = {}
removed_count = 0
added_count = 0

# Process each row separately
for index, row in df.iterrows():
    try:
        price_dict = parse_price_dict(row["Closing Prices"])
        if not price_dict:
            print(f"Skipping row {index}: Empty price dictionary")
            continue
    except Exception as e:
        print(f"Error parsing row {index}: {e}")
        continue


    # Convert the price dictionary into a DataFrame
    temp_df = pd.DataFrame(price_dict.items(), columns=["Date", "Closing Price"])
    temp_df["Date"] = pd.to_datetime(temp_df["Date"]).dt.date  # Ensure datetime format

    if temp_df.empty:
        print(f"Skipping row {index}: No valid price data")
        continue

    # Calculate simple returns (returns for each day)
    temp_df["Simple Return"] = temp_df["Closing Price"].pct_change()

    # Add identifying columns
    temp_df["Buyers/Investors"] = row["Buyers/Investors"]
    temp_df["M&A Announced Date"] = row["M&A Announced Date"]
    temp_df["Ticker"] = row["Ticker"]

    # Merge with market returns, risk-free yield and fama_french factors based on date
    temp_df = temp_df.merge(market_returns_df, on="Date", how="left")
    temp_df = temp_df.merge(risk_free_yield[["Date", "Yield Curve Spot Rate"]], on="Date", how="left")
    temp_df = temp_df.merge(fama_french_df, on="Date", how="left")

    # If value missing, replace with the last known non-missing value.
    temp_df["Market Simple Return"] = temp_df["Market Simple Return"].ffill()    

    # Calculate excess market return.
    temp_df["Excess Market Return"] = temp_df["Market Simple Return"] - temp_df["Yield Curve Spot Rate"]

    # Make sure Announce Date is in datetime.
    temp_df["M&A Announced Date"] = pd.to_datetime(temp_df["M&A Announced Date"])  # Ensure datetime format
    temp_df['M&A Announced Date'] = temp_df['M&A Announced Date'].dt.date

    # Create a sanitized sheet name
    sheet_name = f"{temp_df['M&A Announced Date'].iloc[0]}_{temp_df['Buyers/Investors'].iloc[0]}"
    sheet_name = re.sub(r'[\\/*?:"<>|]', "_", sheet_name)  # Replace invalid characters with "_"

    # Truncate sheet name to fit within Excel's 31-character limit
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:28] + "..."

    # Only store the table if it has at least 21 rows
    if len(temp_df) >= 21:
        # Check if the sheet name already exists
        if sheet_name in separate_tables:
            print(f"Warning: Duplicate sheet name detected - {sheet_name}")

        # Remove the first row since it is missing data.
        temp_df = temp_df.iloc[1:].reset_index(drop=True)  # Reset index to start from 0

        separate_tables[sheet_name] = temp_df

        added_count += 1
    else:
        print(f"\nTable for {sheet_name}:")
        print(temp_df)
        removed_count += 1  # Increment the counter

# Report the number of removed tables
print(f"Initial length of the dataset: {initial_length}") # initial length = 352
print(f"Number of tables removed with less than 21 rows: {removed_count}") # 5 removed
print(f"Number of tables added to dictionary: {added_count}") # 347
print(f"Current number of tables: {len(separate_tables)}") # number of tables = 347



def has_five_sequential_zeros(series):
    """Check if a Pandas Series contains 3 or more sequential zeros."""
    zero_streak = 0
    for value in series:
        if value == 0:
            zero_streak += 1
            if zero_streak >= 3:
                return True
        else:
            zero_streak = 0
    return False

# Find tables to remove based on the sequence condition
tables_to_remove = [key for key, df in separate_tables.items() if has_five_sequential_zeros(df["Simple Return"])]

# Remove the tables from the dictionary
for key in tables_to_remove:
    del separate_tables[key]

# Report the number of tables removed
print(f"Tables removed due to faulty closing prices: {len(tables_to_remove)}")




# Display the separate tables
#for key, table in separate_tables.items():
#    print(f"\nTable for {key}:")
#    print(table)

# Initialize variables to calculate average, max, and min row counts
row_counts = []

# Loop through each dataframe in separate_tables to collect row counts
for df in separate_tables.values():
    row_counts.append(len(df))

# Calculate the average, maximum, and minimum row counts
average_rows = sum(row_counts) / len(row_counts) if row_counts else 0
max_rows = max(row_counts) if row_counts else 0
min_rows = min(row_counts) if row_counts else 0

# Print the number of dataframes and the row count statistics
print(f"Number of dataframes in separate_tables: {len(separate_tables)}")
print(f"Average number of rows: {average_rows}")
print(f"Highest number of rows: {max_rows}")
print(f"Lowest number of rows: {min_rows}")


""" # Export the dataframes to a single pickle file
output_file = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/FINAL_event_returns_per_merger_merged.pkl"
joblib.dump(separate_tables, output_file)
 """



# Export the dataframes to a single Excel file with multiple sheets
output_file = config["FINAL_FILES"]["FINAL_event_returns_per_merger_merged"] 
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, table in separate_tables.items():
        table.to_excel(writer, sheet_name=sheet_name, index=False)


print(f"✅ Data saved to {output_file}")




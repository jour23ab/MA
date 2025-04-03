import pandas as pd
import ast
import re
import statsmodels.api as sm
import configparser
import warnings
import joblib

# Suppress all FutureWarnings globally
warnings.simplefilter(action="ignore", category=FutureWarning)

# Indlæs config fil
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

# Read your Excel file
input_file = config["STOCK_FILES"]["adj_estimation_prices"]
df = pd.read_excel(input_file)

import pandas as pd

##########################################
# First filter the data to only include mergers with good event data.
##########################################

# Step 1: Convert "M&A Announced Date" to datetime and remove time
df["M&A Announced Date"] = pd.to_datetime(df["M&A Announced Date"]).dt.date

# Step 2: Combine "M&A Announced Date" and "Buyers/Investors" into "Announce_acquirer"
df["Announce_acquirer"] = df["M&A Announced Date"].astype(str) + "_" + df["Buyers/Investors"].astype(str)

# Step 3: Check if the 'Announce_acquirer' column is created
print("Columns in df:", df.columns)
print(f"Announce_acquirer column exists: {'Announce_acquirer' in df.columns}")
print(f"The length of the unfiltered dataset is: {len(df)}")

""" # Step 4: Load the Excel file and create a dictionary of DataFrames
excel_file = config["FINAL_FILES"]["FINAL_event_returns_per_merger_merged"]
sheets_dict = pd.read_excel(excel_file, sheet_name=None)  # sheet_name=None reads all sheets 
"""

# Step 4: Load the pickle file containing the dictionary of DataFrames
pickle_file = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/FINAL_event_returns_per_merger_merged.pkl"
sheets_dict = joblib.load(pickle_file)

# Step 5: Create an empty list to store the combined "M&A Announced Date" and "Buyers/Investors"
announce_acquirer_list = []

# Step 6: Loop through each sheet in the dictionary
for sheet_name, sheet_df in sheets_dict.items():
    # Step 6a: Check if both columns exist in the DataFrame
    if "M&A Announced Date" in sheet_df.columns and "Buyers/Investors" in sheet_df.columns:
        # Convert the "M&A Announced Date" to datetime (and remove time) for the sheet
        sheet_df["M&A Announced Date"] = pd.to_datetime(sheet_df["M&A Announced Date"]).dt.date
        
        # Extract the first row values from the two columns
        announce_date = sheet_df["M&A Announced Date"].iloc[0]  # First row of "M&A Announced Date"
        acquirer_name = sheet_df["Buyers/Investors"].iloc[0]  # First row of "Buyers/Investors"
        
        # Combine the values and add to the list
        combined_value = f"{announce_date}_{acquirer_name}"
        announce_acquirer_list.append(combined_value)

# Step 7: Now filter the dataframe containing estimation prices.
# Check if 'Announce_acquirer' exists before filtering
if 'Announce_acquirer' in df.columns:
    df = df[df['Announce_acquirer'].isin(announce_acquirer_list)]
    print("\nFiltered DataFrame based on the list:")
    print(df)
else:
    print("Error: 'Announce_acquirer' column not found in df!")

print(f"The length of the filtered dataframe is: {len(df)}")


################################################
################################################
################################################

# Ensure column is treated as a string
df["Adj Closing Prices Est. Period"] = df["Adj Closing Prices Est. Period"].astype(str)
initial_length = len(df)

# Read the market returns dataset
filsti = r"C:/Users/b407939/Desktop/Speciale/Clean Start/Test output/market_data.xlsx"
market_returns_df = pd.read_excel(filsti)
market_returns_df["Date"] = pd.to_datetime(market_returns_df["Date"]).dt.date  # Ensure datetime format
market_returns_df = market_returns_df[["Date", "Market Simple Return"]]
#print(market_returns_df)

# Read the risk free rate dataset
filsti = r"C:/Users/b407939/Desktop/Speciale/Clean Start/Raw/Cleaned_ECB_Yield.xlsx"
risk_free_yield = pd.read_excel(filsti)
risk_free_yield["Date"] = pd.to_datetime(risk_free_yield["Date"]).dt.date  # Ensure datetime format
risk_free_yield = risk_free_yield[["Date", "Yield Curve Spot Rate"]]
#print(risk_free_yield)

# Read the eu fama french factors for SMB and HML values
filsti = r"C:/Users/b407939/Desktop/Speciale/Clean Start/Raw/Europe_3_Factors_Daily.csv"
fama_french_df = pd.read_csv(filsti, encoding="utf-8")
fama_french_df["Date"] = pd.to_datetime(fama_french_df["Date"], format='%Y%m%d').dt.date  # Ensure datetime format
fama_french_df = fama_french_df[["Date", "SMB", "HML"]]
#print(fama_french_df)

# Function to convert string to dictionary safely
def parse_price_dict(price_str):
    if not isinstance(price_str, str) or not price_str.strip():
        return {}  # Return an empty dictionary for non-string or empty values

    try:
        cleaned_str = re.sub(r"Timestamp\('([^']+)'\)", r"'\1'", price_str)
        return ast.literal_eval(cleaned_str)  # Convert to dictionary
    except (SyntaxError, ValueError):
        return {}  # Return an empty dictionary if parsing fails

# Create a dictionary to store separate DataFrames
separate_tables = {}
removed_count = 0
added_count = 0

# Process each row separately
for index, row in df.iterrows():
    print(f"Processing {row["Buyers/Investors"]}_{row["M&A Announced Date"]}, index is {index}")
    price_dict = parse_price_dict(row["Adj Closing Prices Est. Period"])  # Convert to dict
    
    # Convert the price dictionary into a DataFrame
    temp_df = pd.DataFrame(price_dict.items(), columns=["Date", "Adj Closing Prices Est. Period"])
    temp_df["Date"] = pd.to_datetime(temp_df["Date"]).dt.date  # Ensure datetime format
    
    # Calculate simple returns (returns for each day)
    temp_df["Simple Return"] = temp_df["Adj Closing Prices Est. Period"].pct_change()

    # Add identifying columns
    temp_df["Buyers/Investors"] = row["Buyers/Investors"]
    temp_df["M&A Announced Date"] = row["M&A Announced Date"]
    temp_df["Ticker"] = row["Ticker"]
    
    # Merge with market returns based on date
    temp_df = temp_df.merge(market_returns_df, on="Date", how="left")

    # Merge with risk-free yield based on date
    temp_df = temp_df.merge(risk_free_yield, on="Date", how="left")

    # Merge with Fama-French factors (SMB and HML) based on date
    temp_df = temp_df.merge(fama_french_df, on="Date", how="left")

    # If value missing, replace with the last known non-missing value.
    temp_df["Market Simple Return"] = temp_df["Market Simple Return"].ffill()

    # Calculate excess market return.
    temp_df["Excess Market Return"] = temp_df["Market Simple Return"] - temp_df["Yield Curve Spot Rate"]

    # Create a sanitized sheet name
    sheet_name = f"{row['M&A Announced Date']}_{row['Buyers/Investors']}"
    sheet_name = re.sub(r'[\\/*?:"<>|]', "_", sheet_name)  # Replace invalid characters with "_"
    
    # Truncate sheet name to fit within Excel's 31-character limit
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:28] + "..."
    
    # Only store the table if it has at least 200 rows
    if len(temp_df) >= 200:
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
print(f"Number of tables removed with less than 200 rows: {removed_count}") # 5 removed
print(f"Number of tables added to dictionary: {added_count}") # 347
print(f"Current number of tables: {len(separate_tables)}") # number of tables = 347



# Define the cutoff date
cutoff_date = pd.to_datetime("2024-10-31")

# Find tables to remove
tables_to_remove = []

for key, df in separate_tables.items():
    # Convert 'Date' column to datetime to ensure correct comparison
    df["Date"] = pd.to_datetime(df["Date"])  # Fix: Ensure datetime format
    
    # Check if any date in the column is after the cutoff
    if df["Date"].max() > cutoff_date:
        tables_to_remove.append(key)

# Remove the tables
for key in tables_to_remove:
    del separate_tables[key]

# Report the number of tables removed
print(f"Removed {len(tables_to_remove)} tables due to missing HML and SMB data")






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


""" # Export the dataframes to a single Excel file with multiple sheets
output_file = config["STOCK_FILES"]["est_returns_regression_ready"]
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, table in separate_tables.items():
        table.to_excel(writer, sheet_name=sheet_name, index=False)
"""

# Export the dataframes to a pickle file containing the est_returns_regression_ready file.
output_file = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/est_returns_regression_ready.pkl"
joblib.dump(separate_tables, output_file)

# Each dataframe in separate_tables contains the columns "Simple Return", "Buyers/Investors", "M&A Announced Date", "Excess Market Return", "SMB" and "HML".
# For each dataframe in separate_tables, i want to run a regression that estimates the 3-factor model by Fama and French. 
# So the dependent variable would be "Simple Return" and the explanatory variables would be "Excess Market Return", "SMB" and "HML".


# Print the number of dataframes in the separate_tables dictionary
print(f"Number of dataframes in separate_tables: {len(separate_tables)}")

# Initialize a dictionary to store the regression results for each dataframe
regression_results = {}

# Loop through each dataframe in the separate_tables dictionary
for key, df in separate_tables.items():
    # Drop rows where any of the relevant variables are NaN
    df_clean = df.dropna(subset=['Simple Return', 'Excess Market Return', 'SMB', 'HML'])

    if df_clean.empty:
        print("Data after cleaning is empty, skipping regression.")
    else:
        # Define the dependent variable (Simple Return) and explanatory variables
        Y = df_clean['Simple Return']
        X = df_clean[['Excess Market Return', 'SMB', 'HML']]

        # Add a constant to the independent variables matrix (for the intercept)
        X = sm.add_constant(X)
        
        print(f"Size of Y: {len(Y)}. Size of X: {len(X)}")
        if len(Y) == 0 or len(X) == 0:
            print(f"Data is empty, skipping regression for this dataset. Key: {key}")
        else:
            model = sm.OLS(Y, X).fit()

            # Convert the regression summary to a DataFrame for easier export
            result_df = pd.read_html(model.summary().tables[1].as_html())[0]
            
            # Create a sanitized sheet name
            df["M&A Announced Date"] = pd.to_datetime(df["M&A Announced Date"], errors="coerce")  # Ensure datetime format
            df['M&A Announced Date'] = df['M&A Announced Date'].dt.date
            sheet_name = f"{df['M&A Announced Date'].iloc[0]}_{df['Buyers/Investors'].iloc[0]}"
            sheet_name = re.sub(r'[\\/*?:"<>|]', "_", sheet_name)  # Replace invalid characters with "_"
            
            # Truncate sheet name to fit within Excel's 31-character limit
            if len(sheet_name) > 31:
                sheet_name = sheet_name[:28] + "..."    

            # Store the DataFrame in the regression_results dictionary
            regression_results[sheet_name] = result_df

""" # Now we can export the results to an Excel file
output_file = config["FINAL_FILES"]["FINAL_regression_results"]
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, result_df in regression_results.items():
        # Write each regression result to its own sheet
        result_df.to_excel(writer, sheet_name=sheet_name, index=False) 
"""

# Export the dataframes to a single pickle file
output_file = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/FINAL_regression_results.pkl"
joblib.dump(regression_results, output_file)

print(f"Regression results have been successfully exported to {output_file}")

import pandas as pd
import ast
import re

# Read your Excel file
df = pd.read_excel(r"C:\Users\b407939\Desktop\Speciale\Clean Start\Test output/raw_v2_adj_event_and_estimation_prices.xlsx")

# Remove rows where "Adj Closing Prices" is empty (NaN)
df = df.dropna(subset=["Adj Closing Prices"])

# Ensure column is treated as a string
df["Adj Closing Prices"] = df["Adj Closing Prices"].astype(str)

# Function to convert string to dictionary safely
def parse_price_dict(price_str):
    cleaned_str = re.sub(r"Timestamp\('([^']+)'\)", r"'\1'", price_str)
    return ast.literal_eval(cleaned_str)  # Convert to dictionary

# Create a dictionary to store separate DataFrames
separate_tables = {}

# Process each row separately
for index, row in df.iterrows():
    price_dict = parse_price_dict(row["Adj Closing Prices"])  # Convert to dict
    
    temp_df = pd.DataFrame(price_dict.items(), columns=["Date", "Adj Closing Price"])
    temp_df["Date"] = pd.to_datetime(temp_df["Date"])  # Ensure datetime format
    
    # Add identifying columns
    temp_df["Acquirer Name"] = row["Acquirer Name"]
    temp_df["Announce Date"] = row["Announce Date"]
    temp_df["Ticker"] = row["Ticker"]
    
    # Create a sanitized sheet name
    sheet_name = f"{row['Acquirer Name']}_{row['Announce Date']}"
    sheet_name = re.sub(r'[\\/*?:"<>|]', "_", sheet_name)  # Replace invalid characters with "_"
    
    # Truncate sheet name to fit within Excel's 31-character limit
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:28] + "..."  # Truncate and add ellipsis

    # Store DataFrame in dictionary using sanitized sheet name
    separate_tables[sheet_name] = temp_df

# Display the separate tables
for key, table in separate_tables.items():
    print(f"\nTable for {key}:")
    print(table)

# Export the dataframes to a single Excel file with multiple sheets
output_file = r"C:\Users\b407939\Desktop\Speciale\Clean Start\Test output/event_stock_prices_per_merger.xlsx" 
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, table in separate_tables.items():
        table.to_excel(writer, sheet_name=sheet_name, index=False)

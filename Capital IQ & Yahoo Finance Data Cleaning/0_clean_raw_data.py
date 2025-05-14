import pandas as pd
import re
import os
import configparser


# Indlæs config fil
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

# List of CSV file paths
file_paths = [
    config["RAW"]["raw_input"],
]

# Function to clean a single file
def clean_data(file_path):
    try:
        # Load the CSV file
        df = pd.read_excel(file_path)

        # Record the number of rows before filtering
        initial_row_count = len(df)

        # Remove unnecessary columns
        df = df.drop(columns=["Transaction Types", "All Transactions Announced Date", 
                              "Exchange:Ticker", "Security Tickers [Buyers/Investors]", 
                              "Transaction Comments"])

        # Remove "(primary)" from the columns Geographic Locations [Target/Issuer] and Geographic Locations [Buyers/Investors]
        pattern = r'\(Primary\)'  # Matches the exact string "(primary)"
        if 'Geographic Locations [Target/Issuer]' in df.columns:
            df['Geographic Locations [Target/Issuer]'] = df['Geographic Locations [Target/Issuer]'].astype(str).str.replace(pattern, '', regex=True)
        else:
            print(f"'Geographic Locations [Target/Issuer]' column not found in {file_path}")

        if 'Geographic Locations [Buyers/Investors]' in df.columns:
            df['Geographic Locations [Buyers/Investors]'] = df['Geographic Locations [Buyers/Investors]'].astype(str).str.replace(pattern, '', regex=True)
        else:
            print(f"'Geographic Locations [Buyers/Investors]' column not found in {file_path}")

        # Remove rows with multiple acquireres
        df = df[df["Company Type [Buyers/Investors]"] == "Public Company"]
        
        # Record the number of rows after filtering
        current_row_count = len(df)
        rows_removed_acq = initial_row_count - current_row_count

        # Remove rows with no transaction value 
        df = df[df["Total Transaction Value (€EURmm, Historical rate)"] != "-"]
        
        # Record the number of rows after filtering
        final_row_count = len(df)
        rows_removed_val = current_row_count - final_row_count

        # Remove the time from the Announcement date column
        df["M&A Announced Date"] = df["M&A Announced Date"].dt.date 

        # Remove all parentheses and their contents
        df['Buyers/Investors'] = df['Buyers/Investors'].str.replace(r'\s*\(.*?\)', '', regex=True)
        
        # Save the cleaned data to a new Excel file
        base_name = os.path.basename(file_path).replace('_preprocessed.xlsx', '_cleaned.xlsx')
        output_dir = os.path.dirname(file_path)
        cleaned_file_path = os.path.join(output_dir, base_name)

        df.to_excel(cleaned_file_path, index=False)

        print(f"✅ Cleaned data saved to: {cleaned_file_path}")
        print(f"Rows with multiple acquirers removed from {file_path}: {rows_removed_acq}\n")
        print(f"Rows with no transaction value data removed from {file_path}: {rows_removed_val}\n")
        print(f"Current amount of rows: {len(df)}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}\n")

# Loop through each file and clean it
for file_path in file_paths:
    clean_data(file_path)

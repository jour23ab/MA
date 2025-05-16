# Merge the Bloomberg variables onto the CAR values.

import pandas as pd
import configparser
import os

# Get the directory where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the config file
config_path = os.path.join(base_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

# Resolve full paths using config and base_dir
file1 = os.path.join(base_dir, config["FINAL_FILES"]["car_values"])
file2 = os.path.join(base_dir, config["CLEANED_FILES"]["no_overlapping"])

# Load the Excel files
cars = pd.read_excel(file1)
bloom_vars = pd.read_excel(file2)

print(cars)
print(bloom_vars)

merged_df = pd.merge(cars, bloom_vars, how="inner", on=["M&A Announced Date", "Buyers/Investors"])

print(merged_df)

# Resolve full output path from config
output_path = os.path.join(base_dir, config["FINAL_FILES"]["merged_cars"])

# Save the DataFrame
merged_df.to_excel(output_path, index=False)

print(f"✅ Successfully exported to: {output_path}")
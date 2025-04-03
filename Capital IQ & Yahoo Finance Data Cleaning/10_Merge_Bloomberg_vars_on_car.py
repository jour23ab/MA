# Merge the Bloomberg variables onto the CAR values.

import pandas as pd
import configparser

# Load config file
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

file1 =config["FINAL_FILES"]["car_values"]
file2 = config["CLEANED_FILES"]["no_overlapping"]

cars = pd.read_excel(file1)
bloom_vars = pd.read_excel(file2)

print(cars)
print(bloom_vars)

merged_df = pd.merge(cars, bloom_vars, how="inner", on=["M&A Announced Date", "Buyers/Investors"])

print(merged_df)

output1 = config["FINAL_FILES"]["merged_cars"]

merged_df.to_excel(output1, index=False)
print(f"Succesfully exported to: {output1}")
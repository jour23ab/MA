import pandas as pd
import configparser
import warnings
import joblib

# Suppress all FutureWarnings globally
warnings.simplefilter(action="ignore", category=FutureWarning)

# Load config file
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

""" # File paths
file1 = config["FINAL_FILES"]["FINAL_regression_results"]
file2 = config["FINAL_FILES"]["FINAL_event_returns_per_merger_merged"]

# Load all sheets into dictionaries
regression_results_dict = pd.read_excel(file1, sheet_name=None)
event_values_dict = pd.read_excel(file2, sheet_name=None) """

# File paths
pickle_file1 = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/FINAL_regression_results.pkl"
pickle_file2 = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/FINAL_event_returns_per_merger_merged.pkl"

# Load all pickle dictionaries into dictionaries
regression_results_dict = joblib.load(pickle_file1)
event_values_dict = joblib.load(pickle_file2)

# reporting variable
faulty_data = 0

# Loop through each sheet in event_values_dict
for sheet_name, values_df in event_values_dict.items():
    if sheet_name in regression_results_dict:  # Ensure a matching regression sheet exists
        regression_df = regression_results_dict[sheet_name]  # Get the corresponding regression results

        # Ensure regression_df has at least 2 rows and 5 columns
        if regression_df.shape[0] > 1 and regression_df.shape[1] > 4:

            # Extract coefficients and ensure they are numeric
            constant = pd.to_numeric(regression_df.iloc[1, 1], errors="coerce")  # Constant
            beta_mkt = pd.to_numeric(regression_df.iloc[1, 2], errors="coerce")  # Market factor coefficient
            beta_smb = pd.to_numeric(regression_df.iloc[1, 3], errors="coerce")  # SMB coefficient
            beta_hml = pd.to_numeric(regression_df.iloc[1, 4], errors="coerce")  # HML coefficient



            # Convert the necessary columns in values_df to numeric
            required_cols = ["Excess Market Return", "SMB", "HML"]
            for col in required_cols:
                if col in values_df.columns:
                    values_df[col] = pd.to_numeric(values_df[col], errors="coerce")  # Force conversion to numeric
                    values_df[col].fillna(0, inplace=True)  # Replace NaN with 0 for multiplication

            # Compute Expected Return
            values_df["Expected Return"] = (
                constant +
                beta_mkt * values_df["Excess Market Return"] +
                beta_smb * values_df["SMB"] +
                beta_hml * values_df["HML"]
            )

            values_df["Abnormal Return"] = values_df["Simple Return"] + values_df["Expected Return"] # Expected return can be negative which is why we use "+".

            # Update dictionary with modified dataframe
            event_values_dict[sheet_name] = values_df  # Update dictionary
        else:
            print(f"Warning: Not enough rows/columns in regression results for '{sheet_name}'")
    else:
        print(f"Warning: No matching regression results found for sheet '{sheet_name}'")
        faulty_data = faulty_data + 1

print(f"Mergers without enough estimation period data: {faulty_data}")
print(f"Length of event values dictionary: {len(event_values_dict)}")
print(f"Length of regression results dictionary: {len(regression_results_dict)}")
# The difference between these two is because there wasn't enough estimation period data
# and therefore the regression results were not... im not quite sure. I think the previous file is the culprit
# That file removed some rows based on it not having enough data for regressing. Thats why regression results dict
# has fewer values. (I think)

""" output_file = config["FINAL_FILES"]["abnormal_returns"]

# Export the updated dictionary to an Excel file with each dataframe as a separate sheet
with pd.ExcelWriter(output_file) as writer:
    for sheet_name, df in event_values_dict.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)  # Export each sheet as a separate dataframe
"""
# Export the updated dictionary to a pickle file as a dictionary
output_file = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/abnormal_returns.pkl"
joblib.dump(event_values_dict, output_file)

print(f"Exported updated data to {output_file}")
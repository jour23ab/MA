import configparser
import os
import pandas as pd

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Build the path to the config.ini file
config_path = os.path.join(base_dir, "config.ini")

# Load the config file
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

# Example: Load the merged macro dataset
merged_data_path = os.path.join(base_dir, config['MACRO_FILES']['merged_data'])
df = pd.read_excel(merged_data_path)

# Convert date columns to datetime format
df['Start Date (Event)'] = pd.to_datetime(df['Start Date (Event)'], errors='coerce').dt.date
df['End Date (Event)'] = pd.to_datetime(df['End Date (Event)'], errors='coerce').dt.date

df['Start Date (Estimation)'] = pd.to_datetime(df['Start Date (Estimation)'], errors='coerce').dt.date
df['End Date (Estimation)'] = pd.to_datetime(df['End Date (Estimation)'], errors='coerce').dt.date

# Sort by Acquirer and Start Date
df = df.sort_values(by=['Buyers/Investors', 'Start Date (Event)']).reset_index(drop=True)

# Identify overlapping events
overlap_indices = set()
overlap_report = {}

# Group by Acquirer Name
for acquirer, group in df.groupby('Buyers/Investors'):
    for i in range(len(group) - 1):
        current_event = group.iloc[i]
        next_event = group.iloc[i + 1]
        
        # Check for overlap
        if current_event['End Date (Event)'] >= next_event['Start Date (Event)']:
            # Add indices of overlapping rows
            overlap_indices.add(current_event.name)
            overlap_indices.add(next_event.name)
            
            # Track overlaps per acquirer
            if acquirer not in overlap_report:
                overlap_report[acquirer] = 2  # First overlap adds 2 events
            else:
                overlap_report[acquirer] += 1  # Subsequent overlaps add 1 event

# Remove overlapping events
df_cleaned = df.drop(index=overlap_indices).reset_index(drop=True)

# Get the relative path from config and build full path
output_path = os.path.join(base_dir, config['CLEANED_FILES']['no_overlapping'])

# Save the cleaned dataset
df_cleaned.to_excel(output_path, index=False)

# Reporting
print(f"✅ Cleaned data saved to: {output_path}")
print(f"❌ Number of overlapping events removed: {len(overlap_indices)}")
print(f"Final row count for non-overlapping events: {len(df_cleaned)}")

# Overlap report by acquirer
print("\n📊 Overlapping Events Report:")
for acquirer, count in overlap_report.items():
    print(f"- {acquirer}: {count} overlapping events")

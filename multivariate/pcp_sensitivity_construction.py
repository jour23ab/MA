import os
import pandas as pd
import datetime as dt
import re
import numpy as np


# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

ma_dir = os.path.dirname(current_dir)

# Set it as the working directory
os.chdir(ma_dir)

# Confirm
print("Working directory set to:", os.getcwd())

# Reading the Excel files
filsti = f"{ma_dir}/data/final/Final_CAR_analysis_ready_1_with_target_type.xlsx"
df = pd.read_excel(filsti)







filsti = f"{ma_dir}/data/processed/2000-2025.xls"
df_full = pd.read_excel(filsti)

# Step 1: Prepare full dataset
df_full['M&A Announced Date'] = pd.to_datetime(df_full['M&A Announced Date'])
df_full['Buyers/Investors'] = df_full['Buyers/Investors'].str.replace(r'\s*\(.*?\)', '', regex=True)
        
df_full = df_full.sort_values(by=['Buyers/Investors', 'M&A Announced Date'])


# Define event windows and horizon options
event_windows = {
    "10": "[-10, 10]",
    "7": "[-7, 7]",
    "5": "[-5, 5]",
    "3": "[-3, 3]",
    "1": "[-1, 1]"
}

lookback_years = [1, 2, 3, 4, 5]

# Function to compute rolling positive CAR %
def compute_running_positive_CAR(group, col, horizon_years):
    result = []
    dates = group['M&A Announced Date']
    for i in range(len(group)):
        current_date = dates.iloc[i]
        horizon_start = current_date - pd.Timedelta(days=365 * horizon_years)
        prev = group.iloc[:i]
        prev_in_horizon = prev[prev['M&A Announced Date'] >= horizon_start]
        pct = (prev_in_horizon[col] > 0).sum() / len(prev_in_horizon) if len(prev_in_horizon) > 0 else 0
        result.append(pct)
    return pd.Series(result, index=group.index)

# Create PCP variables for each combination of event window and horizon
for ew_label, col_name in event_windows.items():
    for horizon in lookback_years:
        new_col = f'pcp_{ew_label}d_{horizon}yr'
        df[new_col] = df.groupby('Buyers/Investors', group_keys=False).apply(
            lambda g: compute_running_positive_CAR(g, col_name, horizon)
        )


# Save result
output = f"{ma_dir}/data/final/pcp_sensitivity_dataset_test2.xlsx"
df.to_excel(output, index=False)



def count_firms_with_prior_mergers_extended(df, lookback_years):
    results = []
    df['M&A Announced Date'] = pd.to_datetime(df['M&A Announced Date'])
    df = df.sort_values(by=['Buyers/Investors', 'M&A Announced Date'])

    for horizon in lookback_years:
        horizon_name = f'{horizon}yr'
        counts = {'Horizon': horizon_name, '1+ M&As': 0, '2+ M&As': 0, '3+ M&As': 0}
        unique_firms = df['Buyers/Investors'].unique()

        for firm in unique_firms:
            firm_deals = df[df['Buyers/Investors'] == firm]
            firm_deals = firm_deals.sort_values('M&A Announced Date')
            max_prior_mergers = 0

            for i in range(1, len(firm_deals)):
                current_date = firm_deals.iloc[i]['M&A Announced Date']
                prior_date = current_date - pd.Timedelta(days=365 * horizon)
                past_deals = firm_deals[firm_deals['M&A Announced Date'] < current_date]
                past_in_horizon = past_deals[past_deals['M&A Announced Date'] >= prior_date]
                num_past = len(past_in_horizon)

                if num_past > max_prior_mergers:
                    max_prior_mergers = num_past

            if max_prior_mergers >= 1:
                counts['1+ M&As'] += 1
            if max_prior_mergers >= 2:
                counts['2+ M&As'] += 1
            if max_prior_mergers >= 3:
                counts['3+ M&As'] += 1

        results.append(counts)

    return pd.DataFrame(results)

# Use the simulated df_full
lookback_years = [1, 2, 3, 4, 5]
extended_counts = count_firms_with_prior_mergers_extended(df, lookback_years)

#print(extended_counts)

def rowwise_merger_counts(df, lookback_years):
    df['M&A Announced Date'] = pd.to_datetime(df['M&A Announced Date'])
    df = df.sort_values(by=['Buyers/Investors', 'M&A Announced Date'])

    results = []

    for horizon in lookback_years:
        firm_with_mergers = set()
        counts_by_firm = {}

        for firm, firm_deals in df.groupby('Buyers/Investors'):
            firm_deals = firm_deals.sort_values('M&A Announced Date')
            for i in range(1, len(firm_deals)):
                current_date = firm_deals.iloc[i]['M&A Announced Date']
                prior_date = current_date - pd.Timedelta(days=365 * horizon)
                past_deals = firm_deals[firm_deals['M&A Announced Date'] < current_date]
                past_in_horizon = past_deals[past_deals['M&A Announced Date'] >= prior_date]
                num_past = len(past_in_horizon)
                if num_past > 0:
                    firm_with_mergers.add(firm)
                    counts_by_firm[firm] = max(counts_by_firm.get(firm, 0), num_past)

        # Aggregate number of firms with at least N prior mergers
        summary = {'Horizon': f'{horizon}yr'}
        for n in range(1, 6):
            summary[f'{n}+ M&As'] = sum(1 for v in counts_by_firm.values() if v >= n)

        results.append(summary)

    return pd.DataFrame(results)

lookback_years = [1, 2, 3, 4, 5]
rowwise_summary = rowwise_merger_counts(df, lookback_years)

print(rowwise_summary)
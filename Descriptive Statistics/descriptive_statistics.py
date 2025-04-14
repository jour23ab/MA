continuous_vars = [
    '[-10, 10]', '[-7, 7]', '[-5, 5]', '[-3, 3]', '[-1, 1]',
    'Total Transaction Value (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Revenue (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - EBITDA (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Net Income (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Debt (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Assets (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Common Equity (at Announcement) (€EURmm, Historical rate)',
    'Acquirer Market Cap 1-Day Prior (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)',
    'running_positive_CAR_percentage_10', 'running_positive_CAR_percentage_7',
    'running_positive_CAR_percentage_5', 'running_positive_CAR_percentage_3',
    'running_positive_CAR_percentage_1', 'gdp_lag1_tgt', 'Revenue', 'EBITDA',
    'Earnings', 'Debt', 'TotalAssets', 'CommonEquity', 'MarketCap',
    'Cash_and_Equivalents', 'Size', 'BookEquity', 'MtoB', 'DtoE',
    'StoMC', 'StoE', 'StoC', 'Margin'
]


import pandas as pd
import os


# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

ma_dir = os.path.dirname(current_dir)

# Set it as the working directory
os.chdir(ma_dir)

# Confirm
print("Working directory set to:", os.getcwd())

# Load your Excel file
filsti = f"{ma_dir}/data/processed/CAR_v5_extra_vars_cleaned.xlsx"
df = pd.read_excel(filsti)


# Select only the continuous columns
continuous_df = df[continuous_vars]

# Calculate descriptive stats
desc_stats = continuous_df.describe().T[['count', 'mean', 'std', 'min', '50%', 'max']]
desc_stats.rename(columns={'50%': 'median'}, inplace=True)

# Optionally round for cleaner presentation
desc_stats = desc_stats.round(3)

# Export to Excel
desc_stats.to_excel(f"{ma_dir}/Descriptive Statistics/continuous_descriptive_stats.xlsx")

# Display the resulting DataFrame
print(desc_stats)
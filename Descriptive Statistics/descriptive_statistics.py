import os
import pandas as pd

# Define variables in structured order
ordered_vars = [
    # CARs
    '[-1, 1]', '[-3, 3]', '[-5, 5]', '[-7, 7]', '[-10, 10]',
    
    # Deal info
    'Total Transaction Value (€EURmm, Historical rate)',

    # Acquirer Financials
    'Acquirer LTM Financials - Total Revenue (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - EBITDA (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Net Income (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Debt (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Assets (at Announcement) (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Common Equity (at Announcement) (€EURmm, Historical rate)',
    'Acquirer Market Cap 1-Day Prior (€EURmm, Historical rate)',
    'Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)',

    # Running CAR benchmarks
    'running_positive_CAR_percentage_10', 'running_positive_CAR_percentage_7',
    'running_positive_CAR_percentage_5', 'running_positive_CAR_percentage_3',
    'running_positive_CAR_percentage_1', 'gdp_lag1_tgt',

    # Financial indicators
    'Revenue', 'EBITDA', 'Earnings', 'Debt', 'TotalAssets', 'CommonEquity',
    'MarketCap', 'Cash_and_Equivalents', 'Size', 'BookEquity',

    # Ratios
    'MtoB', 'DtoE', 'StoMC', 'StoE', 'StoC', 'Margin'
]

# Map to nice display names
variable_names = {
    '[-1, 1]': '1-day CAR',
    '[-3, 3]': '3-day CAR',
    '[-5, 5]': '5-day CAR',
    '[-7, 7]': '7-day CAR',
    '[-10, 10]': '10-day CAR',
    'Total Transaction Value (€EURmm, Historical rate)': 'Deal value (EUR million)',
    'Acquirer LTM Financials - Total Revenue (at Announcement) (€EURmm, Historical rate)': 'Acquirer revenue',
    'Acquirer LTM Financials - EBITDA (at Announcement) (€EURmm, Historical rate)': 'Acquirer EBITDA',
    'Acquirer LTM Financials - Net Income (at Announcement) (€EURmm, Historical rate)': 'Acquirer net income',
    'Acquirer LTM Financials - Total Debt (at Announcement) (€EURmm, Historical rate)': 'Acquirer total debt',
    'Acquirer LTM Financials - Total Assets (at Announcement) (€EURmm, Historical rate)': 'Acquirer total assets',
    'Acquirer LTM Financials - Total Common Equity (at Announcement) (€EURmm, Historical rate)': 'Acquirer common equity',
    'Acquirer Market Cap 1-Day Prior (€EURmm, Historical rate)': 'Acquirer market cap',
    'Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)': 'Acquirer cash & ST investments',
    'running_positive_CAR_percentage_10': 'CAR > 0 (%), 10d window',
    'running_positive_CAR_percentage_7': 'CAR > 0 (%), 7d window',
    'running_positive_CAR_percentage_5': 'CAR > 0 (%), 5d window',
    'running_positive_CAR_percentage_3': 'CAR > 0 (%), 3d window',
    'running_positive_CAR_percentage_1': 'CAR > 0 (%), 1d window',
    'gdp_lag1_tgt': 'Target GDP growth (t-1)',
    'Revenue': 'Target revenue',
    'EBITDA': 'Target EBITDA',
    'Earnings': 'Target earnings',
    'Debt': 'Target debt',
    'TotalAssets': 'Target total assets',
    'CommonEquity': 'Target common equity',
    'MarketCap': 'Target market cap',
    'Cash_and_Equivalents': 'Target cash & equivalents',
    'Size': 'Relative size (target/acquirer)',
    'BookEquity': 'Target book equity',
    'MtoB': 'Market-to-book',
    'DtoE': 'Debt-to-equity',
    'StoMC': 'Sales-to-market cap',
    'StoE': 'Sales-to-equity',
    'StoC': 'Sales-to-cash',
    'Margin': 'EBITDA margin'
}

# Set up working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# Load data
filsti = os.path.join(ma_dir, "data", "processed", "CAR_v5_extra_vars_cleaned.xlsx")
df = pd.read_excel(filsti)

# Create descriptive stats
stats = df[ordered_vars].describe().T[['mean', '50%', 'std', 'min', 'max', 'count']]
stats.rename(columns={'50%': 'median', 'std': 'Std. Dev.', 'count': 'Obs'}, inplace=True)
stats.index.name = 'Variable'
stats = stats[['mean', 'median', 'Std. Dev.', 'min', 'max', 'Obs']].round(3)

# Reset index and map display names
stats.reset_index(inplace=True)
stats['Variable'] = stats['Variable'].map(variable_names).fillna(stats['Variable'])

# Export
out_path = os.path.join(ma_dir, "Descriptive Statistics", "continuous_descriptive_stats_v2.xlsx")
stats.to_excel(out_path, index=False)

print("✔ Descriptive statistics table saved to:", out_path)

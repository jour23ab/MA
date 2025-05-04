import os
import pandas as pd

# Define variables in structured order
ordered_vars = [
    # CARs
    '[-1, 1]', '[-3, 3]', '[-5, 5]', '[-7, 7]', 'CAR_10_wins',
    
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
    'PCP10', 'PCP7',
    'PCP5', 'PCP3',
    'PCP1', 'GDPG',

    # Financial indicators
    'Revenue', 'EBITDA', 'Earnings', 'Debt', 'TotalAssets', 'CommonEquity',
    'MarketCap', 'CashAndEquivalents', 'Size', 'BookEquity',

    # Ratios
    'MtoB', 'DtoE', 'StoMC', 'StoC', 'Margin'
]

# Map to nice display names
variable_names = {
    '[-1, 1]': '1-day CAR',
    '[-3, 3]': '3-day CAR',
    '[-5, 5]': '5-day CAR',
    '[-7, 7]': '7-day CAR',
    'CAR_10_wins': '10-day CAR',
    'Total Transaction Value (€EURmm, Historical rate)': 'Deal value (EUR million)',
    'Acquirer LTM Financials - Total Revenue (at Announcement) (€EURmm, Historical rate)': 'Acquirer revenue',
    'Acquirer LTM Financials - EBITDA (at Announcement) (€EURmm, Historical rate)': 'Acquirer EBITDA',
    'Acquirer LTM Financials - Net Income (at Announcement) (€EURmm, Historical rate)': 'Acquirer net income',
    'Acquirer LTM Financials - Total Debt (at Announcement) (€EURmm, Historical rate)': 'Acquirer total debt',
    'Acquirer LTM Financials - Total Assets (at Announcement) (€EURmm, Historical rate)': 'Acquirer total assets',
    'Acquirer LTM Financials - Total Common Equity (at Announcement) (€EURmm, Historical rate)': 'Acquirer common equity',
    'Acquirer Market Cap 1-Day Prior (€EURmm, Historical rate)': 'Acquirer market cap',
    'Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)': 'Acquirer cash & ST investments',
    'PCP10': 'CAR > 0 (%), 10d window',
    'PCP7': 'CAR > 0 (%), 7d window',
    'PCP5': 'CAR > 0 (%), 5d window',
    'PCP3': 'CAR > 0 (%), 3d window',
    'PCP1': 'CAR > 0 (%), 1d window',
    'GDPG': 'Target GDP growth (t-1)',
    'Revenue': 'Acquirer revenue',
    'EBITDA': 'Acquirer EBITDA',
    'Earnings': 'Acquirer earnings',
    'Debt': 'Acquirer debt',
    'TotalAssets': 'Acquirer total assets',
    'CommonEquity': 'Acquirer common equity',
    'MarketCap': 'Acquirer market cap',
    'CashAndEquivalents': 'Acquirer cash & equivalents',
    'Size': 'Relative size (deal value / acquirer)',
    'BookEquity': 'Acquirer book equity',
    'MtoB': 'Market-to-book',
    'DtoE': 'Debt-to-equity',
    'StoMC': 'Sales-to-market cap',
    'StoC': 'Sales-to-cash',
    'Margin': 'EBITDA margin'
}

# Set up working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# Load data
filsti = os.path.join(ma_dir, "data", "final", "graph_data.xlsx")
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

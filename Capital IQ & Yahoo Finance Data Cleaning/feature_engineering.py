import pandas as pd

file = "C:/Users/b407939/Desktop/Speciale/Capital IQ/Test output/CAR_analysis_ready_ML_part_1.xlsx"
df = pd.read_excel(file)

# Renaming columns for easier use
df = df.rename(columns={
    "Acquirer LTM Financials - Total Revenue (at Announcement) (€EURmm, Historical rate)": "acquirer_revenue",
    "Acquirer LTM Financials - EBITDA (at Announcement) (€EURmm, Historical rate)": "acquirer_ebitda",
    "Acquirer LTM Financials - Net Income (at Announcement) (€EURmm, Historical rate)": "acquirer_net_income",
    "Acquirer LTM Financials - Total Debt (at Announcement) (€EURmm, Historical rate)": "acquirer_debt",
    "Acquirer LTM Financials - Total Assets (at Announcement) (€EURmm, Historical rate)": "acquirer_assets",
    "Acquirer LTM Financials - Total Common Equity (at Announcement) (€EURmm, Historical rate)": "acquirer_equity",
    "Acquirer Market Cap 1-Day Prior (€EURmm, Historical rate)": "acquirer_market_cap",
    "Acquirer LTM Financials - Total Cash & ST Investments (at Announcement) (€EURmm, Historical rate)": "acquirer_cash_and_investments",
    "Total Transaction Value (€EURmm, Historical rate)": "transaction_value",
    "Consideration Offered": "payment_type",
    "Geographic Locations [Buyers/Investors]": "acquirer_country",
    "Geographic Locations [Target/Issuer]": "target_country",
    "Primary Sector [Buyers/Investors]": "acquirer_sector",
    "Primary Sector [Target/Issuer]": "target_sector"
})

# Remove rows with empty or zero values for key financial metrics
def clean_column(df, column_name):
    return df[df[column_name] != "-"]

# Add another function to filter out rows where any key metric is 0
def remove_zero_values(df, column_name):
    return df[df[column_name] != 0]

# Clean the dataframe
columns_to_clean = [
    "transaction_value",
    "acquirer_revenue",
    "acquirer_ebitda",
    "acquirer_net_income",
    "acquirer_debt",
    "acquirer_assets",
    "acquirer_equity",
    "acquirer_market_cap",
    "acquirer_cash_and_investments",
    "Primary Sector [Buyers/Investors]"
]

# Apply cleaning function to each column
for column in columns_to_clean:
    df = clean_column(df, column)
    print(f"Remaining rows after cleaning {column}: {len(df)}")

# Define the key metrics columns that need to have zero values removed
key_columns = [
    "acquirer_revenue",
    "acquirer_ebitda",
    "acquirer_net_income",
    "acquirer_debt",
    "acquirer_assets",
    "acquirer_equity",
    "acquirer_market_cap",
    "acquirer_cash_and_investments",
    "transaction_value"
]

# Apply remove_zero_values function to each key metric column
for column in key_columns:
    df = remove_zero_values(df, column)
    print(f"Remaining rows after removing zero values from {column}: {len(df)}")

# Create ratios
df["ebitda_to_rev"] = df["acquirer_ebitda"] / df["acquirer_revenue"]
df["net_inc_margin"] = df["acquirer_net_income"] / df["acquirer_revenue"]
df["return_on_asset"] = df["acquirer_net_income"] / df["acquirer_assets"]
df["return_on_equity"] = df["acquirer_net_income"] / df["acquirer_equity"]
df["asset_turnover"] = df["acquirer_revenue"] / df["acquirer_assets"]
df["debt_to_equity"] = df["acquirer_debt"] / df["acquirer_equity"]
df["debt_to_assets"] = df["acquirer_debt"] / df["acquirer_assets"]
df["ebitda_to_debt"] = df["acquirer_ebitda"] / df["acquirer_debt"]
df["cash_to_debt"] = df["acquirer_cash_and_investments"] / df["acquirer_debt"]
df["cash_to_assets"] = df["acquirer_cash_and_investments"] / df["acquirer_assets"]
df["ev_to_ebitda"] = df["acquirer_market_cap"] / df["acquirer_ebitda"]
df["market_cap_to_rev"] = df["acquirer_market_cap"] / df["acquirer_revenue"]
df["deal_size_to_rev"] = df["transaction_value"] / df["acquirer_revenue"]

# Print out the df to inspect the results
print(df)

# Make the cross-border variable
df["cross_border"] = (df["acquirer_country"] != df["target_country"]).astype(int)

# Make the cross-sector variable
df["cross_sector"] = (df["acquirer_sector"] != df["target_sector"]).astype(int)




# ML model notes:

# Target variable is df["[-5, 5]"] (this is the 5-day CAR)

# features are:
# cross_border, cross_sector,  payment_type, ebitda_to_rev, net_income_margin,
# return_on_equity, asset_turnover, debt_to_equity, debt_to_assets
# ebitda_to_debt, cash_to_debt, cash_to_assets, ev_to_ebitda,
# market_cap_to_rev, deal_size_to_rev


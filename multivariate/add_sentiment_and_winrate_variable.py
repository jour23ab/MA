import os
import pandas as pd
import datetime as dt

# Get the directory where the current script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

ma_dir = os.path.dirname(current_dir)

# Set it as the working directory
os.chdir(ma_dir)

# Confirm
print("Working directory set to:", os.getcwd())

##############################################
# Add bull-bear-spread (sentiment) variable
##############################################


# Reading the Excel files
filsti = f"{ma_dir}/data/processed/CAR_v5.xlsx"
df = pd.read_excel(filsti)

inv_sentiment_sti = f"{ma_dir}/data/processed/sentiment.xls"
sentiment = pd.read_excel(inv_sentiment_sti)

# Ensure the 'Date' column is in datetime format
sentiment["Date"] = pd.to_datetime(sentiment["Date"])

# Convert to date-only format
sentiment["Date"] = sentiment["Date"].dt.date

# Filter sentiment data to include only dates after January 1st, 2003
sentiment = sentiment[sentiment["Date"] > dt.date(2003, 1, 1)]

# Ensure both 'M&A Announced Date' and 'Date' are in datetime format
df['M&A Announced Date'] = pd.to_datetime(df['M&A Announced Date'])
sentiment['Date'] = pd.to_datetime(sentiment['Date'])

# Calculate the weekly returns
#sentiment['S&P 500 Weekly Return'] = sentiment['S&P 500 Weekly Close'].pct_change() * 100 # prob not good to have in the model. Would rather have EUR STOXX 600.

# Sort the data by date to ensure that the closest previous date is found
df = df.sort_values(by='M&A Announced Date')
sentiment = sentiment.sort_values(by='Date')

# Perform an as-of merge to get the closest previous Date
df = pd.merge_asof(df, sentiment, left_on='M&A Announced Date', right_on='Date', direction='backward')

# Check the result
df = (df.drop(columns=["Bullish 8-week Mov Avg", 
                       "S&P 500 Weekly High", 
                       "S&P 500 Weekly Low", 
                       "Total", 
                       "S&P 500 Weekly Close", 
                       "Date", 
                       "Bullish", 
                       "Bearish", 
                       "Neutral"
                    ])
                    .rename(columns={"Bull-Bear Spread": "Bull_Bear_Spread"})
)

print(df)

##############################################
# Add running winrate variable
##############################################


import pandas as pd
filsti = f"{ma_dir}/data/processed/2000-2025.xls"
df_full = pd.read_excel(filsti)


# Step 1: Prepare full dataset
df_full['M&A Announced Date'] = pd.to_datetime(df_full['M&A Announced Date'])
df_full['Buyers/Investors'] = df_full['Buyers/Investors'].str.replace(r'\s*\(.*?\)', '', regex=True)
        
df_full = df_full.sort_values(by=['Buyers/Investors', 'M&A Announced Date'])

# Step 2: Count prior mergers within 5 years
def count_recent_mergers(group):
    dates = group['M&A Announced Date'].tolist()
    counts = []
    for i, current_date in enumerate(dates):
        five_years_ago = current_date - pd.Timedelta(days=1825-365*4)
        prior_dates = dates[:i]
        count = sum((d >= five_years_ago) and (d < current_date) for d in prior_dates)
        counts.append(count)
    return pd.Series(counts, index=group.index)

df_full['num_prior_mergers'] = df_full.groupby('Buyers/Investors', group_keys=False).apply(count_recent_mergers)

print(df_full)

# Step 3: Merge with current dataframe
df['M&A Announced Date'] = pd.to_datetime(df['M&A Announced Date'])

df = pd.merge(
    df,
    df_full[['Buyers/Investors', 'M&A Announced Date', 'num_prior_mergers']],
    on=['Buyers/Investors', 'M&A Announced Date'],
    how='left'
)

print(df)


# Step 2: Running CAR % per window (same as before)
event_windows = {
    "10": "[-10, 10]",
    "7": "[-7, 7]",
    "5": "[-5, 5]",
    "3": "[-3, 3]",
    "1": "[-1, 1]"
}

def compute_running_positive_CAR(group, col):
    result = []
    for i in range(len(group)):
        prev = group.iloc[:i]
        pct = (prev[col] > 0).sum() / len(prev) if len(prev) > 0 else 0
        result.append(pct)
    return pd.Series(result, index=group.index)

for label, col_name in event_windows.items():
    new_col = f'running_positive_CAR_percentage_{label}'
    df[new_col] = df.groupby('Buyers/Investors', group_keys=False).apply(
        lambda g: compute_running_positive_CAR(g, col_name)
    )

# Save result
output = f"{ma_dir}/data/processed/CAR_v5_extra_vars.xlsx"
df.to_excel(output, index=False)











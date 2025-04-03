import pandas as pd
import yfinance as yf
import time
import configparser

# Indlæs config fil
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

# Load the dataset with tickers, start, and end dates
input_file = config["STOCK_FILES"]["adj_event_prices"]
df = pd.read_excel(input_file)

# Find amount of rows removed because of no data over event date:
initial_length = len(df)

df = df[df["Closing Prices"].notna()]

final_rows_1 = len(df)
removed_rows = initial_length - final_rows_1
print(f"Rows removed because no closing prices over event window {input_file}: {removed_rows}\n")
print(f"Det vil tage ca. {1 * len(df["Ticker"]) / 60} minutter at hente deres estimation data")

# Ensure the relevant columns exist
# Example columns: 'Acquirer Name', 'Ticker', 'Start Date', 'End Date'
# Convert dates if they are not datetime already
df['Start Date (Estimation)'] = pd.to_datetime(df['Start Date (Estimation)'], errors='coerce').dt.date
df['End Date (Estimation)'] = pd.to_datetime(df['End Date (Estimation)'], errors='coerce').dt.date

# Function to get historical closing prices
def get_closing_prices(ticker, start_date, end_date):
    try:
        print(f"Fetching {ticker} from {start_date} to {end_date}... (Attempt 1)")
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Flatten MultiIndex if necessary
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]  # Keep only the first level (Price type)
        
        print(data.head())  # Debugging: Print first few rows
        
        if not data.empty:
            # Use "Close"
            if "Close" in data.columns:
                print(f"✔️  Using 'Close' for {ticker}")
                return data["Close"].to_dict()
            else:
                print(f"⚠️ No 'Close' data available for {ticker}")
                return None
        else:
            print(f"⚠️ No data fetched for {ticker}")
            return None
    except Exception as e:
        print(f"⚠️ Error fetching data for {ticker}: {e}")
        return None



# Fetch historical data for each ticker
closing_prices = []

for index, row in df.iterrows():
    ticker = row['Ticker']
    start_date = row['Start Date (Estimation)']
    end_date = row['End Date (Estimation)']

    if pd.notnull(ticker) and pd.notnull(start_date) and pd.notnull(end_date):
        prices = get_closing_prices(ticker, start_date, end_date)
        
        closing_prices.append(prices)
        time.sleep(1)  # Avoid rate limits
    else:
        closing_prices.append(None)

# Add the closing prices as a new column
df['Adj Closing Prices Est. Period'] = closing_prices

# Output the dataframe to check the new column
print(df[['Ticker', 'Adj Closing Prices Est. Period']].head())

df[df['Adj Closing Prices Est. Period'].notna()]

final_rows_2 = len(df)
removed_rows_tck = final_rows_1 - final_rows_2

print(f"Initial row count: {final_rows_1}")
print(f"Rows removed because of no estimation data: {removed_rows_tck}")
print(f"Final row count: {final_rows_2}")

# Save the updated dataset
output_file = config['STOCK_FILES']["adj_estimation_prices"]
df.to_excel(output_file, index=False)

print(f"Historical prices saved to {output_file}")

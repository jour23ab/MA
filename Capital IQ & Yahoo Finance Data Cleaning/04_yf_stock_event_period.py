import pandas as pd
import yfinance as yf
import time
import configparser
import random

# Load config file
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

# Load the dataset
input_file = config["STOCK_FILES"]["with_tickers"]
df = pd.read_excel(input_file)

initial_length = len(df)

# Remove rows with missing tickers
df = df[df["Ticker"].notna()].copy()
print(f"Listen af unikke virksomheder er {len(df["Ticker"].notna())} lang")
print(f"Det vil tage ca. {1 * len(df["Ticker"].notna()) / 60} minutter at hente deres event data")


# Convert dates
df["Start Date (Event)"] = pd.to_datetime(df["Start Date (Event)"], errors="coerce").dt.date
df["End Date (Event)"] = pd.to_datetime(df["End Date (Event)"], errors="coerce").dt.date

def get_closing_prices(ticker, start_date, end_date):
    try:
        print(f"Fetching {ticker} from {start_date} to {end_date}... (Attempt 1)")
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        # Flatten MultiIndex if necessary
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]  # Keep only the first level (Price type)
        
        print(data.head())  # Debugging: Print first few rows
        
        if not data.empty:
            # Use "Close" if "Adj Close" is missing
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
    start_date = row['Start Date (Event)']
    end_date = row['End Date (Event)']

    if pd.notnull(ticker) and pd.notnull(start_date) and pd.notnull(end_date):
        prices = get_closing_prices(ticker, start_date, end_date)
        
        closing_prices.append(prices)
        time.sleep(1)  # Avoid rate limits
    else:
        closing_prices.append(None)

# Add the closing_prices list as a new column in the dataframe
df['Closing Prices'] = closing_prices

# Output the dataframe to check the new column
print(df[['Ticker', 'Closing Prices']].head())

df[df["Closing Prices"].notna()]

final_length = len(df)
removed_rows_tck = initial_length - final_length

print(f"Initial row count: {initial_length}")
print(f"Rows removed because of no event data: {removed_rows_tck}")
print(f"Final row count: {final_length}")

# Save to Excel
output_file = config["STOCK_FILES"]["adj_event_prices"]
df.to_excel(output_file, index=False)

print(f"Event prices successfully saved to {output_file}")
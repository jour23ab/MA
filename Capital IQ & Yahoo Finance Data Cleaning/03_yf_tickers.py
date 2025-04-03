import pandas as pd
import requests
import time
import random
import configparser


# Indlæs config fil
config = configparser.ConfigParser()
config.read("C:/Users/b407939/Desktop/Speciale/Capital IQ/Kode/config.ini", encoding="utf-8")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

# Load company names from Excel
input_file = config["CLEANED_FILES"]["no_overlapping"]
df = pd.read_excel(input_file)

initial_length = len(df)

# Ensure the column is named 'Company'
companies = df['Buyers/Investors'].dropna().drop_duplicates().tolist()
print(f"Listen af unikke virksomheder er {len(companies)} lang")
print(f"Det vil tage ca. {1 * len(companies) / 60} minutter at hente deres tickers")

# Function to search Yahoo Finance for a ticker
def get_ticker_from_name(company_name):
    try:
        # Inside the get_ticker_from_name function:
        headers = {
            "User-Agent": random.choice(user_agents)
        }

        # Yahoo Finance search API
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}"
        response = requests.get(url, headers=headers)
        #print(response.status_code, response.text)


        if response.status_code == 200:
            data = response.json()
            if data['quotes']:
                return data['quotes'][0]['symbol']  # Get the first result
        return None
    except Exception as e:
        print(f"Error for {company_name}: {e}")
        return None

# Loop through companies and fetch tickers
tickers = []
for company in companies:
    ticker = get_ticker_from_name(company)
    print(f"Company: {company} has ticker: {ticker}")
    tickers.append(ticker)
    time.sleep(1)  # Waits between 2 to 5 seconds randomly

# Create a mapping of company names to tickers
ticker_mapping = dict(zip(companies, tickers))

# Add tickers to the original dataframe
df['Ticker'] = df['Buyers/Investors'].map(ticker_mapping)

# Remove rows with no ticker
df = df[df["Ticker"].notna()]

final_length = len(df)
removed_rows_tck = initial_length - final_length

print(f"Initial row count: {initial_length}")
print(f"Rows removed because of no ticker: {removed_rows_tck}")
print(f"Final row count: {final_length}")

# Save to Excel
output_file = config["STOCK_FILES"]["with_tickers"]
df.to_excel(output_file, index=False)

print(f"Tickers successfully saved to {output_file}")


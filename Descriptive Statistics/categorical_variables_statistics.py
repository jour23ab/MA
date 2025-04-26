import os
import pandas as pd
import matplotlib.pyplot as plt

# Directory setup
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# Load data
filsti = os.path.join(ma_dir, "data", "processed", "CAR_v5_extra_vars_cleaned.xlsx")
df = pd.read_excel(filsti)

# Define categorical variables (excluding the date)
categorical_vars = [
    'Transaction Status',
    'Industry Classifications [Buyers/Investors]',
    'Industry Classifications [Target/Issuer]',
    'Primary Sector [Target/Issuer]',
    'Geographic Locations [Buyers/Investors]',
    'Geographic Locations [Target/Issuer]',
    'Target Security Types',
    'Target Type',
    'Diversification',
    'CrossBorder',
    'Crisis'
]

# Helper to sanitize filenames
def safe_filename(name):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

# Directory to save graphs and tables
out_dir = os.path.join(ma_dir, "Descriptive Statistics", "Categorical")
os.makedirs(out_dir, exist_ok=True)

# Generate bar plots and summary tables
for var in categorical_vars:
    counts = df[var].value_counts(dropna=False)
    percents = df[var].value_counts(normalize=True, dropna=False) * 100
    summary = pd.DataFrame({'Count': counts, 'Percentage': percents.round(2)})

    # Save table
    summary_path = os.path.join(out_dir, f"{safe_filename(var)}_summary.xlsx")
    summary.to_excel(summary_path)

    # Plot bar chart
    plt.figure(figsize=(10, 6))
    counts.plot(kind='bar')
    plt.title(f"{var} - Value Counts")
    plt.xlabel(var)
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plot_path = os.path.join(out_dir, f"{safe_filename(var)}_barplot.png")
    plt.savefig(plot_path)
    plt.close()

# Special case: M&A announcements per year
date_var = 'M&A Announced Date'
df[date_var] = pd.to_datetime(df[date_var], errors='coerce')
df['Year'] = df[date_var].dt.year
year_counts = df['Year'].value_counts().sort_index()

# Save plot
plt.figure(figsize=(10, 6))
year_counts.plot(kind='bar')
plt.title("M&A Announcements per Year")
plt.xlabel("Year")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "MA_announced_by_year.png"))
plt.close()

# Save year counts to Excel
year_counts.to_frame(name="M&A Count").to_excel(os.path.join(out_dir, "MA_announced_by_year.xlsx"))

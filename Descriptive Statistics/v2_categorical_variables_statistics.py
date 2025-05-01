import os
import pandas as pd
import matplotlib.pyplot as plt

class PlotGenerator:
    def __init__(self, df, categorical_vars, output_dir, custom_plot_labels=None):
        self.df = df
        self.categorical_vars = categorical_vars
        self.output_dir = output_dir
        self.custom_plot_labels = custom_plot_labels if custom_plot_labels else {}
        os.makedirs(self.output_dir, exist_ok=True)

    def safe_filename(self, name):
        return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

    def generate_summary_and_plots(self):
        for var in self.categorical_vars:
            self._save_summary(var)
            self._save_plot(var)

    def _save_summary(self, var):
        counts = self.df[var].value_counts(dropna=False)
        percents = self.df[var].value_counts(normalize=True, dropna=False) * 100
        summary = pd.DataFrame({'Count': counts, 'Percentage': percents.round(2)})
        summary_path = os.path.join(self.output_dir, f"{self.safe_filename(var)}_summary.xlsx")
        summary.to_excel(summary_path)

    def _save_plot(self, var):
        plt.figure(figsize=(10, 6))
        counts = self.df[var].value_counts(dropna=False)
        counts.index = counts.index.map(lambda x: self.custom_plot_labels.get(var, {}).get("legend_labels", {}).get(x, x))
        counts.plot(kind='bar')

        title = self.custom_plot_labels.get(var, {}).get("title", f"{var} - Value Counts")
        xlabel = self.custom_plot_labels.get(var, {}).get("xlabel", var)
        ylabel = self.custom_plot_labels.get(var, {}).get("ylabel", "Count")

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plot_path = os.path.join(self.output_dir, f"{self.safe_filename(var)}_barplot.png")
        plt.savefig(plot_path)
        plt.close()

    def plot_ma_announcements_by_year(self, date_var):
        self.df[date_var] = pd.to_datetime(self.df[date_var], errors='coerce')
        self.df['Year'] = self.df[date_var].dt.year
        year_counts = self.df['Year'].value_counts().sort_index()

        plt.figure(figsize=(10, 6))
        year_counts.plot(kind='bar')
        plt.title("M&A Announcements per Year")
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "MA_announced_by_year.png"))
        plt.close()

        # Save year counts to Excel
        year_counts.to_frame(name="M&A Count").to_excel(os.path.join(self.output_dir, "MA_announced_by_year.xlsx"))

# --- Usage ---

# Setup directories
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
filsti = os.path.join(ma_dir, "data", "processed", "CAR_v5_extra_vars_cleaned.xlsx")
out_dir = os.path.join(ma_dir, "Descriptive Statistics", "Categorical")

# Load data
df = pd.read_excel(filsti)

# Define variables
categorical_vars = [
    'Primary Sector [Target/Issuer]',
    'Geographic Locations [Buyers/Investors]',
    'Geographic Locations [Target/Issuer]',
    'Target Type',
    'Diversification',
    'CrossBorder',
    'Crisis',
    'Consideration Offered'
    
]

# Define custom plot labels (example)
custom_plot_labels = {
    "Primary Sector [Target/Issuer]": {
        "title": "Distribution of Target's Primary Sector",
        "xlabel": "Target Sector",
        "ylabel": "Number of Deals"
    },
    "Geographic Locations [Buyers/Investors]": {
        "title": "Distribution of Country of Buyer",
        "xlabel": "Buyer Sector",
        "ylabel": "Number of Deals"
    },
    "Geographic Locations [Target/Issuer]": {
        "title": "Distribution of Country of Target",
        "xlabel": "Target Sector",
        "ylabel": "Number of Deals"
    },
    "Target Type": {
        "title": "Distribution by Target Type",
        "xlabel": "Target Type",
        "ylabel": "Deal Count",
        "legend_labels": {"public": "Public", "private": "Private"}
    },
    "Diversification": {
        "title": "Distribution of Conglomerate vs. Non-conglomerate",
        "xlabel": "Deal Type",
        "ylabel": "Number of Deals",
        "legend_labels": {0: "Non-conglomerate", 1: "Conglomerate"}
    },
    "CrossBorder": {
        "title": "Distribution of Cross-Border vs. Domestic Deals",
        "xlabel": "Deal Type",
        "ylabel": "Number of Deals",
        "legend_labels": {0: "Domestic", 1: "Cross-Border"}
    },
    "Crisis": {
        "title": "Distribution of Crisis vs. Non-Crisis",
        "xlabel": "Deal Type",
        "ylabel": "Number of Deals",
        "legend_labels": {0: "Non-Crisis", 1: "Crisis"}
    },
}    

# Create and run plot generator
generator = PlotGenerator(df, categorical_vars, out_dir, custom_plot_labels)
generator.generate_summary_and_plots()
generator.plot_ma_announcements_by_year('M&A Announced Date')







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



print("We done.")



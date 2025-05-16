import matplotlib.pyplot as plt
import pandas as pd
import configparser
import numpy as np
import os
from scipy.stats import t

class CAARAnalyzer:
    def __init__(self, event_data, char_data, characteristic_column, grouping_func,
                 event_window=(-10, 10), plot_dir=None, plot_options=None, winsorize=True):
        self.event_data = event_data
        self.char_data = char_data
        self.characteristic_column = characteristic_column
        self.grouping_func = grouping_func
        self.event_window = event_window
        self.plot_dir = plot_dir
        self.plot_options = plot_options or {}
        self.winsorize = winsorize

        self.group_mapping = {}
        self.groups = []
        self.aar_dict = {}
        self.caar_dict = {}
        self.group_sizes = {}
        self.outlier_bounds = None

    def prepare_groups(self):
        if self.characteristic_column == "All Observations":
            # Special case: assign all to one group
            self.char_data['group'] = "All"
            self.group_mapping = dict(zip(self.char_data['Sheet Name'], self.char_data['group']))
            self.groups = ["All"]
            self.group_sizes = {"All": len(self.group_mapping)}
        else:
            # Regular case
            self.char_data['group'] = self.char_data[self.characteristic_column].apply(self.grouping_func)
            self.group_mapping = dict(zip(self.char_data['Sheet Name'], self.char_data['group']))
            self.groups = list(self.char_data['group'].dropna().unique())
            self.group_sizes = {g: sum(1 for v in self.group_mapping.values() if v == g) for g in self.groups}

        print("Group sizes:")
        for g, count in self.group_sizes.items():
            print(f"  {g}: {count}")

    def compute_outlier_bounds(self):
        all_returns = []
        for df in self.event_data.values():
            if 'Abnormal Return' in df.columns:
                all_returns.extend(df['Abnormal Return'].dropna().tolist())
        self.outlier_bounds = (
            np.percentile(all_returns, 1),
            np.percentile(all_returns, 99)
        )

    def calculate_aar_caar(self):
        print(f"Winsorization is {'ON' if self.winsorize else 'OFF'}")
        start, end = self.event_window
        days = list(range(start, end + 1))
        self.aar_dict = {g: [] for g in self.groups}

        for day_offset in days:
            group_returns = {g: [] for g in self.groups}

            for sheet, df in self.event_data.items():
                group = self.group_mapping.get(sheet)
                if group is None or group not in self.groups:
                    continue

                if all(col in df.columns for col in ["M&A Announced Date", "Abnormal Return", "Date"]):
                    df['Date'] = pd.to_datetime(df['Date']).dt.date
                    df['M&A Announced Date'] = pd.to_datetime(df['M&A Announced Date']).dt.date
                    announce_date = df['M&A Announced Date'].iloc[0]

                    if announce_date in df['Date'].values:
                        idx = df[df['Date'] == announce_date].index[0]
                        day_idx = idx + day_offset

                        if 0 <= day_idx < len(df):
                            try:
                                ar = df.loc[day_idx, 'Abnormal Return']
                                # Winsorize
                                if self.winsorize and self.outlier_bounds is not None:
                                    ar = max(min(ar, self.outlier_bounds[1]), self.outlier_bounds[0])
                                group_returns[group].append(ar)
                            except Exception as e:
                                print(f"Error extracting abnormal return for sheet '{sheet}' on day {day_offset}: {e}")
                        else:
                            if day_offset == 0:
                                print(f"Warning: day_idx {day_idx} out of bounds for sheet '{sheet}' on day {day_offset}")
                    else:
                        if day_offset == 0:
                            print(f"Warning: Announcement date {announce_date} not found in dates for sheet '{sheet}'")

            for g in self.groups:
                aar = sum(group_returns[g]) / len(group_returns[g]) if group_returns[g] else None
                self.aar_dict[g].append(aar)

        self.caar_dict = {g: pd.Series(self.aar_dict[g]).cumsum().tolist() for g in self.groups}
        return days

    def plot(self, days):
        plt.figure(figsize=(10, 6))

        # Fallbacks if no options provided
        title = self.plot_options.get("title", f"CAAR by {self.characteristic_column}")
        xlabel = self.plot_options.get("xlabel", "Days Relative to Announcement Date")
        ylabel = self.plot_options.get("ylabel", "Cumulative Average Abnormal Return")
        legend_labels = self.plot_options.get("legend_labels", {})
        subtitle = self.plot_options.get("subtitle", "")

        for g in self.groups:
            label = legend_labels.get(g, f"CAAR ({g})")
            plt.plot(days, self.caar_dict[g], label=label, linestyle='--', marker='x')

        plt.title(title, fontsize=14)
        if subtitle:
            plt.suptitle(subtitle, fontsize=10, y=0.92)
        plt.xlabel("Days Relative to Announcement (Event Window)", fontsize=12)
        plt.ylabel("CAAR", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Add annotation with group sizes
        group_info = ", ".join([f"{g}: {self.group_sizes[g]}" for g in self.groups])
        plt.annotate(f"Group sizes: {group_info}", xy=(0.5, -0.15), xycoords='axes fraction',
                     ha='center', fontsize=9)

        if self.plot_dir:
            os.makedirs(self.plot_dir, exist_ok=True)
            filename = f"CAAR_{self.characteristic_column.replace(' ', '_')}.png"
            plt.savefig(os.path.join(self.plot_dir, filename), bbox_inches='tight')

        plt.show()

    def analyze(self):
        print(f"\n=== Analyzing: {self.characteristic_column} ===")
        self.prepare_groups()
        self.compute_outlier_bounds()
        days = self.calculate_aar_caar()
        self.plot(days)
        self.summarize_results()

    def summarize_results(self):
        print(f"\n=== Summary Statistics for {self.characteristic_column} ===")
        for g in self.groups:
            aar_series = pd.Series([aar for aar in self.aar_dict[g] if aar is not None])
            if aar_series.empty:
                print(f"Group {g}: No valid AAR values found.")
                continue

            final_caar = self.caar_dict[g][-1]  # Last CAAR value
            std_error = aar_series.std(ddof=1) / np.sqrt(len(aar_series))
            t_stat = final_caar / std_error if std_error != 0 else float('inf')
            p_value = 2 * (1 - t.cdf(abs(t_stat), df=len(aar_series) - 1))

            print(f"\nGroup: {g}")
            print(f"  Final CAAR: {final_caar:.5f}")
            print(f"  Standard Error: {std_error:.5f}")
            print(f"  t-Statistic: {t_stat:.5f}")
            print(f"  p-Value: {p_value:.5f}")



# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# === Load config and event data ===
config_path = os.path.join(base_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

# Resolve abnormal_returns.xlsx (from config)
abnormal_returns_path = os.path.join(base_dir, config["FINAL_FILES"]["abnormal_returns"])
event_values_dict = pd.read_excel(abnormal_returns_path, sheet_name=None)

# === Load merger characteristics from data/final/ ===
project_root = os.path.dirname(base_dir)  # Go up one level to MA/
char_file = os.path.join(project_root, "data", "final", "data_prepped_FINAL_CAR_gpdg_pcp.xlsx")
char_df = pd.read_excel(char_file)


print(f"Intial length of char_df: {len(char_df)}")
# === Drop NAs for the same columns which we regress on ===
# === Rename columns ===
char_df.rename(columns={
    "gdp_lag1_tgt": "GDPG",
    "running_positive_CAR_percentage_10": "PCP10",
    "[-10, 10]": "CAR_10_wins",
    "Cash_and_Equivalents": "CashAndEquivalents",
    "Bull_Bear_Spread": "BullBearSpread",
}, inplace=True)

cols_to_keep = [
    "CAR_10_wins", "Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis",
    "PCP10", "GDPG", "Margin", "DtoE", "Hybrid", "Size", "CashAndEquivalents",
    "TargetAsset", "BullBearSpread"
]

char_df = char_df.dropna(subset=cols_to_keep)
""" 
# === REMOVE OUTLIERS ===
# Calculate 1st and 99th percentile thresholds
lower_bound = char_df["CAR_10_wins"].quantile(0.01)
upper_bound = char_df["CAR_10_wins"].quantile(0.99)

# Filter out outliers
before = len(char_df)
print(f"Before: {before}")
char_df = char_df[(char_df["CAR_10_wins"] >= lower_bound) & (char_df["CAR_10_wins"] <= upper_bound)]
after = len(char_df)
print(f"After: {after}")

print(f"Removed {before - after} outlier rows based on CAR_10_wins (outside 1st–99th percentile).")
 """

print("Before filtering:")
print(f"Number of sheets in event_values_dict: {len(event_values_dict)}")
print(f"Number of mergers in char_df: {len(char_df)}")

# === Keep only event sheets that exist in char_df["Sheet Name"] ===
valid_sheet_names = set(char_df["Sheet Name"])
event_values_dict = {k: v for k, v in event_values_dict.items() if k in valid_sheet_names}
print(f"Number of sheets in event_values_dict: {len(event_values_dict)}")

# After filtering event_values_dict
valid_sheet_names = set(char_df["Sheet Name"])
existing_sheet_names = set(event_values_dict.keys())

# Find sheet names that are in char_df but missing from event_values_dict
missing_sheets = valid_sheet_names - existing_sheet_names

if missing_sheets:
    print(f"\nMissing sheet(s) in event_values_dict ({len(missing_sheets)} total):")
    for sheet in missing_sheets:
        print(f"  - {sheet}")
else:
    print("\nNo missing sheets. All Sheet Names match.")



# Go up one level to reach the project root (e.g., /MA/)
project_root = os.path.dirname(base_dir)

# Build the full path to data/final/graph_data.xlsx
output_path = os.path.join(project_root, "data", "final", "graph_data.xlsx")

# Save the DataFrame
char_df.to_excel(output_path, index=False)

print(f"✅ Saved to: {output_path}")


# Create a subfolder path relative to your script's directory
plot_folder = os.path.join(base_dir, "plots", "CAAR characteristics", "New")

# Ensure the folder exists
os.makedirs(plot_folder, exist_ok=True)


# === Define medians ===
mean_val_mtob = char_df["MtoB"].mean()
mean_win_rate = char_df["PCP10"].mean()
mean_gdp_lag1_tgt = char_df["GDPG"].mean()

# === Define grouping strategies ===
configs = {
    "All Observations": lambda val: "All",
    "Consideration Offered": lambda val: ("Cash" if isinstance(val, str) and "cash" in val.lower() else "Stock" if isinstance(val, str) and val.lower() == "common equity" else None),
    "Target Type": lambda val: "Public" if str(val).strip().lower() == "public" else "Private",
    "CrossBorder": lambda val: "Cross-border" if val == 1 else "Domestic",
    "Diversification": lambda val: "Conglomerate" if val == 1 else "Non-conglomerate",
    "Crisis": lambda val: "Crisis" if val == 1 else "No-crisis",
    "MtoB": lambda val: "Top Percentile" if val >= mean_val_mtob else "Bottom Percentile",
    "PCP10": lambda val: "Top Percentile" if val >= mean_win_rate else "Bottom Percentile",
    "GDPG": lambda val: "Top Percentile" if val >= mean_gdp_lag1_tgt else "Bottom Percentile",
}

custom_plot_labels = {
    "All Observations": {
        "title": "CAAR for All Observations",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"All": "All Deals"}
    },
    "Consideration Offered": {
        "title": "Effect of Payment Method on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Cash": "Cash Deals", "Stock": "Stock Deals"}
    },
    "Target Type": {
        "title": "Effect of Target Type on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Public": "Public Targets", "Private": "Private Targets"}
    },
    "Diversification": {
        "title": "Effect of Diversification on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Conglomerate": "Conglomerate Transactions", "Non-conglomerate": "Non-conglomerate Transactions"}
    },
    "CrossBorder": {
        "title": "Effect of Cross-border on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Cross-border": "Cross-border Transactions", "Domestic": "Domestic Transactions"}
    },
    "Crisis": {
        "title": "Effect of Crisis Periods on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Crisis": "Crisis-Period Transactions", "No-crisis": "Non-Crisis-Period Transactions"}
    },
    "MtoB": {
        "title": "Effect of MtoB Ratio on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Top Percentile": "Top 50th Percentile Ratio", "Bottom Percentile": "Bottom 50th Percentile Ratio"}
    },
    "PCP10": {
        "title": "Effect of Success Rate on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Top Percentile": "Top 50th Percentile Success Rate", "Bottom Percentile": "Bottom 50th Percentile Success Rate"}
    },
    "GDPG": {
        "title": "Effect of Target Country GDP growth rate on CAAR",
        "xlabel": "Trading Days Around Announcement (Event Window)",
        "ylabel": "CAAR",
        "legend_labels": {"Top Percentile": "Top 50th Percentile Growth Rate", "Bottom Percentile": "Bottom 50th Percentile Growth Rate"}
    }
}


# === Run analysis for each characteristic ===
for characteristic, func in configs.items():
    analyzer = CAARAnalyzer(
        event_data=event_values_dict,
        char_data=char_df,
        characteristic_column=characteristic,
        grouping_func=func,
        plot_dir=plot_folder,
        plot_options=custom_plot_labels.get(characteristic, {}),
        winsorize=True  # This line pulls the right customization
    )
    analyzer.analyze()


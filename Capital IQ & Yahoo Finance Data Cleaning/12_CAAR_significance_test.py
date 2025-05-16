import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import configparser
import os

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load config file
config_path = os.path.join(base_dir, "config.ini")
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

# Resolve full path to the merged_cars file
file1 = os.path.join(base_dir, config["FINAL_FILES"]["merged_cars"])

# Load the sheet with CAR values for each event window
df = pd.read_excel(file1)


print(df)


def test_caar_significance(car_values, event_window, alpha=0.05):
    """
    Performs a t-test to determine the statistical significance of CAAR.
    Also plots a histogram of CAR values with the theoretical normal distribution.
    
    Parameters:
    car_values (array-like): A list or NumPy array of CAR values (one per firm).
    alpha (float): Significance level (default: 0.05).
    
    Returns:
    pd.DataFrame: A table with CAAR, t-statistic, p-value, and significance result.
    """
    N = len(car_values)  # Number of firms
    CAAR = np.mean(car_values)  # Average CAR
    SE_CAR = np.std(car_values, ddof=1) / np.sqrt(N)  # Standard error of CAAR
    
    # t-statistic
    t_stat = CAAR / SE_CAR
    
    # Two-tailed p-value
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=N-1))
    
    # Significance check
    significant = p_value < alpha
    
    # Plotting the histogram and normal distribution overlay
    plt.figure(figsize=(8, 6))
    plt.hist(car_values, bins=10, edgecolor='black', density=True, alpha=0.6, label='CAR values')
    
    # Theoretical normal distribution parameters
    mean_car = np.mean(car_values)
    std_car = np.std(car_values, ddof=1)
    
    # Overlay the theoretical normal distribution
    x = np.linspace(min(car_values), max(car_values), 100)
    y = stats.norm.pdf(x, mean_car, std_car)
    plt.plot(x, y, label=f'Normal dist. (mean={mean_car:.3f}, std={std_car:.3f})', color='red', lw=2)
    
    plt.title(f'Histogram of {event_window} CAR values with Normal Distribution Overlay for Window')
    plt.xlabel('CAR')
    plt.ylabel('Density')
    plt.legend()
    plt.show()
    
    # Creating a table (DataFrame) for the results
    results = pd.DataFrame({
        "Metric": ["CAAR", "t-statistic", "p-value", "Significant"],
        "Value": [CAAR, t_stat, p_value, "Yes" if significant else "No"]
    })
    
    return results



# USAGE


column_list = ["[-10, 10]", "[-7, 7]", "[-5, 5]", "[-3, 3]", "[-1, 1]"]

for column in column_list:

    car_values = df[column]
    result = test_caar_significance(car_values, event_window=column)

    print(f"Results for {column}")
    print(result)

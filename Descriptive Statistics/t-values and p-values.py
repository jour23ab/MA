import pandas as pd
import os
from scipy.stats import t


# Corrected data extracted from images and updated with correct coefficient and SE values
# Reduced dataset based on the latest image provided by the user
data = {
    "Variable": [
        "Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis",
        "PCP10", "PCP7", "PCP5", "PCP3", "PCP1", "GDPG"
    ],
    "CAR_10_Coef": [
        -1.257, -0.458, -0.934, 0.554, -0.008, 0.181,
        0.228, None, None, None, None, 0.063
    ],
    "CAR_10_SE": [
        0.574, 0.618, 0.333, 0.424, 0.008, 0.400,
        0.390, None, None, None, None, 0.039
    ],
    "CAR_7_Coef": [
        -0.615, -0.380, -0.388, 0.190, 0.009, 0.349,
        None, 0.118, None, None, None, 0.021
    ],
    "CAR_7_SE": [
        0.487, 0.565, 0.280, 0.307, 0.006, 0.345,
        None, 0.361, None, None, None, 0.035
    ],
    "CAR_5_Coef": [
        -0.931, -0.661, -0.048, 0.136, 0.008, 0.645,
        None, None, 0.151, None, None, 0.035
    ],
    "CAR_5_SE": [
        0.406, 0.400, 0.212, 0.267, 0.005, 0.274,
        None, None, 0.255, None, None, 0.027
    ],
    "CAR_3_Coef": [
        -0.572, -0.502, -0.107, -0.012, 0.002, 0.404,
        None, None, None, -0.308, None, 0.037
    ],
    "CAR_3_SE": [
        0.369, 0.302, 0.181, 0.228, 0.003, 0.221,
        None, None, None, 0.214, None, 0.024
    ],
    "CAR_1_Coef": [
        -0.412, -0.121, -0.202, 0.030, 0.001, 0.128,
        None, None, None, None, -0.189, 0.020
    ],
    "CAR_1_SE": [
        0.203, 0.212, 0.107, 0.153, 0.002, 0.123,
        None, None, None, None, 0.132, 0.013
    ]
}


df = pd.DataFrame(data)

# Degrees of freedom
dfs = {
    "CAR_10": 269,
    "CAR_7": 269,
    "CAR_5": 269,
    "CAR_3": 269,
    "CAR_1": 269
}

# Calculate stats for each model
for model, df_val in dfs.items():
    coef = df[f"{model}_Coef"]
    se = df[f"{model}_SE"]
    t_stat = coef / se

    df[f"{model}_t"] = t_stat
    df[f"{model}_p_two_tailed"] = 2 * t.sf(abs(t_stat), df=df_val)
    df[f"{model}_p_right"] = t.sf(t_stat, df=df_val)
    df[f"{model}_p_left"] = t.cdf(t_stat, df=df_val)

# Export to Excel
output_path = os.path.join("Descriptive Statistics", "P-values and t-values/regression_results_corrected_values.xlsx")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, index=False)

output_path

print("done")
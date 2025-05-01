import pandas as pd
import os
from scipy.stats import t

# Corrected coefficients and standard errors from manual hardcoding
data = {
    "Variable": [
        "Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis",
        "PCP10", "PCP7", "PCP5", "PCP3", "PCP1", "GDPG", "Margin", "DtoE",
        "Hybrid", "Size", "CashAndEquivalents", "TargetAsset", "BullBearSpread", "Constant"
    ],
    "CAR_10_Coef": [
        -1.615, -0.212, -0.675, 0.476, 0.003, 0.489,
        0.491, None, None, None, None,
        0.059, 0.001, -0.058, -1.535, 0.030, 0.031, 0.147, 1.999, 2.016
    ],
    "CAR_10_SE": [
        0.615, 0.882, 0.323, 0.423, 0.029, 0.404,
        0.420, None, None, None, None,
        0.037, 0.001, 0.128, 0.695, 0.044, 0.043, 0.383, 0.936, 1.069
    ],
    "CAR_7_Coef": [
        -1.042, -0.345, -0.064, 0.476, 0.021, 0.491,
        None, 0.399, None, None, None,
        0.030, 0.001, -0.075, -1.181, 0.056, 0.041, 0.016, 0.966, 1.084
    ],
    "CAR_7_SE": [
        0.526, 0.771, 0.267, 0.325, 0.027, 0.337,
        None, 0.381, None, None, None,
        0.033, 0.001, 0.111, 0.594, 0.038, 0.040, 0.331, 0.780, 0.926
    ],
    "CAR_5_Coef": [
        -1.176, -0.233, -0.035, 0.253, 0.021, 0.565,
        None, None, 0.336, None, None,
        0.030, 0.001, 0.043, -1.301, 0.077, 0.017, 0.181, 0.689, 1.071
    ],
    "CAR_5_SE": [
        0.472, 0.619, 0.210, 0.286, 0.020, 0.283,
        None, None, 0.270, None, None,
        0.025, 0.001, 0.100, 0.517, 0.035, 0.033, 0.255, 0.697, 0.783
    ],
    "CAR_3_Coef": [
        -0.735, -0.382, -0.098, 0.128, 0.017, 0.437,
        None, None, None, 0.071, None,
        0.017, 0.001, 0.096, -1.009, 0.009, 0.032, 0.122, 0.670, 0.997
    ],
    "CAR_3_SE": [
        0.399, 0.465, 0.170, 0.213, 0.017, 0.216,
        None, None, None, 0.210, None,
        0.022, 0.001, 0.071, 0.439, 0.038, 0.024, 0.195, 0.577, 0.595
    ],
    "CAR_1_Coef": [
        -0.283, -0.288, -0.101, -0.104, 0.007, 0.195,
        None, None, None, None, -0.277,
        0.005, 0.001, 0.044, -0.301, 0.001, 0.018, 0.087, 0.505, 0.663
    ],
    "CAR_1_SE": [
        0.186, 0.287, 0.101, 0.139, 0.010, 0.119,
        None, None, None, None, 0.133,
        0.013, 0.0003, 0.041, 0.211, 0.019, 0.014, 0.135, 0.409, 0.345
    ]
}

df = pd.DataFrame(data)

# Degrees of freedom
dfs = {
    "CAR_10": 293,
    "CAR_7": 293,
    "CAR_5": 293,
    "CAR_3": 293,
    "CAR_1": 293
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
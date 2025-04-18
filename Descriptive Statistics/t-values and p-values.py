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
        -1.607, -0.200, -0.670, 0.478, 0.003, 0.489, 0.489, None, None, None, None,
        0.059, 0.001, -0.058, -1.530, 0.030, 0.032, 0.147, 1.997, 1.992
    ],
    "CAR_10_SE": [
        0.609, 0.875, 0.321, 0.422, 0.029, 0.420, 0.418, None, None, None, None,
        0.037, 0.001, 0.129, 0.689, 0.044, 0.043, 0.383, 0.933, 1.060
    ],
    "CAR_7_Coef": [
        -0.860, -0.405, -0.086, 0.394, 0.020, 0.477, None, 0.315, None, None, None,
        0.028, 0.001, -0.071, -1.040, 0.053, 0.039, -0.063, 0.914, 1.062
    ],
    "CAR_7_SE": [
        0.503, 0.756, 0.262, 0.318, 0.027, 0.333, None, 0.369, None, None, None,
        0.033, 0.001, 0.110, 0.582, 0.038, 0.339, 0.325, 0.770, 0.910
    ],
    "CAR_5_Coef": [
        -1.028, -0.280, -0.035, 0.193, 0.021, 0.561, None, None, 0.283, None, None,
        0.028, 0.001, 0.043, -1.176, 0.075, 0.016, 0.120, 0.656, 1.028
    ],
    "CAR_5_SE": [
        0.459, 0.616, 0.207, 0.281, 0.022, 0.281, None, None, 0.265, None, None,
        0.025, 0.001, 0.100, 0.509, 0.035, 0.033, 0.254, 0.688, 0.775
    ],
    "CAR_3_Coef": [
        -0.717, -0.387, -0.099, 0.122, 0.017, 0.435, None, None, None, 0.064, None,
        0.017, 0.001, 0.096, -0.995, 0.009, 0.932, 0.114, 0.653, 0.993
    ],
    "CAR_3_SE": [
        0.373, 0.465, 0.168, 0.208, 0.014, 0.215, None, None, None, 0.064, None,
        0.022, 0.001, 0.070, 0.421, 0.039, 0.024, 0.191, 0.569, 0.588
    ],
    "CAR_1_Coef": [
        -0.272, -0.275, -0.100, -0.110, 0.007, 0.199, None, None, None, None, -0.286,
        0.005, 0.001, 0.043, -0.296, 0.002, 0.017, 0.099, 0.481, 0.648
    ],
    "CAR_1_SE": [
        0.175, 0.288, 0.101, 0.136, 0.010, 0.120, None, None, None, None, 0.130,
        0.013, 0.0003, 0.041, 0.203, 0.019, 0.014, 0.138, 0.320, 0.348
    ]
}

df = pd.DataFrame(data)

# Degrees of freedom
dfs = {
    "CAR_10": 293,
    "CAR_7": 296,
    "CAR_5": 296,
    "CAR_3": 296,
    "CAR_1": 296
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
output_path = os.path.join("Descriptive Statistics", "regression_results_corrected_values.xlsx")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, index=False)

output_path

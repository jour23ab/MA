import pandas as pd
import os
from scipy.stats import t

# Manually transcribed coefficients and standard errors from the images for 5 CAR windows
data = {
    "Variable": [
        "Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis",
        "PCP10", "PCP7", "PCP5", "PCP3", "PCP1", "GDPG", "Margin", "DtoE",
        "Hybrid", "Size", "CashAndEquivalents", "TargetAsset", "BullBearSpread", "Constant"
    ],
    "CAR_10_Coef": [
        -1.265, -0.346, -0.939, 0.545, -0.008, 0.178,
        0.242, None, None, None, None,
        0.062, 0.001, 0.152, -1.392, 0.054, 0.036, -0.148, 1.669, 2.006
    ],
    "CAR_10_SE": [
        0.576, 0.816, 0.336, 0.427, 0.008, 0.401,
        0.389, None, None, None, None,
        0.039, 0.001, 0.137, 0.707, 0.048, 0.041, 0.352, 0.893, 0.975
    ],
    "CAR_7_Coef": [
        -0.619, -0.446, -0.396, 0.182, 0.010, 0.340,
        None, 0.123, None, None, None,
        0.021, 0.0004, -0.037, -0.944, 0.054, 0.042, -0.325, 0.500, 1.285
    ],
    "CAR_7_SE": [
        0.490, 0.786, 0.283, 0.310, 0.006, 0.345,
        None, 0.360, None, None, None,
        0.035, 0.001, 0.073, 0.620, 0.038, 0.040, 0.293, 0.783, 0.922
    ],
    "CAR_5_Coef": [
        -0.942, -0.493, -0.055, 0.121, 0.008, 0.643,
        None, None, 0.172, None, None,
        0.034, 0.001, 0.017, -1.197, 0.077, 0.018, -0.156, 0.236, 1.298
    ],
    "CAR_5_SE": [
        0.412, 0.540, 0.214, 0.273, 0.005, 0.277,
        None, None, 0.253, None, None,
        0.027, 0.001, 0.063, 0.500, 0.032, 0.033, 0.225, 0.659, 0.689
    ],
    "CAR_3_Coef": [
        -0.576, -0.425, -0.112, -0.023, 0.003, 0.398,
        None, None, None, -0.307, None,
        0.036, 0.001, -0.039, -0.839, 0.025, 0.039, -0.163, 0.278, 1.181
    ],
    "CAR_3_SE": [
        0.374, 0.373, 0.180, 0.231, 0.003, 0.223,
        None, None, None, 0.214, None,
        0.023, 0.001, 0.038, 0.453, 0.034, 0.025, 0.188, 0.549, 0.507
    ],
    "CAR_1_Coef": [
        -0.412, -0.232, -0.207, 0.027, 0.001, 0.121,
        None, None, None, None, -0.194,
        0.019, 0.001, 0.078, -0.314, 0.012, 0.022, 0.057, 0.646, 0.728
    ],
    "CAR_1_SE": [
        0.204, 0.298, 0.108, 0.153, 0.002, 0.123,
        None, None, None, None, 0.132,
        0.013, 0.0003, 0.037, 0.240, 0.021, 0.015, 0.114, 0.312, 0.348
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
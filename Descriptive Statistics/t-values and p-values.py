import pandas as pd
import os
from scipy.stats import t

# === Set working directory ===
current_dir = os.path.dirname(os.path.abspath(__file__))
ma_dir = os.path.dirname(current_dir)
os.chdir(ma_dir)

# === Define regression results ===
data = {
    "Variable": [
        "Cash", "Private", "CrossBorder", "Diversification", "MtoB", "Crisis", "PCP10", "PCP7", "PCP5", "PCP3", "PCP1",
        "GDPG", "Margin", "DtoE", "Hybrid", "Size", "CashAndEquivalents", "TargetAsset", "BullBearSpread", "Constant"
    ],
    "CAR_10_Coef": [
        -1.677, -0.200, -0.670, 0.478, 0.003, 0.631, 0.489, None, None, None, None,
        0.059, 0.001, -0.058, -1.530, 0.826, 0.629, 0.147, 1.997, 1.992
    ],
    "CAR_10_SE": [
        0.609, 0.875, 0.321, 0.422, 0.012, 0.420, 0.418, None, None, None, None,
        0.837, 0.001, 0.129, 0.690, 0.844, 0.933, 0.383, 0.931, 1.066
    ],
    "CAR_7_Coef": [
        -0.860, -0.485, -0.866, 0.394, 0.026, 0.477, None, 0.315, None, None, None,
        0.028, 0.001, -0.071, -1.040, 0.833, 0.926, 0.183, 0.914, 1.062
    ],
    "CAR_7_SE": [
        0.563, 0.756, 0.262, 0.398, 0.018, 0.333, None, 0.360, None, None, None,
        0.823, 0.001, 0.104, 0.582, 0.838, 0.770, 0.325, 0.967, 0.910
    ],
    "CAR_5_Coef": [
        -1.028, -0.516, -0.809, 0.193, 0.021, 0.561, None, None, 0.283, None, None,
        0.028, 0.001, -0.043, -1.176, 0.863, 0.985, 0.229, 0.655, 1.028
    ],
    "CAR_5_SE": [
        0.459, 0.616,  0.207, 0.364, 0.017, 0.281, None, None, 0.265, None, None,
        0.821, 0.001, 0.090, 0.523, 0.835, 0.779, 0.254, 0.893, 0.775
    ],
    "CAR_3_Coef": [
        -0.717, -0.387, -0.809, 0.122, 0.027, 0.435, None, None, None, 0.064, None,
        0.017, 0.001, 0.006, -0.995, 0.818, 0.958, 0.149, 0.589, 0.993
    ],
    "CAR_3_SE": [
        0.373, 0.465, 0.168, 0.321, 0.017, 0.215, None, None, None, 0.204, None,
        0.822, 0.001, 0.090, 0.421, 0.839, 0.763, 0.191, 0.850, 0.588
    ],
    "CAR_1_Coef": [
        -0.272, -0.275, -0.180, -0.110, 0.027, 0.199, None, None, None, None, -0.286,
        0.019, 0.001, -0.022, -0.617, 0.819, 0.856, 0.149, 0.481, 0.648
    ],
    "CAR_1_SE": [
        0.175, 0.288, 0.101, 0.267, 0.017, 0.120, None, None, None, None, 0.139,
        0.823, 0.001, 0.064, 0.402, 0.837, 0.743, 0.199, 0.818, 0.348
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Degrees of freedom per model
dfs = {
    "CAR_10": 293,
    "CAR_7": 296,
    "CAR_5": 296,
    "CAR_3": 296,
    "CAR_1": 296
}

# Compute t-stats and p-values for each model
for model, df_val in dfs.items():
    coef_col = f"{model}_Coef"
    se_col = f"{model}_SE"
    t_col = f"{model}_t"
    p_col = f"{model}_p"

    df[t_col] = df[coef_col] / df[se_col]
    df[p_col] = 2 * t.sf(abs(df[t_col]), df=df_val)

# Export to Excel
output_path = os.path.join(ma_dir, "Descriptive Statistics", "regression_results_with_t_p_values.xlsx")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, index=False)

print("✅ Output saved to:", output_path)

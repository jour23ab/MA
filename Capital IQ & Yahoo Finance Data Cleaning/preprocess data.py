import pandas as pd

filsti = r"C:\Users\b407939\Desktop\Speciale\Capital IQ\Raw\v6_020120.xls"
df = pd.read_excel(filsti)

print(df)

filsti = r"C:\Users\b407939\Desktop\Speciale\Capital IQ\Raw\v6_020120_preprocessed.xlsx"
df.to_excel(filsti, index=False)
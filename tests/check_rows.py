"""Check what rows are being captured."""

import pandas as pd

df = pd.read_csv('data/darta_clean.csv')
print(f"Total rows: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 20 reg_no values:")
for i, reg in enumerate(df['reg_no'].head(20)):
    print(f"{i}: {reg}")

print(f"\nRow 11 full details:")
print(df.iloc[11])

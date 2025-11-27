"""Check column order after processing."""

import pandas as pd

df = pd.read_csv('data/darta_clean.csv')

print("Column Order:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print(f"\n✓ Total columns: {len(df.columns)}")
print(f"✓ Total records: {len(df)}")

expected_order = ['year', 'month', 'day', 'reg_no', 'province_code', 'district_code']
actual_start = df.columns[:6].tolist()

if actual_start == expected_order:
    print("\n✅ Column order is perfect!")
else:
    print(f"\n⚠️  Expected: {expected_order}")
    print(f"   Actual:   {actual_start}")

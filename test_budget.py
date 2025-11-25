"""Test budget processing."""

from data_pipeline.budget import process_monthly_data

result = process_monthly_data(xlsx_file='data/82-83.xlsx')

print(f"\nProcessed {len(result):,} records")
if 'Year' in result.columns:
    print(f"Year: {result['Year'].iloc[0]}")
print(f"Output: 2082.csv")

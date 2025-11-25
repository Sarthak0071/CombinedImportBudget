"""Test budget processing with real data."""

from data_pipeline.budget import process_monthly_data

print("="*60)
print("BUDGET PROCESSING - Extract Clean Year Data")
print("="*60)
print("✅ No done.csv needed - just extract clean data!\n")

# Primary use case: Just extract clean year data (NO merging)
result = process_monthly_data(
    xlsx_file='data/82-83.xlsx'
    # That's it! No old_data needed
)

print(f"\n{'='*60}")
print(f"SUCCESS! Processed {len(result):,} clean records")
print(f"{'='*60}")

if 'Year' in result.columns:
    year = result['Year'].iloc[0]
    print(f"\nYear: {year}")
    print(f"Records: {len(result):,}")

print("\nFile created:")
print("  ✅ 2082.csv (clean year data)")
print("\nNo merging, no historical data needed!")

"""Test budget processing with real data."""

from data_pipeline.budget import process_monthly_data, extract_year_data

print("="*60)
print("OPTION 1: Full Processing (extract + merge)")
print("="*60)

result = process_monthly_data(
    xlsx_file='data/82-83.xlsx',
    old_data='data/done.csv',
    output_name='output.csv'
)

print(f"\nSUCCESS! Processed {len(result):,} records")

if 'Year' in result.columns:
    print("\nRecords by year:")
    for year in sorted(result['Year'].unique()):
        count = len(result[result['Year'] == year])
        print(f"  {year}: {count:,} records")

print("\nFiles created:")
print("  1. 2082.csv (year-specific clean data)")
print("  2. output.csv (all years combined)")

print("\n" + "="*60)
print("OPTION 2: Extract Year Only (no merge)")
print("="*60)

result2 = extract_year_data('data/82-83.xlsx')
print(f"\nExtracted {len(result2):,} clean records for year {result2['Year'].iloc[0]}")
print("\nFile created:")
print("  - 2082.csv (clean year data)")

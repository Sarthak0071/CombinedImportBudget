"""Test trade processing with real data."""

from data_pipeline.trade import process_monthly_data

# Process cumulative import/export data
result = process_monthly_data(
    xlsx_file='data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
    old_data='data/done.csv',
    output_name='updateddone.csv'
)

print(f"\n{'='*60}")
print(f"SUCCESS! Processed {len(result):,} records")
print(f"{'='*60}")

if 'Direction' in result.columns:
    imports = len(result[result['Direction'] == 'I'])
    exports = len(result[result['Direction'] == 'E'])
    print(f"Imports: {imports:,}")
    print(f"Exports: {exports:,}")

print("\nFiles created:")
print("  1. month.csv (monthly data for current month)")
print("  2. updateddone.csv (historical + new month)")

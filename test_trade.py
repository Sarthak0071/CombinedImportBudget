"""Test trade processing."""

from data_pipeline.trade import process_monthly_data

result = process_monthly_data(
    xlsx_file='data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
    old_data='data/done.csv',
    output_name='updateddone.csv'
)

print(f"\nProcessed {len(result):,} records")
if 'Direction' in result.columns:
    imports = len(result[result['Direction'] == 'I'])
    exports = len(result[result['Direction'] == 'E'])
    print(f"Imports: {imports:,}, Exports: {exports:,}")
print(f"Outputs: month.csv, updateddone.csv")

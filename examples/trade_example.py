"""Example: Processing trade data (Import/Export)."""

from pathlib import Path
from data_pipeline.trade import process_monthly_data

def main():
    """Process cumulative trade data to calculate monthly values."""
    
    # Input files
    xlsx_file = 'data/FTS_uptoAsoj_208283_ci1nozq.xlsx'  # Cumulative import/export
    old_data = 'data/done.csv'                            # Historical monthly records
    output_name = 'updateddone.csv'                       # Output filename
    
    print("=" * 60)
    print("TRADE DATA PROCESSING - Import/Export")
    print("=" * 60)
    print(f"Input: {xlsx_file}")
    print(f"Historical data: {old_data}")
    print(f"Output: {output_name}")
    print()
    
    try:
        result = process_monthly_data(
            xlsx_file=xlsx_file,
            old_data=old_data,
            output_name=output_name
        )
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"Total records: {len(result):,}")
        
        if 'Direction' in result.columns:
            imports = len(result[result['Direction'] == 'I'])
            exports = len(result[result['Direction'] == 'E'])
            print(f"Imports: {imports:,}")
            print(f"Exports: {exports:,}")
        
        print("\nFiles created:")
        print("  1. month.csv (monthly data only)")
        print(f"  2. {output_name} (historical + new)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have the required files:")
        print(f"  - {xlsx_file}")
        print(f"  - {old_data}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    main()

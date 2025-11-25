"""Example: Processing budget data."""

from pathlib import Path
from data_pipeline.budget import process_monthly_data, extract_year_data

def example_full_processing():
    """Process budget data and merge with base."""
    
    # Input files
    xlsx_file = 'data/82-83.xlsx'   # Budget file for fiscal year
    old_data = 'done.csv'            # Historical multi-year data
    output_name = 'output.csv'       # Output filename
    
    print("=" * 60)
    print("BUDGET DATA PROCESSING - Full Merge")
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
        
        if 'Year' in result.columns:
            print("\nRecords by year:")
            for year in sorted(result['Year'].unique()):
                count = len(result[result['Year'] == year])
                print(f"  {year}: {count:,} records")
        
        print("\nFiles created:")
        print("  1. 2082.csv (year-specific data)")
        print(f"  2. {output_name} (all years combined)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have the required files:")
        print(f"  - {xlsx_file}")
        print(f"  - {old_data}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_extract_only():
    """Extract year data only without merging."""
    
    xlsx_file = 'data/82-83.xlsx'
    
    print("\n" + "=" * 60)
    print("BUDGET DATA EXTRACTION - Year Only")
    print("=" * 60)
    print(f"Input: {xlsx_file}")
    print("No base data needed - extracting year only")
    print()
    
    try:
        result = extract_year_data(xlsx_file)
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"Extracted records: {len(result):,}")
        
        if 'Year' in result.columns:
            year = result['Year'].iloc[0]
            print(f"Year: {year}")
        
        print("\nFile created:")
        print("  - 2082.csv (clean year data)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\nMake sure you have: {xlsx_file}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Run both examples."""
    example_full_processing()
    print("\n" * 2)
    example_extract_only()


if __name__ == '__main__':
    main()

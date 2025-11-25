"""Example: Processing budget data."""

from pathlib import Path
from data_pipeline.budget import process_monthly_data

def example_simple_extraction():
    """Extract clean year data - PRIMARY USE CASE."""
    
    xlsx_file = 'data/82-83.xlsx'
    
    print("=" * 60)
    print("BUDGET PROCESSING - Extract Clean Year Data")
    print("=" * 60)
    print(f"Input: {xlsx_file}")
    print("✅ No done.csv needed!\n")
    
    try:
        # Just extract clean year data (no merging)
        result = process_monthly_data(xlsx_file=xlsx_file)
        
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"Extracted records: {len(result):,}")
        
        if 'Year' in result.columns:
            year = result['Year'].iloc[0]
            print(f"Year: {year}")
        
        print("\nFile created:")
        print("  ✅ 2082.csv (clean year data)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\nMake sure you have: {xlsx_file}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_with_merge():
    """OPTIONAL: Merge with historical data."""
    
    xlsx_file = 'data/82-83.xlsx'
    old_data = 'done.csv'
    output_name = 'output.csv'
    
    print("\n" + "=" * 60)
    print("BUDGET PROCESSING - With Historical Merge (Optional)")
    print("=" * 60)
    print(f"Input: {xlsx_file}")
    print(f"Historical data: {old_data}")
    print(f"Output: {output_name}\n")
    
    try:
        # Extract + merge with historical
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
        print("  ✅ 2082.csv (year-specific data)")
        print(f"  ✅ {output_name} (all years combined)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    """Run examples."""
    # Primary use case
    example_simple_extraction()
    
    # Optional: with merge
    print("\n" * 2)
    example_with_merge()


if __name__ == '__main__':
    main()

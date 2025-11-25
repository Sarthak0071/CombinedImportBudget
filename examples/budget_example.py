"""Budget processing examples."""

from data_pipeline.budget import process_monthly_data


def example_extract_only():
    """Extract clean year data without merging."""
    xlsx_file = 'data/82-83.xlsx'
    
    try:
        result = process_monthly_data(xlsx_file=xlsx_file)
        
        print(f"Extracted {len(result):,} records")
        if 'Year' in result.columns:
            print(f"Year: {result['Year'].iloc[0]}")
        print(f"Output: 2082.csv")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def example_with_merge():
    """Extract and merge with historical data."""
    xlsx_file = 'data/82-83.xlsx'
    old_data = 'done.csv'
    output_name = 'output.csv'
    
    try:
        result = process_monthly_data(
            xlsx_file=xlsx_file,
            old_data=old_data,
            output_name=output_name
        )
        
        print(f"Total records: {len(result):,}")
        
        if 'Year' in result.columns:
            for year in sorted(result['Year'].unique()):
                count = len(result[result['Year'] == year])
                print(f"  {year}: {count:,}")
        
        print(f"Outputs: 2082.csv, {output_name}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    example_extract_only()
    print()
    example_with_merge()

"""Trade data processing example."""

from data_pipeline.trade import process_monthly_data


def main():
    """Process cumulative trade data to calculate monthly values."""
    xlsx_file = 'data/FTS_uptoAsoj_208283_ci1nozq.xlsx'
    old_data = 'data/done.csv'
    output_name = 'updateddone.csv'
    
    try:
        result = process_monthly_data(
            xlsx_file=xlsx_file,
            old_data=old_data,
            output_name=output_name
        )
        
        print(f"Total records: {len(result):,}")
        
        if 'Direction' in result.columns:
            imports = len(result[result['Direction'] == 'I'])
            exports = len(result[result['Direction'] == 'E'])
            print(f"Imports: {imports:,}, Exports: {exports:,}")
        
        print(f"Outputs: month.csv, {output_name}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()

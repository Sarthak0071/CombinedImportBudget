import logging
from pathlib import Path
import pandas as pd

from .handlers import extract_budget_data, load_csv, standardize_data
from ..core.io import merge_with_base, save_csv
from ..core.utils import setup_logging, get_logger

setup_logging(level=logging.INFO)
logger = get_logger(__name__)


# Process budget file and return clean data (optionally merge with historical)
def process_monthly_data(xlsx_file: str, old_data: str = None, 
                         output_name: str = None) -> pd.DataFrame:
    
    try:
        input_file = Path(xlsx_file)
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {xlsx_file}")
        
        file_ext = input_file.suffix.lower()
        
        # Read Excel or CSV
        if file_ext in ['.xlsx', '.xls', '.xlsm']:
            new_data = extract_budget_data(input_file)
        elif file_ext == '.csv':
            new_data = load_csv(input_file)
            new_data = standardize_data(new_data)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Save year-specific file
        year = new_data['Year'].iloc[0] if 'Year' in new_data.columns else 'unknown'
        year_csv_name = f"{year}.csv".replace('/', '-')
        save_csv(new_data, Path(year_csv_name), f"Year {year} data")
        
        # Optionally merge with historical data
        if old_data:
            base_file = Path(old_data)
            if not base_file.exists():
                raise FileNotFoundError(f"Base file not found: {old_data}")
            
            merged = merge_with_base(new_data, base_file)
            output_path = Path(output_name or 'output.csv')
            save_csv(merged, output_path, "Combined budget data")
            return merged
        
        return new_data
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


# Extract year data only (no merging)
def extract_year_data(xlsx_file: str, output_name: str = None) -> pd.DataFrame:
    
    try:
        input_file = Path(xlsx_file)
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {xlsx_file}")
        
        file_ext = input_file.suffix.lower()
        
        if file_ext in ['.xlsx', '.xls', '.xlsm']:
            data = extract_budget_data(input_file)
        elif file_ext == '.csv':
            data = load_csv(input_file)
            data = standardize_data(data)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        if output_name is None:
            year = data['Year'].iloc[0] if 'Year' in data.columns else 'unknown'
            output_name = f"{year}.csv".replace('/', '-')
        
        save_csv(data, Path(output_name), "Year data")
        return data
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


# Wrapper for Excel files
def process_excel_data(excel_file: str, old_data: str = 'done.csv', 
                       output_name: str = 'updated.csv') -> pd.DataFrame:
    return process_monthly_data(excel_file, old_data, output_name)


# Wrapper for CSV files
def process_csv_data(csv_file: str, old_data: str = 'done.csv', 
                     output_name: str = 'updated.csv') -> pd.DataFrame:
    return process_monthly_data(csv_file, old_data, output_name)


__all__ = ['process_monthly_data', 'process_excel_data', 'process_csv_data', 'extract_year_data']


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m data_pipeline.budget <input_file> [base_data] [output_file]")
        print("Example: python -m data_pipeline.budget data/new.xlsx done.csv output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    base_data = sys.argv[2] if len(sys.argv) > 2 else 'done.csv'
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'output.csv'
    
    result = process_monthly_data(input_file, base_data, output_file)
    print(f"\nDone! Processed {len(result):,} records")

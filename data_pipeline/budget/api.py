import logging
from pathlib import Path
import pandas as pd

from .handlers import extract_budget_data, load_csv, standardize_data
from ..core.io import merge_with_base, save_csv
from ..core.utils import setup_logging, get_logger, get_file_type

setup_logging(level=logging.INFO)
logger = get_logger(__name__)


def process_data(xlsx_file: str, old_data: str = None, 
                 output_name: str = None) -> pd.DataFrame:
    
    try:
        input_file = Path(xlsx_file)
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {xlsx_file}")
        
        file_type = get_file_type(input_file)
        
        if file_type == 'excel':
            new_data = extract_budget_data(input_file)
        elif file_type == 'csv':
            new_data = load_csv(input_file)
            new_data = standardize_data(new_data)
        
        year = new_data['Year'].iloc[0] if 'Year' in new_data.columns else 'unknown'
        year_csv_name = f"{year}.csv".replace('/', '-')
        save_csv(new_data, Path(year_csv_name), f"Year {year} data")
        
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


__all__ = ['process_data']


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m data_pipeline.budget <input_file> [base_data] [output_file]")
        print("Example: python -m data_pipeline.budget data/new.xlsx done.csv output.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    base_data = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'output.csv'
    
    result = process_data(input_file, base_data, output_file)
    print(f"\nDone! Processed {len(result):,} records")

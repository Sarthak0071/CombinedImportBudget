"""Main API for budget data processing."""

import logging
from pathlib import Path
import pandas as pd

from .handlers import extract_budget_data, load_csv, standardize_data
from ..core.io import merge_with_base, save_csv
from ..core.utils import setup_logging, get_logger

setup_logging(level=logging.INFO)
logger = get_logger(__name__)


def process_monthly_data(
    xlsx_file: str,
    old_data: str = None,
    output_name: str = None
) -> pd.DataFrame:
    """
    Process budget data from Excel/CSV and return clean DataFrame.
    
    Primary use: Extract clean year data only (no merging needed).
    Optional: Merge with base data if old_data is provided.
    
    Args:
        xlsx_file: Path to input file (.xlsx, .xls, or .csv)
        old_data: Optional path to base historical data (if you want to merge)
        output_name: Optional output filename for combined data
    
    Returns:
        Clean budget DataFrame
    
    Outputs created:
        - {year}.csv: Year-specific clean data (e.g., 2082.csv) - ALWAYS created
        - {output_name}: Combined historical + new data - ONLY if old_data provided
    """
    try:
        logger.info(f"Starting budget data processing")
        
        input_file = Path(xlsx_file)
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {xlsx_file}")
        
        file_ext = input_file.suffix.lower()
        
        if file_ext in ['.xlsx', '.xls', '.xlsm']:
            logger.info("Detected Excel file")
            new_data = extract_budget_data(input_file)
            
        elif file_ext == '.csv':
            logger.info("Detected CSV file")
            new_data = load_csv(input_file)
            new_data = standardize_data(new_data)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}. Supported: .xlsx, .xls, .csv")
        
        # Extract year from new data
        year = new_data['Year'].iloc[0] if 'Year' in new_data.columns else 'unknown'
        year_csv_name = f"{year}.csv".replace('/', '-')
        
        # ALWAYS save year-specific CSV
        save_csv(new_data, Path(year_csv_name), f"Year {year} data")
        
        # OPTIONAL: Merge with base if old_data provided
        if old_data:
            base_file = Path(old_data)
            if not base_file.exists():
                raise FileNotFoundError(f"Base file not found: {old_data}")
            
            logger.info(f"Merging with base: {old_data}")
            merged = merge_with_base(new_data, base_file)
            
            # Save merged output
            output_path = Path(output_name or 'output.csv')
            save_csv(merged, output_path, "Combined budget data")
            
            logger.info(f"SUCCESS: Created {year_csv_name} and {output_path.name}")
            return merged
        else:
            logger.info(f"SUCCESS: Created {year_csv_name} (clean year data only)")
            return new_data
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise


def extract_year_data(xlsx_file: str, output_name: str = None) -> pd.DataFrame:
    """
    Extract and clean year data from Excel/CSV WITHOUT merging.
    
    No done.csv needed - just extracts the year data and saves it.
    Perfect for getting clean data for a single year.
    
    Args:
        xlsx_file: Path to input file (.xlsx, .xls, or .csv)
        output_name: Optional output filename (default: auto-generated from year)
    
    Returns:
        DataFrame with clean year data
        
    Example:
        df = extract_year_data('data/82-83.xlsx')
        # Creates: 2082.csv
    """
    try:
        logger.info(f"Extracting year data from: {xlsx_file}")
        
        input_file = Path(xlsx_file)
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {xlsx_file}")
        
        file_ext = input_file.suffix.lower()
        
        if file_ext in ['.xlsx', '.xls', '.xlsm']:
            logger.info("Detected Excel file")
            data = extract_budget_data(input_file)
            
        elif file_ext == '.csv':
            logger.info("Detected CSV file")
            data = load_csv(input_file)
            data = standardize_data(data)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        # Determine output filename
        if output_name is None:
            year = data['Year'].iloc[0] if 'Year' in data.columns else 'unknown'
            output_name = f"{year}.csv".replace('/', '-')
        
        # Save to CSV
        save_csv(data, Path(output_name), f"Year data")
        logger.info("SUCCESS: Extracted clean year data")
        
        return data
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise


def process_excel_data(excel_file: str, old_data: str = 'done.csv', output_name: str = 'updated.csv') -> pd.DataFrame:
    """Process Excel budget file, return merged DataFrame."""
    return process_monthly_data(excel_file, old_data, output_name)


def process_csv_data(csv_file: str, old_data: str = 'done.csv', output_name: str = 'updated.csv') -> pd.DataFrame:
    """Process CSV budget file, return merged DataFrame."""
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

"""Main API for processing monthly trade data."""

import sys
import logging
from pathlib import Path
from typing import Union
import pandas as pd

from .excel_reader import read_cumulative_excel
from .csv_handler import (
    read_done_csv,
    filter_prev_data,
    save_updated_csv
)
from .calculator import (
    process_trade_type,
    combine_import_export
)
from .cleaner import clean_monthly_data
from .config import DATA_DIR, TARGET_YEAR, TARGET_MONTH, NEPALI_MONTHS
from ..core.io import create_backup, save_csv
from ..core.utils import setup_logging, get_logger

setup_logging(level=logging.INFO)
logger = get_logger(__name__)


def process_monthly_data(
    xlsx_file: Union[str, Path],
    old_data: Union[str, Path],
    output_name: str = 'updateddone.csv'
) -> pd.DataFrame:
    """
    Process cumulative trade data and calculate monthly values.
    
    Args:
        xlsx_file: Path to Excel file with cumulative import/export data
        old_data: Path to historical CSV file
        output_name: Name for output file
    
    Returns:
        DataFrame with updated combined data
    """
    xlsx_path = Path(xlsx_file)
    old_data_path = Path(old_data)
    
    if not xlsx_path.exists():
        raise FileNotFoundError(f"File not found: {xlsx_path}")
    if not old_data_path.exists():
        raise FileNotFoundError(f"File not found: {old_data_path}")
    
    file_ext = xlsx_path.suffix.lower()
    
    if file_ext in ['.xlsx', '.xls']:
        import_cumulative, export_cumulative = read_cumulative_excel(xlsx_path)
        if import_cumulative is None and export_cumulative is None:
            raise ValueError("Failed to read import and export data")
    
    elif file_ext == '.csv':
        cumulative_df = pd.read_csv(xlsx_path)
        if 'Direction' not in cumulative_df.columns:
            raise ValueError("CSV must have 'Direction' column with 'I' or 'E'")
        
        import_cumulative = cumulative_df[cumulative_df['Direction'] == 'I'].copy() if 'I' in cumulative_df['Direction'].values else None
        export_cumulative = cumulative_df[cumulative_df['Direction'] == 'E'].copy() if 'E' in cumulative_df['Direction'].values else None
        
        if import_cumulative is None and export_cumulative is None:
            raise ValueError("CSV must contain records with Direction 'I' or 'E'")
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    done_df = read_done_csv(old_data_path)
    previous_filtered = filter_prev_data(done_df)
    
    import_monthly = pd.DataFrame()
    if import_cumulative is not None:
        import_monthly = process_trade_type(import_cumulative, previous_filtered, 'import')
    
    export_monthly = pd.DataFrame()
    if export_cumulative is not None:
        export_monthly = process_trade_type(export_cumulative, previous_filtered, 'export')
    
    monthly_df = combine_import_export(import_monthly, export_monthly)
    monthly_df = clean_monthly_data(monthly_df)
    
    monthly_only_path = old_data_path.parent / 'month.csv'
    save_csv(monthly_df, monthly_only_path, "Monthly data")
    
    create_backup(old_data_path)
    final_path = save_updated_csv(old_data_path, monthly_df, output_name)
    
    result_df = pd.read_csv(final_path)
    return result_df


__all__ = ['process_monthly_data']


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python -m data_pipeline.trade <xlsx_file> <old_data> [output_name]")
        print("Example: python -m data_pipeline.trade data/FTS.xlsx data/done.csv updateddone.csv")
        sys.exit(1)
    
    xlsx = sys.argv[1]
    old = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else 'updateddone.csv'
    
    result = process_monthly_data(xlsx, old, output)
    print(f"\nDone! Processed {len(result):,} records")

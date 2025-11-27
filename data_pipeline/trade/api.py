import sys
import logging
from pathlib import Path
from typing import Union
import pandas as pd

from .excel_reader import read_cumulative_excel
from .csv_handler import read_done_csv, filter_prev_data, save_updated_csv
from .calculator import process_trade_type, combine_import_export
from .cleaner import clean_monthly_data
from ..core.io import create_backup, save_csv
from ..core.utils import setup_logging, get_logger, get_file_type

setup_logging(level=logging.INFO)
logger = get_logger(__name__)


def process_data(xlsx_file: Union[str, Path], old_data: Union[str, Path], 
                 output_name: str = 'updateddone.csv',
                 replace_existing: bool = True) -> pd.DataFrame:
    
    xlsx_path = Path(xlsx_file)
    old_data_path = Path(old_data)
    
    if not xlsx_path.exists():
        raise FileNotFoundError(f"File not found: {xlsx_path}")
    if not old_data_path.exists():
        raise FileNotFoundError(f"File not found: {old_data_path}")
    
    file_type = get_file_type(xlsx_path)
    
    # Extract metadata from Excel file
    metadata = None
    if file_type == 'excel':
        from .excel_reader import TradeExcelReader
        reader = TradeExcelReader(xlsx_path)
        metadata = reader.extract_metadata()
        reader.close()
        
        if not metadata:
            raise ValueError(f"Could not extract year/month metadata from {xlsx_path.name}. "
                           "Please ensure the Excel file has proper headers with fiscal year and month range.")
        
        year = metadata['year']
        target_month = metadata['target_month']
        previous_month = metadata['previous_month']
        
        logger.info(f"✓ Detected metadata: Year={year}, Month={target_month}, "
                   f"Previous={previous_month} ({xlsx_path.name})")
        
        import_cumulative, export_cumulative = read_cumulative_excel(xlsx_path)
        if import_cumulative is None and export_cumulative is None:
            raise ValueError("Failed to read import and export data")
    
    elif file_type == 'csv':
        cumulative_df = pd.read_csv(xlsx_path)
        if 'Direction' not in cumulative_df.columns:
            raise ValueError("CSV must have 'Direction' column")
        
        # For CSV, try to extract from filename
        from .header_parser import _extract_year_from_filename
        year = _extract_year_from_filename(xlsx_path)
        if not year:
            raise ValueError(f"Could not extract year from CSV filename: {xlsx_path.name}")
        
        # CSV files need month to be specified - use default or raise error
        logger.warning("CSV input detected - assuming current month for processing")
        target_month = 6  # Default fallback - ideally this should be a parameter
        previous_month = 5
        
        import_cumulative = cumulative_df[cumulative_df['Direction'] == 'I'].copy() \
            if 'I' in cumulative_df['Direction'].values else None
        export_cumulative = cumulative_df[cumulative_df['Direction'] == 'E'].copy() \
            if 'E' in cumulative_df['Direction'].values else None
        
        if import_cumulative is None and export_cumulative is None:
            raise ValueError("No data with Direction 'I' or 'E'")
    
    done_df = read_done_csv(old_data_path)
    previous_filtered = filter_prev_data(done_df, year, previous_month)
    
    import_monthly = pd.DataFrame()
    if import_cumulative is not None:
        import_monthly = process_trade_type(import_cumulative, previous_filtered, 'import', year, target_month)
    
    export_monthly = pd.DataFrame()
    if export_cumulative is not None:
        export_monthly = process_trade_type(export_cumulative, previous_filtered, 'export', year, target_month)
    
    monthly_df = combine_import_export(import_monthly, export_monthly)
    monthly_df = clean_monthly_data(monthly_df)
    
    monthly_only_path = old_data_path.parent / 'month.csv'
    save_csv(monthly_df, monthly_only_path, "Monthly data")
    
    create_backup(old_data_path)
    final_path = save_updated_csv(old_data_path, monthly_df, output_name, replace_existing)
    
    return pd.read_csv(final_path)


__all__ = ['process_data']


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python -m data_pipeline.trade <xlsx_file> <old_data> [output_name]")
        print("Example: python -m data_pipeline.trade data/FTS.xlsx data/done.csv updateddone.csv")
        sys.exit(1)
    
    xlsx = sys.argv[1]
    old = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else 'updateddone.csv'
    
    result = process_data(xlsx, old, output)
    print(f"\nDone! Processed {len(result):,} records")

"""Public API for darta data processing."""

import logging
from pathlib import Path
import pandas as pd

from .pdf_reader import extract_tables_from_pdf
from .cleaner import process_darta_data
from ..core.io import save_csv
from ..core.utils import setup_logging, get_logger

setup_logging(level=logging.INFO)
logger = get_logger(__name__)


def process_data(pdf_file: str, output_name: str = 'darta_output.csv') -> pd.DataFrame:
    """
    Process darta PDF file and generate clean CSV.
    
    Args:
        pdf_file: Path to PDF file
        output_name: Output CSV filename
    
    Returns:
        Processed DataFrame
    """
    try:
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_file}")
        
        df = extract_tables_from_pdf(pdf_path)
        
        df = process_darta_data(df)
        
        output_path = Path(output_name)
        save_csv(df, output_path, "Darta data")
        
        return df
        
    except Exception as e:
        logger.error(f"Error processing darta data: {e}")
        raise


__all__ = ['process_data']


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m data_pipeline.darta <pdf_file> [output_name]")
        print("Example: python -m data_pipeline.darta data/darta.pdf darta_output.csv")
        sys.exit(1)
    
    pdf = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'darta_output.csv'
    
    result = process_data(pdf, output)
    print(f"\nDone! Processed {len(result):,} records")

"""Budget data handlers."""

import pandas as pd
import logging
from pathlib import Path

from ..core.io import read_csv, merge_with_base
from ..core.utils import clean_year_value
from .excel_reader import extract_budget_data
from .config import STANDARD_COLUMNS

logger = logging.getLogger(__name__)


def load_csv(csv_path: Path) -> pd.DataFrame:
    """Load and validate CSV file."""
    df = read_csv(csv_path)
    
    missing = set(STANDARD_COLUMNS) - set(df.columns)
    if missing:
        logger.warning(f"Missing columns: {missing}")
    
    return df


def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize CSV data."""
    if 'Year' in df.columns:
        df['Year'] = df['Year'].apply(clean_year_value)
    
    df = df.dropna(how='all')
    available_cols = [col for col in STANDARD_COLUMNS if col in df.columns]
    df = df[available_cols]
    
    if 'Year' in df.columns:
        for year in sorted(df['Year'].unique()):
            logger.info(f"Year {year}: {len(df[df['Year'] == year]):,} rows")
    
    return df


__all__ = ['extract_budget_data', 'load_csv', 'standardize_data', 'merge_with_base']

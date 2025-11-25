"""CSV handler for trade data."""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional

from ..core.io import read_csv, save_csv, create_backup
from .config import TARGET_YEAR, PREVIOUS_MONTH, EXPECTED_COLUMNS

logger = logging.getLogger(__name__)


def read_done_csv(csv_path: Path) -> pd.DataFrame:
    """Read done.csv file."""
    df = read_csv(csv_path)
    logger.info(f"Years in done.csv: {sorted(df['Year'].unique().tolist())}")
    return df


def filter_prev_data(done_df: pd.DataFrame) -> pd.DataFrame:
    """Filter data for previous months in target year."""
    filtered = done_df[
        (done_df['Year'] == TARGET_YEAR) &
        (done_df['Month'] <= PREVIOUS_MONTH)
    ].copy()
    
    if len(filtered) == 0:
        logger.warning(f"No data for Year={TARGET_YEAR}, Month≤{PREVIOUS_MONTH}")
    else:
        logger.info(f"Filtered {len(filtered):,} records (I:{len(filtered[filtered['Direction'] == 'I']):,}, E:{len(filtered[filtered['Direction'] == 'E']):,})")
    
    return filtered


def save_updated_csv(
    original_path: Path,
    monthly_df: pd.DataFrame,
    output_name: str = 'doneupdated.csv'
) -> Path:
    """Append monthly data to done.csv and save updated version."""
    done_df = read_csv(original_path)
    updated_df = pd.concat([done_df, monthly_df], ignore_index=True)
    
    logger.info(f"Appended {len(monthly_df):,} new records ({len(done_df):,} -> {len(updated_df):,})")
    
    output_path = original_path.parent / output_name
    return save_csv(updated_df, output_path, "Updated CSV")


def validate_csv_structure(df: pd.DataFrame) -> bool:
    """Validate CSV has expected column structure."""
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    
    if missing_cols:
        raise ValueError(f"CSV missing columns: {missing_cols}")
    
    return True

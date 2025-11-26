"""CSV handler for trade data."""

import pandas as pd
import logging
from pathlib import Path

from ..core.io import read_csv, save_csv
from .config import TARGET_YEAR, PREVIOUS_MONTH

logger = logging.getLogger(__name__)


def read_done_csv(csv_path: Path) -> pd.DataFrame:
    df = read_csv(csv_path)
    logger.info(f"Years in done.csv: {sorted(df['Year'].unique().tolist())}")
    return df


def filter_prev_data(done_df: pd.DataFrame) -> pd.DataFrame:
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
    done_df = read_csv(original_path)
    updated_df = pd.concat([done_df, monthly_df], ignore_index=True)
    
    logger.info(f"Appended {len(monthly_df):,} new records ({len(done_df):,} -> {len(updated_df):,})")
    
    output_path = original_path.parent / output_name
    return save_csv(updated_df, output_path, "Updated CSV")

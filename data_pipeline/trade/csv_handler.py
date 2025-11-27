"""CSV handler for trade data - now with functional filters."""

import pandas as pd
import logging
from pathlib import Path

from ..core.io import read_csv, save_csv
from ..core.utils import create_filter, combine_filters

logger = logging.getLogger(__name__)


def read_done_csv(csv_path: Path) -> pd.DataFrame:
    """Read historical done.csv file."""
    df = read_csv(csv_path)
    logger.info(f"Years in done.csv: {sorted(df['Year'].unique().tolist())}")
    return df


def filter_prev_data(done_df: pd.DataFrame, year: int, previous_month: int) -> pd.DataFrame:
    """Filter previous data using functional composition."""
    year_filter = create_filter('Year', '==', year)
    month_filter = create_filter('Month', '<=', previous_month)
    
    combined_filter = combine_filters(year_filter, month_filter)
    filtered = combined_filter(done_df)
    
    if len(filtered) == 0:
        logger.warning(f"No data for Year={year}, Month≤{previous_month}"
)
    else:
        logger.info(f"Filtered {len(filtered):,} records (I:{len(filtered[filtered['Direction'] == 'I']):,}, "
                    f"E:{len(filtered[filtered['Direction'] == 'E']):,})")
    
    return filtered


def save_updated_csv(
    original_path: Path,
    monthly_df: pd.DataFrame,
    output_name: str = 'doneupdated.csv'
) -> Path:
    """Append monthly data to done.csv and save."""
    done_df = read_csv(original_path)
    updated_df = pd.concat([done_df, monthly_df], ignore_index=True)
    
    logger.info(f"Appended {len(monthly_df):,} new records ({len(done_df):,} -> {len(updated_df):,})")
    
    output_path = original_path.parent / output_name
    return save_csv(updated_df, output_path, "Updated CSV")

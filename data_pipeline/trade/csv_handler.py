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
    """Filter previous data using functional composition (fiscal year aware)."""
    year_filter = create_filter('Year', '==', year)
    
    if previous_month >= 4:
        # Case 1: Mid-year months (4-12)
        # Fiscal year starts at month 4, so get months from 4 to previous_month
        fiscal_start_filter = create_filter('Month', '>=', 4)
        month_filter = create_filter('Month', '<=', previous_month)
        combined_filter = combine_filters(year_filter, fiscal_start_filter, month_filter)
        
    else:
        # Case 2: End-of-year months (1-3)
        # Get months 4-12 (fiscal year start) AND months 1 to previous_month
        # Example: For month 2 (Jestha), previous_month=1, get [4-12] + [1]
        # This requires OR logic: (Month >= 4) OR (Month <= previous_month)
        
        # Filter for months >= 4
        fiscal_start_subset = done_df[(done_df['Year'] == year) & (done_df['Month'] >= 4)]
        # Filter for months <= previous_month
        early_months_subset = done_df[(done_df['Year'] == year) & (done_df['Month'] <= previous_month)]
        # Combine with OR (union)
        filtered = pd.concat([fiscal_start_subset, early_months_subset]).drop_duplicates()
        
        if len(filtered) == 0:
            logger.warning(f"No data for Year={year}, Months≥4 or ≤{previous_month}")
        else:
            months_str = sorted(filtered['Month'].unique())
            logger.info(f"Filtered {len(filtered):,} records for months {months_str} "
                       f"(I:{len(filtered[filtered['Direction'] == 'I']):,}, "
                       f"E:{len(filtered[filtered['Direction'] == 'E']):,})")
        
        return filtered
    
    # Apply filter for case 1
    filtered = combined_filter(done_df)
    
    if len(filtered) == 0:
        logger.warning(f"No data for Year={year}, Month≥4 and ≤{previous_month}")
    else:
        logger.info(f"Filtered {len(filtered):,} records (I:{len(filtered[filtered['Direction'] == 'I']):,}, "
                    f"E:{len(filtered[filtered['Direction'] == 'E']):,})")
    
    return filtered


def save_updated_csv(
    original_path: Path,
    monthly_df: pd.DataFrame,
    output_name: str = 'doneupdated.csv',
    replace_existing: bool = True
) -> Path:
    """Append monthly data to done.csv, optionally replacing existing year-month data."""
    done_df = read_csv(original_path)
    
    if replace_existing and not monthly_df.empty:
        if all(col in monthly_df.columns for col in ['Year', 'Month', 'Direction']):
            new_combinations = monthly_df[['Year', 'Month', 'Direction']].drop_duplicates()
            
            for _, row in new_combinations.iterrows():
                year = row['Year']
                month = row['Month']
                direction = row['Direction']
                
                mask = ((done_df['Year'] == year) & 
                        (done_df['Month'] == month) & 
                        (done_df['Direction'] == direction))
                
                removed_count = mask.sum()
                done_df = done_df[~mask]
                
                if removed_count > 0:
                    dir_name = 'Import' if direction == 'I' else 'Export'
                    logger.info(f"Removed {removed_count:,} {dir_name} records for Year={year}, Month={month}")
    
    updated_df = pd.concat([done_df, monthly_df], ignore_index=True)
    
    logger.info(f"Appended {len(monthly_df):,} new records ({len(done_df):,} -> {len(updated_df):,})")
    
    output_path = original_path.parent / output_name
    return save_csv(updated_df, output_path, "Updated CSV")

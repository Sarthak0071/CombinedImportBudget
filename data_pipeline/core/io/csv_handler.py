import pandas as pd
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


def read_csv(csv_path: Path, encoding: str = 'utf-8-sig') -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    df = pd.read_csv(csv_path, encoding=encoding)
    logger.info(f"Read {csv_path.name}: {len(df):,} records")
    
    return df


def save_csv(df: pd.DataFrame, output_path: Path, description: str = "DataFrame",
             encoding: str = 'utf-8-sig') -> Path:
    df.to_csv(output_path, index=False, encoding=encoding)
    size_mb = output_path.stat().st_size / 1024 / 1024
    logger.info(f"Saved {description} to {output_path.name} ({len(df):,} records, {size_mb:.2f} MB)")
    return output_path


def create_backup(csv_path: Path, backup_count: int = 5):
    if not csv_path.exists():
        logger.warning(f"Cannot backup {csv_path.name}: file not found")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = csv_path.parent / f"{csv_path.stem}_backup_{timestamp}.csv"
    
    shutil.copy2(csv_path, backup_path)
    logger.info(f"Created backup: {backup_path.name}")
    
    backup_files = sorted(
        csv_path.parent.glob(f"{csv_path.stem}_backup_*.csv"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    for old_backup in backup_files[backup_count:]:
        old_backup.unlink()
        logger.info(f"Removed old backup: {old_backup.name}")


def merge_with_base(new_df: pd.DataFrame, base_path: Path, 
                    strategy: str = 'append') -> pd.DataFrame:
    base_df = read_csv(base_path)
    logger.info(f"Merging: {len(base_df):,} base + {len(new_df):,} new rows")
    
    common_cols = list(set(base_df.columns) & set(new_df.columns))
    if set(base_df.columns) != set(new_df.columns):
        logger.warning(f"Using {len(common_cols)} common columns")
        base_df, new_df = base_df[common_cols], new_df[common_cols]
    
    merged = pd.concat([base_df, new_df], ignore_index=True)
    
    if 'Year' in merged.columns:
        merged['Year'] = merged['Year'].astype(str)
        for year in sorted(merged['Year'].unique()):
            logger.info(f"  {year}: {len(merged[merged['Year'] == year]):,} rows")
    
    return merged

"""Shared data utilities - consolidated from both projects."""

import re
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def extract_fiscal_year(filename: str) -> Optional[str]:
    """Extract fiscal year from filename (e.g., 82-83.xlsx -> 82-83)."""
    filename = Path(filename).stem
    match = re.search(r'(\d{2,4})[_-](\d{2})', filename)
    return f"{match.group(1)}-{match.group(2)}" if match else None


def clean_year_value(year_val) -> str:
    """Standardize year value (77-78 -> 2077, 2077/78 -> 2077)."""
    year_str = str(year_val).strip()
    if "/" in year_str:
        return year_str.split("/")[0]
    if "-" in year_str:
        parts = year_str.split("-")
        return "20" + parts[0] if len(parts[0]) == 2 else parts[0]
    if len(year_str) == 2:
        return "20" + year_str
    return year_str


def clean_numeric_column(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """Clean and convert column to numeric."""
    df = df.copy()
    
    if col_name in df.columns:
        df[col_name] = pd.to_numeric(df[col_name], errors='coerce').fillna(0)
    
    return df


def remove_total_rows(df: pd.DataFrame, key_column: str = 'HS_Code') -> pd.DataFrame:
    """Remove rows that contain 'total' in specified column."""
    df = df.copy()
    
    if key_column in df.columns:
        df = df[~df[key_column].astype(str).str.lower().str.contains('total', na=False)]
    
    return df


def standardize_column_names(df: pd.DataFrame, mode: str = 'generic') -> pd.DataFrame:
    """
    Clean and standardize column names.
    
    Args:
        df: DataFrame to process
        mode: 'generic' for basic cleaning, 'trade' for trade-specific, 'budget' for budget-specific
    """
    df = df.copy()
    
    if mode == 'budget':
        # Budget mode: Clean nulls and whitespace
        new_columns = []
        for col in df.columns:
            if pd.isna(col) or str(col).strip() == "":
                new_columns.append(None)
                continue
            col_str = str(col).strip()
            col_str = re.sub(r'\s+', ' ', col_str).replace('\n', '')
            new_columns.append(col_str)
        df.columns = new_columns
        return df.loc[:, df.columns.notna()]
    
    elif mode == 'trade':
        # Trade mode: Normalize and map to expected columns
        df.columns = [
            str(c).lower().strip().replace(' ', '_').replace('.', '') 
            for c in df.columns
        ]
        
        col_map = {}
        for col in df.columns:
            if any(x in col for x in ['hscode', 'hs_code', 'code', 'hs']):
                col_map[col] = 'HS_Code'
            elif any(x in col for x in ['description', 'commodity', 'item']):
                col_map[col] = 'Commodity'
            elif any(x in col for x in ['partner', 'country', 'countries']):
                col_map[col] = 'Country'
            elif col == 'unit':
                col_map[col] = 'Unit'
            elif 'quantity' in col:
                col_map[col] = 'Quantity'
            elif 'value' in col:
                col_map[col] = 'Value'
            elif 'revenue' in col:
                col_map[col] = 'Revenue'
        
        df = df.rename(columns=col_map)
        return df
    
    else:
        # Generic mode: Basic cleaning
        df.columns = [str(c).strip() for c in df.columns]
        return df


def find_data_start_row(df_sample: pd.DataFrame) -> int:
    """Find the row where actual data headers start in Excel."""
    for row_idx, row in df_sample.iterrows():
        row_str = ' '.join(str(val).lower() for val in row)
        row_str = row_str.replace('_', '').replace(' ', '')
        
        if 'hscode' in row_str or 'code' in row_str:
            return row_idx
    
    return 0


# Validate DataFrame has required columns
def validate_columns(df: pd.DataFrame, required_cols: list) -> bool:
    missing = [col for col in required_cols if col not in df.columns]
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return True

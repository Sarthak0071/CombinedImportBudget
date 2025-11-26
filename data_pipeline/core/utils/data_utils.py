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


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names (remove nulls, whitespace, newlines)."""
    df = df.copy()
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


def find_data_start_row(df_sample: pd.DataFrame) -> int:
    """Find the row where actual data headers start in Excel."""
    for row_idx, row in df_sample.iterrows():
        row_str = ' '.join(str(val).lower() for val in row)
        row_str = row_str.replace('_', '').replace(' ', '')
        
        if 'hscode' in row_str or 'code' in row_str:
            return row_idx
    
    return 0


def find_target_sheet(sheet_names: list, keywords: list) -> Optional[str]:
    """Find Excel sheet containing target data based on keywords."""
    for name in sheet_names:
        name_lower = name.lower()
        for keyword in keywords:
            if str(keyword) in name_lower:
                return name
    
    return None


def get_file_type(file_path: Path) -> str:
    """Detect file type from extension."""
    ext = file_path.suffix.lower()
    if ext in ['.xlsx', '.xls', '.xlsm']:
        return 'excel'
    elif ext == '.csv':
        return 'csv'
    raise ValueError(f"Unsupported file type: {ext}")


def create_key(df: pd.DataFrame, *cols) -> pd.DataFrame:
    """Create composite key from multiple columns."""
    df = df.copy()
    df['_key'] = df[list(cols)].astype(str).agg('|'.join, axis=1)
    return df


def clean_hs_code(df: pd.DataFrame) -> pd.DataFrame:
    """Clean HS_Code column (remove .0 suffix, strip whitespace)."""
    df = df.copy()
    if 'HS_Code' in df.columns:
        df['HS_Code'] = df['HS_Code'].astype(str).str.strip().str.replace('.0', '', regex=False)
    return df


from difflib import SequenceMatcher
from typing import Optional, List, Dict
import pandas as pd


def find_column(df: pd.DataFrame, target: str, threshold: float = 0.85) -> Optional[str]:
    """
    Find column in DataFrame using fuzzy matching.
    
    Handles variations like:
    - 'HS_Code' matches 'HSCode', 'HS Code', 'HS-Code', 'HSCODE'
    - 'Country' matches 'Partner', 'Partner Country', 'Countries'
    
    Args:
        df: DataFrame to search
        target: Target column name
        threshold: Similarity threshold (0.0-1.0)
    
    Returns:
        Actual column name if found, None otherwise
    """
    target_clean = target.lower().replace('_', '').replace(' ', '').replace('-', '')
    
    best_match = None
    best_ratio = 0
    
    for col in df.columns:
        col_clean = str(col).lower().replace('_', '').replace(' ', '').replace('-', '')
        ratio = SequenceMatcher(None, target_clean, col_clean).ratio()
        
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = col
    
    return best_match


def find_columns(df: pd.DataFrame, targets: List[str], threshold: float = 0.85) -> Dict[str, Optional[str]]:
    """
    Find multiple columns at once.
    
    Args:
        df: DataFrame to search
        targets: List of target column names
        threshold: Similarity threshold
    
    Returns:
        Dict mapping target -> actual column name
    """
    mapping = {}
    for target in targets:
        actual = find_column(df, target, threshold)
        if actual:
            mapping[target] = actual
    return mapping


def rename_columns_fuzzy(df: pd.DataFrame, column_map: Dict[str, str], threshold: float = 0.85) -> pd.DataFrame:
    """
    Rename DataFrame columns using fuzzy matching.
    
    Args:
        df: DataFrame to rename
        column_map: {'expected_name': 'standard_name'}
        threshold: Matching threshold
    
    Returns:
        DataFrame with renamed columns
    """
    rename_dict = {}
    
    for expected, standard in column_map.items():
        actual = find_column(df, expected, threshold)
        if actual:
            rename_dict[actual] = standard
    
    return df.rename(columns=rename_dict)

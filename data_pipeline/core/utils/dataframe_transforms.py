"""Composable DataFrame transformation functions."""

import pandas as pd
from typing import Callable
from .functional_utils import with_column, apply_if_exists


def to_numeric_safe(series: pd.Series) -> pd.Series:
    """Convert to numeric with error handling."""
    return pd.to_numeric(series, errors='coerce').fillna(0)


def clean_numerics(*columns: str) -> Callable:
    """Returns function that cleans numeric columns."""
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in columns:
            if col in result.columns:
                result[col] = to_numeric_safe(result[col])
        return result
    return transform


def clean_hs_codes_fn(df: pd.DataFrame) -> pd.DataFrame:
    """Clean HS_Code column."""
    return with_column(
        df, 
        'HS_Code',
        lambda s: s.astype(str).str.strip().str.replace('.0', '', regex=False)
    )


def strip_strings(*columns: str) -> Callable:
    """Returns function that strips string columns."""
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in columns:
            if col in result.columns and result[col].dtype == object:
                result[col] = result[col].astype(str).str.strip()
        return result
    return transform


def add_composite_key(*columns: str) -> Callable:
    """Returns function that creates composite key from columns."""
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result['_key'] = result[list(columns)].astype(str).agg('|'.join, axis=1)
        return result
    return transform


def remove_nulls(*columns: str) -> Callable:
    """Returns function that removes rows with null values in specified columns."""
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        for col in columns:
            if col in result.columns:
                result = result[result[col].notna()]
        return result
    return transform


def remove_rows_containing(column: str, substring: str) -> Callable:
    """Returns function that removes rows where column contains substring."""
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        if column not in df.columns:
            return df
        result = df.copy()
        mask = ~result[column].astype(str).str.lower().str.contains(substring.lower(), na=False)
        return result[mask]
    return transform


def apply_to_column(column: str, func: Callable) -> Callable:
    """Returns function that applies func to each element in specific column."""
    def transform(df: pd.DataFrame) -> pd.DataFrame:
        if column not in df.columns:
            return df
        result = df.copy()
        result[column] = result[column].apply(func)
        return result
    return transform

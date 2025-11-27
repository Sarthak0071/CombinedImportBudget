"""Functional programming utilities for composable data operations."""

from functools import reduce
from typing import Callable, List, Any
import pandas as pd


def pipe(data: Any, *functions: Callable) -> Any:
    """Apply functions in sequence (left to right).
    
    Example:
        result = pipe(df, clean_numerics('Value'), remove_nulls('Country'))
    """
    return reduce(lambda x, f: f(x), functions, data)


def compose(*functions: Callable) -> Callable:
    """Compose functions (right to left)."""
    return lambda x: reduce(lambda acc, f: f(acc), reversed(functions), x)


def with_column(df: pd.DataFrame, column: str, transform_fn: Callable) -> pd.DataFrame:
    """Apply transformation only if column exists."""
    if column not in df.columns:
        return df
    result = df.copy()
    result[column] = transform_fn(result[column])
    return result


def create_filter(column: str, operator: str, value: Any) -> Callable:
    """Create DataFrame filter function.
    
    Example:
        year_filter = create_filter('Year', '==', 2082)
        filtered = year_filter(df)
    """
    ops = {
        '==': lambda df: df[column] == value,
        '!=': lambda df: df[column] != value,
        '<=': lambda df: df[column] <= value,
        '>=': lambda df: df[column] >= value,
        '<': lambda df: df[column] < value,
        '>': lambda df: df[column] > value,
        'in': lambda df: df[column].isin(value if isinstance(value, list) else [value])
    }
    
    if operator not in ops:
        raise ValueError(f"Unsupported operator: {operator}")
    
    return ops[operator]


def combine_filters(*filters: Callable) -> Callable:
    """Combine multiple filters with AND logic."""
    def apply_all(df: pd.DataFrame) -> pd.DataFrame:
        if not filters:
            return df
        mask = filters[0](df)
        for f in filters[1:]:
            mask &= f(df)
        return df[mask].copy()
    return apply_all


def filter_by_column(column: str, operator: str, value: Any) -> Callable:
    """Create reusable column filter."""
    filter_fn = create_filter(column, operator, value)
    return lambda df: df[filter_fn(df)].copy()


def safe_copy_transform(transform_fn: Callable) -> Callable:
    """Decorator ensuring DataFrame copy before transformation."""
    def wrapper(df: pd.DataFrame) -> pd.DataFrame:
        return transform_fn(df.copy())
    return wrapper


def apply_if_exists(df: pd.DataFrame, column: str, operation: Callable) -> pd.DataFrame:
    """Apply operation to column only if it exists."""
    if column in df.columns:
        result = df.copy()
        result[column] = operation(result[column])
        return result
    return df

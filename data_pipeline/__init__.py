"""Unified data processing pipeline for Nepal data."""

from .trade import process_monthly_data as process_trade_data
from .budget import (
    process_monthly_data as process_budget_data,
    extract_year_data
)

__version__ = '1.0.0'
__all__ = ['process_trade_data', 'process_budget_data', 'extract_year_data']

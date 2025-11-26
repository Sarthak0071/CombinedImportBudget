"""Tests for budget processing."""
import pytest
from pathlib import Path
import pandas as pd


def test_budget_import():
    """Test that budget module can be imported."""
    from data_pipeline.budget import process_data
    assert process_data is not None


def test_budget_processing():
    """Test budget processing with actual files if they exist."""
    from data_pipeline.budget import process_data
    
    data_dir = Path('data')
    xlsx_file = data_dir / '82-83.xlsx'
    
    if not xlsx_file.exists():
        pytest.skip(f"Test data not found: {xlsx_file}")
    
    # Process data
    result = process_data(str(xlsx_file))
    
    # Verify result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    
    # Verify expected columns exist
    assert 'Year' in result.columns
    assert 'Amount' in result.columns
    
    # Clean up test output
    year_csv = Path('2082.csv')
    if year_csv.exists():
        year_csv.unlink()


def test_budget_config():
    """Test budget configuration constants."""
    from data_pipeline.budget.config import (
        STANDARD_COLUMNS,
        COLUMN_MAPPING,
        COLUMNS_TO_REMOVE,
        SHEET_PATTERNS
    )
    
    # Verify configuration exists
    assert len(STANDARD_COLUMNS) > 0
    assert 'Year' in STANDARD_COLUMNS
    assert 'Amount' in STANDARD_COLUMNS
    
    assert 'BUD_YEAR' in COLUMN_MAPPING
    assert COLUMN_MAPPING['BUD_YEAR'] == 'Year'
    
    assert len(COLUMNS_TO_REMOVE) > 0
    assert len(SHEET_PATTERNS) > 0


def test_no_duplicate_functions():
    """Verify duplicate functions were removed from config."""
    from data_pipeline.budget import config
    
    # These should NOT exist in budget.config anymore
    assert not hasattr(config, 'extract_fiscal_year')
    assert not hasattr(config, 'clean_year_value')
    assert not hasattr(config, 'standardize_column_names')
    assert not hasattr(config, 'get_government_level')
    
    # But they should exist in core.utils
    from data_pipeline.core.utils import extract_fiscal_year, clean_year_value
    assert extract_fiscal_year is not None
    assert clean_year_value is not None

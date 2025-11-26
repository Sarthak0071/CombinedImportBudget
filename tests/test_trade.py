"""Tests for trade processing."""
import pytest
from pathlib import Path
import pandas as pd


def test_trade_import():
    """Test that trade module can be imported."""
    from data_pipeline.trade import process_data
    assert process_data is not None


def test_trade_processing():
    """Test trade processing with actual files if they exist."""
    from data_pipeline.trade import process_data
    
    data_dir = Path('data')
    xlsx_file = data_dir / 'FTS_uptoAsoj_208283_ci1nozq.xlsx'
    old_data = data_dir / 'done.csv'
    
    if not xlsx_file.exists():
        pytest.skip(f"Test data not found: {xlsx_file}")
    
    if not old_data.exists():
        pytest.skip(f"Test data not found: {old_data}")
    
    # Process data
    result = process_data(str(xlsx_file), str(old_data), 'test_output.csv')
    
    # Verify result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    
    # Clean up test output
    test_output = Path('test_output.csv')
    if test_output.exists():
        test_output.unlink()


def test_trade_core_utils():
    """Test core utilities used by trade module."""
    from data_pipeline.core.utils import (
        extract_fiscal_year,
        clean_year_value,
        standardize_column_names,
        find_data_start_row,
        find_target_sheet
    )
    
    # Test fiscal year extraction
    # Note: FTS filename doesn't follow standard pattern, returns None
    assert extract_fiscal_year('82-83.xlsx') == '82-83'
    assert extract_fiscal_year('2082-83.xlsx') == '2082-83'
    
    # Test year cleaning
    assert clean_year_value('77-78') == '2077'
    assert clean_year_value('2077/78') == '2077'
    assert clean_year_value('2077') == '2077'
    
    # Test column standardization
    df = pd.DataFrame(columns=['  Test  ', None, 'Another\nColumn'])
    cleaned = standardize_column_names(df)
    assert 'Test' in cleaned.columns
    assert 'Another Column' in cleaned.columns
    assert None not in cleaned.columns

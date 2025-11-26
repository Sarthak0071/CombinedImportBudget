"""Tests for core utilities cleanup."""
import pytest
import pandas as pd


def test_removed_functions():
    """Verify unused functions were removed."""
    from data_pipeline.core import utils
    
    # These should NOT exist anymore
    assert not hasattr(utils, 'create_composite_key')
    assert not hasattr(utils, 'validate_dataframe')
    assert not hasattr(utils, 'find_columns')
    assert not hasattr(utils, 'rename_columns_fuzzy')
    
    # These SHOULD still exist
    assert hasattr(utils, 'extract_fiscal_year')
    assert hasattr(utils, 'clean_year_value')
    assert hasattr(utils, 'standardize_column_names')
    assert hasattr(utils, 'find_column')


def test_find_column_optimized():
    """Test optimized find_column function."""
    from data_pipeline.core.utils import find_column
    
    df = pd.DataFrame(columns=['HS Code', 'Country Name', 'Value'])
    
    # Should find columns with fuzzy matching
    assert find_column(df, 'HS_Code') == 'HS Code'
    assert find_column(df, 'Country', threshold=0.5) == 'Country Name'  # Lower threshold for partial match
    assert find_column(df, 'Value') == 'Value'
    
    # Should return None if no match
    assert find_column(df, 'NonExistent') is None


def test_standardize_column_names_generic():
    """Test that standardize_column_names is now generic only."""
    from data_pipeline.core.utils import standardize_column_names
    
    # Create test DataFrame
    df = pd.DataFrame(columns=['  Test  ', None, 'Another\nColumn', ''])
    
    # Should clean whitespace and remove nulls/empty
    cleaned = standardize_column_names(df)
    
    assert 'Test' in cleaned.columns
    assert 'Another Column' in cleaned.columns
    assert len(cleaned.columns) == 2  # Only 2 valid columns
    
    # Verify it doesn't have mode parameter anymore
    import inspect
    sig = inspect.signature(standardize_column_names)
    assert 'mode' not in sig.parameters


def test_csv_handler_cleanup():
    """Verify unused CSV handler functions were removed."""
    from data_pipeline.core.io import csv_handler
    
    # These should NOT exist anymore
    assert not hasattr(csv_handler, 'detect_file_type')
    assert not hasattr(csv_handler, 'validate_csv_structure')
    
    # These SHOULD still exist
    assert hasattr(csv_handler, 'read_csv')
    assert hasattr(csv_handler, 'save_csv')
    assert hasattr(csv_handler, 'create_backup')
    assert hasattr(csv_handler, 'merge_with_base')

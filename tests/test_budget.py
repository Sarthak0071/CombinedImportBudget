"""Tests for budget data processing."""

import pytest
import pandas as pd
from pathlib import Path
from data_pipeline.budget import process_data


class TestBudgetProcessing:
    """Test suite for budget module."""
    
    def test_budget_extraction(self):
        """Test basic budget data extraction."""
        result = process_data('data/82-83.xlsx')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert len(result) == 44263
        
    def test_budget_columns(self):
        """Test budget output has expected columns."""
        result = process_data('data/82-83.xlsx')
        
        expected_cols = ['Year', 'Project_Code', 'Amount']
        for col in expected_cols:
            assert col in result.columns
            
    def test_budget_year_extraction(self):
        """Test fiscal year is correctly extracted."""
        result = process_data('data/82-83.xlsx')
        
        assert result['Year'].notna().all()
        assert 2082 in result['Year'].values or '2082' in result['Year'].values

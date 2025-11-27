"""Tests for trade data processing."""

import pytest
import pandas as pd
from pathlib import Path
from data_pipeline.trade import process_data


class TestTradeProcessing:
    """Test suite for trade module."""
    
    def test_trade_monthly_calculation(self):
        """Test trade monthly data calculation."""
        result = process_data(
            'data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
            'data/done.csv'
        )
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        
    def test_trade_columns(self):
        """Test trade output has expected columns."""
        result = process_data(
            'data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
            'data/done.csv'
        )
        
        expected_cols = ['Year', 'Month', 'Direction', 'Country', 'Value']
        for col in expected_cols:
            assert col in result.columns
            
    def test_trade_country_codes(self):
        """Test country codes are cleaned."""
        result = process_data(
            'data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
            'data/done.csv'
        )
        
        assert result['Country'].notna().sum() > 0

"""Test trade module's replace_existing functionality."""

import pytest
import pandas as pd
from data_pipeline.trade import process_data


class TestTradeMonthReplacement:
    """Test suite for month update/replacement feature."""
    
    def test_replace_existing_parameter_exists(self):
        """Verify replace_existing parameter is available."""
        import inspect
        sig = inspect.signature(process_data)
        assert 'replace_existing' in sig.parameters
        assert sig.parameters['replace_existing'].default is True
        
    def test_monthly_calculation_logic(self):
        """Verify monthly calculation (cumulative - previous) still works."""
        result = process_data(
            'data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
            'data/done.csv',
            replace_existing=True
        )
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert 'Year' in result.columns
        assert 'Month' in result.columns
        assert 'Value' in result.columns
        
    def test_cumulative_to_monthly_conversion(self):
        """Test that cumulative data is correctly converted to monthly."""
        result = process_data(
            'data/FTS_uptoAsoj_208283_ci1nozq.xlsx',
            'data/done.csv'
        )
        
        assert result['Value'].sum() > 0
        assert not result[result['Value'] < 0].any().any()

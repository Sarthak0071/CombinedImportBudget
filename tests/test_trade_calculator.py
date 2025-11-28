"""Tests for trade calculator module - cumulative to monthly conversion."""
import pytest
import pandas as pd
from data_pipeline.trade.calculator import (
    calculate_previous_cumulative,
    calculate_monthly_values,
    process_trade_type,
    combine_import_export
)


class TestCalculatePreviousCumulative:
    """Test calculation of previous cumulative values."""
    
    @pytest.fixture
    def sample_previous_data(self):
        """Sample previous months data."""
        return pd.DataFrame({
            'Direction': ['I', 'I', 'I', 'E', 'E'],
            'HS_Code': ['1001', '1001', '1002', '2001', '2002'],
            'Country': ['IN', 'CN', 'IN', 'US', 'UK'],
            'Value': [100, 50, 200, 300, 150],
            'Quantity': [10, 5, 20, 30, 15],
            'Unit': ['kg', 'kg', 'kg', 'pcs', 'pcs'],
            'Revenue': [50, 25, 100, 0, 0]
        })
    
    def test_calculate_import_cumulative(self, sample_previous_data):
        """Test calculation for import data."""
        result = calculate_previous_cumulative(sample_previous_data, 'import')
        
        assert len(result) > 0, "Should return cumulative data"
        assert all(result['Value'] > 0), "All values should be positive"
        
        # Check aggregation for HS_Code 1001 (should sum IN + CN)
        hs1001 = result[result['HS_Code'] == '1001']
        if len(hs1001) > 0:
            # Should be aggregated by HS_Code+Country combination
            assert len(hs1001) == 2, "Should have 2 entries for different countries"
    
    def test_calculate_export_cumulative(self, sample_previous_data):
        """Test calculation for export data."""
        result = calculate_previous_cumulative(sample_previous_data, 'export')
        
        assert len(result) > 0, "Should return cumulative data"
        # Note: Direction column is not in result after groupby
    
    def test_empty_data_returns_empty(self):
        """Test that empty dataframe returns empty result."""
        empty_df = pd.DataFrame({'Direction': []})
        result = calculate_previous_cumulative(empty_df, 'import')
        
        assert len(result) == 0, "Empty input should return empty output"


class TestCalculateMonthlyValues:
    """Test monthly value calculation (current - previous)."""
    
    @pytest.fixture
    def current_cumulative(self):
        """Current cumulative data."""
        return pd.DataFrame({
            'HS_Code': ['1001', '1002', '1003'],
            'Country': ['IN', 'CN', 'US'],
            'Value': [500, 300, 200],
            'Quantity': [50, 30, 20],
            'Unit': ['kg', 'kg', 'pcs'],
            'Revenue': [250, 150, 0]
        })
    
    @pytest.fixture
    def previous_cumulative(self):
        """Previous cumulative data."""
        return pd.DataFrame({
            '_key': ['1001_IN', '1002_CN'],
            'HS_Code': ['1001', '1002'],
            'Country': ['IN', 'CN'],
            'Value': [300, 100],
            'Quantity': [30, 10],
            'Unit': ['kg', 'kg'],
            'Revenue': [150, 50]
        })
    
    def test_calculate_monthly_positive_values(self, current_cumulative, previous_cumulative):
        """Test monthly calculation with positive results."""
        result = calculate_monthly_values(
            current_cumulative,
            previous_cumulative,
            'import',
            2081,
            6
        )
        
        assert len(result) > 0, "Should return monthly data"
        assert all(result['Year'] == 2081), "Year should be 2081"
        assert all(result['Month'] == 6), "Month should be 6"
        assert all(result['Direction'] == 'I'), "Direction should be I"
    
    def test_calculate_monthly_filters_negatives(self, current_cumulative, previous_cumulative):
        """Test that negative/zero values are filtered out."""
        # Make previous larger than current to create negatives
        previous_large = previous_cumulative.copy()
        previous_large['Value'] = [1000, 1000]
        
        result = calculate_monthly_values(
            current_cumulative,
            previous_large,
            'import',
            2081,
            6
        )
        
        # Should filter out negative values
        if len(result) > 0:
            assert all(result['Value'] > 0), "Should not return negative values"
    
    def test_new_items_without_previous(self, current_cumulative):
        """Test items that don't exist in previous data."""
        empty_previous = pd.DataFrame()
        
        result = calculate_monthly_values(
            current_cumulative,
            empty_previous,
            'import',
            2081,
            4
        )
        
        # All current items should appear (no previous to subtract)
        assert len(result) > 0, "Should return data for new items"


class TestProcessTradeType:
    """Test the main trade type processing function."""
    
    @pytest.fixture
    def sample_done_data(self):
        """Sample done.csv data."""
        return pd.DataFrame({
            'Year': [2081] * 6,
            'Month': [4, 4, 4, 5, 5, 5],
            'Direction': ['I', 'I', 'I', 'I', 'I', 'I'],
            'HS_Code': ['1001', '1002', '1003', '1001', '1002', '1003'],
            'Country': ['IN', 'CN', 'US', 'IN', 'CN', 'US'],
            'Value': [100, 200, 50, 150, 250, 75],
            'Quantity': [10, 20, 5, 15, 25, 7],
            'Unit': ['kg'] * 6,
            'Revenue': [50, 100, 25, 75, 125, 37]
        })
    
    @pytest.fixture
    def current_cumulative_data(self):
        """Current cumulative Excel data."""
        return pd.DataFrame({
            'HS_Code': ['1001', '1002', '1003'],
            'Country': ['IN', 'CN', 'US'],
            'Value': [400, 600, 150],
            'Quantity': [40, 60, 15],
            'Unit': ['kg', 'kg', 'kg'],
            'Revenue': [200, 300, 75]
        })
    
    def test_process_trade_type_returns_dataframe(self, current_cumulative_data, sample_done_data):
        """Test that process_trade_type returns a valid DataFrame."""
        result = process_trade_type(
            current_cumulative_data,
            sample_done_data,
            'import',
            2081,
            6
        )
        
        assert isinstance(result, pd.DataFrame), "Should return DataFrame"


class TestCombineImportExport:
    """Test combining import and export data."""
    
    def test_combine_both_datasets(self):
        """Test combining import and export data."""
        import_df = pd.DataFrame({
            'Year': [2081],
            'Month': [6],
            'Direction': ['I'],
            'HS_Code': ['1001'],
            'Country': ['IN'],
            'Value': [100],
            'Quantity': [10],
            'Unit': ['kg'],
            'Revenue': [50]
        })
        
        export_df = pd.DataFrame({
            'Year': [2081],
            'Month': [6],
            'Direction': ['E'],
            'HS_Code': ['2001'],
            'Country': ['US'],
            'Value': [200],
            'Quantity': [20],
            'Unit': ['pcs']
        })
        
        result = combine_import_export(import_df, export_df)
        
        assert len(result) == 2, "Should have 2 records"
        assert 'I' in result['Direction'].values, "Should have import"
        assert 'E' in result['Direction'].values, "Should have export"
    
    def test_combine_import_only(self):
        """Test with only import data."""
        import_df = pd.DataFrame({
            'Year': [2081],
            'Month': [6],
            'Direction': ['I'],
            'HS_Code': ['1001'],
            'Country': ['IN'],
            'Value': [100],
            'Quantity': [10],
            'Unit': ['kg'],
            'Revenue': [50]
        })
        
        export_df = pd.DataFrame()
        
        result = combine_import_export(import_df, export_df)
        
        assert len(result) > 0, "Should return import data"
        assert all(result['Direction'] == 'I'), "Should only have import"

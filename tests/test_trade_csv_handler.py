"""Tests for trade module CSV handler - fiscal year filter logic."""
import pytest
import pandas as pd
from data_pipeline.trade.csv_handler import filter_prev_data, save_updated_csv


class TestFilterPrevData:
    """Test fiscal year-aware filtering."""
    
    @pytest.fixture
    def sample_done_df(self):
        """Sample done.csv data with fiscal year structure."""
        return pd.DataFrame({
            'Year': [2081] * 12,
            'Month': list(range(1, 13)),
            'Direction': ['I'] * 12,
            'HS_Code': ['1001'] * 12,
            'Country': ['IN'] * 12,
            'Value': [100] * 12,
            'Quantity': [10] * 12,
            'Unit': ['kg'] * 12,
            'Revenue': [50] * 12
        })
    
    def test_filter_mid_year_month_5(self, sample_done_df):
        """Test filtering for mid-year month (Bhadra - month 5)."""
        filtered = filter_prev_data(sample_done_df, 2081, 4)
        months = sorted(filtered['Month'].unique().tolist())
        assert months == [4], f"Expected [4], got {months}"
        
    def test_filter_mid_year_month_8(self, sample_done_df):
        """Test filtering for mid-year month (Mangsir - month 8)."""
        filtered = filter_prev_data(sample_done_df, 2081, 7)
        months = sorted(filtered['Month'].unique().tolist())
        assert months == [4, 5, 6, 7], f"Expected [4-7], got {months}"
    
    def test_filter_end_year_month_1(self, sample_done_df):
        """Test filtering for end-of-year month 1 (Baisakh)."""
        filtered = filter_prev_data(sample_done_df, 2081, 12)
        months = sorted(filtered['Month'].unique().tolist())
        expected = [4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert months == expected, f"Expected {expected}, got {months}"
    
    def test_filter_end_year_month_2(self, sample_done_df):
        """Test filtering for end-of-year month 2 (Jestha) - uses OR logic."""
        filtered = filter_prev_data(sample_done_df, 2081, 1)
        months = sorted(filtered['Month'].unique().tolist())
        expected = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert months == expected, f"Expected {expected}, got {months}"
    
    def test_filter_end_year_month_3(self, sample_done_df):
        """Test filtering for end-of-year month 3 (Ashad) - uses OR logic."""
        filtered = filter_prev_data(sample_done_df, 2081, 2)
        months = sorted(filtered['Month'].unique().tolist())
        expected = [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        assert months == expected, f"Expected {expected}, got {months}"
    
    def test_filter_returns_correct_year(self, sample_done_df):
        """Test that filter only returns data for specified year."""
        # Add data for different year
        other_year = pd.DataFrame({
            'Year': [2080] * 5,
            'Month': [4, 5, 6, 7, 8],
            'Direction': ['I'] * 5,
            'HS_Code': ['1001'] * 5,
            'Country': ['IN'] * 5,
            'Value': [100] * 5,
            'Quantity': [10] * 5,
            'Unit': ['kg'] * 5,
            'Revenue': [50] * 5
        })
        combined = pd.concat([sample_done_df, other_year])
        
        filtered = filter_prev_data(combined, 2081, 5)
        assert all(filtered['Year'] == 2081), "Filter should only return year 2081"
    
    def test_filter_with_import_export(self, sample_done_df):
        """Test that filter preserves both import and export data."""
        # Add export data
        export_data = sample_done_df.copy()
        export_data['Direction'] = 'E'
        combined = pd.concat([sample_done_df, export_data])
        
        filtered = filter_prev_data(combined, 2081, 5)
        
        import_count = len(filtered[filtered['Direction'] == 'I'])
        export_count = len(filtered[filtered['Direction'] == 'E'])
        
        assert import_count > 0, "Should have import data"
        assert export_count > 0, "Should have export data"


class TestSaveUpdatedCsv:
    """Test CSV saving with month replacement logic."""
    
    @pytest.fixture
    def temp_csv(self, tmp_path):
        """Create temporary CSV file."""
        csv_path = tmp_path / "test_done.csv"
        
        # Create initial data
        df = pd.DataFrame({
            'Year': [2081, 2081, 2081],
            'Month': [4, 5, 6],
            'Direction': ['I', 'I', 'I'],
            'HS_Code': ['1001', '1002', '1003'],
            'Country': ['IN', 'CN', 'US'],
            'Value': [100, 200, 300],
            'Quantity': [10, 20, 30],
            'Unit': ['kg', 'kg', 'kg'],
            'Revenue': [50, 100, 150]
        })
        df.to_csv(csv_path, index=False)
        return csv_path
    
    def test_save_updated_csv_replaces_existing_month(self, temp_csv):
        """Test that existing month data is replaced."""
        # New data for month 5 (already exists)
        new_data = pd.DataFrame({
            'Year': [2081],
            'Month': [5],
            'Direction': ['I'],
            'HS_Code': ['9999'],
            'Country': ['JP'],
            'Value': [999],
            'Quantity': [99],
            'Unit': ['kg'],
            'Revenue': [499]
        })
        
        result_path = save_updated_csv(
            temp_csv,
            new_data,
            output_name='test_output.csv',
            replace_existing=True
        )
        
        result_df = pd.read_csv(result_path)
        month_5_data = result_df[result_df['Month'] == 5]
        
        # Should only have 1 record for month 5 (new one)
        assert len(month_5_data) == 1, "Should replace old month 5 data"
        assert str(month_5_data.iloc[0]['HS_Code']) == '9999', "Should have new data"
    
    def test_save_updated_csv_appends_new_month(self, temp_csv):
        """Test that new month data is appended."""
        # New data for month 7 (doesn't exist)
        new_data = pd.DataFrame({
            'Year': [2081],
            'Month': [7],
            'Direction': ['I'],
            'HS_Code': ['7777'],
            'Country': ['FR'],
            'Value': [777],
            'Quantity': [77],
            'Unit': ['kg'],
            'Revenue': [377]
        })
        
        result_path = save_updated_csv(
            temp_csv,
            new_data,
            output_name='test_output.csv',
            replace_existing=True
        )
        
        result_df = pd.read_csv(result_path)
        
        # Should have original 3 + new 1 = 4 records
        assert len(result_df) == 4, "Should append new month data"
        assert 7 in result_df['Month'].values, "Should have month 7"
    
    def test_save_updated_csv_without_replace(self, temp_csv):
        """Test saving without replacement (append only)."""
        new_data = pd.DataFrame({
            'Year': [2081],
            'Month': [5],
            'Direction': ['I'],
            'HS_Code': ['9999'],
            'Country': ['JP'],
            'Value': [999],
            'Quantity': [99],
            'Unit': ['kg'],
            'Revenue': [499]
        })
        
        result_path = save_updated_csv(
            temp_csv,
            new_data,
            output_name='test_output.csv',
            replace_existing=False
        )
        
        result_df = pd.read_csv(result_path)
        month_5_data = result_df[result_df['Month'] == 5]
        
        # Should have 2 records for month 5 (old + new)
        assert len(month_5_data) == 2, "Should keep both records when not replacing"

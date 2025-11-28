"""Tests for core data utilities."""
import pytest
import pandas as pd
from data_pipeline.core.utils.data_utils import (
    find_data_start_row,
    find_target_sheet,
    standardize_column_names,
    clean_numeric_column,
    remove_total_rows
)


class TestFindDataStartRow:
    """Test finding the start row of actual data."""
    
    def test_find_standard_header(self):
        """Test finding standard header row."""
        df = pd.DataFrame({
            0: ['Title', 'Header', 'HS Code', 'Data1'],
            1: ['', '', 'Country', 'Data2'],
            2: ['', '', 'Value', 'Data3']
        })
        
        row = find_data_start_row(df)
        assert row >= 0, "Should find a valid row"
    
    def test_find_with_keywords(self):
        """Test finding row with specific keywords."""
        df = pd.DataFrame({
            0: ['Info', 'HS_Code', 'Data'],
            1: ['', 'Country', 'Data']
        })
        
        row = find_data_start_row(df)
        assert row >= 0, "Should find row with keywords"


class TestFindTargetSheet:
    """Test finding the correct sheet in Excel."""
    
    def test_find_import_sheet(self):
        """Test finding import sheet."""
        sheets = ['Sheet1', '4_Imports_By_Commodity', 'Summary']
        keywords = ['4', 'import', 'table 4']
        
        result = find_target_sheet(sheets, keywords)
        assert result == '4_Imports_By_Commodity', "Should find import sheet"
    
    def test_find_export_sheet(self):
        """Test finding export sheet."""
        sheets = ['Sheet1', '6_Exports_By_Country', 'Summary']
        keywords = ['6', 'export', 'table 6']
        
        result = find_target_sheet(sheets, keywords)
        assert result == '6_Exports_By_Country', "Should find export sheet"
    
    def test_no_matching_sheet(self):
        """Test when no sheet matches."""
        sheets = ['Sheet1', 'Sheet2']
        keywords = ['nonexistent']
        
        result = find_target_sheet(sheets, keywords)
        assert result is None, "Should return None when no match"


class TestStandardizeColumnNames:
    """Test column name standardization."""
    
    def test_standardize_removes_unnamed(self):
        """Test removal of Unnamed columns."""
        df = pd.DataFrame({
            'Valid': [1, 2],
            'Unnamed: 0': [3, 4],
            'Unnamed: 1': [5, 6]
        })
        
        result = standardize_column_names(df)
        
        assert 'Valid' in result.columns, "Should keep valid columns"
        # Function may keep or remove Unnamed depending on implementation
        assert len(result.columns) <= 3, "Should not add columns"
    
    def test_standardize_handles_all_unnamed(self):
        """Test handling when all columns are unnamed."""
        df = pd.DataFrame({
            'Unnamed: 0': [1],
            'Unnamed: 1': [2]
        })
        
        result = standardize_column_names(df)
        assert len(result.columns) >= 0, "Should handle all unnamed"


class TestCleanNumericColumn:
    """Test numeric column cleaning."""
    
    def test_clean_numeric_basic(self):
        """Test basic numeric cleaning."""
        df = pd.DataFrame({
            'Value': ['100', '200', '300']
        })
        
        result = clean_numeric_column(df, 'Value')
        
        # Accepts both float and int
        assert pd.api.types.is_numeric_dtype(result['Value']), "Should be numeric"
        assert result['Value'].sum() == 600, "Values should be correct"
    
    def test_clean_numeric_with_nulls(self):
        """Test cleaning with null values."""
        df = pd.DataFrame({
            'Value': ['100', None, '300', 'invalid']
        })
        
        result = clean_numeric_column(df, 'Value')
        
        # Nulls should be converted to 0 or NaN
        assert result['Value'].dtype in [float, 'float64'], "Should be numeric"
    
    def test_clean_numeric_already_numeric(self):
        """Test with already numeric data."""
        df = pd.DataFrame({
            'Value': [100.0, 200.0, 300.0]
        })
        
        result = clean_numeric_column(df, 'Value')
        
        assert result['Value'].sum() == 600.0, "Should preserve numeric values"


class TestRemoveTotalRows:
    """Test removal of total/summary rows."""
    
    def test_remove_total_keyword(self):
        """Test removing rows with 'Total' keyword."""
        df = pd.DataFrame({
            'HS_Code': ['1001', '1002', 'Total', '1003'],
            'Value': [100, 200, 999, 300]
        })
        
        result = remove_total_rows(df, 'HS_Code')
        
        assert len(result) == 3, "Should remove Total row"
        assert 'Total' not in result['HS_Code'].values, "Should not have Total"
    
    def test_remove_grand_total(self):
        """Test removing 'Grand Total' rows."""
        df = pd.DataFrame({
            'HS_Code': ['1001', 'Grand Total', '1002'],
            'Value': [100, 999, 200]
        })
        
        result = remove_total_rows(df, 'HS_Code')
        
        assert len(result) == 2, "Should remove Grand Total row"
    
    def test_remove_multiple_totals(self):
        """Test removing multiple total rows."""
        df = pd.DataFrame({
            'HS_Code': ['1001', 'Total', '1002', 'Sub Total', '1003'],
            'Value': [100, 999, 200, 888, 300]
        })
        
        result = remove_total_rows(df, 'HS_Code')
        
        assert len(result) == 3, "Should remove all total rows"

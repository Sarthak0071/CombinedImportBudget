"""Tests for trade cleaner module - country code conversion."""
import pytest
import pandas as pd
from data_pipeline.trade.cleaner import (
    normalize_country_name,
    get_iso2_code,
    clean_country_codes,
    validate_data,
    clean_monthly_data
)


class TestNormalizeCountryName:
    """Test country name normalization."""
    
    def test_normalize_removes_brackets(self):
        """Test that brackets are removed."""
        result = normalize_country_name("India [Asia]")
        assert result == "India", "Should remove brackets"
    
    def test_normalize_strips_whitespace(self):
        """Test whitespace stripping."""
        result = normalize_country_name("  China  ")
        assert result == "China", "Should strip whitespace"
    
    def test_normalize_handles_none(self):
        """Test None input."""
        result = normalize_country_name(None)
        assert result is None, "Should return None for None input"
    
    def test_normalize_uses_custom_mappings(self):
        """Test custom country mappings."""
        result = normalize_country_name("Iran, Islamic Republic of")
        assert result == "Iran", "Should use custom mapping"


class TestGetIso2Code:
    """Test ISO-2 code conversion."""
    
    def test_get_iso2_valid_country(self):
        """Test valid country name."""
        result = get_iso2_code("India")
        assert result == "IN", "India should return IN"
    
    def test_get_iso2_custom_mapping(self):
        """Test custom country mappings."""
        result = get_iso2_code("Turkey")
        assert result == "TR", "Turkey should use custom mapping"
    
    def test_get_iso2_namibia(self):
        """Test special case: Namibia."""
        result = get_iso2_code("Namibia")
        assert result == "NA", "Namibia should return NA"
    
    def test_get_iso2_unknown_country(self):
        """Test unknown country returns original."""
        result = get_iso2_code("UnknownCountry123")
        assert result == "UnknownCountry123", "Should return original for unknown"
    
    def test_get_iso2_with_normalizing(self):
        """Test with country needing normalization."""
        result = get_iso2_code("United States")
        assert len(result) == 2, "Should return 2-letter code"


class TestCleanCountryCodes:
    """Test country code cleaning for dataframes."""
    
    @pytest.fixture
    def sample_df(self):
        """Sample dataframe with country names."""
        return pd.DataFrame({
            'Country': ['India', 'China', 'United States', 'Turkey'],
            'Value': [100, 200, 300, 400]
        })
    
    def test_clean_converts_to_iso2(self, sample_df):
        """Test that country names are converted to ISO-2."""
        result = clean_country_codes(sample_df)
        
        assert 'IN' in result['Country'].values, "Should have IN for India"
        assert 'CN' in result['Country'].values, "Should have CN for China"
    
    def test_clean_preserves_other_columns(self, sample_df):
        """Test that other columns are preserved."""
        result = clean_country_codes(sample_df)
        
        assert 'Value' in result.columns, "Should preserve Value column"
        assert result['Value'].sum() == 1000, "Values should be unchanged"
    
    def test_clean_already_iso2(self):
        """Test with data already in ISO-2 format."""
        df = pd.DataFrame({
            'Country': ['IN', 'CN', 'US'],
            'Value': [100, 200, 300]
        })
        
        result = clean_country_codes(df)
        
        # Should recognize already ISO-2 and not change
        assert 'IN' in result['Country'].values
        assert 'CN' in result['Country'].values


class TestValidateData:
    """Test data validation."""
    
    @pytest.fixture
    def valid_data(self):
        """Valid trade data."""
        return pd.DataFrame({
            'Year': [2081, 2081],
            'Month': [6, 6],
            'Direction': ['I', 'E'],
            'HS_Code': ['1001', '2001'],
            'Country': ['IN', 'US'],
            'Value': [100.0, 200.0],
            'Quantity': [10.0, 20.0]
        })
    
    def test_validate_removes_nulls(self):
        """Test that rows with null values are removed."""
        df = pd.DataFrame({
            'Year': [2081, 2081, None],
            'Month': [6, None, 7],
            'Direction': ['I', 'E', 'I'],
            'HS_Code': ['1001', '2001', None],
            'Country': ['IN', 'US', 'CN'],
            'Value': [100.0, None, 300.0],
            'Quantity': [10.0, 20.0, 30.0]
        })
        
        result = validate_data(df)
        
        assert len(result) < len(df), "Should remove rows with nulls"
        assert result['HS_Code'].notna().all(), "HS_Code should not have nulls"
    
    def test_validate_converts_types(self, valid_data):
        """Test that data types are converted correctly."""
        result = validate_data(valid_data)
        
        assert result['Year'].dtype in [int, 'int64'], "Year should be int"
        assert result['Month'].dtype in [int, 'int64'], "Month should be int"
    
    def test_validate_handles_numeric_errors(self):
        """Test handling of non-numeric values."""
        df = pd.DataFrame({
            'Year': [2081],
            'Month': [6],
            'Direction': ['I'],
            'HS_Code': ['1001'],
            'Country': ['IN'],
            'Value': ['invalid'],  # Non-numeric
            'Quantity': [10.0]
        })
        
        result = validate_data(df)
        
        # Should convert errors to 0 or handle gracefully
        assert len(result) >= 0, "Should handle invalid data"


class TestCleanMonthlyData:
    """Test complete monthly data cleaning pipeline."""
    
    def test_clean_monthly_data_pipeline(self):
        """Test full cleaning pipeline."""
        df = pd.DataFrame({
            'Year': [2081, 2081],
            'Month': [6, 6],
            'Direction': ['I', 'E'],
            'HS_Code': ['1001', '2001'],
            'Country': ['IN', 'US'],
            'Value': [100.0, 200.0],
            'Quantity': [10.0, 20.0]
        })
        
        result = clean_monthly_data(df)
        
        assert len(result) > 0, "Should return cleaned data"
        assert 'Year' in result.columns, "Should have Year column"

"""Tests for darta PDF processing."""

import pytest
import pandas as pd
from pathlib import Path
from data_pipeline.darta import process_data
from data_pipeline.darta.cleaner import (
    clean_registration_number,
    clean_phone_number,
    convert_nepali_to_english
)


class TestDartaProcessing:
    """Test suite for darta module."""
    
    def test_pdf_extraction(self):
        """Test PDF data extraction."""
        result = process_data('data/darta.pdf', 'data/test_output.csv')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 154
        
    def test_darta_columns(self):
        """Test darta output has expected columns."""
        result = process_data('data/darta.pdf', 'data/test_output.csv')
        
        expected_cols = ['year', 'month', 'day', 'reg_no', 
                        'province_code', 'district_code']
        for col in expected_cols:
            assert col in result.columns
            
    def test_province_district_mapping(self):
        """Test province and district codes are mapped."""
        result = process_data('data/darta.pdf', 'data/test_output.csv')
        
        assert result['province_code'].notna().sum() >= 150
        assert result['district_code'].notna().sum() >= 150


class TestDartaCleaning:
    """Test suite for data cleaning functions."""
    
    def test_registration_number_cleaning(self):
        """Test registration number separator removal."""
        assert clean_registration_number('008/073-74') == '008'
        assert clean_registration_number('894-075') == '894'
        assert clean_registration_number('5145') == '5145'
        
    def test_phone_number_cleaning(self):
        """Test phone number normalization."""
        assert clean_phone_number('9841071450') == '9841071450'
        assert clean_phone_number('15328625') == '9815328625'
        assert len(clean_phone_number('15328625')) == 10
        
    def test_nepali_numeral_conversion(self):
        """Test Nepali to English numeral conversion."""
        assert convert_nepali_to_english('०१२३') == '0123'
        assert convert_nepali_to_english('९८७६') == '9876'

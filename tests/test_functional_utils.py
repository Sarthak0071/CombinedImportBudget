"""Tests for functional programming utilities."""

import pytest
import pandas as pd
from data_pipeline.core.utils import (
    pipe, compose, with_column, create_filter, combine_filters,
    filter_by_column, clean_numerics, clean_hs_codes_fn,
    add_composite_key, remove_nulls, apply_to_column, strip_strings
)


class TestPipeCompose:
    
    def test_pipe_single_transform(self):
        df = pd.DataFrame({'Value': ['100', '200', '300']})
        result = pipe(df, clean_numerics('Value'))
        assert result['Value'].sum() == 600
    
    def test_pipe_multiple_transforms(self):
        df = pd.DataFrame({
            'HS_Code': ['1234.0', '5678.0'],
            'Country': ['  Nepal  ', '  India  ']
        })
        result = pipe(df, clean_hs_codes_fn, strip_strings('Country'))
        assert '.' not in result['HS_Code'].iloc[0]
        assert result['Country'].iloc[0] == 'Nepal'
    
    def test_compose_functions(self):
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        composed = compose(double, add_one)
        assert composed(5) == 12


class TestFilters:
    
    def test_filter_equals(self):
        df = pd.DataFrame({'Year': [2081, 2082, 2083]})
        year_filter = create_filter('Year', '==', 2082)
        mask = year_filter(df)
        assert mask.sum() == 1
    
    def test_filter_less_equal(self):
        df = pd.DataFrame({'Month': [1, 2, 3, 4, 5]})
        month_filter = create_filter('Month', '<=', 3)
        mask = month_filter(df)
        assert mask.sum() == 3
    
    def test_filter_in_list(self):
        df = pd.DataFrame({'Country': ['NP', 'IN', 'CN', 'US']})
        country_filter = create_filter('Country', 'in', ['NP', 'IN'])
        mask = country_filter(df)
        assert mask.sum() == 2
    
    def test_combine_multiple_filters(self):
        df = pd.DataFrame({
            'Year': [2082, 2082, 2083, 2083],
            'Month': [1, 5, 1, 5]
        })
        year_filter = create_filter('Year', '==', 2082)
        month_filter = create_filter('Month', '<=', 3)
        combined = combine_filters(year_filter, month_filter)
        result = combined(df)
        assert len(result) == 1
        assert result['Month'].iloc[0] == 1
    
    def test_filter_by_column(self):
        df = pd.DataFrame({'Status': ['active', 'inactive', 'active']})
        filter_fn = filter_by_column('Status', '==', 'active')
        result = filter_fn(df)
        assert len(result) == 2


class TestTransforms:
    
    def test_with_column_transform(self):
        df = pd.DataFrame({'Value': [1, 2, 3]})
        result = with_column(df, 'Value', lambda s: s * 2)
        assert result['Value'].tolist() == [2, 4, 6]
    
    def test_with_column_missing(self):
        df = pd.DataFrame({'Value': [1, 2, 3]})
        result = with_column(df, 'Missing', lambda s: s * 2)
        assert result.equals(df)
    
    def test_clean_numerics_multiple_cols(self):
        df = pd.DataFrame({
            'Value': ['100', 'invalid', '300'],
            'Quantity': ['10', '20', 'bad']
        })
        transform = clean_numerics('Value', 'Quantity')
        result = transform(df)
        assert result['Value'].sum() == 400
        assert result['Quantity'].sum() == 30
    
    def test_clean_hs_codes(self):
        df = pd.DataFrame({'HS_Code': ['1234.0', '  5678.0  ', '9012']})
        result = clean_hs_codes_fn(df)
        assert result['HS_Code'].iloc[0] == '1234'
        assert result['HS_Code'].iloc[1] == '5678'
    
    def test_strip_strings_multiple(self):
        df = pd.DataFrame({
            'Country': ['  Nepal  ', ' India '],
            'City': ['  Kathmandu  ', 'Delhi']
        })
        transform = strip_strings('Country', 'City')
        result = transform(df)
        assert result['Country'].iloc[0] == 'Nepal'
        assert result['City'].iloc[0] == 'Kathmandu'
    
    def test_add_composite_key(self):
        df = pd.DataFrame({
            'HS_Code': ['1234', '5678'],
            'Country': ['NP', 'IN']
        })
        transform = add_composite_key('HS_Code', 'Country')
        result = transform(df)
        assert '_key' in result.columns
        assert result['_key'].iloc[0] == '1234|NP'
    
    def test_remove_nulls(self):
        df = pd.DataFrame({
            'A': [1, None, 3],
            'B': [10, 20, None]
        })
        transform = remove_nulls('A', 'B')
        result = transform(df)
        assert len(result) == 1
    
    def test_apply_to_column(self):
        df = pd.DataFrame({'Value': [1, 2, 3]})
        transform = apply_to_column('Value', lambda x: x * 10)
        result = transform(df)
        assert result['Value'].tolist() == [10, 20, 30]


class TestIntegration:
    
    def test_full_pipeline(self):
        df = pd.DataFrame({
            'Year': [2082, 2082, 2083],
            'Month': [1, 5, 1],
            'HS_Code': ['1234.0', '5678.0', '9012.0'],
            'Country': ['  Nepal  ', ' India ', 'China'],
            'Value': ['100', '200', 'invalid']
        })
        
        year_filter = create_filter('Year', '==', 2082)
        month_filter = create_filter('Month', '<=', 3)
        combined_filter = combine_filters(year_filter, month_filter)
        
        result = pipe(
            df,
            combined_filter,
            clean_numerics('Value'),
            clean_hs_codes_fn,
            strip_strings('Country'),
            add_composite_key('HS_Code', 'Country')
        )
        
        assert len(result) == 1
        assert result['HS_Code'].iloc[0] == '1234'
        assert result['Country'].iloc[0] == 'Nepal'
        assert result['Value'].iloc[0] == 100.0
        assert '_key' in result.columns


class TestEdgeCases:
    
    def test_empty_dataframe(self):
        df = pd.DataFrame()
        result = pipe(df, clean_numerics('Value'))
        assert len(result) == 0
    
    def test_missing_column_graceful(self):
        df = pd.DataFrame({'A': [1, 2, 3]})
        result = clean_hs_codes_fn(df)
        assert result.equals(df)
    
    def test_all_null_values(self):
        df = pd.DataFrame({'Value': [None, None, None]})
        transform = clean_numerics('Value')
        result = transform(df)
        assert result['Value'].sum() == 0
    
    def test_filter_no_matches(self):
        df = pd.DataFrame({'Year': [2081, 2082]})
        year_filter = create_filter('Year', '==', 2099)
        combined = combine_filters(year_filter)
        result = combined(df)
        assert len(result) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

"""Comprehensive tests for dynamic year/month extraction."""
import pytest
from pathlib import Path
import pandas as pd


def test_header_parser_import():
    """Test that header_parser module can be imported."""
    from data_pipeline.trade.header_parser import (
        extract_header_metadata,
        parse_fiscal_year_from_header,
        parse_month_range_from_header
    )
    assert extract_header_metadata is not None
    assert parse_fiscal_year_from_header is not None
    assert parse_month_range_from_header is not None


def test_fiscal_year_parsing():
    """Test fiscal year extraction from various header formats."""
    from data_pipeline.trade.header_parser import parse_fiscal_year_from_header
    
    # Test various patterns
    assert parse_fiscal_year_from_header("FY 2082/83") == 2082
    assert parse_fiscal_year_from_header("FY 2082-83") == 2082
    assert parse_fiscal_year_from_header("2082/83 Data") == 2082
    assert parse_fiscal_year_from_header("Report for 2082-83") == 2082
    assert parse_fiscal_year_from_header("Based on FY 2082/83 (Mid July 2025)") == 2082


def test_month_range_parsing():
    """Test month range extraction from various header formats."""
    from data_pipeline.trade.header_parser import parse_month_range_from_header
    
    # Test with parentheses (actual Excel format)
    result = parse_month_range_from_header("First Three Months (Shrawan-Asoj) of FY")
    assert result == (4, 6), f"Expected (4, 6) but got {result}"
    
    # Test other formats
    result = parse_month_range_from_header("Shrawan-Ashwin")
    assert result == (4, 6), f"Expected (4, 6) but got {result}"
    
    result = parse_month_range_from_header("Bhadra to Kartik")
    assert result == (5, 7), f"Expected (5, 7) but got {result}"
    
    result = parse_month_range_from_header("(Baishakh-Jestha)")
    assert result == (1, 2), f"Expected (1, 2) but got {result}"


def test_month_name_variations():
    """Test that various month name spellings are recognized."""
    from data_pipeline.trade.header_parser import _find_month_number
    
    # Standard names
    assert _find_month_number("Shrawan") == 4
    assert _find_month_number("Ashwin") == 6
    assert _find_month_number("Asoj") == 6  # Alternative name for Ashwin
    
    # Case variations
    assert _find_month_number("shrawan") == 4
    assert _find_month_number("ASHWIN") == 6
    assert _find_month_number("asoj") == 6


def test_metadata_extraction_from_excel():
    """Test complete metadata extraction from actual Excel file."""
    from data_pipeline.trade.header_parser import extract_header_metadata
    
    excel_path = Path("data/FTS_uptoAsoj_208283_ci1nozq.xlsx")
    
    if not excel_path.exists():
        pytest.skip(f"Test data not found: {excel_path}")
    
    metadata = extract_header_metadata(excel_path)
    
    # Verify metadata was extracted
    assert metadata is not None, "Failed to extract metadata"
    assert 'year' in metadata
    assert 'target_month' in metadata
    assert 'previous_month' in metadata
    
    # Verify specific values
    assert metadata['year'] == 2082, f"Expected year 2082, got {metadata['year']}"
    assert metadata['target_month'] == 6, f"Expected target month 6 (Asoj/Ashwin), got {metadata['target_month']}"
    assert metadata['previous_month'] == 5, f"Expected previous month 5 (Bhadra), got {metadata['previous_month']}"
    assert metadata['start_month'] == 4, f"Expected start month 4 (Shrawan), got {metadata['start_month']}"
    assert metadata['end_month'] == 6, f"Expected end month 6 (Asoj), got {metadata['end_month']}"


def test_excel_reader_metadata():
    """Test TradeExcelReader.extract_metadata() method."""
    from data_pipeline.trade.excel_reader import TradeExcelReader
    
    excel_path = Path("data/FTS_uptoAsoj_208283_ci1nozq.xlsx")
    
    if not excel_path.exists():
        pytest.skip(f"Test data not found: {excel_path}")
    
    reader = TradeExcelReader(excel_path)
    metadata = reader.extract_metadata()
    reader.close()
    
    assert metadata is not None
    assert metadata['year'] == 2082
    assert metadata['target_month'] == 6


def test_trade_processing_with_dynamic_extraction():
    """Test end-to-end trade processing with dynamic year/month extraction."""
    from data_pipeline.trade import process_data
    
    data_dir = Path('data')
    xlsx_file = data_dir / 'FTS_uptoAsoj_208283_ci1nozq.xlsx'
    old_data = data_dir / 'done.csv'
    
    if not xlsx_file.exists():
        pytest.skip(f"Test data not found: {xlsx_file}")
    
    if not old_data.exists():
        pytest.skip(f"Test data not found: {old_data}")
    
    # Process data
    output_file = 'test_dynamic_output.csv'
    result = process_data(str(xlsx_file), str(old_data), output_file)
    
    # Verify result
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    
    # Verify the new records have correct year and month
    month_df = pd.read_csv(data_dir / 'month.csv')
    assert 'Year' in month_df.columns
    assert 'Month' in month_df.columns
    
    # All new records should have Year=2082 and Month=6
    assert (month_df['Year'] == 2082).all(), "All records should have Year=2082"
    assert (month_df['Month'] == 6).all(), "All records should have Month=6 (Asoj/Ashwin)"
    
    # Clean up test outputs
    for file in [output_file, 'month.csv']:
        test_output = data_dir / file
        if test_output.exists():
            test_output.unlink()


def test_filename_fallback():
    """Test year extraction fallback from filename."""
    from data_pipeline.trade.header_parser import _extract_year_from_filename
    
    # Test various filename patterns
    assert _extract_year_from_filename(Path("FTS_uptoAsoj_208283_ci1nozq.xlsx")) == 2082
    assert _extract_year_from_filename(Path("data_2082.xlsx")) == 2082
    assert _extract_year_from_filename(Path("report_2083_q1.xlsx")) == 2083


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

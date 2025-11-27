"""Test script for verifying dynamic year/month extraction."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from data_pipeline.trade.header_parser import extract_header_metadata
from data_pipeline.trade.excel_reader import TradeExcelReader

def test_header_extraction():
    """Test header extraction from the Excel file."""
    print("=" * 60)
    print("Testing Dynamic Year/Month Extraction")
    print("=" * 60)
    
    excel_path = Path("data/FTS_uptoAsoj_208283_ci1nozq.xlsx")
    
    if not excel_path.exists():
        print(f"❌ File not found: {excel_path}")
        return False
    
    print(f"\n📁 Testing file: {excel_path.name}")
    
    # Test 1: Direct header extraction
    print("\n1️⃣  Testing header_parser.extract_header_metadata()...")
    metadata = extract_header_metadata(excel_path)
    
    if metadata:
        print("   ✅ SUCCESS!")
        print(f"   Year: {metadata['year']}")
        print(f"   Month Range: {metadata['start_month']} - {metadata['end_month']}")
        print(f"   Target Month: {metadata['target_month']}")
        print(f"   Previous Month: {metadata['previous_month']}")
    else:
        print("   ❌ FAILED to extract metadata")
        return False
    
    # Test 2: Via TradeExcelReader
    print("\n2️⃣  Testing TradeExcelReader.extract_metadata()...")
    reader = TradeExcelReader(excel_path)
    metadata2 = reader.extract_metadata()
    reader.close()
    
    if metadata2:
        print("   ✅ SUCCESS!")
        print(f"   Year: {metadata2['year']}")
        print(f"   Target Month: {metadata2['target_month']} (expected: 6 for Ashwin)")
        print(f"   Previous Month: {metadata2['previous_month']} (expected: 5 for Bhadra)")
    else:
        print("   ❌ FAILED")
        return False
    
    # Verify expected values
    print("\n3️⃣  Verifying expected values...")
    expected_year = 2082
    expected_target_month = 6  # Ashwin
    expected_previous_month = 5  # Bhadra
    
    if metadata['year'] == expected_year:
        print(f"   ✅ Year matches: {expected_year}")
    else:
        print(f"   ❌ Year mismatch: expected {expected_year}, got {metadata['year']}")
        return False
    
    if metadata['target_month'] == expected_target_month:
        print(f"   ✅ Target month matches: {expected_target_month}")
    else:
        print(f"   ❌ Target month mismatch: expected {expected_target_month}, got {metadata['target_month']}")
        return False
    
    if metadata['previous_month'] == expected_previous_month:
        print(f"   ✅ Previous month matches: {expected_previous_month}")
    else:
        print(f"   ❌ Previous month mismatch: expected {expected_previous_month}, got {metadata['previous_month']}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_header_extraction()
    sys.exit(0 if success else 1)

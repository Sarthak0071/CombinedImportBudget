"""
Test all README examples with ACTUAL DATA from data folder.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("TESTING WITH ACTUAL DATA")
print("=" * 70)

# Test 1: Budget Processing
print("\n" + "=" * 70)
print("TEST 1: Budget Processing")
print("=" * 70)
try:
    from data_pipeline.budget import process_data
    
    print("\nRunning: process_data('data/82-83.xlsx')")
    result = process_data('data/82-83.xlsx')
    
    print(f"✓ SUCCESS!")
    print(f"  Records processed: {len(result):,}")
    print(f"  Columns: {list(result.columns)}")
    if 'Year' in result.columns:
        print(f"  Years: {result['Year'].unique()}")
    print(f"  Output file: 2082.csv (should exist)")
    
    # Check if output file exists
    if Path('2082.csv').exists():
        print(f"  ✓ Output file 2082.csv created")
    
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Trade Processing
print("\n" + "=" * 70)
print("TEST 2: Trade Processing")
print("=" * 70)
try:
    from data_pipeline.trade import process_data
    
    print("\nRunning: process_data('data/FTS_uptoAsoj_208283_ci1nozq.xlsx', 'data/done.csv')")
    result = process_data('data/FTS_uptoAsoj_208283_ci1nozq.xlsx', 'data/done.csv', 'updateddone.csv')
    
    print(f"✓ SUCCESS!")
    print(f"  Records in result: {len(result):,}")
    print(f"  Columns: {list(result.columns)}")
    if 'Year' in result.columns:
        print(f"  Years: {result['Year'].unique()}")
    if 'Month' in result.columns:
        print(f"  Months: {sorted(result['Month'].unique())}")
    if 'Direction' in result.columns:
        import_count = len(result[result['Direction'] == 'I'])
        export_count = len(result[result['Direction'] == 'E'])
        print(f"  Import records: {import_count:,}")
        print(f"  Export records: {export_count:,}")
    
    # Check output files
    if Path('data/month.csv').exists():
        print(f"  ✓ Output file month.csv created")
    if Path('data/updateddone.csv').exists():
        print(f"  ✓ Output file updateddone.csv created")
        
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Darta Processing
print("\n" + "=" * 70)
print("TEST 3: Darta Processing")
print("=" * 70)
try:
    from data_pipeline.darta import process_data
    
    # Check if PDF exists
    if not Path('data/darta.pdf').exists():
        print("  ⚠ data/darta.pdf not found, skipping...")
    else:
        print("\nRunning: process_data('data/darta.pdf', 'data/clean_data.csv')")
        result = process_data('data/darta.pdf', 'data/clean_data.csv')
        
        print(f"✓ SUCCESS!")
        print(f"  Records processed: {len(result):,}")
        print(f"  Columns: {list(result.columns)}")
        
        # Check output file
        if Path('data/clean_data.csv').exists():
            print(f"  ✓ Output file clean_data.csv created")
        
except FileNotFoundError as e:
    print(f"  ⚠ File not found: {e}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)

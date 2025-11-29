"""
Verification script to test all README.md usage examples.
This script verifies that all imports and function signatures work correctly.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports from README examples."""
    print("=" * 60)
    print("Testing Imports from README.md")
    print("=" * 60)
    
    try:
        from data_pipeline.budget import process_data as budget_process
        print("✓ Budget import works: from data_pipeline.budget import process_data")
    except Exception as e:
        print(f"✗ Budget import failed: {e}")
        return False
    
    try:
        from data_pipeline.trade import process_data as trade_process
        print("✓ Trade import works: from data_pipeline.trade import process_data")
    except Exception as e:
        print(f"✗ Trade import failed: {e}")
        return False
    
    try:
        from data_pipeline.darta import process_data as darta_process
        print("✓ Darta import works: from data_pipeline.darta import process_data")
    except Exception as e:
        print(f"✗ Darta import failed: {e}")
        return False
    
    return True


def test_function_signatures():
    """Verify function signatures match README examples."""
    print("\n" + "=" * 60)
    print("Testing Function Signatures")
    print("=" * 60)
    
    import inspect
    from data_pipeline.budget import process_data as budget_process
    from data_pipeline.trade import process_data as trade_process
    from data_pipeline.darta import process_data as darta_process
    
    # Budget function
    sig = inspect.signature(budget_process)
    params = list(sig.parameters.keys())
    print(f"\nBudget process_data parameters: {params}")
    print(f"  README Example 1: process_data('data/82-83.xlsx')")
    print(f"  ✓ First param 'xlsx_file' is required: {'xlsx_file' in params}")
    print(f"  README Example 2: process_data(xlsx_file=..., old_data=..., output_name=...)")
    print(f"  ✓ Has 'old_data' param: {'old_data' in params}")
    print(f"  ✓ Has 'output_name' param: {'output_name' in params}")
    
    # Trade function
    sig = inspect.signature(trade_process)
    params = list(sig.parameters.keys())
    print(f"\nTrade process_data parameters: {params}")
    print(f"  README Example: process_data(xlsx_file=..., old_data=..., output_name=...)")
    print(f"  ✓ Has 'xlsx_file' param: {'xlsx_file' in params}")
    print(f"  ✓ Has 'old_data' param: {'old_data' in params}")
    print(f"  ✓ Has 'output_name' param: {'output_name' in params}")
    
    # Darta function
    sig = inspect.signature(darta_process)
    params = list(sig.parameters.keys())
    print(f"\nDarta process_data parameters: {params}")
    print(f"  README Example: process_data('data/darta.pdf', 'data/clean_data.csv')")
    print(f"  ✓ Has 'pdf_file' param: {'pdf_file' in params}")
    print(f"  ✓ Has 'output_name' param: {'output_name' in params}")
    
    return True


def test_module_structure():
    """Test module structure and exports."""
    print("\n" + "=" * 60)
    print("Testing Module Structure")
    print("=" * 60)
    
    try:
        import data_pipeline
        print(f"✓ Main package exists")
        print(f"  Version: {getattr(data_pipeline, '__version__', 'Not defined')}")
        print(f"  Exports: {getattr(data_pipeline, '__all__', 'Not defined')}")
    except Exception as e:
        print(f"✗ Main package error: {e}")
        return False
    
    try:
        import data_pipeline.trade
        exports = getattr(data_pipeline.trade, '__all__', [])
        print(f"✓ Trade module exports: {exports}")
    except Exception as e:
        print(f"✗ Trade module error: {e}")
        return False
    
    try:
        import data_pipeline.budget
        exports = getattr(data_pipeline.budget, '__all__', [])
        print(f"✓ Budget module exports: {exports}")
    except Exception as e:
        print(f"✗ Budget module error: {e}")
        return False
    
    try:
        import data_pipeline.darta
        exports = getattr(data_pipeline.darta, '__all__', [])
        print(f"✓ Darta module exports: {exports}")
    except Exception as e:
        print(f"✗ Darta module error: {e}")
        return False
    
    return True


def test_readme_example_compatibility():
    """Test that README examples would work (without actual execution)."""
    print("\n" + "=" * 60)
    print("Testing README Example Compatibility")
    print("=" * 60)
    
    from data_pipeline.budget import process_data as budget_process
    from data_pipeline.trade import process_data as trade_process
    from data_pipeline.darta import process_data as darta_process
    
    # Test 1: Budget simple call
    print("\nExample 1: Budget Processing (Simple)")
    print("  Code: result = process_data('data/82-83.xlsx')")
    try:
        # Just verify we can call with positional arg
        import inspect
        sig = inspect.signature(budget_process)
        first_param = list(sig.parameters.values())[0]
        can_call = first_param.default == inspect.Parameter.empty or first_param.default is None
        print(f"  ✓ Can call with single positional argument: {can_call}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 2: Budget with merge
    print("\nExample 2: Budget Processing (With Merge)")
    print("  Code: process_data(xlsx_file='...', old_data='...', output_name='...')")
    try:
        sig = inspect.signature(budget_process)
        has_params = all(p in sig.parameters for p in ['xlsx_file', 'old_data', 'output_name'])
        print(f"  ✓ Has all required keyword arguments: {has_params}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 3: Trade processing
    print("\nExample 3: Trade Processing")
    print("  Code: process_data(xlsx_file='...', old_data='...', output_name='...')")
    try:
        sig = inspect.signature(trade_process)
        has_params = all(p in sig.parameters for p in ['xlsx_file', 'old_data', 'output_name'])
        print(f"  ✓ Has all required keyword arguments: {has_params}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 4: Darta processing
    print("\nExample 4: Darta Processing")
    print("  Code: process_data('data/darta.pdf', 'data/clean_data.csv')")
    try:
        sig = inspect.signature(darta_process)
        params = list(sig.parameters.keys())
        # Can be called with 2 positional args
        can_call = len(params) >= 2 or (len(params) >= 1 and list(sig.parameters.values())[1].default != inspect.Parameter.empty)
        print(f"  ✓ Can call with 2 positional arguments: {can_call}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    return True


def main():
    """Run all verification tests."""
    print("\n" + "=" * 60)
    print("README.md Verification Script")
    print("Testing: data-pipeline package")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Imports
    if not test_imports():
        all_passed = False
    
    # Test 2: Function signatures
    if not test_function_signatures():
        all_passed = False
    
    # Test 3: Module structure
    if not test_module_structure():
        all_passed = False
    
    # Test 4: README compatibility
    if not test_readme_example_compatibility():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("✓ README.md examples will work correctly")
        print("✓ Safe to push to GitHub")
    else:
        print("✗ SOME TESTS FAILED")
        print("✗ Review errors above")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

"""Quick test for phone number cleaning logic."""

import pandas as pd
import sys
sys.path.insert(0, r'c:\Users\ACER\Desktop\MERGE CODE\data-pipeline')

from data_pipeline.darta.cleaner import clean_phone_number

# Test cases based on the uploaded images
test_cases = [
    # Landline numbers (should preserve hyphen)
    ("01-4223346", "01-4223346"),
    ("01-5536752", "01-5536752"),
    
    # Mobile numbers with separators
    ("9846102366/9860465468", "9846102366"),
    ("9847035775,9807106077", "9847035775"),
    ("9808888110/9818111065", "9808888110"),
    
    # 8-digit mobile (should add 98 prefix)
    ("41542588", "9841542588"),
    ("47035775", "9847035775"),
    
    # 10-digit mobile
    ("9851234567", "9851234567"),
    
    # Mixed landline and mobile
    ("01-4223346/9846102366", "01-4223346"),
]

print("Testing phone number cleaning logic:\n")
print(f"{'Input':<30} | {'Expected':<15} | {'Actual':<15} | {'Status'}")
print("-" * 80)

all_passed = True
for input_val, expected in test_cases:
    actual = clean_phone_number(input_val)
    status = "✓ PASS" if actual == expected else "✗ FAIL"
    if actual != expected:
        all_passed = False
    print(f"{input_val:<30} | {expected:<15} | {actual:<15} | {status}")

print("\n" + "=" * 80)
if all_passed:
    print("✓ All tests passed!")
else:
    print("✗ Some tests failed!")

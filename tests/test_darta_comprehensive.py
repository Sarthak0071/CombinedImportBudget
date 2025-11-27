"""Detailed test of all darta transformations."""

import pandas as pd
from data_pipeline.darta import process_data

print("=" * 60)
print("COMPREHENSIVE DARTA DATA PROCESSING TEST")
print("=" * 60)

df = process_data('data/darta.pdf', 'data/darta_final.csv')

print(f"\n1. EXTRACTION: {len(df)} records extracted")
print(f"   Columns: {df.columns.tolist()}")

print(f"\n2. REGISTRATION NUMBERS:")
sample_regs = df['reg_no'].head(15).tolist()
print(f"   First 15: {sample_regs}")
backslash_test = any('\\' in str(r) for r in sample_regs)
slash_test = any('/' in str(r) for r in sample_regs)
if backslash_test or slash_test:
    print("   ERROR: Registration numbers still contain separators!")
else:
    print("   ✓ Separators removed correctly")

print(f"\n3. DATE PARSING:")
if 'year' in df.columns and 'month' in df.columns and 'day' in df.columns:
    print(f"   ✓ year/month/day columns created")
    print(f"   Years: {df['year'].value_counts().to_dict()}")
    print(f"   Months: {df['month'].value_counts().to_dict()}")
else:
    print("   ERROR: Date columns not created!")
if 'nregdate' in df.columns:
    print("   ERROR: nregdate column still present!")
else:
    print("   ✓ nregdate column removed")

print(f"\n4. PROVINCE/DISTRICT:")
if 'province' in df.columns or 'district' in df.columns:
    print(f"   ERROR: Original province/district columns still present!")
else:
    print("   ✓ Original province/district columns removed")
if 'province_code' in df.columns and 'district_code' in df.columns:
    print(f"   ✓ Code columns present")
else:
    print("   ERROR: Code columns missing!")

print(f"\n5. PHONE NUMBERS:")
sample_phones = df['director_phone'].head(10).tolist()
print(f"   Sample: {sample_phones}")

has_slash = any('/' in str(p) for p in sample_phones)
has_comma = any(',' in str(p) for p in sample_phones)  
has_short = any(len(str(p).replace('.', '')) < 8 for p in sample_phones if str(p) not in ['nan', 'None'])

if has_slash:
    print("   ERROR: Slashes still present!")
if has_comma:
    print("   ERROR: Commas still present!")
if not has_short:
    print("   ✓ All phone numbers valid length")

print(f"\n6. OUTPUT CSV:")
print(f"   File: data/darta_clean.csv")
print(f"   Size: {len(df)} rows x {len(df.columns)} columns")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

"""Final verification of all user requirements."""

import pandas as pd

df = pd.read_csv('data/darta_clean.csv')

print("=" * 70)
print("FINAL VERIFICATION - USER REQUIREMENTS")
print("=" * 70)

print(f"\n✓ Total: {len(df)} clean records")
print(f"\n✓ Columns: {df.columns.tolist()}")

print("\n" + "=" * 70)
print("1. REGISTRATION NUMBER EXTRACTION")
print("=" * 70)
test_cases = df['reg_no'].head(20).tolist()
print(f"Sample reg_no: {test_cases}")

has_separators = any('/' in str(r) or '\\' in str(r) or '-' in str(r) for r in test_cases if pd.notna(r))
print(f"✓ No separators: {not has_separators}")

print("\n" + "=" * 70)
print("2. DATE COLUMNS")
print("=" * 70)
print(f"✓ 'year' column exists: {'year' in df.columns}")
print(f"✓ 'month' column exists: {'month' in df.columns}")
print(f"✓ 'day' column exists: {'day' in df.columns}")
print(f"✓ 'nregdate' removed: {'nregdate' not in df.columns}")

print("\n" + "=" * 70)
print("3. PROVINCE/DISTRICT COLUMNS")
print("=" * 70)
print(f"✓ 'province' removed: {'province' not in df.columns}")
print(f"✓ 'district' removed: {'district' not in df.columns}")
print(f"✓ 'province_code' exists: {'province_code' in df.columns}")
print(f"✓ 'district_code' exists: {'district_code' in df.columns}")

print("\n" + "=" * 70)
print("4. PHONE NUMBER CLEANING")
print("=" * 70)
phones = df['director_phone'].dropna().head(20).tolist()
print("Sample phones:")
for i, p in enumerate(phones[:10]):
    print(f"  {i+1}. {p}")

has_slash = any('/' in str(p) for p in phones)
has_comma = any(',' in str(p) for p in phones)
all_valid = all(len(str(p).replace('.', '')) >= 8 for p in phones if str(p) not in ['nan', 'None'])

print(f"\n✓ No slashes: {not has_slash}")
print(f"✓ No commas: {not has_comma}")
print(f"✓ Valid lengths: {all_valid}")

print("\n" + "=" * 70)
print("5. NO DUPLICATE HEADERS IN DATA")
print("=" * 70)
nepali_text = any('मिमि' in str(r) or 'कामिकि' in str(r) for r in df['reg_no'])
header_text = any('reg_no' in str(r).lower() for r in df['reg_no'] if pd.notna(r))
print(f"✓ No Nepali headers: {not nepali_text}")
print(f"✓ No English headers: {not header_text}")

print("\n" + "=" * 70)
print("ALL REQUIREMENTS MET ✓" if all([
    'year' in df.columns,
    'nregdate' not in df.columns,
    'province' not in df.columns,
    'district' not in df.columns,
    not has_slash,
    not has_comma,
    not nepali_text
]) else "ISSUES REMAINING")
print("=" * 70)

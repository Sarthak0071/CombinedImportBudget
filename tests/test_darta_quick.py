"""Test darta PDF processing."""

from data_pipeline.darta import process_data

print("Testing darta processing...")
result = process_data('data/darta.pdf', 'data/darta_output.csv')
print(f"Success! Result shape: {result.shape}")
print(f"\nColumns: {list(result.columns)}")
print(f"\nFirst 3 rows:")
print(result.head(3))
print(f"\nSample reg_no values: {result['reg_no'].head(5).tolist()}")
if 'nregdate_year' in result.columns:
    print(f"Sample dates: Year={result['nregdate_year'].head(3).tolist()}")
if 'province_code' in result.columns:
    print(f"Province codes: {result['province_code'].value_counts().to_dict()}")
if 'district_code' in result.columns:
    print(f"District codes: {result['district_code'].value_counts().to_dict()}")

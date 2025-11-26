"""Test budget processing."""

from data_pipeline.budget import process_data

print("Testing budget processing...")
result = process_data('data/82-83.xlsx')
print(f"✅ Success! Result shape: {result.shape}")

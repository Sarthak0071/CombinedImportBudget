"""Quick test to verify code works."""

from data_pipeline.trade import process_data

print("Testing trade processing...")
result = process_data('data/FTS_uptoAsoj_208283_ci1nozq.xlsx', 'data/done.csv')
print(f"✅ Success! Result shape: {result.shape}")

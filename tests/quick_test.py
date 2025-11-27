"""Quick test for trade processing."""

import os
from pathlib import Path

# Get the root directory (parent of tests/)
root_dir = Path(__file__).parent.parent

from data_pipeline.trade import process_data

print("Testing trade processing...")
result = process_data(
    str(root_dir / 'data/FTS_uptoAsoj_208283_ci1nozq.xlsx'),
    str(root_dir / 'data/done.csv')
)
print(f"✅ Success! Result shape: {result.shape}")

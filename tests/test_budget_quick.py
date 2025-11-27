"""Quick test for budget processing."""

import os
from pathlib import Path

# Get the root directory (parent of tests/)
root_dir = Path(__file__).parent.parent

from data_pipeline.budget import process_data

print("Testing budget processing...")
result = process_data(str(root_dir / 'data/82-83.xlsx'))
print(f"✅ Success! Result shape: {result.shape}")

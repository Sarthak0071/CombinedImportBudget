"""Debug PDF extraction to see actual structure."""

import pdfplumber
from pathlib import Path

pdf_path = Path('data/darta.pdf')

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}\n")
    
    for page_num, page in enumerate(pdf.pages[:2], 1):
        print(f"=== PAGE {page_num} ===")
        tables = page.extract_tables()
        print(f"Tables found: {len(tables)}")
        
        if tables:
            for i, table in enumerate(tables):
                print(f"\nTable {i+1}:")
                print(f"Rows: {len(table)}")
                if table:
                    print("First 3 rows:")
                    for j, row in enumerate(table[:3]):
                        print(f"  Row {j}: {row}")
        print("\n")

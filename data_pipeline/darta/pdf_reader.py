"""PDF extraction utilities for darta data."""

import pdfplumber
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_tables_from_pdf(pdf_path: Path) -> pd.DataFrame:
    """Extract all tables from PDF and combine into single DataFrame."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    all_rows = []
    header_found = False
    headers = None
    
    with pdfplumber.open(pdf_path) as pdf:
        logger.info(f"Processing {pdf_path.name} ({len(pdf.pages)} pages)")
        
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            
            if not tables:
                continue
            
            for table in tables:
                if not table:
                    continue
                
                for row in table:
                    if not row or all(not cell or str(cell).strip() == '' for cell in row):
                        continue
                    
                    row_text = ' '.join(str(cell).lower() for cell in row if cell)
                    
                    if 'reg_no' in row_text and 'province' in row_text and 'district' in row_text:
                        if not header_found:
                            headers = [str(cell).strip() if cell else '' for cell in row]
                            header_found = True
                            logger.info(f"Headers detected on page {page_num}: {headers}")
                        else:
                            logger.info(f"Skipping duplicate header on page {page_num}")
                        continue
                    
                    if header_found and len(row) == len(headers):
                        first_cell = str(row[0]).strip() if row[0] else ''
                        
                        if first_cell.lower() in ['reg_no', 'altname', '']:
                            continue
                        
                        if 'मिमि' in first_cell or 'कामिकि' in first_cell or 'सञ्चार' in first_cell:
                            logger.info(f"Skipping Nepali header row on page {page_num}")
                            continue
                        
                        all_rows.append(row)
    
    if not header_found:
        raise ValueError("Could not find table headers in PDF")
    
    if not all_rows:
        raise ValueError("No data rows found in PDF")
    
    df = pd.DataFrame(all_rows, columns=headers)
    df = df.loc[:, df.columns.notna() & (df.columns != '')]
    
    logger.info(f"Extracted {len(df)} rows, {len(df.columns)} columns (before filtering)")
    return df

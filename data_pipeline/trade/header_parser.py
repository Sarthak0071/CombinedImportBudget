"""Header parsing utilities for extracting year and month metadata from Excel files."""

import re
import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from .config import MONTH_NAME_TO_NUMBER, NEPALI_MONTHS

logger = logging.getLogger(__name__)


def extract_header_metadata(excel_path: Path) -> Dict[str, Any]:
    """Extract fiscal metadata from Excel headers or filename."""
    try:
        header_text = _read_excel_header(excel_path)
        
        year = parse_fiscal_year_from_header(header_text)
        month_range = parse_month_range_from_header(header_text)
        
        if not year:
            year = _extract_year_from_filename(excel_path)
        
        if year and month_range:
            start_month, end_month = month_range
            target_month = end_month
            previous_month = target_month - 1 if target_month > 1 else 12
            
            logger.info(f"Extracted metadata: Year={year}, Months={start_month}-{end_month}, "
                       f"Target={target_month}, Previous={previous_month}")
            
            return {
                'year': year,
                'start_month': start_month,
                'end_month': end_month,
                'target_month': target_month,
                'previous_month': previous_month
            }
        
        logger.warning(f"Could not extract complete metadata from {excel_path.name}")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting metadata: {e}", exc_info=True)
        return None


def _read_excel_header(excel_path: Path, max_rows: int = 10) -> str:
    """Read first few rows of Excel to extract header text."""
    try:
        xls = pd.ExcelFile(excel_path)
        first_sheet = xls.sheet_names[0]
        
        df_header = pd.read_excel(
            excel_path,
            sheet_name=first_sheet,
            nrows=max_rows,
            header=None
        )
        
        header_text = ' '.join(
            str(val) for row in df_header.values 
            for val in row if pd.notna(val)
        )
        
        logger.debug(f"Header text: {header_text[:200]}")
        return header_text
        
    except Exception as e:
        logger.error(f"Error reading Excel header: {e}")
        return ""


def parse_fiscal_year_from_header(header_text: str) -> Optional[int]:
    """Extract fiscal year from header text using regex patterns."""
    patterns = [
        r'FY\s*(\d{4})/\d{2}',
        r'FY\s*(\d{4})-\d{2}',
        r'(\d{4})/\d{2}',
        r'(\d{4})-\d{2}',
        r'20(\d{2})/(\d{2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, header_text, re.IGNORECASE)
        if match:
            year_str = match.group(1)
            year = int(year_str)
            logger.debug(f"Extracted year: {year} using pattern: {pattern}")
            return year
    
    logger.warning(f"Could not extract fiscal year from header: {header_text[:100]}")
    return None


def parse_month_range_from_header(header_text: str) -> Optional[Tuple[int, int]]:
    """Extract Nepali month range from header text."""
    month_pattern = _build_month_pattern()
    
    patterns = [
        rf'\(({month_pattern})\s*[-–—]\s*({month_pattern})\)',
        rf'\b({month_pattern})\s*[-–—]\s*({month_pattern})\b',
        rf'\b({month_pattern})\s+to\s+({month_pattern})\b',
        rf'({month_pattern})\s*[-–—]\s*({month_pattern})',
    ]
    
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, header_text, re.IGNORECASE)
        if match:
            start_name = match.group(1).strip()
            end_name = match.group(2).strip()
            
            start_month = _find_month_number(start_name)
            end_month = _find_month_number(end_name)
            
            if start_month and end_month:
                logger.debug(f"Extracted month range using pattern {i+1}: {start_name}({start_month}) - "
                           f"{end_name}({end_month})")
                return (start_month, end_month)
            else:
                logger.debug(f"Pattern {i+1} matched but couldn't resolve months: '{start_name}' or '{end_name}'")
    
    logger.warning(f"Could not extract month range from header: {header_text[:150]}")
    return None


def _build_month_pattern() -> str:
    """Build regex pattern matching all Nepali month names."""
    month_names = list(MONTH_NAME_TO_NUMBER.keys())
    return '|'.join(month_names)


def _find_month_number(month_name: str) -> Optional[int]:
    """Map month name to number with fuzzy matching."""
    month_name_clean = month_name.strip().lower()
    

    for name, num in MONTH_NAME_TO_NUMBER.items():
        if name.lower() == month_name_clean:
            return num
    

    for name, num in MONTH_NAME_TO_NUMBER.items():
        name_lower = name.lower()
        if name_lower.startswith(month_name_clean) or month_name_clean.startswith(name_lower[:4]):
            logger.debug(f"Fuzzy matched '{month_name}' to '{name}' ({num})")
            return num
    
    variations = {
        'asoj': 'Ashwin',
        'kartik': 'Kartik',
        'mangsir': 'Mangsir',
    }
    
    for variant, canonical in variations.items():
        if variant in month_name_clean or month_name_clean in variant:
            return MONTH_NAME_TO_NUMBER.get(canonical)
    
    logger.warning(f"Could not match month name: {month_name}")
    return None


def _extract_year_from_filename(file_path: Path) -> Optional[int]:
    """Fallback extraction from filename if header parsing fails."""
    filename = file_path.stem
    
    patterns = [
        r'(\d{4})(\d{2})',
        r'(\d{4})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            year_str = match.group(1)
            year = int(year_str)
            if 2000 <= year <= 2100:
                logger.debug(f"Extracted year from filename: {year}")
                return year
    
    logger.warning(f"Could not extract year from filename: {filename}")
    return None


def detect_target_month(start_month: int, end_month: int) -> int:
    """Return latest month in range."""
    return end_month

"""Data cleaning utilities for darta processing."""

import pandas as pd
import re
import logging
from typing import Optional

from .config import NEPALI_TO_ENGLISH_DIGITS, REG_NUMBER_SEPARATORS, PROVINCE_MAPPING, DISTRICT_MAPPING
from ..core.utils import convert_nepali_to_english as _convert_nepali, fuzzy_string_match

logger = logging.getLogger(__name__)


def convert_nepali_to_english(text: str) -> str:
    """Convert Nepali numerals to English numerals."""
    return _convert_nepali(text, NEPALI_TO_ENGLISH_DIGITS)


def clean_registration_number(reg_no: str) -> str:
    """
    Extract registration number before separator.
    
    Examples:
        008/073-74 -> 008
        780\074 -> 780
        894-075 -> 894
        ११०११९-०६९-०७२ -> 110119 (also converts Nepali)
        1,2,3,4 -> 1,2,3,4 (keeps comma-separated)
    """
    if pd.isna(reg_no):
        return reg_no
    
    reg_str = str(reg_no).strip()
    reg_str = convert_nepali_to_english(reg_str)
    
    if ',' in reg_str and all(c.isdigit() or c == ',' for c in reg_str):
        return reg_str
    
    all_separators = REG_NUMBER_SEPARATORS + ['\\']
    for separator in all_separators:
        if separator in reg_str:
            parts = reg_str.split(separator)
            return parts[0].strip()
    
    return reg_str


def parse_date_components(date_str: str) -> dict:
    """
    Parse date string into year, month, day components.
    
    Handles formats: YYYY-MM-DD, YYYY/MM/DD, or similar
    """
    if pd.isna(date_str):
        return {'year': None, 'month': None, 'day': None}
    
    date_clean = convert_nepali_to_english(str(date_str).strip())
    
    patterns = [
        r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})',
        r'(\d{4})\s+(\d{1,2})\s+(\d{1,2})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, date_clean)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return {'year': year, 'month': month, 'day': day}
    
    logger.warning(f"Could not parse date: {date_str}")
    return {'year': None, 'month': None, 'day': None}


def fuzzy_find_code(name: str, mapping: dict, threshold: float = 0.75) -> Optional[str]:
    """Find code using fuzzy matching."""
    if pd.isna(name):
        return None
    
    name_clean = str(name).strip()
    
    if name_clean in mapping:
        return mapping[name_clean]
    
    best_match = None
    best_ratio = threshold
    
    for key, code in mapping.items():
        ratio = fuzzy_string_match(name_clean, key)
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = code
    
    if best_match:
        return best_match
    
    logger.warning(f"No mapping found for: {name}")
    return None


def clean_phone_number(phone: str) -> str:
    """
    Clean phone numbers comprehensively.
    
    Rules:
    - Keep landline numbers (01-xxx) as-is with hyphen
    - Extract first valid 10-digit mobile starting with 9
    - Split on /, comma for multiple numbers
    - Add 98 prefix to 8-digit mobile numbers
    """
    if pd.isna(phone):
        return phone
    
    phone_str = str(phone).strip()
    phone_str = convert_nepali_to_english(phone_str)
    
    # Handle separators (/, ,) - process these first
    separators = ['/', ',']
    for sep in separators:
        if sep in phone_str:
            parts = [p.strip() for p in phone_str.split(sep)]
            for part in parts:
                # Check if this part is a landline
                if part.startswith('01') and '-' in part:
                    return part
                # Check for valid mobile number
                digits = ''.join(c for c in part if c.isdigit())
                if len(digits) == 10 and digits[0] == '9':
                    return digits
                elif len(digits) == 8 and not part.startswith('01'):
                    return '98' + digits
            # If no valid number found, use first part
            phone_str = parts[0] if parts else phone_str
    
    # Check for single landline (no separators)
    if phone_str.startswith('01') and '-' in phone_str:
        return phone_str
    
    # Process single number without separators
    digits_only = ''.join(c for c in phone_str if c.isdigit())
    
    # 10-digit mobile starting with 9
    if len(digits_only) == 10 and digits_only[0] == '9':
        return digits_only
    
    # 8-digit mobile (add 98 prefix)
    if len(digits_only) == 8:
        return '98' + digits_only
    
    # Return as-is if no valid pattern matched
    return phone_str


def apply_province_code(df: pd.DataFrame) -> pd.DataFrame:
    """Map province names to codes."""
    df = df.copy()
    if 'province' in df.columns:
        df['province_code'] = df['province'].apply(lambda x: fuzzy_find_code(x, PROVINCE_MAPPING))
        logger.info(f"Mapped {df['province_code'].notna().sum()}/{len(df)} province codes")
    return df


def apply_district_code(df: pd.DataFrame) -> pd.DataFrame:
    """Map district names to codes."""
    df = df.copy()
    if 'district' in df.columns:
        df['district_code'] = df['district'].apply(lambda x: fuzzy_find_code(x, DISTRICT_MAPPING))
        logger.info(f"Mapped {df['district_code'].notna().sum()}/{len(df)} district codes")
    return df


def process_darta_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning transformations to darta data."""
    logger.info(f"Processing {len(df)} records")
    
    df = df.copy()
    
    if 'reg_no' in df.columns:
        df['reg_no'] = df['reg_no'].apply(clean_registration_number)
    
    if 'director_phone' in df.columns:
        df['director_phone'] = df['director_phone'].apply(clean_phone_number)
    
    if 'editor_phone' in df.columns:
        df['editor_phone'] = df['editor_phone'].apply(clean_phone_number)
    
    if 'nregdate' in df.columns:
        date_components = df['nregdate'].apply(parse_date_components)
        df['year'] = date_components.apply(lambda x: x['year'])
        df['month'] = date_components.apply(lambda x: x['month'])
        df['day'] = date_components.apply(lambda x: x['day'])
        df = df.drop(columns=['nregdate'])
    
    df = apply_province_code(df)
    df = apply_district_code(df)
    
    columns_to_drop = []
    if 'province' in df.columns and 'province_code' in df.columns:
        columns_to_drop.append('province')
    if 'district' in df.columns and 'district_code' in df.columns:
        columns_to_drop.append('district')
    
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)
    
    column_order = ['year', 'month', 'day', 'reg_no', 'province_code', 'district_code']
    other_columns = [col for col in df.columns if col not in column_order]
    final_order = column_order + other_columns
    df = df[[col for col in final_order if col in df.columns]]
    
    logger.info(f"Processing complete: {len(df)} records")
    return df
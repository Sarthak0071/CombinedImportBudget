"""Clean and standardize country codes."""
import pandas as pd
import pycountry
from difflib import SequenceMatcher
import re
import logging
from functools import lru_cache
from typing import Optional

from .config import CUSTOM_COUNTRY_MAPPINGS, COUNTRY_NAME_NORMALIZATIONS

logger = logging.getLogger(__name__)


def normalize_country_name(name: str) -> Optional[str]:
    """Normalize country name for better matching."""
    if pd.isna(name):
        return None
    
    if name in COUNTRY_NAME_NORMALIZATIONS:
        return COUNTRY_NAME_NORMALIZATIONS[name]
    
    normalized = str(name).strip()
    normalized = re.sub(r'\[.*?\]', '', normalized).strip()
    
    return normalized if normalized else None


def fuzzy_match_country(name: str, threshold: float = 0.85) -> Optional[str]:
    """Find country using fuzzy string matching."""
    best_match = None
    best_ratio = 0
    name_lower = name.lower()
    
    try:
        for country in pycountry.countries:
            ratio = SequenceMatcher(None, name_lower, country.name.lower()).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = country
            
            if hasattr(country, 'common_name'):
                ratio = SequenceMatcher(None, name_lower, country.common_name.lower()).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match = country
        
        if best_ratio >= threshold and best_match:
            return best_match.alpha_2
        
        return None
        
    except Exception as e:
        logger.error(f"Error in fuzzy matching for '{name}': {e}")
        return None


@lru_cache(maxsize=512)
def get_iso2_code(country_name: str) -> str:
    """Get ISO 3166-1 alpha-2 code for country name."""
    if pd.isna(country_name):
        return country_name
    
    original_name = str(country_name)
    
    if country_name in CUSTOM_COUNTRY_MAPPINGS:
        return CUSTOM_COUNTRY_MAPPINGS[country_name]
    
    normalized = normalize_country_name(country_name)
    if not normalized:
        return original_name
    
    try:
        country = pycountry.countries.get(name=normalized)
        if country:
            return country.alpha_2
    except (LookupError, AttributeError):
        pass
    
    try:
        results = pycountry.countries.search_fuzzy(normalized)
        if results:
            return results[0].alpha_2
    except (LookupError, AttributeError):
        pass
    
    code = fuzzy_match_country(normalized)
    if code:
        return code
    
    logger.warning(f"No ISO-2 mapping found for: '{country_name}'")
    return original_name


def clean_country_codes(df: pd.DataFrame) -> pd.DataFrame:
    """Convert all country names to ISO-2 codes."""
    if 'Country' not in df.columns:
        raise ValueError("DataFrame must have 'Country' column")
    
    df = df.copy()
    
    sample_countries = df['Country'].dropna().unique()[:5]
    already_iso2 = all(len(str(c)) == 2 for c in sample_countries if pd.notna(c))
    
    if already_iso2:
        logger.info("Countries already in ISO-2 format")
    else:
        df['Country'] = df['Country'].apply(get_iso2_code)
        
        df.loc[df['Country'] == 'Namibia', 'Country'] = 'NA'
        logger.info(f"Converted countries to ISO-2: {df['Country'].nunique()} unique codes")
    
    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Final validation and cleaning."""
    df = df.copy()
    initial_count = len(df)
    
    df = df[df['HS_Code'].notna()]
    df = df[df['Country'].notna()]
    df = df[df['Value'].notna()]
    
    df['Year'] = df['Year'].astype(int)
    df['Month'] = df['Month'].astype(int)
    df['Direction'] = df['Direction'].astype(str)
    df['HS_Code'] = df['HS_Code'].astype(str)
    df['Country'] = df['Country'].astype(str)
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
    
    final_count = len(df)
    
    if final_count != initial_count:
        logger.warning(f"Removed {initial_count - final_count} invalid records")
    
    logger.info(f"Validated: {final_count:,} records")
    
    return df


def clean_monthly_data(df: pd.DataFrame) -> pd.DataFrame:
    """Complete cleaning pipeline for monthly data."""
    logger.info(f"Cleaning monthly data: {len(df):,} records")
    
    df = validate_data(df)
    
    logger.info(f"Cleaning complete: {len(df):,} records ready")
    
    return df
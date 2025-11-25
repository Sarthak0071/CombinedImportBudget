"""Utility functions for budget data processing."""

import re
import pandas as pd
from pathlib import Path

# Configuration constants
STANDARD_COLUMNS = [
    "Year", "Project_Code", "Sub_Project_Code", "Economic_Code",
    "District_Code", "Component_Code", "Donor_Code", 
    "Source_Type_Code", "Activity_Code", "Amount"
]

COLUMN_MAPPING = {
    "BUD_YEAR": "Year", "PROJECT_CODE": "Project_Code",
    "SUB_PROJECT_CODE": "Sub_Project_Code", "ECONOMIC_CODE5": "Economic_Code",
    "DISTRICT_CODE": "District_Code", "COMPONENT_CODE": "Component_Code",
    "DONOR_CODE": "Donor_Code", "SOURCE_TYPE_CODE": "Source_Type_Code",
    "ACTIVITY_CODE": "Activity_Code", "AMOUNT": "Amount"
}

COLUMNS_TO_REMOVE = [
    "VIN", "VOUT", "NET_BUDGET", "SUM(EXP)",
    "MINISTRY_CODE", "MINISTRY_NDESC", "MAIN_ACTIVITY_NDESC4",
    "PROJECT_NDESC", "SUB_PROJECT_NDESC", "MINISTRY", "GOVERNMENT_LEVEL"
]

SHEET_PATTERNS = {
    "federal": ["federal", "Federal", "FEDERAL"],
    "province": ["province", "Province", "PROVINCE", "provience"],
    "local": ["local", "Local", "LOCAL"]
}


def extract_fiscal_year(filename: str) -> str:
    """Extract fiscal year from filename (e.g., 82-83.xlsx -> 82-83)."""
    filename = Path(filename).stem
    match = re.search(r'(\d{2,4})[_-](\d{2})', filename)
    return f"{match.group(1)}-{match.group(2)}" if match else None


def clean_year_value(year_val) -> str:
    """Standardize year value (77-78 -> 2077, 2077/78 -> 2077)."""
    year_str = str(year_val).strip()
    if "/" in year_str:
        return year_str.split("/")[0]
    if "-" in year_str:
        parts = year_str.split("-")
        return "20" + parts[0] if len(parts[0]) == 2 else parts[0]
    if len(year_str) == 2:
        return "20" + year_str
    return year_str


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize column names."""
    new_columns = []
    for col in df.columns:
        if pd.isna(col) or str(col).strip() == "":
            new_columns.append(None)
            continue
        col_str = str(col).strip()
        col_str = re.sub(r'\s+', ' ', col_str).replace('\n', '')
        new_columns.append(col_str)
    df.columns = new_columns
    return df.loc[:, df.columns.notna()]


def get_government_level(sheet_name: str) -> str:
    """Determine government level from sheet name."""
    sheet_lower = sheet_name.lower()
    if "federal" in sheet_lower:
        return "Federal"
    elif "province" in sheet_lower or "provience" in sheet_lower:
        return "Province"
    elif "local" in sheet_lower:
        return "Local"
    return "Unknown"

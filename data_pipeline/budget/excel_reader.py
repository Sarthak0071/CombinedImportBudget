"""Budget-specific Excel reader."""

import pandas as pd
import logging
from pathlib import Path
from typing import List

from ..core.io import BaseExcelReader
from ..core.utils import extract_fiscal_year, clean_year_value
from .config import STANDARD_COLUMNS, COLUMN_MAPPING, COLUMNS_TO_REMOVE, SHEET_PATTERNS

logger = logging.getLogger(__name__)


def get_government_level(sheet_name: str) -> str:
    """Determine government level from sheet name using fuzzy matching."""
    from difflib import SequenceMatcher
    
    sheet_clean = sheet_name.lower().strip()
    
    keywords = {
        'Federal': ['federal', 'फेडरल', 'federel', 'fedarel'],
        'Province': ['province', 'प्रदेश', 'provience', 'provine', 'provinc'],
        'Local': ['local', 'स्थानीय', 'lokal', 'lokl']
    }
    
    best_match = 'Unknown'
    best_ratio = 0.6
    
    for level, terms in keywords.items():
        for term in terms:
            if term in sheet_clean:
                return level
            ratio = SequenceMatcher(None, term, sheet_clean).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = level
    
    return best_match


class BudgetExcelReader(BaseExcelReader):
    """Excel reader for budget data (Federal/Province/Local sheets)."""
    
    def detect_budget_sheets(self) -> List[str]:
        """Auto-detect relevant sheet names in Excel file."""
        relevant = [
            s for s in self.sheet_names
            if any(p in s.lower() for patterns in SHEET_PATTERNS.values() for p in patterns)
        ]
        logger.info(f"Detected {len(relevant)} budget sheets: {relevant}")
        return relevant
    
    def extract_budget_data(self, year: str = None) -> pd.DataFrame:
        """Extract and process budget data from Excel file."""
        year = year or extract_fiscal_year(self.excel_path.name)
        if not year:
            raise ValueError(f"Could not extract fiscal year from: {self.excel_path.name}")
        
        logger.info(f"Processing {self.excel_path.name} (Year: {year})")
        sheet_names = self.detect_budget_sheets()
        
        if not sheet_names:
            raise ValueError(f"No relevant sheets found in {self.excel_path.name}")
        
        all_data = []
        for sheet in sheet_names:
            try:
                df = self.read_sheet(sheet, skip_rows=0, header=0)
                df = self._standardize_budget_columns(df)
                
                # Remove unwanted columns
                for col in COLUMNS_TO_REMOVE + [c for c in df.columns if "SUBSTR" in str(c).upper()]:
                    if col in df.columns:
                        df = df.drop(columns=[col])
                
                if "BUD_YEAR" not in df.columns:
                    df.insert(0, "BUD_YEAR", year)
                df["GOVERNMENT_LEVEL"] = get_government_level(sheet)
                df = df.dropna(how='all')
                
                logger.info(f"  {sheet}: {len(df)} rows")
                all_data.append(df)
            except Exception as e:
                logger.error(f"  Failed {sheet}: {e}")
        
        if not all_data:
            raise ValueError(f"No data extracted from {self.excel_path.name}")
        
        combined = pd.concat(all_data, ignore_index=True)
        combined["BUD_YEAR"] = combined["BUD_YEAR"].apply(clean_year_value)
        combined = combined.rename(columns=COLUMN_MAPPING)
        
        available_cols = [col for col in STANDARD_COLUMNS if col in combined.columns]
        logger.info(f"Extracted {len(combined):,} total rows")
        return combined[available_cols]
    
    def _standardize_budget_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize budget column names."""
        import re
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


def extract_budget_data(file_path: Path, year: str = None) -> pd.DataFrame:
    """Extract and process budget data from Excel file."""
    reader = BudgetExcelReader(file_path)
    data = reader.extract_budget_data(year)
    reader.close()
    return data

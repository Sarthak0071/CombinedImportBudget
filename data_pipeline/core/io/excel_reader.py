"""Base Excel reading functionality."""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)


class BaseExcelReader:
    """Base class for reading Excel files with domain-specific implementations."""
    
    def __init__(self, excel_path: Path):
        if not excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        self.excel_path = excel_path
        self.xl_file = pd.ExcelFile(excel_path)
        self.sheet_names = self.xl_file.sheet_names
        logger.info(f"Loaded Excel: {excel_path.name} ({len(self.sheet_names)} sheets)")
    
    def detect_sheets(self, keywords: List[str]) -> List[str]:
        """Detect relevant sheet names based on keywords."""
        relevant = []
        for name in self.sheet_names:
            name_lower = name.lower()
            for keyword in keywords:
                if str(keyword).lower() in name_lower:
                    relevant.append(name)
                    break
        
        logger.info(f"Detected {len(relevant)} relevant sheets: {relevant}")
        return relevant
    
    def read_sheet(
        self,
        sheet_name: str,
        skip_rows: int = 0,
        header: Optional[int] = 0
    ) -> pd.DataFrame:
        """Read a specific sheet from Excel."""
        logger.info(f"Reading sheet: {sheet_name}")
        
        df = pd.read_excel(
            self.excel_path,
            sheet_name=sheet_name,
            skiprows=skip_rows,
            header=header
        )
        
        logger.info(f"  Loaded {len(df):,} rows, {len(df.columns)} columns")
        return df
    
    def close(self):
        """Close Excel file."""
        self.xl_file.close()

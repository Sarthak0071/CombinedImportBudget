"""Trade-specific Excel reader for import/export data."""

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Tuple

from ..core.io import BaseExcelReader
from ..core.utils import (
    find_data_start_row,
    find_target_sheet,
    standardize_column_names,
    clean_numeric_column,
    remove_total_rows
)
from .config import IMPORT_SHEET_KEYWORDS, EXPORT_SHEET_KEYWORDS
from .header_parser import extract_header_metadata

logger = logging.getLogger(__name__)


class TradeExcelReader(BaseExcelReader):
    """Excel reader for trade data (Table 4 = Import, Table 6 = Export)."""
    
    def extract_metadata(self):
        """Extract year/month metadata from Excel file headers."""
        return extract_header_metadata(self.excel_path)
    
    def read_import_data(self) -> Optional[pd.DataFrame]:
        """Read import data from Excel file (Table 4)."""
        return self._read_trade_data('import', IMPORT_SHEET_KEYWORDS)
    
    def read_export_data(self) -> Optional[pd.DataFrame]:
        """Read export data from Excel file (Table 6)."""
        return self._read_trade_data('export', EXPORT_SHEET_KEYWORDS)
    
    def _read_trade_data(
        self,
        trade_type: str,
        keywords: list
    ) -> Optional[pd.DataFrame]:
        """Internal function to read trade data from Excel."""
        try:
            target_sheet = find_target_sheet(self.sheet_names, keywords)
            
            if not target_sheet:
                logger.warning(f"No {trade_type} sheet found")
                return None
            
            logger.info(f"Reading {trade_type} from {self.excel_path.name}, sheet: {target_sheet}")
            
            # Find data start row
            df_sample = pd.read_excel(
                self.excel_path,
                sheet_name=target_sheet,
                nrows=10,
                header=None
            )
            skip_rows = find_data_start_row(df_sample)
            
            # Read actual data
            df = pd.read_excel(
                self.excel_path,
                sheet_name=target_sheet,
                skiprows=skip_rows
            )
            
            df = standardize_column_names(df)
            
            df.columns = [
                str(c).lower().strip().replace(' ', '_').replace('.', '') 
                for c in df.columns
            ]
            
            col_map = {}
            for col in df.columns:
                if any(x in col for x in ['hscode', 'hs_code', 'code', 'hs']):
                    col_map[col] = 'HS_Code'
                elif any(x in col for x in ['description', 'commodity', 'item']):
                    col_map[col] = 'Commodity'
                elif any(x in col for x in ['partner', 'country', 'countries']):
                    col_map[col] = 'Country'
                elif col == 'unit':
                    col_map[col] = 'Unit'
                elif 'quantity' in col:
                    col_map[col] = 'Quantity'
                elif 'value' in col:
                    col_map[col] = 'Value'
                elif 'revenue' in col:
                    col_map[col] = 'Revenue'
            
            df = df.rename(columns=col_map)
            
            if 'Unit' not in df.columns:
                df['Unit'] = 'pcs'
            if 'Quantity' not in df.columns:
                df['Quantity'] = 0
            if trade_type == 'import' and 'Revenue' not in df.columns:
                df['Revenue'] = 0
            
            df = df[df['HS_Code'].notna()]
            df = remove_total_rows(df, key_column='HS_Code')
            df = df.dropna(how='all')
            
            for col in ['Value', 'Quantity', 'Revenue']:
                if col in df.columns:
                    df = clean_numeric_column(df, col)
            
            df['HS_Code'] = df['HS_Code'].astype(str).str.strip()
            df['Country'] = df['Country'].astype(str).str.strip().replace(
                ['nan', 'None', ''], 'Unknown'
            )
            
            logger.info(f"Cleaned {trade_type} data: {len(df):,} records")
            
            return df
            
        except Exception as e:
            logger.error(f"Error reading {trade_type} data: {e}", exc_info=True)
            return None


def read_cumulative_excel(excel_path: Path) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Read both import and export data from cumulative Excel file."""
    reader = TradeExcelReader(excel_path)
    
    import_df = reader.read_import_data()
    if import_df is None:
        logger.error("Failed to read import data")
    
    export_df = reader.read_export_data()
    if export_df is None:
        logger.error("Failed to read export data")
    
    reader.close()
    
    return import_df, export_df

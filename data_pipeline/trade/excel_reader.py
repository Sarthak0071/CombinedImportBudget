"""Trade-specific Excel reader for import/export data."""

import pandas as pd
import logging
            
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
            
            df = standardize_column_names(df, mode='trade')
            
            # Add missing columns with defaults
            if 'Unit' not in df.columns:
                df['Unit'] = 'pcs'
            if 'Quantity' not in df.columns:
                df['Quantity'] = 0
            if trade_type == 'import' and 'Revenue' not in df.columns:
                df['Revenue'] = 0
            
            # Clean data
            df = df[df['HS_Code'].notna()]
            df = remove_total_rows(df, key_column='HS_Code')
            df = df.dropna(how='all')
            
            # Clean numeric columns
            for col in ['Value', 'Quantity', 'Revenue']:
                if col in df.columns:
                    df = clean_numeric_column(df, col)
            
            # Clean string columns
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

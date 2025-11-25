"""Convert cumulative values to monthly values."""
import pandas as pd
import logging
from typing import Tuple

from .config import TARGET_YEAR, TARGET_MONTH, NEPALI_MONTHS
from .cleaner import get_iso2_code  

logger = logging.getLogger(__name__)


def calculate_previous_cumulative(
    previous_df: pd.DataFrame, 
    trade_type: str
) -> pd.DataFrame:
    """Sum monthly records to get cumulative values."""
    direction = 'I' if trade_type == 'import' else 'E'
    df = previous_df[previous_df['Direction'] == direction].copy()
    
    if len(df) == 0:
        logger.warning(f"No {trade_type} data in filtered dataset")
        return pd.DataFrame()
    
    logger.info(f"Calculating {trade_type} cumulative from {len(df):,} records")
    
    df['HS_Code'] = df['HS_Code'].astype(str).str.strip().str.replace('.0', '', regex=False)
    df['Country'] = df['Country'].astype(str).str.strip()
    df['_key'] = df['HS_Code'] + '|' + df['Country']
    
    agg_dict = {
        'HS_Code': 'first',
        'Country': 'first',
        'Value': 'sum',
        'Quantity': 'sum',
        'Unit': 'first'
    }
    
    if trade_type == 'import' and 'Revenue' in df.columns:
        agg_dict['Revenue'] = 'sum'
    
    cumulative = df.groupby('_key', as_index=False).agg(agg_dict)
    logger.info(f"Result: {len(cumulative):,} unique keys, total value: {cumulative['Value'].sum():,.2f}")
    
    return cumulative


def calculate_monthly_values(
    current_cumulative: pd.DataFrame,
    previous_cumulative: pd.DataFrame,
    trade_type: str
) -> pd.DataFrame:
    """Calculate monthly values by subtracting previous cumulative from current."""
    logger.info(f"Calculating monthly {trade_type} values")
    
    current_cumulative = current_cumulative.copy()
    current_cumulative['HS_Code'] = current_cumulative['HS_Code'].astype(str).str.strip().str.replace('.0', '', regex=False)
    current_cumulative['Country'] = current_cumulative['Country'].apply(get_iso2_code)
    current_cumulative['_key'] = current_cumulative['HS_Code'] + '|' + current_cumulative['Country']
    
    agg_dict = {
        'HS_Code': 'first',
        'Country': 'first',
        'Value': 'sum',
        'Quantity': 'sum',
        'Unit': 'first'
    }
    
    if trade_type == 'import' and 'Revenue' in current_cumulative.columns:
        agg_dict['Revenue'] = 'sum'
    
    current_aggregated = current_cumulative.groupby('_key', as_index=False).agg(agg_dict)
    current_dict = current_aggregated.set_index('_key').to_dict('index')
    
    if not previous_cumulative.empty:
        previous_dict = previous_cumulative.set_index('_key').to_dict('index')
    else:
        previous_dict = {}
        logger.info("No previous month data available")
    
    all_keys = set(current_dict.keys()) | set(previous_dict.keys())
    
    monthly_records = []
    zero_count = 0
    
    for key in all_keys:
        current_values = current_dict.get(key, {})
        previous_values = previous_dict.get(key, {})
        
        monthly_value = current_values.get('Value', 0) - previous_values.get('Value', 0)
        monthly_quantity = current_values.get('Quantity', 0) - previous_values.get('Quantity', 0)
        
        if monthly_value > 0 or monthly_quantity > 0:
            record = {
                'Year': TARGET_YEAR,
                'Month': TARGET_MONTH,
                'Direction': 'I' if trade_type == 'import' else 'E',
                'HS_Code': current_values.get('HS_Code') or previous_values.get('HS_Code'),
                'Country': current_values.get('Country') or previous_values.get('Country'),
                'Value': monthly_value,
                'Quantity': monthly_quantity,
                'Unit': current_values.get('Unit') or previous_values.get('Unit', 'pcs')
            }
            
            if trade_type == 'import':
                record['Revenue'] = current_values.get('Revenue', 0) - previous_values.get('Revenue', 0)
            
            monthly_records.append(record)
        else:
            zero_count += 1
    
    if not monthly_records:
        logger.warning(f"No positive monthly records for {trade_type}")
        return pd.DataFrame()
    
    monthly_df = pd.DataFrame(monthly_records)
    logger.info(f"Result: {len(monthly_df):,} records (filtered {zero_count:,} zero/negative), total: {monthly_df['Value'].sum():,.2f}")
    
    return monthly_df


def process_trade_type(
    current_cumulative: pd.DataFrame,
    previous_filtered: pd.DataFrame,
    trade_type: str
) -> pd.DataFrame:
    previous_cumulative = calculate_previous_cumulative(previous_filtered, trade_type)
    
    monthly_df = calculate_monthly_values(
        current_cumulative, 
        previous_cumulative, 
        trade_type
    )
    
    return monthly_df


def combine_import_export(
    import_df: pd.DataFrame, 
    export_df: pd.DataFrame
) -> pd.DataFrame:
    """Combine import and export dataframes."""
    dfs_to_combine = []
    
    if not import_df.empty:
        dfs_to_combine.append(import_df)
    if not export_df.empty:
        dfs_to_combine.append(export_df)
    
    if not dfs_to_combine:
        raise ValueError("No data to combine - both import and export empty")
    
    combined = pd.concat(dfs_to_combine, ignore_index=True)
    
    column_order = ['Year', 'Month', 'Direction', 'HS_Code', 'Country',
                   'Value', 'Quantity', 'Unit', 'Revenue']
    combined = combined[[col for col in column_order if col in combined.columns]]
    
    logger.info(f"Combined {len(combined):,} records")
    return combined


def create_cumulative_dataframe(
    import_cumulative: pd.DataFrame,
    export_cumulative: pd.DataFrame
) -> pd.DataFrame:
    """Create combined cumulative dataframe from import and export data."""
    dfs = []
    
    if import_cumulative is not None and not import_cumulative.empty:
        imp = import_cumulative.copy()
        imp['Direction'] = 'I'
        dfs.append(imp)
    
    if export_cumulative is not None and not export_cumulative.empty:
        exp = export_cumulative.copy()
        exp['Direction'] = 'E'
        dfs.append(exp)
    
    if not dfs:
        raise ValueError("No cumulative data available")
    
    cum = pd.concat(dfs, ignore_index=True)
    
    column_order = ['HS_Code', 'Commodity', 'Country', 'Direction',
                   'Value', 'Quantity', 'Unit', 'Revenue']
    
    cum = cum[[col for col in column_order if col in cum.columns]]
    
    logger.info(f"Created cumulative dataframe: {len(cum):,} records")
    return cum

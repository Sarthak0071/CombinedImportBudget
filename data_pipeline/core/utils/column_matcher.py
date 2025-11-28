from typing import Optional
import pandas as pd
from .data_utils import fuzzy_string_match


def find_column(df: pd.DataFrame, target: str, threshold: float = 0.85) -> Optional[str]:
    """Find column in DataFrame using fuzzy matching."""
    target_clean = target.lower().replace('_', '').replace(' ', '').replace('-', '')
    
    def similarity_score(col):
        col_clean = str(col).lower().replace('_', '').replace(' ', '').replace('-', '')
        return fuzzy_string_match(target_clean, col_clean)
    
    if not df.columns.empty:
        best_match = max(df.columns, key=similarity_score)
        if similarity_score(best_match) >= threshold:
            return best_match
    
    return None




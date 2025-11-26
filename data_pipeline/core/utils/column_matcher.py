from difflib import SequenceMatcher
from typing import Optional, List, Dict
import pandas as pd


def find_column(df: pd.DataFrame, target: str, threshold: float = 0.85) -> Optional[str]:
    """Find column in DataFrame using fuzzy matching."""
    target_clean = target.lower().replace('_', '').replace(' ', '').replace('-', '')
    
    def similarity_score(col):
        col_clean = str(col).lower().replace('_', '').replace(' ', '').replace('-', '')
        return SequenceMatcher(None, target_clean, col_clean).ratio()
    
    if not df.columns.empty:
        best_match = max(df.columns, key=similarity_score)
        if similarity_score(best_match) >= threshold:
            return best_match
    
    return None




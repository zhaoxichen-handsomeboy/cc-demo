from typing import Dict, List, Any
import pandas as pd
import numpy as np


def infer_column_type(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "date"
    if pd.api.types.is_numeric_dtype(series):
        return "number"
    return "text"


def summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    column_types = {}
    missing_stats = {}
    for col in df.columns:
        column_types[col] = infer_column_type(df[col])
        missing_stats[col] = int(df[col].isna().sum())
    return {
        "columns": list(df.columns),
        "row_count": len(df),
        "column_types": column_types,
        "missing_stats": missing_stats,
    }


def get_preview(df: pd.DataFrame, limit: int = 100) -> List[Dict[str, Any]]:
    preview_df = df.head(limit)
    return preview_df.replace({np.nan: None}).to_dict(orient="records")

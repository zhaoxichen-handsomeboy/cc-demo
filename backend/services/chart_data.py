from typing import Dict, Any, List
import pandas as pd
import numpy as np


AGG_MAP = {
    "sum": "sum",
    "mean": "mean",
    "count": "count",
    "max": "max",
    "min": "min",
}


def generate_chart_data(
    df: pd.DataFrame,
    chart_type: str,
    x_field: str,
    y_field: str,
    agg_func: str,
    group_by: str = None,
) -> Dict[str, Any]:
    if x_field not in df.columns:
        raise ValueError(f"X field '{x_field}' not found")
    if y_field not in df.columns:
        raise ValueError(f"Y field '{y_field}' not found")
    if group_by and group_by not in df.columns:
        raise ValueError(f"Group by field '{group_by}' not found")

    pandas_agg = AGG_MAP.get(agg_func, "sum")

    if chart_type == "pie":
        grouped = df.groupby(x_field)[y_field].agg(pandas_agg).reset_index()
        categories = grouped[x_field].astype(str).tolist()
        series_data = grouped[y_field].tolist()
        return {
            "categories": categories,
            "series": [{"name": y_field, "data": series_data}],
        }

    if group_by:
        grouped = df.groupby([x_field, group_by])[y_field].agg(pandas_agg).unstack(fill_value=0)
        categories = grouped.index.astype(str).tolist()
        series = []
        for col in grouped.columns:
            series.append({
                "name": str(col),
                "data": grouped[col].tolist(),
            })
        return {"categories": categories, "series": series}

    grouped = df.groupby(x_field)[y_field].agg(pandas_agg).reset_index()
    categories = grouped[x_field].astype(str).tolist()
    values = grouped[y_field].tolist()
    return {
        "categories": categories,
        "series": [{"name": y_field, "data": values}],
    }

import pandas as pd
from typing import Dict, Any


def drop_na(df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    subset = params.get("subset")
    how = params.get("how", "any")
    return df.dropna(subset=subset, how=how)


def fill_na(df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    column = params.get("column")
    strategy = params.get("strategy", "mean")
    fill_value = params.get("fill_value")

    if column and column not in df.columns:
        raise ValueError(f"Column '{column}' not found")

    target = df[column] if column else df

    if strategy == "mean":
        val = target.mean() if column else df.mean(numeric_only=True)
    elif strategy == "median":
        val = target.median() if column else df.median(numeric_only=True)
    elif strategy == "constant":
        val = fill_value
    else:
        val = fill_value

    if column:
        df = df.copy()
        df[column] = df[column].fillna(val)
        return df
    return df.fillna(val)


def drop_duplicates(df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    subset = params.get("subset")
    keep = params.get("keep", "first")
    return df.drop_duplicates(subset=subset, keep=keep)


def cast_type(df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    column = params.get("column")
    target_type = params.get("target_type")
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found")

    df = df.copy()
    if target_type == "number":
        df[column] = pd.to_numeric(df[column], errors="coerce")
    elif target_type == "text":
        df[column] = df[column].astype(str)
    elif target_type == "date":
        df[column] = pd.to_datetime(df[column], errors="coerce")
    else:
        raise ValueError(f"Unsupported target type: {target_type}")
    return df


OPERATION_MAP = {
    "drop_na": drop_na,
    "fill_na": fill_na,
    "drop_duplicates": drop_duplicates,
    "cast_type": cast_type,
}


def apply_operations(df: pd.DataFrame, operations: list) -> pd.DataFrame:
    for op in operations:
        op_type = op.type
        params = op.params or {}
        fn = OPERATION_MAP.get(op_type)
        if fn is None:
            raise ValueError(f"Unknown operation: {op_type}")
        df = fn(df, params)
    return df

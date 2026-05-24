from fastapi import APIRouter, HTTPException, Query

import config
from models.schemas import CleanRequest, CleanOperation
from services.data_cleaning import apply_operations
from services.data_summary import summarize_dataframe
from services.file_parser import parse_file
from utils.file_storage import get_data_file
import pandas as pd

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


def _load_df(workspace_id: str, dataset_id: str) -> pd.DataFrame:
    meta = config.datasets_meta.get(dataset_id)
    if not meta or meta.get("workspace_id") != workspace_id:
        raise HTTPException(status_code=404, detail="Dataset not found")
    fpath = get_data_file(workspace_id, dataset_id)
    if not fpath:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    return parse_file(fpath)


def _save_df(df: pd.DataFrame, workspace_id: str, dataset_id: str):
    fpath = get_data_file(workspace_id, dataset_id)
    ext = fpath.suffix.lower()
    if ext == ".csv":
        df.to_csv(fpath, index=False, encoding="utf-8-sig")
    elif ext in {".xlsx", ".xls"}:
        df.to_excel(fpath, index=False, engine="openpyxl")


@router.post("/{dataset_id}/clean")
async def clean_dataset(
    dataset_id: str,
    request: CleanRequest,
    workspace_id: str = Query(...),
):
    df = _load_df(workspace_id, dataset_id)
    try:
        df = apply_operations(df, request.operations)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleaning failed: {str(e)}")

    _save_df(df, workspace_id, dataset_id)
    summary = summarize_dataframe(df)
    meta = config.datasets_meta.get(dataset_id, {})
    meta.update(summary)
    config.datasets_meta[dataset_id] = meta
    return summary


@router.get("/{dataset_id}/columns")
async def get_columns(dataset_id: str, workspace_id: str = Query(...)):
    df = _load_df(workspace_id, dataset_id)
    columns = []
    for col in df.columns:
        from services.data_summary import infer_column_type
        columns.append({"name": col, "type": infer_column_type(df[col])})
    return {"columns": columns}

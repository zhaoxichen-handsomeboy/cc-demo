import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import FileResponse

import config
from models.schemas import DatasetInfo
from services.file_parser import parse_file
from services.data_summary import summarize_dataframe, get_preview
from utils.file_storage import save_upload_file, get_data_file, delete_dataset_files
import pandas as pd

router = APIRouter(prefix="/api/datasets", tags=["datasets"])


def _load_df(workspace_id: str, dataset_id: str) -> pd.DataFrame:
    meta = config.datasets_meta.get(dataset_id)
    if not meta or meta.get("workspace_id") != workspace_id:
        raise HTTPException(status_code=404, detail="Dataset not found")
    fpath = get_data_file(workspace_id, dataset_id)
    if not fpath:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    return parse_file(fpath)


@router.post("/upload", response_model=DatasetInfo)
async def upload_dataset(
    file: UploadFile = File(...),
    workspace_id: str = Form(...),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    ext = file.filename.split(".")[-1].lower()
    if f".{ext}" not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}")

    content = await file.read()
    if len(content) > config.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    dataset_id = str(uuid.uuid4())
    fpath = save_upload_file(workspace_id, dataset_id, file.filename, content)

    try:
        df = parse_file(fpath, content)
    except Exception as e:
        delete_dataset_files(workspace_id, dataset_id)
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    summary = summarize_dataframe(df)
    info = DatasetInfo(
        id=dataset_id,
        name=file.filename,
        workspace_id=workspace_id,
        row_count=summary["row_count"],
        columns=summary["columns"],
        column_types=summary["column_types"],
        missing_stats=summary["missing_stats"],
        created_at=datetime.now().isoformat(),
    )
    config.datasets_meta[dataset_id] = info.model_dump()
    return info


@router.get("", response_model=List[DatasetInfo])
async def list_datasets(workspace_id: str = Query(...)):
    result = []
    for ds_id, meta in config.datasets_meta.items():
        if meta.get("workspace_id") == workspace_id:
            result.append(DatasetInfo(**meta))
    return result


@router.delete("/{dataset_id}")
async def delete_dataset(dataset_id: str, workspace_id: str = Query(...)):
    meta = config.datasets_meta.get(dataset_id)
    if not meta or meta.get("workspace_id") != workspace_id:
        raise HTTPException(status_code=404, detail="Dataset not found")
    delete_dataset_files(workspace_id, dataset_id)
    del config.datasets_meta[dataset_id]
    return {"message": "Deleted"}


@router.get("/{dataset_id}/preview")
async def preview_dataset(
    dataset_id: str,
    workspace_id: str = Query(...),
    limit: int = Query(100, ge=1, le=1000),
):
    df = _load_df(workspace_id, dataset_id)
    data = get_preview(df, limit)
    return {"data": data, "columns": list(df.columns)}


@router.get("/{dataset_id}/summary")
async def dataset_summary(dataset_id: str, workspace_id: str = Query(...)):
    df = _load_df(workspace_id, dataset_id)
    return summarize_dataframe(df)


@router.get("/{dataset_id}/export/csv")
async def export_csv(dataset_id: str, workspace_id: str = Query(...)):
    df = _load_df(workspace_id, dataset_id)
    meta = config.datasets_meta.get(dataset_id, {})
    filename = meta.get("name", "export").rsplit(".", 1)[0] + ".csv"
    export_path = get_data_file(workspace_id, dataset_id).parent / filename
    df.to_csv(export_path, index=False, encoding="utf-8-sig")
    return FileResponse(path=export_path, filename=filename, media_type="text/csv")


@router.get("/{dataset_id}/export/excel")
async def export_excel(dataset_id: str, workspace_id: str = Query(...)):
    df = _load_df(workspace_id, dataset_id)
    meta = config.datasets_meta.get(dataset_id, {})
    filename = meta.get("name", "export").rsplit(".", 1)[0] + ".xlsx"
    export_path = get_data_file(workspace_id, dataset_id).parent / filename
    df.to_excel(export_path, index=False, engine="openpyxl")
    return FileResponse(
        path=export_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

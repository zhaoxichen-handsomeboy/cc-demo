import os
import shutil
import uuid
from pathlib import Path
from typing import Optional

import config


def get_dataset_dir(workspace_id: str, dataset_id: str) -> Path:
    path = Path(config.UPLOAD_DIR) / workspace_id / dataset_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_upload_file(workspace_id: str, dataset_id: str, filename: str, content: bytes) -> Path:
    d = get_dataset_dir(workspace_id, dataset_id)
    ext = Path(filename).suffix.lower()
    target = d / f"data{ext}"
    with open(target, "wb") as f:
        f.write(content)
    return target


def get_data_file(workspace_id: str, dataset_id: str) -> Optional[Path]:
    d = get_dataset_dir(workspace_id, dataset_id)
    for ext in [".csv", ".xlsx", ".xls"]:
        candidate = d / f"data{ext}"
        if candidate.exists():
            return candidate
    return None


def delete_dataset_files(workspace_id: str, dataset_id: str) -> None:
    d = Path(config.UPLOAD_DIR) / workspace_id / dataset_id
    if d.exists():
        shutil.rmtree(d)

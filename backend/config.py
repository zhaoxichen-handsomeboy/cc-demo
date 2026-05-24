import os

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "uploads")
MAX_UPLOAD_SIZE = int(os.environ.get("MAX_UPLOAD_SIZE", 50 * 1024 * 1024))  # 50MB
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

# 内存缓存数据集元数据，Phase 1 无持久化
datasets_meta: dict = {}
workspaces_meta: dict = {}

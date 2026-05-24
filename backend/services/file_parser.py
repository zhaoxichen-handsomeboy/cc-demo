import io
import chardet
import pandas as pd
from pathlib import Path
from typing import Tuple


def detect_encoding(content: bytes) -> str:
    result = chardet.detect(content)
    encoding = result.get("encoding", "utf-8") or "utf-8"
    confidence = result.get("confidence", 0)
    if confidence < 0.5:
        return "utf-8"
    return encoding


def detect_delimiter(text: str) -> str:
    first_line = text.split("\n")[0] if text else ""
    delimiters = [",", "\t", ";", "|"]
    counts = {d: first_line.count(d) for d in delimiters}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else ","


def parse_csv(content: bytes) -> pd.DataFrame:
    encoding = detect_encoding(content)
    text = content.decode(encoding, errors="replace")
    delimiter = detect_delimiter(text)
    df = pd.read_csv(io.StringIO(text), delimiter=delimiter, encoding=encoding)
    return df


def parse_excel(content: bytes) -> pd.DataFrame:
    bio = io.BytesIO(content)
    df = pd.read_excel(bio, engine="openpyxl")
    return df


def parse_file(file_path: Path, content: bytes = None) -> pd.DataFrame:
    ext = file_path.suffix.lower()
    if content is None:
        content = file_path.read_bytes()
    if ext == ".csv":
        return parse_csv(content)
    elif ext in {".xlsx", ".xls"}:
        return parse_excel(content)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

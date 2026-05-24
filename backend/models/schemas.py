from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum


class DatasetInfo(BaseModel):
    id: str
    name: str
    workspace_id: str
    row_count: int
    columns: List[str]
    column_types: Dict[str, str]
    missing_stats: Dict[str, int]
    created_at: str


class CleanOperationType(str, Enum):
    drop_na = "drop_na"
    fill_na = "fill_na"
    drop_duplicates = "drop_duplicates"
    cast_type = "cast_type"


class CleanOperation(BaseModel):
    type: CleanOperationType
    params: Dict[str, Any] = {}


class CleanRequest(BaseModel):
    operations: List[CleanOperation]


class AggFunc(str, Enum):
    sum = "sum"
    mean = "mean"
    count = "count"
    max = "max"
    min = "min"


class ChartType(str, Enum):
    bar = "bar"
    line = "line"
    pie = "pie"


class ChartConfig(BaseModel):
    chart_type: ChartType
    x_field: str
    y_field: str
    agg_func: AggFunc
    group_by: Optional[str] = None


class ChartDataResponse(BaseModel):
    categories: List[str]
    series: List[Dict[str, Any]]

from fastapi import APIRouter, HTTPException, Query

import config
from models.schemas import ChartConfig, ChartDataResponse
from services.chart_data import generate_chart_data
from services.file_parser import parse_file
from utils.file_storage import get_data_file

router = APIRouter(prefix="/api/charts", tags=["charts"])


def _load_df(workspace_id: str, dataset_id: str):
    meta = config.datasets_meta.get(dataset_id)
    if not meta or meta.get("workspace_id") != workspace_id:
        raise HTTPException(status_code=404, detail="Dataset not found")
    fpath = get_data_file(workspace_id, dataset_id)
    if not fpath:
        raise HTTPException(status_code=404, detail="Dataset file not found")
    return parse_file(fpath)


@router.post("/{dataset_id}/data", response_model=ChartDataResponse)
async def chart_data(
    dataset_id: str,
    config_body: ChartConfig,
    workspace_id: str = Query(...),
):
    df = _load_df(workspace_id, dataset_id)
    try:
        result = generate_chart_data(
            df,
            chart_type=config_body.chart_type.value,
            x_field=config_body.x_field,
            y_field=config_body.y_field,
            agg_func=config_body.agg_func.value,
            group_by=config_body.group_by,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart generation failed: {str(e)}")

    return ChartDataResponse(**result)

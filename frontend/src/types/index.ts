export interface DatasetInfo {
  id: string
  name: string
  workspace_id: string
  row_count: number
  columns: string[]
  column_types: Record<string, string>
  missing_stats: Record<string, number>
  created_at: string
}

export type CleanOpType = 'drop_na' | 'fill_na' | 'drop_duplicates' | 'cast_type'

export interface CleanOperation {
  type: CleanOpType
  params: Record<string, any>
}

export type AggFunc = 'sum' | 'mean' | 'count' | 'max' | 'min'
export type ChartType = 'bar' | 'line' | 'pie'

export interface ChartConfig {
  chart_type: ChartType
  x_field: string
  y_field: string
  agg_func: AggFunc
  group_by?: string
}

export interface Workspace {
  id: string
  name: string
  created_at: string
}

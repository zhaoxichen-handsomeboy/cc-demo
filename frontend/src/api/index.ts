import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    const msg = err.response?.data?.detail || err.message || '请求失败'
    ElMessage.error(msg)
    return Promise.reject(err)
  }
)

export default api

export function uploadDataset(file: File, workspaceId: string) {
  const form = new FormData()
  form.append('file', file)
  form.append('workspace_id', workspaceId)
  return api.post('/datasets/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function listDatasets(workspaceId: string) {
  return api.get('/datasets', { params: { workspace_id: workspaceId } })
}

export function deleteDataset(datasetId: string, workspaceId: string) {
  return api.delete(`/datasets/${datasetId}`, { params: { workspace_id: workspaceId } })
}

export function previewDataset(datasetId: string, workspaceId: string, limit = 100) {
  return api.get(`/datasets/${datasetId}/preview`, { params: { workspace_id: workspaceId, limit } })
}

export function datasetSummary(datasetId: string, workspaceId: string) {
  return api.get(`/datasets/${datasetId}/summary`, { params: { workspace_id: workspaceId } })
}

export function cleanDataset(datasetId: string, workspaceId: string, operations: any[]) {
  return api.post(`/analysis/${datasetId}/clean`, { operations }, { params: { workspace_id: workspaceId } })
}

export function getColumns(datasetId: string, workspaceId: string) {
  return api.get(`/analysis/${datasetId}/columns`, { params: { workspace_id: workspaceId } })
}

export function getChartData(datasetId: string, workspaceId: string, config: any) {
  return api.post(`/charts/${datasetId}/data`, config, { params: { workspace_id: workspaceId } })
}

export function exportCsvUrl(datasetId: string, workspaceId: string) {
  return `/api/datasets/${datasetId}/export/csv?workspace_id=${workspaceId}`
}

export function exportExcelUrl(datasetId: string, workspaceId: string) {
  return `/api/datasets/${datasetId}/export/excel?workspace_id=${workspaceId}`
}

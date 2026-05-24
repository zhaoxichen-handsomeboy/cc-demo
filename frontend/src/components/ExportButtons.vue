<template>
  <el-space>
    <el-button type="primary" plain @click="exportCsv">
      <Download /> 导出 CSV
    </el-button>
    <el-button type="success" plain @click="exportExcel">
      <Download /> 导出 Excel
    </el-button>
  </el-space>
</template>

<script setup lang="ts">
import { Download } from '@element-plus/icons-vue'

const props = defineProps<{
  datasetId: string
  workspaceId: string
}>()

function exportCsv() {
  const url = `/api/datasets/${props.datasetId}/export/csv?workspace_id=${props.workspaceId}`
  window.open(url, '_blank')
}

function exportExcel() {
  const url = `/api/datasets/${props.datasetId}/export/excel?workspace_id=${props.workspaceId}`
  window.open(url, '_blank')
}
</script>

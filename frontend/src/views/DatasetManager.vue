<template>
  <el-container class="dataset-page">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-header">
        <el-button text size="small" @click="goHome">
          <el-icon><ArrowLeft /></el-icon>
          返回工作区
        </el-button>
      </div>
      <div class="workspace-title">
        <el-icon><OfficeBuilding /></el-icon>
        {{ workspaceStore.currentWorkspace?.name }}
      </div>
      <el-menu :default-active="$route.path" router>
        <el-menu-item :index="`/workspace/${id}/datasets`">
          <el-icon><Document /></el-icon>
          <span>数据集管理</span>
        </el-menu-item>
        <el-menu-item :index="`/workspace/${id}/analysis`">
          <el-icon><DataLine /></el-icon>
          <span>可视化分析</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-main>
      <el-row :gutter="24">
        <el-col :span="8">
          <el-card shadow="never">
            <template #header>
              <span>上传数据集</span>
            </template>
            <FileUploader @upload="handleUpload" />
          </el-card>

          <el-card shadow="never" style="margin-top: 16px">
            <template #header>
              <span>数据集列表</span>
            </template>
            <div v-loading="listLoading" style="min-height: 60px">
              <el-empty v-if="!datasetStore.datasets.length && !listLoading" description="暂无数据集" />
              <el-menu v-else-if="datasetStore.datasets.length" class="dataset-list">
              <el-menu-item
                v-for="ds in datasetStore.datasets"
                :key="ds.id"
                :class="{ active: datasetStore.currentDataset?.id === ds.id }"
                @click="selectDataset(ds)"
              >
                <el-icon><Document /></el-icon>
                <span>{{ ds.name }}</span>
                <el-button
                  type="danger"
                  text
                  size="small"
                  style="margin-left: auto"
                  @click.stop="removeDataset(ds.id)"
                >
                  <Delete />
                </el-button>
              </el-menu-item>
            </el-menu>
            </div>
          </el-card>
        </el-col>

        <el-col :span="16">
          <template v-if="datasetStore.currentDataset">
            <el-card shadow="never">
              <template #header>
                <div class="card-header">
                  <span>{{ datasetStore.currentDataset.name }}</span>
                  <ExportButtons
                    :dataset-id="datasetStore.currentDataset.id"
                    :workspace-id="id"
                  />
                </div>
              </template>

              <el-descriptions :column="3" border size="small">
                <el-descriptions-item label="行数">{{ datasetStore.currentDataset.row_count }}</el-descriptions-item>
                <el-descriptions-item label="列数">{{ datasetStore.currentDataset.columns.length }}</el-descriptions-item>
                <el-descriptions-item label="创建时间">
                  {{ new Date(datasetStore.currentDataset.created_at).toLocaleString('zh-CN') }}
                </el-descriptions-item>
              </el-descriptions>

              <el-divider />

              <h4>字段信息</h4>
              <el-table :data="fieldInfo" size="small" border style="margin-bottom: 16px">
                <el-table-column prop="name" label="字段名" />
                <el-table-column prop="type" label="推断类型">
                  <template #default="{ row }">
                    <el-tag :type="row.type === 'number' ? 'success' : row.type === 'date' ? 'warning' : 'info'" size="small">
                      {{ typeLabel(row.type) }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="missing" label="缺失值">
                  <template #default="{ row }">
                    {{ row.missing }} ({{ ((row.missing / datasetStore.currentDataset.row_count) * 100).toFixed(1) }}%)
                  </template>
                </el-table-column>
              </el-table>

              <DataPreviewTable
                :data="datasetStore.previewData"
                :columns="datasetStore.previewColumns"
                :loading="previewLoading"
                :limit="previewLimit"
                @update:limit="onPreviewLimitChange"
              />

              <DataCleaningPanel
                :columns="datasetStore.currentDataset.columns"
                :loading="cleanLoading"
                @apply="handleClean"
              />
            </el-card>
          </template>
          <el-empty v-else description="请选择一个数据集" />
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, DataLine, OfficeBuilding, Delete, ArrowLeft } from '@element-plus/icons-vue'
import { useWorkspaceStore } from '../stores/workspace'
import { useDatasetStore } from '../stores/dataset'
import FileUploader from '../components/FileUploader.vue'
import DataPreviewTable from '../components/DataPreviewTable.vue'
import DataCleaningPanel from '../components/DataCleaningPanel.vue'
import ExportButtons from '../components/ExportButtons.vue'
import {
  uploadDataset,
  listDatasets,
  deleteDataset,
  previewDataset,
  datasetSummary,
  cleanDataset,
} from '../api'
import type { DatasetInfo } from '../types'

const props = defineProps<{ id: string }>()
const router = useRouter()

function goHome() {
  router.push('/')
}

const workspaceStore = useWorkspaceStore()
const datasetStore = useDatasetStore()
const previewLoading = ref(false)
const cleanLoading = ref(false)
const listLoading = ref(false)
const previewLimit = ref(100)

const fieldInfo = computed(() => {
  const ds = datasetStore.currentDataset
  if (!ds) return []
  return ds.columns.map((col) => ({
    name: col,
    type: ds.column_types[col] || 'text',
    missing: ds.missing_stats[col] || 0,
  }))
})

function typeLabel(type: string) {
  const map: Record<string, string> = { number: '数值', text: '文本', date: '日期' }
  return map[type] || type
}

async function loadDatasets() {
  listLoading.value = true
  try {
    const res = await listDatasets(props.id)
    datasetStore.setDatasets(res.data)
  } finally {
    listLoading.value = false
  }
}

async function selectDataset(ds: DatasetInfo) {
  datasetStore.selectDataset(ds)
  previewLoading.value = true
  try {
    const [previewRes, summaryRes] = await Promise.all([
      previewDataset(ds.id, props.id, previewLimit.value),
      datasetSummary(ds.id, props.id),
    ])
    datasetStore.setPreview(previewRes.data.data, previewRes.data.columns)
    const meta = { ...ds, ...summaryRes.data }
    datasetStore.currentDataset = meta
  } finally {
    previewLoading.value = false
  }
}

async function handleUpload(file: File) {
  try {
    const res = await uploadDataset(file, props.id)
    datasetStore.addDataset(res.data)
    ElMessage.success('上传成功')
    await selectDataset(res.data)
  } catch {
    // error handled by interceptor
  }
}

async function removeDataset(datasetId: string) {
  try {
    await ElMessageBox.confirm('确定要删除该数据集吗？此操作不可撤销。', '确认删除', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await deleteDataset(datasetId, props.id)
    datasetStore.removeDataset(datasetId)
    ElMessage.success('已删除')
  } catch {
    // cancelled or error handled by interceptor
  }
}

async function reloadPreview() {
  const ds = datasetStore.currentDataset
  if (!ds) return
  previewLoading.value = true
  try {
    const previewRes = await previewDataset(ds.id, props.id, previewLimit.value)
    datasetStore.setPreview(previewRes.data.data, previewRes.data.columns)
  } finally {
    previewLoading.value = false
  }
}

function onPreviewLimitChange(val: number) {
  previewLimit.value = val
  if (datasetStore.currentDataset) {
    reloadPreview()
  }
}

async function handleClean(operations: any[]) {
  if (!datasetStore.currentDataset) return
  cleanLoading.value = true
  try {
    const res = await cleanDataset(datasetStore.currentDataset.id, props.id, operations)
    datasetStore.currentDataset!.row_count = res.data.row_count
    datasetStore.currentDataset!.column_types = res.data.column_types
    datasetStore.currentDataset!.missing_stats = res.data.missing_stats
    ElMessage.success('清洗完成')
    await selectDataset(datasetStore.currentDataset!)
  } finally {
    cleanLoading.value = false
  }
}

onMounted(loadDatasets)
watch(() => props.id, loadDatasets)
</script>

<style scoped>
.dataset-page {
  min-height: 100vh;
  background: #f5f7fa;
}
.sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}
.sidebar-header {
  padding: 8px 12px;
  border-bottom: 1px solid #e4e7ed;
}
.sidebar-header .el-button {
  color: #606266;
}
.workspace-title {
  padding: 16px;
  font-weight: bold;
  font-size: 16px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dataset-list .el-menu-item {
  display: flex;
  align-items: center;
}
.dataset-list .el-menu-item.active {
  background: #ecf5ff;
  color: #409eff;
}
h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #606266;
}
</style>

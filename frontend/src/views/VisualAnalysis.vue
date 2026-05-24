<template>
  <el-container class="analysis-page">
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
        <el-col :span="6">
          <el-card shadow="never">
            <template #header>
              <span>选择数据集</span>
            </template>
            <el-select
              v-model="selectedDatasetId"
              placeholder="选择数据集"
              style="width: 100%"
              @change="onDatasetChange"
            >
              <el-option
                v-for="ds in datasetStore.datasets"
                :key="ds.id"
                :label="ds.name"
                :value="ds.id"
              />
            </el-select>
          </el-card>

          <el-card v-if="currentDataset" shadow="never" style="margin-top: 16px">
            <template #header>
              <span>数据集信息</span>
            </template>
            <el-descriptions :column="1" size="small" border>
              <el-descriptions-item label="名称">{{ currentDataset.name }}</el-descriptions-item>
              <el-descriptions-item label="行数">{{ currentDataset.row_count }}</el-descriptions-item>
              <el-descriptions-item label="列数">{{ currentDataset.columns.length }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <ChartConfigPanel
            v-if="currentDataset"
            :columns="currentDataset.columns"
            :column-types="currentDataset.column_types"
            @generate="generateChart"
            @export-png="exportPng"
          />
        </el-col>

        <el-col :span="18">
          <el-card shadow="never">
            <template #header>
              <span>图表预览</span>
            </template>
            <ChartRenderer
              :chart-type="chartType"
              :categories="categories"
              :series="series"
              :loading="chartLoading"
              ref="chartRef"
            />
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, DataLine, OfficeBuilding, ArrowLeft } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useWorkspaceStore } from '../stores/workspace'
import { useDatasetStore } from '../stores/dataset'
import ChartConfigPanel from '../components/ChartConfigPanel.vue'
import ChartRenderer from '../components/ChartRenderer.vue'
import { listDatasets, getChartData } from '../api'
import type { ChartConfig, ChartType, DatasetInfo } from '../types'

const props = defineProps<{ id: string }>()
const router = useRouter()

function goHome() {
  router.push('/')
}

const workspaceStore = useWorkspaceStore()
const datasetStore = useDatasetStore()
const selectedDatasetId = ref('')
const chartLoading = ref(false)
const chartType = ref<ChartType>('bar')
const categories = ref<string[]>([])
const series = ref<any[]>([])
const chartRef = ref<any>(null)

const currentDataset = computed<DatasetInfo | null>(() =>
  datasetStore.datasets.find((d) => d.id === selectedDatasetId.value) || null
)

async function loadDatasets() {
  const res = await listDatasets(props.id)
  datasetStore.setDatasets(res.data)
}

function onDatasetChange() {
  const ds = datasetStore.datasets.find((d) => d.id === selectedDatasetId.value)
  if (ds) datasetStore.selectDataset(ds)
}

async function generateChart(config: ChartConfig) {
  if (!selectedDatasetId.value) {
    ElMessage.warning('请先选择数据集')
    return
  }
  chartLoading.value = true
  try {
    const res = await getChartData(selectedDatasetId.value, props.id, config)
    chartType.value = config.chart_type
    categories.value = res.data.categories
    series.value = res.data.series
  } catch {
    categories.value = []
    series.value = []
  } finally {
    chartLoading.value = false
  }
}

function exportPng() {
  if (chartRef.value) {
    const chart = chartRef.value.$el.querySelector('canvas')
    if (chart) {
      const url = chart.toDataURL('image/png')
      const a = document.createElement('a')
      a.href = url
      a.download = 'chart.png'
      a.click()
    }
  }
}

onMounted(loadDatasets)
watch(() => props.id, loadDatasets)
</script>

<style scoped>
.analysis-page {
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
</style>

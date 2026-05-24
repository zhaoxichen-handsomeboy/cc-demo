<template>
  <el-card shadow="never">
    <template #header>
      <span>图表配置</span>
    </template>

    <el-form label-width="80px" size="small">
      <el-form-item label="图表类型">
        <el-radio-group v-model="config.chart_type">
          <el-radio-button label="bar">柱状图</el-radio-button>
          <el-radio-button label="line">折线图</el-radio-button>
          <el-radio-button label="pie">饼图</el-radio-button>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="X 轴 / 维度">
        <el-select v-model="config.x_field" placeholder="选择字段" clearable>
          <el-option v-for="c in columns" :key="c" :label="c" :value="c" />
        </el-select>
      </el-form-item>

      <el-form-item label="Y 轴 / 指标">
        <el-select v-model="config.y_field" placeholder="选择字段" clearable>
          <el-option v-for="c in numericColumns" :key="c" :label="c" :value="c" />
        </el-select>
      </el-form-item>

      <el-form-item label="聚合方式">
        <el-select v-model="config.agg_func" placeholder="选择聚合">
          <el-option label="求和" value="sum" />
          <el-option label="平均" value="mean" />
          <el-option label="计数" value="count" />
          <el-option label="最大值" value="max" />
          <el-option label="最小值" value="min" />
        </el-select>
      </el-form-item>

      <el-form-item label="分组字段">
        <el-select v-model="config.group_by" placeholder="可选" clearable>
          <el-option v-for="c in columns" :key="c" :label="c" :value="c" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="emit('generate', { ...config })"
          >生成图表</el-button
        >
        <el-button @click="exportPng">导出 PNG</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import type { ChartConfig } from '../types'

const props = defineProps<{
  columns: string[]
  columnTypes: Record<string, string>
}>()

const emit = defineEmits<{
  (e: 'generate', config: ChartConfig): void
  (e: 'export-png'): void
}>()

const config = reactive<ChartConfig>({
  chart_type: 'bar',
  x_field: '',
  y_field: '',
  agg_func: 'sum',
  group_by: undefined,
})

const numericColumns = computed(() =>
  props.columns.filter((c) => props.columnTypes[c] === 'number')
)

function exportPng() {
  emit('export-png')
}
</script>

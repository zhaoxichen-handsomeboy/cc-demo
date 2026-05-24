<template>
  <div class="chart-box" v-loading="loading">
    <v-chart v-if="option" class="chart" :option="option" autoresize />
    <el-empty v-else description="请选择图表配置" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import type { ChartType } from '../types'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent,
])

const props = defineProps<{
  chartType: ChartType
  categories: string[]
  series: any[]
  loading?: boolean
}>()

const option = computed(() => {
  if (!props.categories.length && !props.series.length) return null

  const base = {
    tooltip: { trigger: props.chartType === 'pie' ? 'item' : 'axis' },
    legend: { bottom: 0 },
    grid: { left: '3%', right: '4%', bottom: '10%', containLabel: true },
  }

  if (props.chartType === 'pie') {
    return {
      ...base,
      series: [
        {
          type: 'pie',
          radius: ['40%', '70%'],
          data: props.categories.map((name, i) => ({
            name,
            value: props.series[0]?.data[i] ?? 0,
          })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        },
      ],
    }
  }

  return {
    ...base,
    xAxis: {
      type: 'category',
      data: props.categories,
      axisLabel: { rotate: props.categories.length > 10 ? 45 : 0 },
    },
    yAxis: { type: 'value' },
    series: props.series.map((s) => ({
      name: s.name,
      type: props.chartType,
      data: s.data,
      smooth: props.chartType === 'line',
    })),
  }
})
</script>

<style scoped>
.chart-box {
  width: 100%;
  height: 480px;
}
.chart {
  width: 100%;
  height: 100%;
}
</style>

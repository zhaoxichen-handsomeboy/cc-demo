<template>
  <div class="preview-table" v-loading="loading">
    <div class="table-header">
      <div class="table-header-left">
        <span>数据预览（前 {{ data.length }} 行）</span>
        <el-select
          v-model="currentLimit"
          size="small"
          style="width: 100px; margin-left: 12px"
          @change="onLimitChange"
        >
          <el-option :value="50" label="50 行" />
          <el-option :value="100" label="100 行" />
          <el-option :value="200" label="200 行" />
          <el-option :value="500" label="500 行" />
          <el-option :value="1000" label="1000 行" />
        </el-select>
      </div>
      <el-tag type="info" size="small">{{ columns.length }} 列</el-tag>
    </div>
    <el-table :data="data" height="400" border stripe size="small">
      <el-table-column
        v-for="col in columns"
        :key="col"
        :prop="col"
        :label="col"
        min-width="120"
        show-overflow-tooltip
      />
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  data: any[]
  columns: string[]
  loading?: boolean
  limit?: number
}>()

const emit = defineEmits<{
  (e: 'update:limit', val: number): void
}>()

const currentLimit = ref(props.limit ?? 100)

watch(() => props.limit, (val) => {
  if (val !== undefined) currentLimit.value = val
})

function onLimitChange(val: number) {
  emit('update:limit', val)
}
</script>

<style scoped>
.preview-table {
  margin-top: 16px;
}
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 500;
}
.table-header-left {
  display: flex;
  align-items: center;
}
</style>

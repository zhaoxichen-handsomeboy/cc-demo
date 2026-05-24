<template>
  <el-card class="cleaning-panel" shadow="never">
    <template #header>
      <div class="panel-header">
        <span>数据清洗</span>
        <el-button type="primary" size="small" @click="apply" :loading="loading"
          >应用操作</el-button
        >
      </div>
    </template>

    <div class="operations">
      <div
        v-for="(op, index) in operations"
        :key="index"
        class="operation-row"
      >
        <el-select v-model="op.type" placeholder="选择操作" size="small" style="width: 160px">
          <el-option label="删除空值" value="drop_na" />
          <el-option label="填充空值" value="fill_na" />
          <el-option label="删除重复行" value="drop_duplicates" />
          <el-option label="修改字段类型" value="cast_type" />
        </el-select>

        <template v-if="op.type === 'drop_na'">
          <el-select v-model="op.params.how" placeholder="方式" size="small" style="width: 100px">
            <el-option label="任意空值" value="any" />
            <el-option label="全部空值" value="all" />
          </el-select>
        </template>

        <template v-if="op.type === 'fill_na'">
          <el-select v-model="op.params.column" placeholder="选择列" size="small" style="width: 140px">
            <el-option v-for="c in columns" :key="c" :label="c" :value="c" />
          </el-select>
          <el-select v-model="op.params.strategy" placeholder="策略" size="small" style="width: 100px">
            <el-option label="均值" value="mean" />
            <el-option label="中位数" value="median" />
            <el-option label="常数" value="constant" />
          </el-select>
          <el-input
            v-if="op.params.strategy === 'constant'"
            v-model="op.params.fill_value"
            placeholder="填充值"
            size="small"
            style="width: 100px"
          />
        </template>

        <template v-if="op.type === 'cast_type'">
          <el-select v-model="op.params.column" placeholder="选择列" size="small" style="width: 140px">
            <el-option v-for="c in columns" :key="c" :label="c" :value="c" />
          </el-select>
          <el-select v-model="op.params.target_type" placeholder="目标类型" size="small" style="width: 100px">
            <el-option label="数值" value="number" />
            <el-option label="文本" value="text" />
            <el-option label="日期" value="date" />
          </el-select>
        </template>

        <el-button type="danger" text size="small" @click="remove(index)">
          <Delete />
        </el-button>
      </div>

      <div class="op-actions">
        <el-button type="primary" text @click="addOperation">
          <Plus /> 添加操作
        </el-button>
        <el-button
          v-if="operations.length > 0"
          type="danger"
          text
          size="small"
          @click="clearAll"
        >
          <Delete /> 清除所有
        </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { Delete, Plus } from '@element-plus/icons-vue'
import type { CleanOperation } from '../types'

const props = defineProps<{
  columns: string[]
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'apply', ops: CleanOperation[]): void
}>()

const operations = ref<CleanOperation[]>([])

function addOperation() {
  operations.value.push({
    type: 'drop_na',
    params: { how: 'any' },
  })
}

function remove(index: number) {
  operations.value.splice(index, 1)
}

async function clearAll() {
  try {
    await ElMessageBox.confirm('确定要清除所有清洗操作吗？', '确认', {
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消',
    })
    operations.value = []
  } catch {
    // cancelled
  }
}

function apply() {
  emit('apply', operations.value)
}
</script>

<style scoped>
.cleaning-panel {
  margin-top: 16px;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.op-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.operation-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
</style>

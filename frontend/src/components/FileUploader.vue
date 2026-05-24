<template>
  <el-upload
    drag
    action="#"
    :auto-upload="false"
    :on-change="handleChange"
    :show-file-list="false"
    accept=".csv,.xlsx,.xls"
    class="uploader"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      拖拽文件到此处，或 <em>点击上传</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        支持 CSV、Excel (.xlsx/.xls)，单个文件不超过 50MB
      </div>
    </template>
  </el-upload>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'

const emit = defineEmits<{
  (e: 'upload', file: File): void
}>()

function handleChange(uploadFile: any) {
  const raw = uploadFile.raw as File
  if (!raw) return
  emit('upload', raw)
}
</script>

<style scoped>
.uploader {
  width: 100%;
}
</style>

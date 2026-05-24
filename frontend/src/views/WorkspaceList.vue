<template>
  <el-container class="workspace-page">
    <el-header>
      <div class="header-content">
        <h2><ElIcon><DataAnalysis /></ElIcon> 数据分析与可视化平台</h2>
      </div>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="6" v-for="ws in workspaceStore.workspaces" :key="ws.id">
          <el-card class="workspace-card" shadow="hover" @click="enterWorkspace(ws)">
            <template #header>
              <div class="card-header">
                <span>{{ ws.name }}</span>
                <el-button v-if="ws.id !== 'default'" type="danger" text size="small" @click.stop="del(ws.id)"><Delete /></el-button>
              </div>
            </template>
            <p class="meta">创建时间: {{ formatDate(ws.created_at) }}</p>
            <el-button type="primary" @click.stop="enterWorkspace(ws)">进入工作区</el-button>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="workspace-card add-card" shadow="hover" @click="showDialog = true">
            <div class="add-icon"><Plus style="width: 48px; height: 48px;" /></div>
            <p>新建工作区</p>
          </el-card>
        </el-col>
      </el-row>
    </el-main>

    <el-dialog v-model="showDialog" title="新建工作区" width="400px">
      <el-input v-model="newName" placeholder="请输入工作区名称" @keyup.enter="confirmCreate" />
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmCreate">确定</el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useWorkspaceStore } from '../stores/workspace'
import { DataAnalysis, Delete, Plus } from '@element-plus/icons-vue'
import type { Workspace } from '../types'

const router = useRouter()
const workspaceStore = useWorkspaceStore()
const showDialog = ref(false)
const newName = ref('')

function confirmCreate() {
  if (!newName.value.trim()) return
  workspaceStore.createWorkspace(newName.value.trim())
  newName.value = ''
  showDialog.value = false
}

function del(id: string) {
  workspaceStore.deleteWorkspace(id)
}

function enterWorkspace(ws: Workspace) {
  workspaceStore.setCurrent(ws.id)
  router.push(`/workspace/${ws.id}/datasets`)
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('zh-CN')
}
</script>

<style scoped>
.workspace-page {
  min-height: 100vh;
  background: #f5f7fa;
}
.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  color: #303133;
}
.header-content h2 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}
.workspace-card {
  cursor: pointer;
  transition: transform 0.2s;
  margin-bottom: 20px;
}
.workspace-card:hover {
  transform: translateY(-4px);
}
.add-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 160px;
  color: #909399;
}
.add-icon {
  margin-bottom: 12px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.meta {
  color: #909399;
  font-size: 13px;
  margin-bottom: 16px;
}
</style>

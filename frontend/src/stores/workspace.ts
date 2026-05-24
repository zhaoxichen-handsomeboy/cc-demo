import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Workspace } from '../types'

export const useWorkspaceStore = defineStore('workspace', () => {
  const workspaces = ref<Workspace[]>([
    { id: 'default', name: '默认工作区', created_at: new Date().toISOString() }
  ])
  const currentWorkspaceId = ref<string>('default')

  const currentWorkspace = computed(() =>
    workspaces.value.find((w) => w.id === currentWorkspaceId.value)
  )

  function createWorkspace(name: string) {
    const ws: Workspace = {
      id: 'ws_' + Date.now(),
      name,
      created_at: new Date().toISOString(),
    }
    workspaces.value.push(ws)
    currentWorkspaceId.value = ws.id
  }

  function deleteWorkspace(id: string) {
    workspaces.value = workspaces.value.filter((w) => w.id !== id)
    if (currentWorkspaceId.value === id && workspaces.value.length > 0) {
      currentWorkspaceId.value = workspaces.value[0].id
    }
  }

  function setCurrent(id: string) {
    currentWorkspaceId.value = id
  }

  return { workspaces, currentWorkspaceId, currentWorkspace, createWorkspace, deleteWorkspace, setCurrent }
})

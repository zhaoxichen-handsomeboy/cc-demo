import { createRouter, createWebHistory } from 'vue-router'
import WorkspaceList from '../views/WorkspaceList.vue'
import DatasetManager from '../views/DatasetManager.vue'
import VisualAnalysis from '../views/VisualAnalysis.vue'

const routes = [
  { path: '/', name: 'Workspaces', component: WorkspaceList },
  { path: '/workspace/:id/datasets', name: 'Datasets', component: DatasetManager, props: true },
  { path: '/workspace/:id/analysis', name: 'Analysis', component: VisualAnalysis, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

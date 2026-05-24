import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DatasetInfo } from '../types'

export const useDatasetStore = defineStore('dataset', () => {
  const datasets = ref<DatasetInfo[]>([])
  const currentDataset = ref<DatasetInfo | null>(null)
  const previewData = ref<any[]>([])
  const previewColumns = ref<string[]>([])

  function setDatasets(list: DatasetInfo[]) {
    datasets.value = list
  }

  function addDataset(ds: DatasetInfo) {
    datasets.value.push(ds)
  }

  function removeDataset(id: string) {
    datasets.value = datasets.value.filter((d) => d.id !== id)
    if (currentDataset.value?.id === id) {
      currentDataset.value = null
    }
  }

  function selectDataset(ds: DatasetInfo | null) {
    currentDataset.value = ds
  }

  function setPreview(data: any[], columns: string[]) {
    previewData.value = data
    previewColumns.value = columns
  }

  return { datasets, currentDataset, previewData, previewColumns, setDatasets, addDataset, removeDataset, selectDataset, setPreview }
})

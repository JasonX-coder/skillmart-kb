import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const sidebarVisible = ref(true)
  const loading = ref(false)

  const toggleSidebar = () => {
    sidebarVisible.value = !sidebarVisible.value
  }

  const setLoading = (value: boolean) => {
    loading.value = value
  }

  return {
    sidebarVisible,
    loading,
    toggleSidebar,
    setLoading
  }
})

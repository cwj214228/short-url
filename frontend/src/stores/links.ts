import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios'

export const useLinksStore = defineStore('links', () => {
  const links = ref<any[]>([])
  const currentLink = ref<any>(null)
  const loading = ref(false)

  async function fetchLinks() {
    loading.value = true
    try {
      const response = await api.get('/links')
      links.value = response.data
    } finally {
      loading.value = false
    }
  }

  async function createLink(data: any) {
    const response = await api.post('/links', data)
    return response.data
  }

  async function updateLink(shortCode: string, data: any) {
    const response = await api.put(`/links/${shortCode}`, data)
    return response.data
  }

  async function deleteLink(shortCode: string) {
    await api.delete(`/links/${shortCode}`)
    links.value = links.value.filter(l => l.short_code !== shortCode)
  }

  async function getLink(shortCode: string) {
    const response = await api.get(`/links/${shortCode}`)
    currentLink.value = response.data
    return response.data
  }

  return { links, currentLink, loading, fetchLinks, createLink, updateLink, deleteLink, getLink }
})

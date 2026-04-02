<template>
  <div>
    <NavBar />
    <div class="max-w-5xl mx-auto py-8 px-4">
      <div class="flex items-center gap-4 mb-6">
        <router-link to="/links" class="text-gray-500 hover:text-gray-700">← 返回链接列表</router-link>
        <h1 class="text-2xl font-bold">链接统计</h1>
      </div>
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else>
        <div class="card p-6 mb-6">
          <div class="flex items-center gap-4 mb-4">
            <span class="font-mono text-xl text-primary-500">{{ shortCode }}</span>
            <span class="px-2 py-1 text-xs rounded" :class="link?.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
              {{ link?.is_active ? '活跃' : '停用' }}
            </span>
          </div>
          <p class="text-gray-500 text-sm mb-4">{{ link?.original_url }}</p>
          <p class="text-xs text-gray-400">创建时间: {{ new Date(link?.created_at).toLocaleString() }}</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">总点击</p>
            <p class="text-3xl font-bold">{{ summary.total_clicks }}</p>
          </div>
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">独立点击</p>
            <p class="text-3xl font-bold">{{ summary.unique_clicks }}</p>
          </div>
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">热门国家</p>
            <p class="text-xl font-bold">{{ topCountry }}</p>
          </div>
          <div class="card p-6">
            <p class="text-sm text-gray-500 mb-1">热门浏览器</p>
            <p class="text-xl font-bold">{{ topBrowser }}</p>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="card p-6">
            <h3 class="font-semibold mb-4">按国家</h3>
            <div class="space-y-2">
              <div v-for="(count, country) in summary.by_country" :key="country" class="flex justify-between">
                <span>{{ country }}</span>
                <span class="font-medium">{{ count }}</span>
              </div>
            </div>
          </div>
          <div class="card p-6">
            <h3 class="font-semibold mb-4">按设备</h3>
            <div class="space-y-2">
              <div v-for="(count, device) in summary.by_device" :key="device" class="flex justify-between">
                <span class="capitalize">{{ device }}</span>
                <span class="font-medium">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'
import api from '@/api/axios'

const route = useRoute()
const linksStore = useLinksStore()

const shortCode = route.params.shortCode as string
const link = ref<any>(null)
const summary = ref({ total_clicks: 0, unique_clicks: 0, by_country: {}, by_device: {}, by_browser: {} })
const loading = ref(false)

const topCountry = computed(() => {
  const countries = summary.value.by_country as Record<string, number>
  return Object.entries(countries).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'
})

const topBrowser = computed(() => {
  const browsers = summary.value.by_browser as Record<string, number>
  return Object.entries(browsers).sort((a, b) => b[1] - a[1])[0]?.[0] || 'N/A'
})

onMounted(async () => {
  loading.value = true
  try {
    link.value = await linksStore.getLink(shortCode)
    const response = await api.get(`/links/${shortCode}/stats`)
    summary.value = response.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

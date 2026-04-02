<template>
  <div>
    <NavBar />
    <div class="max-w-7xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">控制台</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="card p-6">
          <p class="text-sm text-gray-500 mb-1">链接总数</p>
          <p class="text-3xl font-bold text-primary-500">{{ stats.totalLinks }}</p>
        </div>
        <div class="card p-6">
          <p class="text-sm text-gray-500 mb-1">点击总数</p>
          <p class="text-3xl font-bold text-secondary-500">{{ stats.totalClicks }}</p>
        </div>
        <div class="card p-6">
          <p class="text-sm text-gray-500 mb-1">活跃链接</p>
          <p class="text-3xl font-bold text-green-500">{{ stats.activeLinks }}</p>
        </div>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">最近链接</h2>
        <div v-if="recentLinks.length === 0" class="text-center text-gray-500 py-8">
          还没有链接。<router-link to="/links/new" class="text-primary-500 hover:underline">创建一个</router-link>
        </div>
        <div v-else class="space-y-3">
          <div v-for="link in recentLinks" :key="link.id" class="flex items-center justify-between border-b dark:border-gray-700 pb-3">
            <div>
              <span class="font-mono text-primary-500">{{ link.short_code }}</span>
              <p class="text-sm text-gray-500 truncate max-w-md">{{ link.original_url }}</p>
            </div>
            <router-link :to="`/links/${link.short_code}/stats`" class="text-sm text-primary-500 hover:underline">查看统计</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'
import api from '@/api/axios'

const linksStore = useLinksStore()
const allStats = ref<any>(null)

const stats = computed(() => ({
  totalLinks: linksStore.links.length,
  totalClicks: allStats.value || 0,
  activeLinks: linksStore.links.filter(l => l.is_active).length
}))

const recentLinks = computed(() => linksStore.links.slice(0, 5))

onMounted(async () => {
  await linksStore.fetchLinks()
  try {
    let total = 0
    for (const link of linksStore.links) {
      const response = await api.get(`/links/${link.short_code}/stats`)
      total += response.data.total_clicks
    }
    allStats.value = total
  } catch {
    allStats.value = 0
  }
})
</script>

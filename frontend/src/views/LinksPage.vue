<template>
  <div>
    <NavBar />
    <div class="max-w-7xl mx-auto py-8 px-4">
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold">我的链接</h1>
        <router-link to="/links/new" class="btn-primary">创建新链接</router-link>
      </div>
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="links.length === 0" class="card p-12 text-center">
        <p class="text-gray-500 mb-4">你还没有创建任何链接</p>
        <router-link to="/links/new" class="btn-primary">创建你的第一个链接</router-link>
      </div>
      <div v-else class="space-y-4">
        <div v-for="link in links" :key="link.id" class="card p-4 flex items-center justify-between">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="font-mono text-primary-500">{{ link.domain }}/{{ link.short_code }}</span>
              <span v-if="link.is_custom" class="text-xs bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 px-2 py-0.5 rounded">自定义</span>
            </div>
            <p class="text-sm text-gray-500 truncate">{{ link.original_url }}</p>
            <p class="text-xs text-gray-400 mt-1">{{ new Date(link.created_at).toLocaleDateString('zh-CN') }}</p>
          </div>
          <div class="flex items-center gap-2 ml-4">
            <router-link :to="`/links/${link.short_code}/stats`" class="btn-secondary text-sm">统计</router-link>
            <router-link :to="`/links/${link.short_code}/edit`" class="btn-secondary text-sm">编辑</router-link>
            <button @click="handleDelete(link.short_code)" class="text-red-500 hover:text-red-700 text-sm">删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'

const linksStore = useLinksStore()
const links = linksStore.links
const loading = linksStore.loading

onMounted(() => {
  linksStore.fetchLinks()
})

async function handleDelete(shortCode: string) {
  if (confirm('确定要删除这个链接吗？')) {
    await linksStore.deleteLink(shortCode)
  }
}
</script>

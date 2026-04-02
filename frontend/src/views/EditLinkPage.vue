<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">编辑链接</h1>
      <div v-if="loading" class="text-center py-12">加载中...</div>
      <div v-else-if="!link" class="card p-6 text-center">
        <p class="text-gray-500">链接不存在</p>
        <router-link to="/links" class="btn-primary mt-4">返回链接列表</router-link>
      </div>
      <div v-else class="card p-6">
        <form @submit.prevent="handleUpdate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">短链接</label>
            <input :value="`${link.domain}/${link.short_code}`" disabled class="input-field bg-gray-100 dark:bg-gray-700" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">原始链接 *</label>
            <input v-model="form.original_url" type="url" required class="input-field" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">启用状态</label>
            <label class="flex items-center gap-2">
              <input v-model="form.is_active" type="checkbox" class="w-4 h-4" />
              <span>链接启用</span>
            </label>
          </div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <div class="flex gap-4">
            <button type="submit" class="btn-primary" :disabled="loading">保存更改</button>
            <router-link to="/links" class="btn-secondary">取消</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'

const route = useRoute()
const router = useRouter()
const linksStore = useLinksStore()

const link = ref<any>(null)
const form = ref({
  original_url: '',
  is_active: true
})
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  const shortCode = route.params.shortCode as string
  link.value = await linksStore.getLink(shortCode)
  form.value.original_url = link.value.original_url
  form.value.is_active = link.value.is_active
})

async function handleUpdate() {
  loading.value = true
  error.value = ''
  try {
    await linksStore.updateLink(link.value.short_code, form.value)
    router.push('/links')
  } catch (e: any) {
    error.value = e.response?.data?.detail || '更新链接失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">创建新链接</h1>
      <div class="card p-6">
        <form @submit.prevent="handleCreate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">原始链接 *</label>
            <input v-model="form.original_url" type="url" required class="input-field" placeholder="https://example.com/very/long/url" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">自定义别名（可选）</label>
            <input v-model="form.custom_alias" class="input-field" placeholder="my-custom-link" />
            <p class="text-xs text-gray-500 mt-1">3-50个字符，只能包含字母、数字、连字符和下划线</p>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">标签（可选）</label>
            <input v-model="tagsInput" class="input-field" placeholder="标签1, 标签2, 标签3" />
          </div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <div class="flex gap-4">
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? '创建中...' : '创建链接' }}
            </button>
            <router-link to="/links" class="btn-secondary">取消</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import { useLinksStore } from '@/stores/links'

const router = useRouter()
const linksStore = useLinksStore()

const form = ref({
  original_url: '',
  custom_alias: ''
})
const tagsInput = ref('')
const error = ref('')
const loading = ref(false)

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const tags = tagsInput.value ? tagsInput.value.split(',').map(t => t.trim()).filter(Boolean) : []
    await linksStore.createLink({ ...form.value, tags })
    router.push('/links')
  } catch (e: any) {
    error.value = e.response?.data?.detail || '创建链接失败'
  } finally {
    loading.value = false
  }
}
</script>

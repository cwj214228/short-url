<template>
  <div>
    <NavBar />
    <div class="max-w-4xl mx-auto py-20 px-4">
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
          缩短你的链接
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">
          几秒钟内创建短小精悍的链接
        </p>
      </div>
      <div class="card p-6">
        <form @submit.prevent="handleCreate" class="flex gap-4">
          <input
            v-model="url"
            type="url"
            placeholder="在此粘贴你的长链接..."
            required
            class="input-field flex-1"
          />
          <button type="submit" class="btn-primary whitespace-nowrap" :disabled="loading">
            {{ loading ? '创建中...' : '生成短链接' }}
          </button>
        </form>
        <div v-if="shortUrl" class="mt-6 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">你的短链接：</p>
          <div class="flex items-center gap-4">
            <input :value="shortUrl" readonly class="input-field flex-1" ref="copyInput" />
            <button @click="copyToClipboard" class="btn-secondary">复制</button>
          </div>
          <div v-if="copied" class="mt-2 text-green-500 text-sm">复制成功！</div>
        </div>
        <div v-if="error" class="mt-4 text-red-500">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import NavBar from '@/components/NavBar.vue'
import api from '@/api/axios'

const url = ref('')
const shortUrl = ref('')
const error = ref('')
const loading = ref(false)
const copied = ref(false)
const copyInput = ref<HTMLInputElement | null>(null)

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.post('/links', { original_url: url.value })
    shortUrl.value = `${response.data.domain}/${response.data.short_code}`
  } catch (e: any) {
    error.value = e.response?.data?.detail || '创建短链接失败'
  } finally {
    loading.value = false
  }
}

function copyToClipboard() {
  if (copyInput.value) {
    copyInput.value.select()
    document.execCommand('copy')
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  }
}
</script>

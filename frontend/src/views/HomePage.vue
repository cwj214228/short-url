<template>
  <div>
    <NavBar />
    <div class="max-w-4xl mx-auto py-20 px-4">
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold mb-4 bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
          Shorten Your Links
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">
          Create short, memorable links in seconds
        </p>
      </div>
      <div class="card p-6">
        <form @submit.prevent="handleCreate" class="flex gap-4">
          <input
            v-model="url"
            type="url"
            placeholder="Paste your long URL here..."
            required
            class="input-field flex-1"
          />
          <button type="submit" class="btn-primary whitespace-nowrap" :disabled="loading">
            {{ loading ? 'Creating...' : 'Shorten' }}
          </button>
        </form>
        <div v-if="shortUrl" class="mt-6 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Your short URL:</p>
          <div class="flex items-center gap-4">
            <input :value="shortUrl" readonly class="input-field flex-1" ref="copyInput" />
            <button @click="copyToClipboard" class="btn-secondary">Copy</button>
          </div>
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
const copyInput = ref<HTMLInputElement | null>(null)

async function handleCreate() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.post('/links', { original_url: url.value })
    shortUrl.value = `${response.data.domain}/${response.data.short_code}`
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to create short URL'
  } finally {
    loading.value = false
  }
}

function copyToClipboard() {
  if (copyInput.value) {
    copyInput.value.select()
    document.execCommand('copy')
  }
}
</script>

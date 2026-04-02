<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Create New Link</h1>
      <div class="card p-6">
        <form @submit.prevent="handleCreate" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Original URL *</label>
            <input v-model="form.original_url" type="url" required class="input-field" placeholder="https://example.com/very/long/url" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Custom Alias (optional)</label>
            <input v-model="form.custom_alias" class="input-field" placeholder="my-custom-link" />
            <p class="text-xs text-gray-500 mt-1">3-50 characters, letters, numbers, hyphens and underscores only</p>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Tags (optional)</label>
            <input v-model="tagsInput" class="input-field" placeholder="tag1, tag2, tag3" />
          </div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <div class="flex gap-4">
            <button type="submit" class="btn-primary" :disabled="loading">
              {{ loading ? 'Creating...' : 'Create Link' }}
            </button>
            <router-link to="/links" class="btn-secondary">Cancel</router-link>
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
    error.value = e.response?.data?.detail || 'Failed to create link'
  } finally {
    loading.value = false
  }
}
</script>

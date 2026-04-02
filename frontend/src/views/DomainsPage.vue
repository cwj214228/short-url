<template>
  <div>
    <NavBar />
    <div class="max-w-4xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Custom Domains</h1>
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">Add New Domain</h2>
        <form @submit.prevent="handleAdd" class="flex gap-4">
          <input v-model="newDomain" type="text" required class="input-field flex-1" placeholder="example.com" />
          <button type="submit" class="btn-primary" :disabled="loading">Add Domain</button>
        </form>
        <p class="text-sm text-gray-500 mt-2">
          After adding, you'll need to add a DNS TXT record with the verification token to verify ownership.
        </p>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">Your Domains</h2>
        <div v-if="domains.length === 0" class="text-center text-gray-500 py-8">
          No domains added yet.
        </div>
        <div v-else class="space-y-4">
          <div v-for="domain in domains" :key="domain.id" class="flex items-center justify-between border-b dark:border-gray-700 pb-4">
            <div>
              <span class="font-medium">{{ domain.domain }}</span>
              <span v-if="domain.verified_at" class="ml-2 text-xs text-green-500">Verified</span>
              <span v-else class="ml-2 text-xs text-yellow-500">Pending Verification</span>
              <p v-if="!domain.verified_at" class="text-xs text-gray-400 mt-1">Token: {{ domain.verification_token }}</p>
            </div>
            <button @click="handleDelete(domain.domain)" class="text-red-500 hover:text-red-700">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import api from '@/api/axios'

const domains = ref<any[]>([])
const newDomain = ref('')
const loading = ref(false)

async function fetchDomains() {
  const response = await api.get('/domains')
  domains.value = response.data
}

async function handleAdd() {
  loading.value = true
  try {
    await api.post('/domains', { domain: newDomain.value })
    newDomain.value = ''
    await fetchDomains()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleDelete(domain: string) {
  if (confirm(`Delete domain ${domain}?`)) {
    await api.delete(`/domains/${domain}`)
    await fetchDomains()
  }
}

onMounted(fetchDomains)
</script>

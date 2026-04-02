<template>
  <div>
    <NavBar />
    <div class="max-w-4xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">自定义域名</h1>
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">添加新域名</h2>
        <form @submit.prevent="handleAdd" class="flex gap-4">
          <input v-model="newDomain" type="text" required class="input-field flex-1" placeholder="example.com" />
          <button type="submit" class="btn-primary" :disabled="loading">添加域名</button>
        </form>
        <p class="text-sm text-gray-500 mt-2">
          添加后，您需要添加 DNS TXT 记录和验证码来验证域名所有权。
        </p>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">您的域名</h2>
        <div v-if="domains.length === 0" class="text-center text-gray-500 py-8">
          暂无域名。
        </div>
        <div v-else class="space-y-4">
          <div v-for="domain in domains" :key="domain.id" class="flex items-center justify-between border-b dark:border-gray-700 pb-4">
            <div>
              <span class="font-medium">{{ domain.domain }}</span>
              <span v-if="domain.verified_at" class="ml-2 text-xs text-green-500">已验证</span>
              <span v-else class="ml-2 text-xs text-yellow-500">待验证</span>
              <p v-if="!domain.verified_at" class="text-xs text-gray-400 mt-1">令牌: {{ domain.verification_token }}</p>
            </div>
            <button @click="handleDelete(domain.domain)" class="text-red-500 hover:text-red-700">删除</button>
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
  if (confirm(`确定要删除域名 ${domain} 吗？`)) {
    await api.delete(`/domains/${domain}`)
    await fetchDomains()
  }
}

onMounted(fetchDomains)
</script>

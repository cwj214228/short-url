<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-secondary-500">
    <div class="card p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">创建账号</h1>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">邮箱</label>
          <input v-model="email" type="email" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">用户名</label>
          <input v-model="username" type="text" required class="input-field" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">密码</label>
          <input v-model="password" type="password" required class="input-field" />
        </div>
        <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
        <button type="submit" class="btn-primary w-full" :disabled="loading">
          {{ loading ? '创建中...' : '注册' }}
        </button>
      </form>
      <p class="mt-4 text-center text-sm">
        已有账号？ <router-link to="/login" class="text-primary-500 hover:underline">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await authStore.register(email.value, username.value, password.value)
    router.push('/dashboard')
  } catch (e: any) {
    error.value = e.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-bold bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent">
            短链接
          </router-link>
          <div v-if="isAuthenticated" class="ml-10 flex space-x-4">
            <router-link to="/dashboard" class="nav-link">控制台</router-link>
            <router-link to="/links" class="nav-link">链接</router-link>
            <router-link to="/domains" class="nav-link">域名</router-link>
          </div>
        </div>
        <div class="flex items-center">
          <template v-if="isAuthenticated">
            <router-link to="/settings" class="nav-link mr-4">设置</router-link>
            <button @click="handleLogout" class="btn-secondary">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link">登录</router-link>
            <router-link to="/register" class="btn-primary ml-4">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-500 transition-colors;
}
.router-link-active.nav-link {
  @apply text-primary-500;
}
</style>

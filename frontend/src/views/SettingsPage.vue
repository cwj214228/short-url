<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">设置</h1>
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">个人资料</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">邮箱</label>
            <input :value="user?.email" type="email" disabled class="input-field bg-gray-100 dark:bg-gray-700" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">用户名</label>
            <input v-model="form.username" type="text" class="input-field" />
          </div>
          <div v-if="profileMessage" class="text-green-500 text-sm">{{ profileMessage }}</div>
          <div v-if="profileError" class="text-red-500 text-sm">{{ profileError }}</div>
          <button @click="handleUpdateProfile" class="btn-primary" :disabled="loading">保存更改</button>
        </div>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">修改密码</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">新密码</label>
            <input v-model="form.password" type="password" class="input-field" placeholder="输入新密码" />
          </div>
          <div v-if="passwordMessage" class="text-green-500 text-sm">{{ passwordMessage }}</div>
          <div v-if="passwordError" class="text-red-500 text-sm">{{ passwordError }}</div>
          <button @click="handleChangePassword" class="btn-primary" :disabled="loading || !form.password">更新密码</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const user = authStore.user
const form = reactive({ username: '', password: '' })
const profileMessage = ref('')
const profileError = ref('')
const passwordMessage = ref('')
const passwordError = ref('')
const loading = ref(false)

onMounted(async () => {
  await authStore.fetchUser()
  form.username = authStore.user?.username || ''
})

async function handleUpdateProfile() {
  loading.value = true
  profileError.value = ''
  profileMessage.value = ''
  try {
    await authStore.updateProfile({ username: form.username })
    profileMessage.value = '个人资料更新成功'
  } catch (e: any) {
    profileError.value = e.response?.data?.detail || '更新个人资料失败'
  } finally {
    loading.value = false
  }
}

async function handleChangePassword() {
  if (!form.password) return
  loading.value = true
  passwordError.value = ''
  passwordMessage.value = ''
  try {
    await authStore.updatePassword({ password: form.password })
    passwordMessage.value = '密码更新成功'
    form.password = ''
  } catch (e: any) {
    passwordError.value = e.response?.data?.detail || '更新密码失败'
  } finally {
    loading.value = false
  }
}
</script>

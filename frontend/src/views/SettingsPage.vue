<template>
  <div>
    <NavBar />
    <div class="max-w-2xl mx-auto py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Settings</h1>
      <div class="card p-6 mb-6">
        <h2 class="text-lg font-semibold mb-4">Profile</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Email</label>
            <input v-model="user.email" type="email" disabled class="input-field bg-gray-100 dark:bg-gray-700" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Username</label>
            <input v-model="form.username" type="text" class="input-field" />
          </div>
          <button @click="handleUpdateProfile" class="btn-primary" :disabled="loading">Save Changes</button>
        </div>
      </div>
      <div class="card p-6">
        <h2 class="text-lg font-semibold mb-4">Change Password</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">New Password</label>
            <input v-model="form.password" type="password" class="input-field" />
          </div>
          <div v-if="message" class="text-green-500 text-sm">{{ message }}</div>
          <div v-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <button @click="handleChangePassword" class="btn-primary" :disabled="loading">Update Password</button>
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

const user = ref<any>(null)
const form = reactive({ username: '', password: '' })
const message = ref('')
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  await authStore.fetchUser()
  user.value = authStore.user
  form.username = user.value?.username || ''
})

async function handleUpdateProfile() {
  loading.value = true
  error.value = ''
  try {
    await authStore.updateProfile({ username: form.username })
    message.value = 'Profile updated successfully'
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to update profile'
  } finally {
    loading.value = false
  }
}

async function handleChangePassword() {
  loading.value = true
  error.value = ''
  message.value = ''
  try {
    await authStore.updatePassword({ password: form.password })
    message.value = 'Password updated successfully'
    form.password = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to update password'
  } finally {
    loading.value = false
  }
}
</script>

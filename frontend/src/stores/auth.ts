import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<any>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    const response = await api.post('/auth/login', { email, password })
    token.value = response.data.access_token
    localStorage.setItem('token', response.data.access_token)
    await fetchUser()
  }

  async function register(email: string, username: string, password: string) {
    await api.post('/auth/register', { email, username, password })
    await login(email, password)
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch {
      logout()
    }
  }

  async function updateProfile(data: { username?: string }) {
    const response = await api.put('/auth/me', data)
    user.value = response.data
    return response.data
  }

  async function updatePassword(data: { password: string }) {
    await api.put('/auth/me', data)
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  if (token.value && !user.value) {
    fetchUser()
  }

  return { token, user, isAuthenticated, login, register, logout, fetchUser, updateProfile, updatePassword }
})

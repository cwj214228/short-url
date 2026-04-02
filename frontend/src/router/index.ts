import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginPage.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterPage.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links',
      name: 'links',
      component: () => import('@/views/LinksPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links/new',
      name: 'create-link',
      component: () => import('@/views/CreateLinkPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links/:shortCode/edit',
      name: 'edit-link',
      component: () => import('@/views/EditLinkPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/links/:shortCode/stats',
      name: 'link-stats',
      component: () => import('@/views/LinkStatsPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/domains',
      name: 'domains',
      component: () => import('@/views/DomainsPage.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/SettingsPage.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue')
  },
  {
    path: '/layout',
    name: 'Layout',
    component: () => import('@/components/layout/AppLayout.vue'),
    children: [
      {
        path: '',
        redirect: '/knowledge/home'
      },
      {
        path: '/knowledge',
        name: 'KnowledgeList',
        component: () => import('@/views/knowledge/KnowledgeList.vue')
      },
      {
        path: '/knowledge/home',
        name: 'KnowledgeHome',
        component: () => import('@/views/knowledge/KnowledgeHome.vue')
      },
      {
        path: '/knowledge/:id',
        name: 'KnowledgeDetail',
        component: () => import('@/views/knowledge/KnowledgeDetail.vue')
      },
      {
        path: '/knowledge/edit/:id?',
        name: 'KnowledgeEdit',
        component: () => import('@/views/knowledge/KnowledgeEdit.vue')
      },
      {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/views/user/Profile.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

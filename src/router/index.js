import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home/Home.vue'
import Now from '../views/Now/index.vue'
import Backtest from '../views/Backtest/index.vue'
import Forecast from '../views/Forecast/index.vue'
import Policy from '../views/Policy/index.vue'
import Talk from '../views/Talk/index.vue'
import AI from '../views/AI/index.vue'
import StockDetail from '../views/StockDetail/index.vue'
import Login from '../views/Login/index.vue'
import Register from '@/views/Register/index.vue'
import Intalk from '../views/Talk/Intalk.vue'

const routes = [
  { path: '/', component: Home },
  {
    path: '/now',
    name: 'Now',
    component: () => import('../views/Now/index.vue')
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: () => import('@/views/Recommend/index.vue')
  },
  {
    path: '/backtest',
    name: 'Backtest',
    component: Backtest
  },
  {
    path: '/forecast',
    name: 'forecast',
    component: () => import('@/views/Forecast/index.vue')
  },
  {
    path: '/policy',
    name: 'Policy',
    component: Policy
  },
  {
    path: '/talk',
    name: 'Talk',
    component: Talk
  },
  {
    path: '/talk/:code',
    name: 'talk',
    component: () => import('@/views/Talk/index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ai',
    name: 'AI',
    component: AI
  },
  {
    path: '/stock/:code',
    name: 'StockDetail',
    component: () => import('@/views/StockDetail/index.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '用户注册'
    }
  },
  {
    path: '/intalk',
    name: 'intalk',
    component: () => import('@/views/Talk/Intalk.vue')
  },
  {
    path: '/infore',
    name: 'infore',
    component: () => import('@/views/Forecast/Infore.vue')
  },
  {
    path: '/investigation',
    name: 'Investigation',
    component: () => import('@/views/Investigation/index.vue')
  },
  {
    path: '/buy',
    name: 'Buy',
    component: () => import('@/views/buy/index.vue')
  },
  {
    path: '/sell',
    name: 'Sell',
    component: () => import('@/views/sell/index.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
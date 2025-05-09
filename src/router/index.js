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
import Register from '../views/Register/index.vue'

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
    name: 'Forecast',
    component: Forecast
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
    path: '/ai',
    name: 'AI',
    component: AI
  },
  {
    path: '/stock/:code',
    name: 'stock',
    component: () => import('@/views/StockDetail/index.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },,
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
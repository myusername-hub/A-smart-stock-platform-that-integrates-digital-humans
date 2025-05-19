<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <div class="logo">
      <router-link to="/">广财股票量化交易平台</router-link>
    </div>
    
    <div class="nav-links">
      <!-- 未登录状态 -->
      <template v-if="!authStore.loggedIn">
        <router-link to="/login">登录</router-link>
        <router-link to="/register">注册</router-link>
      </template>
      
      <!-- 登录后状态 -->
      <template v-else>
        <router-link to="/dashboard">控制台</router-link>
        <router-link to="/profile">个人中心</router-link>
        <a @click="handleLogout" class="logout-btn">退出登录</a>
      </template>
    </div>
  </nav>
</template>

<style scoped lang="scss">
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: rgba(26, 31, 53, 0.95);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  z-index: 100;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .logo {
    a {
      color: #e6f1ff;
      text-decoration: none;
      font-size: 1.2rem;
      font-weight: 600;
    }
  }

  .nav-links {
    display: flex;
    gap: 1.5rem;
    align-items: center;

    a {
      color: #e6f1ff;
      text-decoration: none;
      font-size: 0.9rem;
      transition: color 0.3s ease;
      
      &:hover {
        color: #64b3f4;
      }

      &.router-link-active {
        color: #64b3f4;
      }
    }

    .logout-btn {
      cursor: pointer;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.1);
      
      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }
    }
  }
}
</style>

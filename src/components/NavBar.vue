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
    <div class="nav-brand">股票量化交易平台</div>
    <div class="nav-links">
      <template v-if="authStore.user">
        <span class="welcome">欢迎您，{{ authStore.user.username }}</span>
        <a @click="handleLogout">退出登录</a>
      </template>
      <template v-else>
        <router-link to="/login">登录</router-link>
        <router-link to="/register">注册</router-link>
      </template>
    </div>
  </nav>
</template>

<style scoped lang="scss">
.navbar {
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);

  .nav-brand {
    color: #e6f1ff;
    font-size: 1.2rem;
  }

  .nav-links {
    display: flex;
    gap: 20px;
    align-items: center;

    a {
      color: #64b3f4;
      text-decoration: none;
      cursor: pointer;
      
      &:hover {
        color: #a8d5f9;
      }
    }

    .welcome {
      color: #e6f1ff;
    }
  }
}
</style>

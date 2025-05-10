<script>
import { ref, onMounted } from 'vue'

export default {
  setup() {
    const loggedInUser = ref(null)

    onMounted(() => {
      // 从 localStorage 获取登录的用户名
      loggedInUser.value = localStorage.getItem('loggedInUser')
    })

    const handleLogout = () => {
      // 清除登录状态
      localStorage.removeItem('loggedInUser')
      loggedInUser.value = null
    }

    return {
      loggedInUser,
      handleLogout
    }
  }
}
</script>

<template>
  <div class="home-container">
    <div v-if="loggedInUser">
      <p>欢迎您，{{ loggedInUser }}</p>
      <button @click="handleLogout">退出登录</button>
    </div>
    <div v-else>
      <button @click="$router.push('/login')">登录</button>
      <button @click="$router.push('/register')">注册</button>
    </div>
  </div>
</template>

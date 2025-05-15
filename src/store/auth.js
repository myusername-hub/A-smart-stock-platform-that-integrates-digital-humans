import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token') || null)

  // 模拟用户数据库
  const users = {
    // 可以添加一些测试用户
  }

  const register = async (username, password) => {
    if (users[username]) {
      throw new Error('用户已存在')
    }
    users[username] = { username, password }
    return { username }
  }

  const login = async (username, password) => {
    const foundUser = users[username]
    if (!foundUser) {
      throw new Error('用户不存在')
    }
    if (foundUser.password !== password) {
      throw new Error('密码错误')
    }
    
    user.value = { username }
    token.value = 'mock_token_' + username
    
    // 保存登录状态
    localStorage.setItem('user', JSON.stringify(user.value))
    localStorage.setItem('token', token.value)
    
    return { username }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  const isLoggedIn = computed(() => !!user.value)
  const username = computed(() => user.value?.username || '')

  return {
    user,
    token,
    register,
    login,
    logout,
    isLoggedIn,
    username
  }
})

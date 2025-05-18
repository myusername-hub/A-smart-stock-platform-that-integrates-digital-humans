import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token')
  }),

  actions: {
    async login(username, password) {
      // 获取本地存储的用户列表
      const users = JSON.parse(localStorage.getItem('users') || '[]')
      const user = users.find(u => u.username === username)
      
      if (!user || user.password !== password) {
        throw new Error('用户名或密码错误')
      }

      this.user = { username }
      this.token = `token_${Date.now()}`
      
      // 保存登录状态
      localStorage.setItem('token', this.token)
      localStorage.setItem('currentUser', JSON.stringify(this.user))
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('currentUser')
    }
  }
})

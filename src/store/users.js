import { defineStore } from 'pinia'

export const useUsersStore = defineStore('users', {
  state: () => ({
    registeredUsers: []
  }),

  actions: {
    // 初始化方法，从localStorage加载数据
    initStore() {
      const stored = localStorage.getItem('registeredUsers')
      if (stored) {
        this.registeredUsers = JSON.parse(stored)
        console.log('加载存储的用户数据:', this.registeredUsers)
      }
    },

    async addUser(username, password) {
      this.initStore() // 确保数据同步
      try {
        if (this.isUserExist(username)) {
          console.log('用户已存在:', username) // 调试日志
          throw new Error('用户已存在')
        }
        
        const newUser = {
          username,
          password,
          createTime: new Date().toISOString()
        }
        
        this.registeredUsers.push(newUser)
        this.saveToStorage()
        console.log('注册成功，当前用户列表:', this.registeredUsers) // 调试日志
        return true
      } catch (error) {
        console.error('添加用户失败:', error)
        throw error
      }
    },
    
    saveToStorage() {
      const data = JSON.stringify(this.registeredUsers)
      localStorage.setItem('registeredUsers', data)
      console.log('保存到localStorage:', data) // 调试日志
    },
    
    isUserExist(username) {
      this.initStore() // 确保数据同步
      return this.registeredUsers.some(user => user.username === username)
    },
    
    getUser(username) {
      const user = this.registeredUsers.find(user => user.username === username)
      console.log('获取用户信息:', username, user) // 调试日志
      return user
    },
    
    async validateLogin(username, password) {
      this.initStore() // 确保数据同步
      
      console.log('验证登录:', {username, users: this.registeredUsers})
      const user = this.registeredUsers.find(u => u.username === username)
      
      if (!user) {
        throw new Error('账号不存在，请先注册')
      }
      
      if (user.password !== password) {
        throw new Error('密码错误，请重试')
      }
      
      return true
    },

    // 添加获取所有用户的方法，用于调试
    getAllUsers() {
      return this.registeredUsers
    }
  }
})

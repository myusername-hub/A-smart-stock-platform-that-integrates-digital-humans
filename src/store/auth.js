import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  }),

  getters: {
    isLoggedIn: (state) => !!state.user,
    currentUser: (state) => state.user?.username
  },

  actions: {
    login(username) {
      this.user = { username }
      localStorage.setItem('user', JSON.stringify({ username }))
    },

    logout() {
      this.user = null
      localStorage.removeItem('user')
    }
  }
})

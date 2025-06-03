import axios from 'axios'
import { encryptPassword } from '@/utils/crypto'

const API_URL = 'http://your-api-url/api'

export const authService = {
  async login(username, password) {
    const encryptedPassword = encryptPassword(password)
    const response = await axios.post(`${API_URL}/login`, {
      username,
      password: encryptedPassword
    })
    if (response.data.token) {
      localStorage.setItem('token', response.data.token)
    }
    return response.data
  },

  async register(username, password) {
    const encryptedPassword = encryptPassword(password)
    const response = await axios.post(`${API_URL}/register`, {
      username,
      password: encryptedPassword
    })
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
  }
}

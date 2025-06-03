import axios from 'axios'

const VITE_API_URL = 'http://localhost:5000'
const MAX_RETRIES = 3
const RETRY_DELAY = 1000

const api = axios.create({
    baseURL: VITE_API_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

export const fetchWithRetry = async (url, config = {}) => {
    let lastError
    for (let i = 0; i < MAX_RETRIES; i++) {
        try {
            console.log(`请求 ${url} (尝试 ${i + 1}/${MAX_RETRIES})`)
            const response = await api.request({
                url,
                ...config
            })
            return response
        } catch (err) {
            lastError = err
            if (i === MAX_RETRIES - 1) break
            console.warn(`请求失败，等待重试: ${err.message}`)
            await new Promise(r => setTimeout(r, RETRY_DELAY * (i + 1)))
        }
    }
    throw lastError
}

export default api

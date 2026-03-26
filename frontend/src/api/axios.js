import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  
  if (authStore.token) {
    // This adds the "Bearer <token>" header automatically!
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api
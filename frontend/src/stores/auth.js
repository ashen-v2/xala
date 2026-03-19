import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { jwtDecode } from "jwt-decode"

export const useAuthStore = defineStore('auth', () => {
  // Initialize from localStorage so login persists on refresh
  const token = ref(localStorage.getItem('token') || null)

  const currentUser = computed(() => {
    if (!token.value) return null
    try {
      // This extracts the payload: { "user_id": 5}
      return jwtDecode(token.value) 
    } catch (error) {
      return null
    }
  })

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
  }

  return { token, setToken, logout, currentUser }
})
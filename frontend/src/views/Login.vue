<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMutation } from '@tanstack/vue-query'
import { useAuthStore } from '../stores/auth'
import api from '../api/axios'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')

// Define the Login Mutation
const { mutate: loginUser, isPending, isError, error } = useMutation({
  mutationFn: async (credentials) => {
    // 1. Prepare Form Data
    const params = new URLSearchParams()
    
    // Use the 'credentials' variable passed from handleLogin
    params.append('username', credentials.email) 
    params.append('password', credentials.password)

    // 2. Make the request and OVERRIDE the content type
    const response = await api.post('v1/users/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    return response.data
  },
  onSuccess: (data) => {
    authStore.setToken(data.access_token)
    alert('Logged in successfully!')
    router.push('/menu-management')
  },
  onError: (err) => {
    console.error("Login Error:", err.response?.data?.detail)
  }
})

function handleLogin() {
  // Fire the mutation
  loginUser({ email: email.value, password: password.value })
}
</script>

<template>
  <form @submit.prevent="handleLogin">
    <input v-model="email" type="email" placeholder="Email" required />
    <input v-model="password" type="password" placeholder="Password" required />

    <button type="submit" :disabled="isPending">
      {{ isPending ? 'Signing in...' : 'Login' }}
    </button>

    <p v-if="isError" class="error">
      {{ error.response?.data?.detail || 'Invalid credentials' }}
    </p>
  </form>
</template>
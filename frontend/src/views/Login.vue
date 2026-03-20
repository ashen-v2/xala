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
  <section class="auth-screen">
    <div class="auth-shell">
      <article class="auth-card">
        <p class="auth-kicker">Welcome Back</p>
        <h1 class="auth-title">Sign In</h1>
        <p class="auth-subtitle">Access Quick Order, Menu Management, and Analytics from one account.</p>

        <form class="auth-form" @submit.prevent="handleLogin">
          <label class="auth-field">
            Email
            <input v-model="email" type="email" placeholder="you@example.com" required />
          </label>

          <label class="auth-field">
            Password
            <input v-model="password" type="password" placeholder="Enter your password" required />
          </label>

          <button type="submit" class="btn-primary" :disabled="isPending">
            {{ isPending ? 'Signing in...' : 'Login' }}
          </button>

          <p v-if="isError" class="status status--error">
            {{ error.response?.data?.detail || 'Invalid credentials' }}
          </p>

          <p class="auth-redirect">
            New here?
            <button type="button" class="auth-link" @click="router.push('/register')">Create an account</button>
          </p>
        </form>
      </article>
    </div>
  </section>
</template>

<style scoped>
.auth-screen {
  min-height: 100svh;
  padding: 0.8rem;
  display: grid;
  align-items: center;
  background:
    radial-gradient(circle at top left, rgba(255, 214, 176, 0.75), transparent 34%),
    radial-gradient(circle at top right, rgba(255, 237, 213, 0.95), transparent 30%),
    linear-gradient(180deg, #fffaf4 0%, #fff 100%);
  color: #442718;
}

.auth-shell {
  width: min(430px, 100%);
  margin: 0 auto;
}

.auth-card {
  border: 1px solid #f4c7a7;
  border-radius: 1.1rem;
  background: linear-gradient(145deg, #fff7ed, #fffdf7);
  box-shadow: 0 14px 32px rgba(128, 58, 22, 0.12);
  padding: 0.95rem;
}

.auth-kicker {
  margin: 0;
  color: #9a3b18;
  text-transform: uppercase;
  letter-spacing: 0.17em;
  font-size: 0.66rem;
  font-weight: 700;
}

.auth-title {
  margin: 0.15rem 0 0;
  color: #492819;
  font-size: 1.45rem;
}

.auth-subtitle {
  margin: 0.25rem 0 0.7rem;
  color: #7c5b45;
  font-size: 0.79rem;
}

.auth-form {
  display: grid;
  gap: 0.58rem;
}

.auth-field {
  display: grid;
  gap: 0.24rem;
  color: #6a4b36;
  font-size: 0.76rem;
  font-weight: 700;
}

.auth-field input {
  border: 1px solid #f1c9a8;
  border-radius: 0.72rem;
  background: #fff;
  color: #3f2417;
  padding: 0.56rem 0.65rem;
  font-size: 0.82rem;
}

.btn-primary {
  border: none;
  border-radius: 0.75rem;
  background: linear-gradient(120deg, #fb923c, #ef4444);
  color: #fff;
  font-weight: 700;
  font-size: 0.82rem;
  padding: 0.6rem 0.72rem;
  cursor: pointer;
}

.btn-primary:disabled {
  opacity: 0.65;
  cursor: wait;
}

.status {
  margin: 0;
  border-radius: 0.75rem;
  padding: 0.5rem 0.65rem;
  font-size: 0.76rem;
}

.status--error {
  background: #fee2e2;
  color: #7f1d1d;
}

.auth-redirect {
  margin: 0.2rem 0 0;
  color: #7c5b45;
  font-size: 0.74rem;
}

.auth-link {
  border: none;
  background: transparent;
  color: #9a3b18;
  font-size: 0.74rem;
  font-weight: 700;
  cursor: pointer;
  padding: 0;
}
</style>
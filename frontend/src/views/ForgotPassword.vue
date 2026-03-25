<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMutation } from '@tanstack/vue-query'
import api from '../api/axios'

const router = useRouter()
const email = ref('')
const isSubmitted = ref(false)

const { mutate: sendResetLink, isPending, isError, error } = useMutation({
  mutationFn: async (userEmail) => {
    const encodedEmail = encodeURIComponent(userEmail)
    const response = await api.post(`/v1/users/forgot-password/${encodedEmail}`)
    return response.data
  },
  onSuccess: () => {
    isSubmitted.value = true
  }
})

function handleForgotPassword() {
  sendResetLink(email.value)
}
</script>

<template>
  <section class="auth-screen">
    <div class="auth-shell">
      <article class="auth-card">
        <p class="auth-kicker">Account Recovery</p>
        <h1 class="auth-title">Forgot Password</h1>
        <p class="auth-subtitle">Enter your account email to receive a reset link and token.</p>

        <form v-if="!isSubmitted" class="auth-form" @submit.prevent="handleForgotPassword">
          <label class="auth-field" for="email">
            Email
            <input id="email" v-model="email" type="email" placeholder="you@example.com" required />
          </label>

          <button type="submit" class="btn-primary" :disabled="isPending">
            {{ isPending ? 'Sending...' : 'Send reset link' }}
          </button>

          <p v-if="isError" class="status status--error">
            {{ error.response?.data?.detail || 'Unable to send reset email. Please try again.' }}
          </p>
        </form>

        <div v-else class="auth-form">
          <p class="status status--success">
            If that email exists, a password reset message has been sent. Check your inbox.
          </p>
          <button type="button" class="btn-primary" @click="router.push('/login')">Back to login</button>
        </div>

        <p class="auth-redirect">
          Remember your password?
          <button type="button" class="auth-link" @click="router.push('/login')">Sign in</button>
        </p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.auth-screen {
  padding: 0.8rem;
  display: grid;
  align-items: center;
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

.auth-form {
  display: grid;
  gap: 0.58rem;
}

.auth-redirect {
  margin: 0.65rem 0 0;
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

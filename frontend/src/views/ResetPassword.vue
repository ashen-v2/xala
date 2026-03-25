<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMutation } from '@tanstack/vue-query'
import api from '../api/axios'

const route = useRoute()
const router = useRouter()

const password = ref('')
const confirmPassword = ref('')
const formError = ref('')
const isResetDone = ref(false)

const resetToken = computed(() => {
  const queryToken = route.query.token
  return typeof queryToken === 'string' ? queryToken : ''
})

const { mutate: resetPassword, isPending, isError, error } = useMutation({
  mutationFn: async (payload) => {
    const response = await api.post('/v1/users/reset-password', payload)
    return response.data
  },
  onSuccess: () => {
    isResetDone.value = true
  }
})

function handleResetPassword() {
  formError.value = ''

  if (!resetToken.value) {
    formError.value = 'Reset token is missing. Use the link from your email.'
    return
  }

  if (password.value.length < 6) {
    formError.value = 'Password must be at least 6 characters.'
    return
  }

  if (password.value !== confirmPassword.value) {
    formError.value = 'Passwords do not match.'
    return
  }

  resetPassword({
    password_token: resetToken.value,
    password: password.value
  })
}
</script>

<template>
  <section class="auth-screen">
    <div class="auth-shell">
      <article class="auth-card">
        <p class="auth-kicker">Account Recovery</p>
        <h1 class="auth-title">Reset Password</h1>
        <p class="auth-subtitle">Create a new password for your account.</p>

        <form v-if="!isResetDone" class="auth-form" @submit.prevent="handleResetPassword">
          <p v-if="!resetToken" class="status status--error">
            Missing reset token. Open this page from the reset link in your email.
          </p>

          <label class="auth-field" for="new-password">
            New Password
            <input
              id="new-password"
              v-model="password"
              type="password"
              placeholder="Enter a new password"
              required
            />
          </label>

          <label class="auth-field" for="confirm-password">
            Confirm Password
            <input
              id="confirm-password"
              v-model="confirmPassword"
              type="password"
              placeholder="Re-enter your new password"
              required
            />
          </label>

          <button type="submit" class="btn-primary" :disabled="isPending || !resetToken">
            {{ isPending ? 'Resetting...' : 'Reset password' }}
          </button>

          <p v-if="formError" class="status status--error">
            {{ formError }}
          </p>

          <p v-if="isError" class="status status--error">
            {{ error.response?.data?.detail || 'Unable to reset password. Please try again.' }}
          </p>
        </form>

        <div v-else class="auth-form">
          <p class="status status--success">Password reset successfully. You can now sign in.</p>
          <button type="button" class="btn-primary" @click="router.push('/login')">Go to login</button>
        </div>

        <p class="auth-redirect">
          Back to sign in?
          <button type="button" class="auth-link" @click="router.push('/login')">Login</button>
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

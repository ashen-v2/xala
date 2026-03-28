<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMutation } from '@tanstack/vue-query'
import api from '../api/axios'

const route = useRoute()
const router = useRouter()

const statusMessage = ref('Preparing verification...')
const isSuccess = ref(false)
const hasAttempted = ref(false)

const emailToken = computed(() => {
  const token = route.query.token
  return typeof token === 'string' ? token : ''
})

const { mutate: verifyEmail, isPending } = useMutation({
  mutationFn: async (token) => {
    const response = await api.post('/v1/users/verify-email', { email_token: token })
    return response.data
  },
  onSuccess: (data) => {
    hasAttempted.value = true
    isSuccess.value = true
    statusMessage.value = data?.message || 'Email verified successfully.'

    setTimeout(() => {
      router.push('/login')
    }, 1800)
  },
  onError: (error) => {
    hasAttempted.value = true
    isSuccess.value = false
    statusMessage.value = error?.response?.data?.detail || 'Verification failed. Please try again with a valid link.'
  }
})

function runVerification() {
  if (!emailToken.value) {
    hasAttempted.value = true
    isSuccess.value = false
    statusMessage.value = 'Verification token is missing. Open this page from the email verification link.'
    return
  }

  verifyEmail(emailToken.value)
}

onMounted(() => {
  runVerification()
})
</script>

<template>
  <section class="auth-screen">
    <div class="auth-shell">
      <article class="auth-card">
        <p class="auth-kicker">Email Verification</p>
        <h1 class="auth-title">Verify Your Email</h1>
        <p class="auth-subtitle">We are confirming your email address so your account is fully activated.</p>

        <div class="auth-form">
          <p v-if="isPending && !hasAttempted" class="status status--info">Verifying your email address...</p>

          <p v-else :class="['status', isSuccess ? 'status--success' : 'status--error']">
            {{ statusMessage }}
          </p>

          <button
            v-if="!isSuccess"
            type="button"
            class="btn-primary"
            :disabled="isPending"
            @click="runVerification"
          >
            {{ isPending ? 'Verifying...' : 'Try again' }}
          </button>

          <button type="button" class="btn-primary" @click="router.push('/login')">
            Go to login
          </button>
        </div>

        <p class="auth-redirect">
          Need a new account?
          <button type="button" class="auth-link" @click="router.push('/register')">Register</button>
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

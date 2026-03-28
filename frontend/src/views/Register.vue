<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'
import { useMutation } from '@tanstack/vue-query'

const router = useRouter()
const name = ref('')
const store_name = ref('')
const email = ref('')
const password = ref('')

const { mutate, isPending, isError, error } = useMutation({
  mutationFn: (newUserData) => {
    return api.post('/v1/users', newUserData)
  },
  onSuccess: () => {
        alert('Account created! Please check your email to verify your address.')
    router.push('/login')
  }
})

function register() {
    mutate({
        name: name.value,
        store_name: store_name.value,
        email: email.value,
        password: password.value
    })
}
</script>
<template>
    <section class="auth-screen">
        <div class="auth-shell">
            <article class="auth-card">
                <p class="auth-kicker">Create Account</p>
                <h1 class="auth-title">Register</h1>
                <p class="auth-subtitle">Set up your store profile to manage menu, orders, and analytics.</p>

                <form class="auth-form" @submit.prevent="register">
                    <label class="auth-field" for="name">
                        Username
                        <input id="name" v-model="name" type="text" placeholder="Your name" required />
                    </label>

                    <label class="auth-field" for="store_name">
                        Store Name
                        <input id="store_name" v-model="store_name" type="text" placeholder="Store name" required />
                    </label>

                    <label class="auth-field" for="email">
                        Email
                        <input id="email" v-model="email" type="email" placeholder="you@example.com" required />
                    </label>

                    <label class="auth-field" for="password">
                        Password
                        <input id="password" v-model="password" type="password" placeholder="Choose a password" required />
                    </label>

                    <button type="submit" class="btn-primary" :disabled="isPending">
                        {{ isPending ? 'Registering...' : 'Register' }}
                    </button>

                    <p v-if="isError" class="status status--error">
                        {{ error.response?.data?.detail || 'Something went wrong' }}
                    </p>

                    <p class="auth-redirect">
                        Already have an account?
                        <button type="button" class="auth-link" @click="router.push('/login')">Go to login</button>
                    </p>
                </form>
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
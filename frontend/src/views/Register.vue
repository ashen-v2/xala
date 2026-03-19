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
    alert('Account created!')
    router.push('/login')
  }
})

async function register() {
    mutate({
        name: name.value,
        store_name: store_name.value,
        email: email.value,
        password: password.value
        
    })
    if (register_data.status === 201) {
        alert('Registration successful!')
    }
    
}
</script>
<template>
    <div class="register">
        <h1>Register</h1>
        <form @submit.prevent="register">
            <div>
                <label for="name">Username:</label>
                <input type="text" id="name" v-model="name" required />
            </div>
             <div>
                <label for="store name">Store Name:</label>
                <input type="text" id="store_name" v-model="store_name" required />
            </div>
            <div>
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit" :disabled="isPending">
                 {{ isPending ? 'Registering...' : 'Register' }}
            </button>

            <p v-if="isError" class="text-red-500">
            Error: {{ error.response?.data?.detail || 'Something went wrong' }}
            </p>
        </form>
    </div>
</template>
<style scoped>
</style>
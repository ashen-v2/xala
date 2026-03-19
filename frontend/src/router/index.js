import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
    { path: '/', redirect: '/dashboard' },
    { path: '/register', name: 'Register', component: Register, meta: { public: true } },
    { path: '/login', name: 'Login', component: Login, meta: { public: true } },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to) => {
    const authStore = useAuthStore()

    if (!to.meta.public && !authStore.token) {
        return { path: '/login' }
    }

    if (to.meta.public && authStore.token) {
        return { path: '/dashboard' }
    }

    return true
})

export default router
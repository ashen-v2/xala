import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import MenuManagement from '../views/MenuManagement.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
    { path: '/', redirect: '/menu-management' },
    { path: '/register', name: 'Register', component: Register, meta: { public: true } },
    { path: '/login', name: 'Login', component: Login, meta: { public: true } },
    { path: '/menu-management', name: 'MenuManagement', component: MenuManagement },
    { path: '/dashboard', redirect: '/menu-management' }
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
        return { path: '/menu-management' }
    }

    return true
})

export default router
import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import MenuManagement from '../views/MenuManagement.vue'
import TrackSales from '../views/TrackSales.vue'
import AnalyticsDashboard from '../views/AnalyticsDashboard.vue'
import Profile from '../views/Profile.vue'
import { useAuthStore } from '../stores/auth'

const routes = [
    { path: '/', redirect: '/track-sales' },
    { path: '/register', name: 'Register', component: Register, meta: { public: true } },
    { path: '/login', name: 'Login', component: Login, meta: { public: true } },
    { path: '/track-sales', name: 'TrackSales', component: TrackSales },
    { path: '/analytics', name: 'AnalyticsDashboard', component: AnalyticsDashboard },
    { path: '/menu-management', name: 'MenuManagement', component: MenuManagement },
    { path: '/profile', name: 'Profile', component: Profile },
    { path: '/dashboard', redirect: '/track-sales' }
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
        return { path: '/track-sales' }
    }

    return true
})

export default router
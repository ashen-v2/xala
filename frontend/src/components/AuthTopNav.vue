<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navItems = [
  { label: 'Track', path: '/track-sales' },
  { label: 'Menu Management', path: '/menu-management' },
  { label: 'Analytics', path: '/analytics' },
  { label: 'Profile', path: '/profile' }
]

const currentPath = computed(() => route.path)

function isActive(path) {
  return currentPath.value === path
}

function go(path) {
  if (currentPath.value === path) return
  router.push(path)
}
</script>

<template>
  <nav class="auth-nav" aria-label="Main navigation">
    <button
      v-for="item in navItems"
      :key="item.path"
      type="button"
      :class="['auth-nav__button', { 'auth-nav__button--active': isActive(item.path) }]"
      @click="go(item.path)"
    >
      {{ item.label }}
    </button>
  </nav>
</template>

<style scoped>
.auth-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.42rem;
}

.auth-nav__button {
  border: 1px solid #f1c9a8;
  background: #fff2e2;
  color: #7b341c;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 0.73rem;
  padding: 0.46rem 0.62rem;
  cursor: pointer;
  transition: transform 120ms ease, background-color 120ms ease;
}

.auth-nav__button:hover {
  background: #ffe4cf;
}

.auth-nav__button--active {
  border-color: #ef4444;
  background: linear-gradient(120deg, #fb923c, #ef4444);
  color: #fff;
}

@media (min-width: 768px) {
  .auth-nav__button {
    font-size: 0.76rem;
    padding: 0.5rem 0.7rem;
  }
}
</style>

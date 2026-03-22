<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const navItems = [
  { label: 'Record Sales', path: '/track-sales' },
  { label: 'Manage Menu', path: '/menu-management' },
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

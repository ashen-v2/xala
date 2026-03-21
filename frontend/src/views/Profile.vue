<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useUser } from '../composables/useUser'
import AuthTopNav from '../components/AuthTopNav.vue'

const router = useRouter()
const authStore = useAuthStore()
const { user, isLoading, isError, error, updateUser, isUpdating, isUpdateError, updateError, isUpdateSuccess } = useUser()

const name = ref('')
const storeName = ref('')
const saveMessage = ref('')

watch(
  user,
  (value) => {
    if (!value) return
    name.value = value.name ?? ''
    storeName.value = value.store_name ?? ''
  },
  { immediate: true }
)

const isDirty = computed(() => {
  if (!user.value) return false
  return name.value !== user.value.name || storeName.value !== user.value.store_name
})

async function saveProfile() {
  saveMessage.value = ''

  if (!isDirty.value) {
    saveMessage.value = 'No changes to save.'
    return
  }

  await updateUser({
    name: name.value,
    store_name: storeName.value
  })

  saveMessage.value = 'Profile updated successfully.'
}

function resetChanges() {
  if (!user.value) return
  name.value = user.value.name
  storeName.value = user.value.store_name
  saveMessage.value = ''
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <section class="profile-screen">
    <div class="profile-shell">
      <header class="profile-header">
        <div>
          <p class="profile-kicker">User Profile</p>
          <h1 class="profile-title">My Account</h1>
          <p class="profile-subtitle">Manage your account details used across menu and order workflows.</p>
        </div>

        <AuthTopNav />
      </header>

      <p v-if="isLoading" class="status status--info">Loading profile...</p>
      <p v-else-if="isError" class="status status--error">
        {{ error?.response?.data?.detail || 'Failed to load profile.' }}
      </p>

      <form v-else-if="user" class="profile-card" @submit.prevent="saveProfile">
        <label class="profile-field">
          Name
          <input v-model="name" type="text" required />
        </label>

        <label class="profile-field">
          Store Name
          <input v-model="storeName" type="text" required />
        </label>

        <label class="profile-field">
          Email
          <input :value="user.email" type="email" readonly />
        </label>

        <div class="profile-actions">
          <button type="button" class="btn-outline" :disabled="isUpdating" @click="resetChanges">Reset</button>
          <button type="submit" class="btn-primary" :disabled="isUpdating || !isDirty">
            {{ isUpdating ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>

        <p v-if="saveMessage" class="status status--success">{{ saveMessage }}</p>
        <p v-if="isUpdateError" class="status status--error">
          {{ updateError?.response?.data?.detail || 'Failed to update profile.' }}
        </p>
        <p v-else-if="isUpdateSuccess" class="status status--info">Your latest profile data is now active.</p>
      </form>

      <section class="logout-card">
        <h2>Session</h2>
        <p>Use logout to securely end this session on this device.</p>
        <button type="button" class="btn-logout" @click="logout">Log out</button>
      </section>
    </div>
  </section>
</template>

<style scoped>
.profile-screen {
  padding: 0.65rem;
}

.profile-shell {
  max-width: 860px;
  margin: 0 auto;
  display: grid;
  gap: 0.7rem;
}

.profile-header,
.profile-card,
.logout-card {
  border: 1px solid #f4c7a7;
  border-radius: 1rem;
  background: linear-gradient(145deg, #fff7ed, #fffdf7);
  box-shadow: 0 14px 32px rgba(128, 58, 22, 0.1);
  padding: 0.75rem;
}

.profile-title {
  margin: 0.1rem 0 0;
  font-size: 1.35rem;
  color: #492819;
}

.profile-subtitle {
  margin: 0.2rem 0 0.6rem;
  font-size: 0.79rem;
  color: #7c5b45;
}

.profile-card {
  display: grid;
  gap: 0.6rem;
}

.profile-field {
  display: grid;
  gap: 0.25rem;
  color: #6a4b36;
  font-size: 0.76rem;
  font-weight: 700;
}

.profile-field input {
  border: 1px solid #f1c9a8;
  border-radius: 0.7rem;
  padding: 0.55rem 0.65rem;
  font-size: 0.82rem;
  color: #3f2417;
  background: #fff;
}

.profile-field input[readonly] {
  background: #fff7ed;
  color: #7c5b45;
}

.profile-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.logout-card h2 {
  margin: 0;
  font-size: 0.95rem;
  color: #492819;
}

.logout-card p {
  margin: 0.28rem 0 0.6rem;
  color: #7c5b45;
  font-size: 0.76rem;
}
</style>

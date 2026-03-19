<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useMenu } from '../composables/useMenu'
import MenuCard from '../components/menu/MenuCard.vue'
import MenuItemForm from '../components/menu/MenuItemForm.vue'

const router = useRouter()
const authStore = useAuthStore()
const {
  items,
  isLoading,
  isError,
  error,
  createItem,
  updateItem,
  deleteItem,
  isCreating,
  isUpdating,
  isDeleting
} = useMenu()

const showCreatePanel = ref(false)
const editingItem = ref(null)
const deletingId = ref(null)

const sortedItems = computed(() => [...items.value].sort((a, b) => b.id - a.id))

function toggleCreatePanel() {
  showCreatePanel.value = !showCreatePanel.value
  if (showCreatePanel.value) {
    editingItem.value = null
  }
}

function openEditPanel(item) {
  editingItem.value = item
  showCreatePanel.value = false
}

function closePanels() {
  showCreatePanel.value = false
  editingItem.value = null
}

async function handleCreate(payload) {
  await createItem(payload)
  showCreatePanel.value = false
}

async function handleEdit(payload) {
  if (!editingItem.value) return

  await updateItem({
    itemId: editingItem.value.id,
    payload
  })

  editingItem.value = null
}

async function handleDelete(item) {
  const shouldDelete = window.confirm(`Delete ${item.name}?`)
  if (!shouldDelete) return

  deletingId.value = item.id
  try {
    await deleteItem(item.id)
    if (editingItem.value?.id === item.id) {
      editingItem.value = null
    }
  } finally {
    deletingId.value = null
  }
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <section class="dashboard">
    <header class="hero">
      <div>
        <p class="eyebrow">Today's Menu</p>
        <h1>Menu Manager</h1>
        <p class="subcopy">Create, edit, and delete menu cards from your phone first.</p>
      </div>

      <div class="hero__actions">
        <button type="button" class="btn btn--primary" @click="toggleCreatePanel">
          {{ showCreatePanel ? 'Hide Create Form' : 'Add New Item' }}
        </button>
        <button type="button" class="btn btn--quiet" @click="logout">Log out</button>
      </div>
    </header>

    <MenuItemForm
      v-if="showCreatePanel"
      title="Create Menu Item"
      submit-label="Create Item"
      :pending="isCreating"
      @submit="handleCreate"
      @cancel="closePanels"
    />

    <MenuItemForm
      v-if="editingItem"
      title="Edit Menu Item"
      submit-label="Save Changes"
      :initial-item="editingItem"
      :pending="isUpdating"
      @submit="handleEdit"
      @cancel="closePanels"
    />

    <p v-if="isLoading" class="info">Loading menu items...</p>
    <p v-else-if="isError" class="error">{{ error?.response?.data?.detail || 'Failed to load menu items' }}</p>

    <section v-else-if="sortedItems.length" class="grid">
      <MenuCard
        v-for="item in sortedItems"
        :key="item.id"
        :item="item"
        :deleting-id="deletingId"
        @edit="openEditPanel"
        @delete="handleDelete"
      />
    </section>

    <section v-else class="empty-state">
      <h2>No menu items yet</h2>
      <p>Tap "Add New Item" to create your first card.</p>
    </section>

    <p v-if="isDeleting && deletingId" class="info">Deleting item...</p>
  </section>
</template>

<style scoped>
.dashboard {
  min-height: 100svh;
  display: grid;
  align-content: start;
  gap: 0.95rem;
  padding: 1rem 0.8rem 1.3rem;
  background:
    radial-gradient(circle at 15% -10%, #ffd0b2 0, transparent 45%),
    radial-gradient(circle at 100% 0%, #ffedd5 0, transparent 55%),
    #fff;
}

.hero {
  display: grid;
  gap: 0.85rem;
  padding: 1rem;
  border-radius: 20px;
  background: linear-gradient(145deg, #fff7ed, #fffbeb);
  border: 1px solid #f6c8a9;
}

.eyebrow {
  margin: 0;
  font-size: 0.73rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #9a3b18;
}

h1 {
  margin: 0;
  font-size: 1.45rem;
  color: #492819;
  line-height: 1.1;
  font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
}

.subcopy {
  margin: 0.42rem 0 0;
  font-size: 0.9rem;
  color: #7c5b45;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.btn {
  border: 0;
  border-radius: 12px;
  padding: 0.6rem 0.82rem;
  font-size: 0.86rem;
  font-weight: 700;
  cursor: pointer;
}

.btn--primary {
  color: #fff;
  background: linear-gradient(120deg, #fb923c, #ef4444);
}

.btn--quiet {
  color: #713f12;
  background: #fef3c7;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.8rem;
}

.info,
.error {
  margin: 0;
  font-size: 0.9rem;
  border-radius: 12px;
  padding: 0.62rem 0.74rem;
}

.info {
  background: #e0f2fe;
  color: #0c4a6e;
}

.error {
  background: #fee2e2;
  color: #991b1b;
}

.empty-state {
  border: 1px dashed #f2be9e;
  border-radius: 16px;
  background: #fff7ed;
  padding: 1.2rem 0.95rem;
  text-align: center;
}

.empty-state h2 {
  margin: 0;
  font-size: 1.06rem;
  color: #5b3018;
}

.empty-state p {
  margin-top: 0.5rem;
  color: #7c5b45;
}

@media (min-width: 768px) {
  .dashboard {
    padding: 1.4rem;
    gap: 1rem;
  }

  .hero {
    grid-template-columns: 1fr auto;
    align-items: center;
  }

  .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (min-width: 1100px) {
  .dashboard {
    max-width: 1100px;
    margin: 0 auto;
  }

  .grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>

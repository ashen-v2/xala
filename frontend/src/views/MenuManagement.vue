<script setup>
import { computed, ref } from 'vue'
import { useMenu } from '../composables/useMenu'
import MenuCard from '../components/menu/MenuCard.vue'
import MenuItemForm from '../components/menu/MenuItemForm.vue'
import AuthTopNav from '../components/AuthTopNav.vue'

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
const expandedDescriptions = ref(new Set())

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

function toggleDescription(itemId) {
  const nextExpanded = new Set(expandedDescriptions.value)

  if (nextExpanded.has(itemId)) {
    nextExpanded.delete(itemId)
  } else {
    nextExpanded.add(itemId)
  }

  expandedDescriptions.value = nextExpanded
}

function isDescriptionExpanded(itemId) {
  return expandedDescriptions.value.has(itemId)
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
</script>

<template>
  <section class="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(255,214,176,0.7),_transparent_34%),radial-gradient(circle_at_top_right,_rgba(255,237,213,0.9),_transparent_30%),linear-gradient(180deg,_#fffaf4_0%,_#fff_100%)] px-3 py-3 pb-28 text-[#442718] md:px-4 lg:px-6">
    <div class="mx-auto flex min-h-[calc(100svh-1.5rem)] max-w-[1320px] flex-col gap-3">
      <header class="grid gap-3 rounded-3xl border border-[#f4c7a7] bg-[linear-gradient(145deg,_#fff7ed,_#fffdf7)] p-3 shadow-[0_14px_32px_rgba(128,58,22,0.10)] md:grid-cols-[minmax(0,1fr)_auto] md:items-center">
        <div class="space-y-1">
          <p class="menu-kicker"> Management</p>
          <h1 class="menu-title">Menu Management</h1>
          <p class="menu-subtitle">Create, edit, and delete menu items</p>
          <p class="menu-subtitle">.</p>
        </div>

        <AuthTopNav />
      </header>

      <div v-if="showCreatePanel || editingItem" class="grid gap-3 lg:grid-cols-[minmax(0,380px)_1fr] lg:items-start">
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
      </div>

      <p v-if="isLoading" class="rounded-2xl bg-sky-100 px-3 py-2 text-sm text-sky-900">Loading menu items...</p>
      <p v-else-if="isError" class="rounded-2xl bg-red-100 px-3 py-2 text-sm text-red-900">{{ error?.response?.data?.detail || 'Failed to load menu items' }}</p>

      <section v-else-if="sortedItems.length" class="grid grid-cols-1 gap-2 md:grid-cols-2 xl:grid-cols-4 xl:gap-3">
        <MenuCard
          v-for="item in sortedItems"
          :key="item.id"
          :item="item"
          :deleting-id="deletingId"
          :expanded="isDescriptionExpanded(item.id)"
          @toggle-description="toggleDescription"
          @edit="openEditPanel"
          @delete="handleDelete"
        />
      </section>

      <section v-else class="rounded-3xl border border-dashed border-[#f2be9e] bg-[#fff7ed] px-4 py-10 text-center">
        <h2 class="m-0 text-base font-semibold text-[#5b3018]">No menu items yet</h2>
        <p class="mt-2 text-sm text-[#7c5b45]">Tap Add New Item to create the first card.</p>
      </section>

      <p v-if="isDeleting && deletingId" class="rounded-2xl bg-sky-100 px-3 py-2 text-sm text-sky-900">Deleting item...</p>

      <div class="fixed bottom-3 left-3 right-3 z-30 mx-auto max-w-[1320px] rounded-2xl border border-[#f4c7a7] bg-[linear-gradient(145deg,_#fff7ed,_#fffdf7)] p-3 shadow-[0_14px_30px_rgba(128,58,22,0.18)] md:left-4 md:right-4 lg:left-6 lg:right-6">
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="m-0 text-[0.62rem] font-semibold uppercase tracking-[0.14em] text-[#9a3b18]">Menu Actions</p>
            <p class="m-0.5 text-xs text-[#7c5b45]">Use this quick action to open the create form.</p>
          </div>
          <button
            type="button"
            class="rounded-xl bg-gradient-to-r from-[#fb923c] to-[#ef4444] px-3.5 py-2 text-sm font-bold text-white shadow-sm transition hover:brightness-105"
            @click="toggleCreatePanel"
          >
            {{ showCreatePanel ? 'Hide Create Form' : 'Add New Item' }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
<style scoped>
.menu-title {
  margin: 0.1rem 0 0;
  font-size: 1.35rem;
  line-height: 1.15;
  color: #492819;
}
.menu-kicker {
  margin: 0;
  color: #9a3b18;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.67rem;
  font-weight: 700;
}
.menu-subtitle {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  color: #7c5b45;
}
</style>
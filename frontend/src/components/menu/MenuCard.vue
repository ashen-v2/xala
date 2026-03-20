<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  deletingId: {
    type: Number,
    default: null
  },
  expanded: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['edit', 'delete', 'toggle-description'])

const fallbackImage = computed(
  () => `https://picsum.photos/seed/food-${props.item.id ?? props.item.name}/720/420`
)
const imageSrc = ref(props.item.image_url || fallbackImage.value)

watch(
  () => props.item,
  () => {
    imageSrc.value = props.item.image_url || fallbackImage.value
  },
  { deep: true }
)

const isDeletingThisCard = computed(() => props.deletingId === props.item.id)

function onImageError() {
  if (imageSrc.value !== fallbackImage.value) {
    imageSrc.value = fallbackImage.value
  }
}

function onToggleDescription() {
  emit('toggle-description', props.item.id)
}

function onEdit() {
  emit('edit', props.item)
}

function onDelete() {
  emit('delete', props.item)
}
</script>

<template>
  <article class="menu-card">
    <img
      class="menu-card__image"
      :src="imageSrc"
      :alt="`Preview image for ${item.name}`"
      loading="lazy"
      @error="onImageError"
    />

    <div class="menu-card__content">
      <div class="flex items-start justify-between gap-2">
        <div class="min-w-0">
          <h3 class="menu-card__title truncate">{{ item.name }}</h3>
          <p class="menu-card__price">${{ Number(item.price).toFixed(2) }}</p>
        </div>

        <button type="button" class="menu-card__toggle" @click="onToggleDescription">
          {{ expanded ? 'Hide details' : 'Details' }}
        </button>
      </div>

      <p v-if="expanded" class="menu-card__desc">
        {{ item.description || 'No description yet.' }}
      </p>

      <div class="menu-card__actions">
        <button type="button" class="btn btn--secondary" @click="onEdit">Edit</button>
        <button
          type="button"
          class="btn btn--danger"
          :disabled="isDeletingThisCard"
          @click="onDelete"
        >
          {{ isDeletingThisCard ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.menu-card {
  overflow: hidden;
  border-radius: 1.25rem;
  border: 1px solid #f1c9a8;
  background: linear-gradient(180deg, #fff9f4 0%, #fffdf9 100%);
  box-shadow: 0 12px 26px rgba(128, 58, 22, 0.10);
}

.menu-card__image {
  width: 100%;
  aspect-ratio: 16 / 8;
  object-fit: cover;
  display: block;
}

.menu-card__content {
  padding: 0.8rem;
  display: grid;
  gap: 0.55rem;
}

.menu-card__title {
  margin: 0;
  font-size: 1rem;
  color: #3f2417;
  font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
}

.menu-card__price {
  margin: 0.2rem 0 0;
  font-size: 0.92rem;
  font-weight: 700;
  color: #8f2e11;
}

.menu-card__desc {
  margin: 0;
  font-size: 0.88rem;
  color: #6a4b36;
  line-height: 1.35;
}

.menu-card__actions {
  display: flex;
  gap: 0.45rem;
}

.btn {
  border: 0;
  border-radius: 0.75rem;
  padding: 0.45rem 0.7rem;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: pointer;
}

.menu-card__toggle {
  border: 1px solid #f3caa7;
  border-radius: 999px;
  background: #fff3e8;
  color: #8a4f21;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.65;
  cursor: wait;
}

.btn--secondary {
  background: #ffe4cf;
  color: #7b341c;
}

.btn--danger {
  background: #972d2d;
  color: #fff;
}
</style>

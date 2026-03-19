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
  }
})

const emit = defineEmits(['edit', 'delete'])

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
      <div class="menu-card__head">
        <h3>{{ item.name }}</h3>
        <p class="menu-card__price">${{ Number(item.price).toFixed(2) }}</p>
      </div>

      <p class="menu-card__desc">
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
  border-radius: 18px;
  border: 1px solid #f1c9a8;
  background: #fff9f4;
  box-shadow: 0 14px 32px rgba(128, 58, 22, 0.12);
}

.menu-card__image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  display: block;
}

.menu-card__content {
  padding: 0.95rem;
  display: grid;
  gap: 0.75rem;
}

.menu-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.menu-card__head h3 {
  margin: 0;
  font-size: 1.06rem;
  color: #3f2417;
  font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
}

.menu-card__price {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 700;
  color: #8f2e11;
}

.menu-card__desc {
  margin: 0;
  font-size: 0.92rem;
  color: #6a4b36;
  line-height: 1.35;
}

.menu-card__actions {
  display: flex;
  gap: 0.55rem;
}

.btn {
  border: 0;
  border-radius: 10px;
  padding: 0.5rem 0.75rem;
  font-weight: 700;
  font-size: 0.84rem;
  cursor: pointer;
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

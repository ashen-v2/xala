<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  submitLabel: {
    type: String,
    required: true
  },
  initialItem: {
    type: Object,
    default: () => ({
      name: '',
      description: '',
      price: ''
    })
  },
  pending: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  name: '',
  description: '',
  price: ''
})

watch(
  () => props.initialItem,
  (item) => {
    form.name = item?.name ?? ''
    form.description = item?.description ?? ''
    form.price = item?.price ?? ''
  },
  { immediate: true, deep: true }
)

function onSubmit() {
  const payload = {
    name: form.name.trim(),
    description: form.description.trim() || null,
    price: Number(form.price)
  }

  if (!payload.name || Number.isNaN(payload.price) || payload.price < 0) {
    return
  }

  emit('submit', payload)
}

function onCancel() {
  emit('cancel')
}
</script>

<template>
  <section class="panel">
    <div class="panel__head">
      <h2>{{ title }}</h2>
      <button type="button" class="ghost" @click="onCancel">Close</button>
    </div>

    <form class="form" @submit.prevent="onSubmit">
      <label>
        Name
        <input v-model="form.name" type="text" maxlength="80" required />
      </label>

      <label>
        Description
        <textarea v-model="form.description" rows="3" maxlength="220" />
      </label>

      <label>
        Price
        <input v-model="form.price" type="number" step="0.01" min="0" required />
      </label>

      <button type="submit" class="submit" :disabled="pending">
        {{ pending ? 'Saving...' : submitLabel }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.panel {
  border-radius: 1.25rem;
  border: 1px solid #ffd2b5;
  background: #fffaf6;
  box-shadow: 0 10px 24px rgba(124, 62, 28, 0.08);
  padding: 0.8rem;
}

.panel__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.65rem;
}

.panel__head h2 {
  margin: 0;
  font-size: 0.98rem;
  color: #4a2716;
  font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
}

.form {
  display: grid;
  gap: 0.55rem;
}

label {
  display: grid;
  gap: 0.28rem;
  font-size: 0.8rem;
  color: #5d4335;
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #efc8af;
  border-radius: 0.8rem;
  background: #fff;
  color: #3e2a1f;
  padding: 0.48rem 0.62rem;
  font-size: 0.86rem;
}
</style>

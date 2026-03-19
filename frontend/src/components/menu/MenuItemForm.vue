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
  border-radius: 18px;
  border: 1px solid #ffd2b5;
  background: #fffaf6;
  box-shadow: 0 10px 28px rgba(124, 62, 28, 0.1);
  padding: 0.95rem;
}

.panel__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.panel__head h2 {
  margin: 0;
  font-size: 1rem;
  color: #4a2716;
  font-family: 'Trebuchet MS', 'Segoe UI', sans-serif;
}

.ghost {
  border: 1px solid #f0b58d;
  background: transparent;
  color: #7b341c;
  border-radius: 10px;
  font-size: 0.82rem;
  font-weight: 700;
  padding: 0.38rem 0.62rem;
  cursor: pointer;
}

.form {
  display: grid;
  gap: 0.7rem;
}

label {
  display: grid;
  gap: 0.35rem;
  font-size: 0.86rem;
  color: #5d4335;
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid #efc8af;
  border-radius: 10px;
  background: #fff;
  color: #3e2a1f;
  padding: 0.54rem 0.66rem;
  font-size: 0.9rem;
}

.submit {
  border: none;
  border-radius: 12px;
  background: linear-gradient(120deg, #f97316, #ef4444);
  color: white;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.62rem 0.82rem;
  cursor: pointer;
}

.submit:disabled {
  opacity: 0.65;
  cursor: wait;
}
</style>

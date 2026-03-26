<script setup>
import { computed, ref } from 'vue'
import { useTrackSales } from '../composables/useTrackSales'
import AuthTopNav from '../components/AuthTopNav.vue'

const {
  menuItems,
  cartItems,
  cartByProductId,
  cartTotal,
  cartCount,
  isMenuLoading,
  isCartLoading,
  menuError,
  cartError,
  addToCart,
  updateCartItem,
  removeCartItem,
  createOrder,
  isCreatingOrder,
  createdOrder
} = useTrackSales()

const isCartOpen = ref(false)
const actionError = ref('')

const visibleItems = computed(() => {
  return [...menuItems.value].sort((a, b) => a.id - b.id).slice(0, 9)
})

const cartRows = computed(() => {
  return cartItems.value.map((cartItem) => {
    const menu = menuItems.value.find((item) => item.id === cartItem.product_id)
    const unitPrice = Number(menu?.price ?? 0)
    return {
      ...cartItem,
      name: menu?.name || cartItem.product_name,
      unitPrice,
      lineTotal: unitPrice * cartItem.quantity
    }
  })
})

function cartItemForProduct(productId) {
  return cartByProductId.value.get(productId) || null
}

async function onCardTap(item) {
  actionError.value = ''
  try {
    await addToCart({ product_id: item.id, quantity: 1 })
  } catch (error) {
    actionError.value = error?.response?.data?.detail || 'Failed to add item to cart.'
  }
}

async function increaseQuantity(item) {
  actionError.value = ''
  const cartItem = cartItemForProduct(item.id)

  try {
    if (!cartItem) {
      await addToCart({ product_id: item.id, quantity: 1 })
      return
    }

    await updateCartItem({
      cartItemId: cartItem.id,
      quantity: cartItem.quantity + 1
    })
  } catch (error) {
    actionError.value = error?.response?.data?.detail || 'Failed to update quantity.'
  }
}

async function decreaseQuantity(item) {
  actionError.value = ''
  const cartItem = cartItemForProduct(item.id)
  if (!cartItem) return

  try {
    if (cartItem.quantity <= 1) {
      await removeCartItem(cartItem.id)
      return
    }

    await updateCartItem({
      cartItemId: cartItem.id,
      quantity: cartItem.quantity - 1
    })
  } catch (error) {
    actionError.value = error?.response?.data?.detail || 'Failed to update quantity.'
  }
}

async function removeRow(cartItemId) {
  actionError.value = ''
  try {
    await removeCartItem(cartItemId)
  } catch (error) {
    actionError.value = error?.response?.data?.detail || 'Failed to remove item.'
  }
}

async function onCreateOrder() {
  actionError.value = ''
  if (!cartCount.value) return

  try {
    await createOrder()
    isCartOpen.value = false
  } catch (error) {
    actionError.value = error?.response?.data?.detail || 'Failed to create order.'
  }
}
</script>

<template>
  <section class="sales-screen">
    <div class="sales-shell">
      <header class="sales-header">
        <div>
          <p class="sales-kicker">Track Sales</p>
          <h1 class="sales-title">Quick Order</h1>
          <p class="sales-subtitle">Tap a card to add, adjust quantity inline, and track sales fast and easy</p>
        </div>

        <AuthTopNav />
      </header>

      <p v-if="isMenuLoading || isCartLoading" class="status status--info">Loading items...</p>
      <p v-if="menuError || cartError" class="status status--error">
        {{ menuError?.response?.data?.detail || cartError?.response?.data?.detail || 'Failed to load data.' }}
      </p>
      <p v-if="actionError" class="status status--error">{{ actionError }}</p>
      <p v-if="createdOrder?.id" class="status status--success">
        Order #{{ createdOrder.id }} created. Total: Rs.{{ Number(createdOrder.total_price ?? 0).toFixed(2) }}
      </p>

      <section class="menu-grid" aria-label="Track sales menu items">
        <button
          v-for="item in visibleItems"
          :key="item.id"
          type="button"
          class="sales-card"
          @click="onCardTap(item)"
        >
          <p class="sales-card__name">{{ item.name }}</p>
          <p class="sales-card__price">Rs.{{ Number(item.price).toFixed(2) }}</p>

          <div class="qty-control" @click.stop>
            <button type="button" class="qty-btn" @click="decreaseQuantity(item)">-</button>
            <span class="qty-value">{{ cartItemForProduct(item.id)?.quantity ?? 0 }}</span>
            <button type="button" class="qty-btn" @click="increaseQuantity(item)">+</button>
          </div>
        </button>
      </section>

      <p v-if="!visibleItems.length && !isMenuLoading" class="status status--info">No menu items yet. Create items in Menu Management first.</p>

      <div class="sticky-order-bar">
        <div>
          <p class="sticky-order-bar__label">Current Order</p>
          <p class="sticky-order-bar__value">{{ cartCount }} items • Rs.{{ cartTotal.toFixed(2) }}</p>
        </div>

        <div class="sticky-order-bar__actions">
          <button type="button" class="btn-outline" @click="isCartOpen = true">View Order</button>
          <button
            type="button"
            class="btn-primary"
            :disabled="!cartCount || isCreatingOrder"
            @click="onCreateOrder"
          >
            {{ isCreatingOrder ? 'Creating...' : 'Create Order' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="isCartOpen" class="cart-drawer-backdrop" @click.self="isCartOpen = false">
      <aside class="cart-drawer" aria-label="Full order view">
        <header class="cart-drawer__head">
          <h2>Order Details</h2>
          <button type="button" class="btn-soft" @click="isCartOpen = false">Close</button>
        </header>

        <ul v-if="cartRows.length" class="cart-list">
          <li v-for="row in cartRows" :key="row.id" class="cart-row">
            <div>
              <p class="cart-row__name">{{ row.name }}</p>
              <p class="cart-row__meta">Rs.{{ row.unitPrice.toFixed(2) }} each</p>
            </div>

            <div class="cart-row__right">
              <div class="qty-control qty-control--small">
                <button type="button" class="qty-btn" @click="decreaseQuantity({ id: row.product_id })">-</button>
                <span class="qty-value">{{ row.quantity }}</span>
                <button type="button" class="qty-btn" @click="increaseQuantity({ id: row.product_id })">+</button>
              </div>
              <p class="cart-row__line-total">Rs.{{ row.lineTotal.toFixed(2) }}</p>
              <button type="button" class="remove-link" @click="removeRow(row.id)">Remove</button>
            </div>
          </li>
        </ul>
        <p v-else class="status status--info">Your cart is empty.</p>

        <footer class="cart-drawer__foot">
          <p class="cart-total">Total: Rs.{{ cartTotal.toFixed(2) }}</p>
          <button
            type="button"
            class="btn-primary"
            :disabled="!cartCount || isCreatingOrder"
            @click="onCreateOrder"
          >
            {{ isCreatingOrder ? 'Creating...' : 'Create Order' }}
          </button>
        </footer>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.sales-screen {
  padding: 0.65rem;
  padding-bottom: 6.3rem;
}

.sales-shell {
  margin: 0 auto;
  max-width: 480px;
  display: grid;
  gap: 0.65rem;
}

.sales-header {
  border: 1px solid #f4c7a7;
  background: linear-gradient(145deg, #fff7ed, #fffdf7);
  border-radius: 1rem;
  box-shadow: 0 14px 32px rgba(128, 58, 22, 0.1);
  padding: 0.7rem;
  display: grid;
  gap: 0.55rem;
}

.sales-title {
  margin: 0.1rem 0 0;
  font-size: 1.3rem;
  color: #492819;
  line-height: 1.15;
}

.sales-subtitle {
  margin: 0.2rem 0 0;
  font-size: 0.78rem;
  color: #7c5b45;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.5rem;
}

.sales-card {
  border: 1px solid #f1c9a8;
  border-radius: 0.9rem;
  background: linear-gradient(180deg, #fff9f4 0%, #fffdf9 100%);
  box-shadow: 0 10px 20px rgba(128, 58, 22, 0.08);
  padding: 0.5rem 0.45rem;
  display: grid;
  gap: 0.3rem;
  text-align: left;
  min-height: 6rem;
}

.sales-card__name {
  margin: 0;
  font-size: 0.76rem;
  font-weight: 700;
  line-height: 1.2;
  color: #3f2417;
}

.sales-card__price {
  margin: 0;
  font-size: 0.72rem;
  color: #8f2e11;
  font-weight: 700;
}

.qty-control {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  gap: 0.25rem;
  border: 1px solid #f1c9a8;
  border-radius: 999px;
  background: #fff3e8;
  padding: 0.14rem;
}

.qty-value {
  font-size: 0.74rem;
  text-align: center;
  color: #6a4b36;
  font-weight: 700;
}

.sticky-order-bar {
  position: fixed;
  left: 0.65rem;
  right: 0.65rem;
  bottom: 0.65rem;
  z-index: 25;
  border: 1px solid #f4c7a7;
  border-radius: 1rem;
  background: linear-gradient(145deg, #fff7ed, #fffdf7);
  box-shadow: 0 14px 30px rgba(128, 58, 22, 0.18);
  padding: 0.6rem;
  display: flex;
  justify-content: space-between;
  gap: 0.7rem;
  align-items: center;
}

.sticky-order-bar__label {
  margin: 0;
  color: #9a3b18;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.58rem;
  font-weight: 700;
}

.sticky-order-bar__value {
  margin: 0.08rem 0 0;
  font-size: 0.8rem;
  color: #492819;
  font-weight: 700;
}

.sticky-order-bar__actions {
  display: flex;
  gap: 0.35rem;
}

.cart-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(57, 33, 22, 0.3);
  z-index: 40;
  display: flex;
  align-items: flex-end;
}

.cart-drawer {
  width: 100%;
  max-height: 78svh;
  border-radius: 1rem 1rem 0 0;
  border: 1px solid #f1c9a8;
  background: #fff9f4;
  padding: 0.8rem;
  display: grid;
  gap: 0.7rem;
}

.cart-drawer__head,
.cart-drawer__foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.55rem;
}

.cart-drawer__head h2 {
  margin: 0;
  font-size: 1rem;
  color: #492819;
}

.cart-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.55rem;
  overflow: auto;
}

.cart-row {
  border: 1px solid #f1c9a8;
  background: #fff;
  border-radius: 0.8rem;
  padding: 0.55rem;
  display: flex;
  justify-content: space-between;
  gap: 0.45rem;
}

.cart-row__name {
  margin: 0;
  font-size: 0.8rem;
  color: #3f2417;
  font-weight: 700;
}

.cart-row__meta,
.cart-row__line-total {
  margin: 0;
  font-size: 0.72rem;
  color: #6a4b36;
}

.cart-row__right {
  display: grid;
  justify-items: end;
  gap: 0.2rem;
}

.qty-control--small {
  min-width: 5.3rem;
}

.remove-link {
  border: none;
  background: transparent;
  color: #b91c1c;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0;
}

.cart-total {
  margin: 0;
  font-size: 0.9rem;
  color: #492819;
  font-weight: 800;
}

@media (min-width: 720px) {
  .sales-shell {
    max-width: 820px;
  }

  .menu-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .sticky-order-bar {
    left: 50%;
    transform: translateX(-50%);
    width: min(760px, calc(100vw - 1.3rem));
  }
}
</style>

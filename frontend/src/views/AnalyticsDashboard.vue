<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAnalytics } from '../composables/useAnalytics'

const router = useRouter()
const authStore = useAuthStore()

const {
  scope,
  year,
  month,
  week,
  weekOptions,
  orders,
  orderDetails,
  orderItems,
  selectedOrderId,
  revenueChart,
  topItemsChart,
  monthlyQuantityChart,
  totalRevenue,
  totalOrders,
  isLoadingAnalytics,
  isLoadingOrders,
  isLoadingOrderDetails,
  analyticsError,
  ordersError,
  orderDetailsError,
  openOrder,
  closeOrder
} = useAnalytics()

const yearOptions = computed(() => {
  const currentYear = new Date().getFullYear()
  return [currentYear - 1, currentYear, currentYear + 1]
})

const monthOptions = [
  { value: 1, label: 'Jan' },
  { value: 2, label: 'Feb' },
  { value: 3, label: 'Mar' },
  { value: 4, label: 'Apr' },
  { value: 5, label: 'May' },
  { value: 6, label: 'Jun' },
  { value: 7, label: 'Jul' },
  { value: 8, label: 'Aug' },
  { value: 9, label: 'Sep' },
  { value: 10, label: 'Oct' },
  { value: 11, label: 'Nov' },
  { value: 12, label: 'Dec' }
]

const revenueMax = computed(() => {
  const maxValue = Math.max(...revenueChart.value.values, 1)
  return maxValue
})

const revenuePoints = computed(() => {
  const values = revenueChart.value.values
  if (!values.length) return ''

  const width = 100
  const height = 100
  const stepX = values.length > 1 ? width / (values.length - 1) : width

  return values
    .map((value, index) => {
      const x = index * stepX
      const y = height - (value / revenueMax.value) * height
      return `${x},${Math.max(0, Math.min(100, y))}`
    })
    .join(' ')
})

const topItemsBars = computed(() => {
  const maxValue = Math.max(...topItemsChart.value.values, 1)

  return topItemsChart.value.labels.map((label, index) => {
    const rawValue = Number(topItemsChart.value.values[index] ?? 0)
    return {
      label,
      value: rawValue,
      width: `${(rawValue / maxValue) * 100}%`
    }
  })
})

const monthlyQuantityBars = computed(() => {
  const maxValue = Math.max(...monthlyQuantityChart.value.values, 1)

  return monthlyQuantityChart.value.labels.map((label, index) => {
    const rawValue = Number(monthlyQuantityChart.value.values[index] ?? 0)
    return {
      label,
      value: rawValue,
      height: `${(rawValue / maxValue) * 100}%`
    }
  })
})

function goToTrackSales() {
  router.push('/track-sales')
}

function goToMenuManagement() {
  router.push('/menu-management')
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <section class="analytics-screen">
    <div class="analytics-shell">
      <header class="analytics-header">
        <div>
          <p class="analytics-kicker">Performance Dashboard</p>
          <h1 class="analytics-title">Analytics</h1>
          <p class="analytics-subtitle">Monitor trends, top items, and order history in one compact mobile view.</p>
        </div>

        <div class="header-actions">
          <button type="button" class="btn-soft" @click="goToTrackSales">Track Sales</button>
          <button type="button" class="btn-soft" @click="goToMenuManagement">Menu Management</button>
          <button type="button" class="btn-soft" @click="logout">Log out</button>
        </div>
      </header>

      <p v-if="analyticsError" class="status status--error">
        {{ analyticsError?.response?.data?.detail || 'Failed to load analytics data.' }}
      </p>
      <p v-if="ordersError" class="status status--error">
        {{ ordersError?.response?.data?.detail || 'Failed to load recent orders.' }}
      </p>

      <section class="metrics-grid">
        <article class="metric-card">
          <p class="metric-card__label">Revenue (Current Scope)</p>
          <p class="metric-card__value">${{ totalRevenue.toFixed(2) }}</p>
        </article>
        <article class="metric-card">
          <p class="metric-card__label">Recent Orders</p>
          <p class="metric-card__value">{{ totalOrders }}</p>
        </article>
      </section>

      <section class="chart-card">
        <div class="chart-head">
          <h2>Sales Trend</h2>
          <p class="chart-subtitle">{{ scope.charAt(0).toUpperCase() + scope.slice(1) }} view</p>
        </div>
        <p v-if="isLoadingAnalytics" class="status status--info">Loading chart...</p>
        <div v-else-if="revenueChart.values.length" class="line-chart-wrap">
          <svg class="line-chart" viewBox="0 0 100 100" preserveAspectRatio="none" role="img" aria-label="Revenue trend chart">
            <polyline :points="revenuePoints" fill="none" stroke="#ef4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <div class="line-chart-labels">
            <span v-for="label in revenueChart.labels" :key="label">{{ label }}</span>
          </div>
        </div>
        <p v-else class="status status--info">No revenue data for selected filters.</p>
      </section>

      <section class="chart-card">
        <div class="chart-head">
          <h2>Top Selling Items</h2>
          <p class="chart-subtitle">Quantity sold</p>
        </div>
        <div v-if="topItemsBars.length" class="bars-list">
          <div v-for="bar in topItemsBars" :key="bar.label" class="bars-list__row">
            <div class="bars-list__meta">
              <span class="bars-list__label">{{ bar.label }}</span>
              <span class="bars-list__value">{{ bar.value }}</span>
            </div>
            <div class="bars-list__track">
              <div class="bars-list__fill" :style="{ width: bar.width }"></div>
            </div>
          </div>
        </div>
        <p v-else class="status status--info">No top item data yet.</p>
      </section>

      <section class="chart-card">
        <div class="chart-head">
          <h2>Monthly Item Volume</h2>
          <p class="chart-subtitle">Total item quantity per month</p>
        </div>
        <div v-if="monthlyQuantityBars.length" class="columns-chart">
          <div
            v-for="bar in monthlyQuantityBars"
            :key="bar.label"
            class="columns-chart__item"
          >
            <div class="columns-chart__column-wrap">
              <div class="columns-chart__column" :style="{ height: bar.height }"></div>
            </div>
            <p class="columns-chart__value">{{ bar.value }}</p>
            <p class="columns-chart__label">{{ bar.label }}</p>
          </div>
        </div>
        <p v-else class="status status--info">No monthly item volume data yet.</p>
      </section>

      <section class="orders-card">
        <div class="chart-head">
          <h2>Recent Orders</h2>
          <p class="chart-subtitle">Latest 50 orders</p>
        </div>

        <p v-if="isLoadingOrders" class="status status--info">Loading orders...</p>
        <ul v-else-if="orders.length" class="orders-list">
          <li v-for="order in orders" :key="order.id">
            <button type="button" class="order-row" @click="openOrder(order.id)">
              <div>
                <p class="order-row__id">Order #{{ order.id }}</p>
                <p class="order-row__time">{{ new Date(order.created_at).toLocaleString() }}</p>
              </div>
              <p class="order-row__amount">${{ Number(order.total_price ?? 0).toFixed(2) }}</p>
            </button>
          </li>
        </ul>
        <p v-else class="status status--info">No orders found yet.</p>
      </section>

      <div class="sticky-filters">
        <div class="scope-switch">
          <button
            type="button"
            :class="['chip', { 'chip--active': scope === 'monthly' }]"
            @click="scope = 'monthly'"
          >
            Monthly
          </button>
          <button
            type="button"
            :class="['chip', { 'chip--active': scope === 'weekly' }]"
            @click="scope = 'weekly'"
          >
            Weekly
          </button>
          <button
            type="button"
            :class="['chip', { 'chip--active': scope === 'daily' }]"
            @click="scope = 'daily'"
          >
            Daily
          </button>
        </div>

        <div class="filter-row">
          <label>
            Year
            <select v-model.number="year">
              <option v-for="option in yearOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </label>

          <label v-if="scope === 'weekly' || scope === 'daily'">
            Month
            <select v-model.number="month">
              <option v-for="option in monthOptions" :key="option.value" :value="option.value">{{ option.label }}</option>
            </select>
          </label>

          <label v-if="scope === 'daily'">
            Week
            <select v-model.number="week">
              <option v-for="option in weekOptions" :key="option" :value="option">Week {{ option }}</option>
            </select>
          </label>
        </div>
      </div>
    </div>

    <div
      v-if="selectedOrderId"
      class="order-drawer-backdrop"
      @click.self="closeOrder"
    >
      <aside class="order-drawer">
        <header class="order-drawer__head">
          <h3>Order #{{ selectedOrderId }}</h3>
          <button type="button" class="btn-soft" @click="closeOrder">Close</button>
        </header>

        <p v-if="orderDetailsError" class="status status--error">
          {{ orderDetailsError?.response?.data?.detail || 'Failed to load order details.' }}
        </p>

        <p v-if="isLoadingOrderDetails" class="status status--info">Loading order details...</p>

        <template v-else>
          <div v-if="orderDetails" class="order-summary">
            <p><strong>Created:</strong> {{ new Date(orderDetails.created_at).toLocaleString() }}</p>
            <p><strong>Total:</strong> ${{ Number(orderDetails.total_price ?? 0).toFixed(2) }}</p>
          </div>

          <ul v-if="orderItems.length" class="order-items-list">
            <li v-for="item in orderItems" :key="item.id" class="order-item-row">
              <div>
                <p class="order-item-row__name">{{ item.product_name }}</p>
                <p class="order-item-row__meta">Qty: {{ item.quantity }}</p>
              </div>
              <p class="order-item-row__amount">${{ Number(item.price ?? 0).toFixed(2) }}</p>
            </li>
          </ul>
          <p v-else class="status status--info">No line items found.</p>
        </template>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.analytics-screen {
  min-height: 100svh;
  padding: 0.65rem;
  padding-bottom: 8rem;
  background:
    radial-gradient(circle at top left, rgba(255, 214, 176, 0.75), transparent 34%),
    radial-gradient(circle at top right, rgba(255, 237, 213, 0.95), transparent 30%),
    linear-gradient(180deg, #fffaf4 0%, #fff 100%);
  color: #442718;
}

.analytics-shell {
  max-width: 920px;
  margin: 0 auto;
  display: grid;
  gap: 0.7rem;
}

.analytics-header {
  border: 1px solid #f4c7a7;
  background: linear-gradient(145deg, #fff7ed, #fffdf7);
  border-radius: 1rem;
  box-shadow: 0 14px 32px rgba(128, 58, 22, 0.1);
  padding: 0.75rem;
  display: grid;
  gap: 0.6rem;
}

.analytics-kicker {
  margin: 0;
  color: #9a3b18;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.67rem;
  font-weight: 700;
}

.analytics-title {
  margin: 0.1rem 0 0;
  font-size: 1.35rem;
  line-height: 1.15;
  color: #492819;
}

.analytics-subtitle {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  color: #7c5b45;
}

.header-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.btn-soft {
  border: 1px solid #f1c9a8;
  background: #fff2e2;
  color: #7b341c;
  border-radius: 0.75rem;
  font-weight: 700;
  font-size: 0.76rem;
  padding: 0.5rem 0.65rem;
  cursor: pointer;
}

.status {
  margin: 0;
  border-radius: 0.75rem;
  padding: 0.5rem 0.65rem;
  font-size: 0.76rem;
}

.status--info {
  background: #fef3c7;
  color: #713f12;
}

.status--error {
  background: #fee2e2;
  color: #7f1d1d;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.6rem;
}

.metric-card,
.chart-card,
.orders-card {
  border: 1px solid #f1c9a8;
  border-radius: 1rem;
  background: linear-gradient(180deg, #fff9f4 0%, #fffdf9 100%);
  box-shadow: 0 10px 20px rgba(128, 58, 22, 0.08);
  padding: 0.7rem;
}

.metric-card__label {
  margin: 0;
  font-size: 0.72rem;
  color: #7c5b45;
}

.metric-card__value {
  margin: 0.25rem 0 0;
  font-size: 1.1rem;
  color: #492819;
  font-weight: 800;
}

.chart-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.5rem;
}

.chart-head h2 {
  margin: 0;
  font-size: 0.94rem;
  color: #492819;
}

.chart-subtitle {
  margin: 0;
  font-size: 0.72rem;
  color: #7c5b45;
}

.line-chart-wrap {
  display: grid;
  gap: 0.45rem;
  margin-top: 0.45rem;
}

.line-chart {
  width: 100%;
  height: 220px;
  border: 1px solid #f1c9a8;
  border-radius: 0.75rem;
  background:
    linear-gradient(to top, rgba(251, 146, 60, 0.15), rgba(251, 146, 60, 0.03));
}

.line-chart-labels {
  display: flex;
  justify-content: space-between;
  gap: 0.35rem;
  font-size: 0.66rem;
  color: #7c5b45;
}

.bars-list {
  display: grid;
  gap: 0.45rem;
  margin-top: 0.55rem;
}

.bars-list__row {
  display: grid;
  gap: 0.24rem;
}

.bars-list__meta {
  display: flex;
  justify-content: space-between;
  gap: 0.3rem;
  font-size: 0.72rem;
  color: #6a4b36;
}

.bars-list__label {
  font-weight: 700;
  color: #492819;
}

.bars-list__value {
  font-weight: 700;
  color: #8f2e11;
}

.bars-list__track {
  width: 100%;
  height: 0.58rem;
  border-radius: 999px;
  background: #ffe8d2;
  overflow: hidden;
}

.bars-list__fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #fb923c, #ef4444);
}

.columns-chart {
  margin-top: 0.55rem;
  min-height: 220px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(34px, 1fr));
  gap: 0.38rem;
  align-items: end;
}

.columns-chart__item {
  display: grid;
  justify-items: center;
  gap: 0.16rem;
}

.columns-chart__column-wrap {
  width: 100%;
  min-height: 150px;
  border-radius: 0.4rem;
  background: #ffe8d2;
  display: flex;
  align-items: flex-end;
}

.columns-chart__column {
  width: 100%;
  border-radius: 0.4rem;
  background: linear-gradient(180deg, #fb923c, #9a3b18);
}

.columns-chart__value {
  margin: 0;
  font-size: 0.62rem;
  color: #8f2e11;
  font-weight: 700;
}

.columns-chart__label {
  margin: 0;
  font-size: 0.6rem;
  color: #7c5b45;
}

.orders-list,
.order-items-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.45rem;
}

.order-row {
  width: 100%;
  border: 1px solid #f1c9a8;
  background: #fff;
  border-radius: 0.75rem;
  padding: 0.55rem;
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  text-align: left;
  cursor: pointer;
}

.order-row__id {
  margin: 0;
  font-size: 0.78rem;
  color: #492819;
  font-weight: 700;
}

.order-row__time {
  margin: 0.15rem 0 0;
  font-size: 0.7rem;
  color: #7c5b45;
}

.order-row__amount {
  margin: 0;
  font-size: 0.82rem;
  color: #8f2e11;
  font-weight: 800;
}

.sticky-filters {
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
  display: grid;
  gap: 0.5rem;
}

.scope-switch {
  display: flex;
  gap: 0.35rem;
}

.chip {
  border: 1px solid #f1c9a8;
  background: #fff;
  color: #7b341c;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.35rem 0.65rem;
}

.chip--active {
  border-color: #ef4444;
  background: #ffe4cf;
  color: #7b341c;
}

.filter-row {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
}

.filter-row label {
  display: grid;
  gap: 0.2rem;
  font-size: 0.68rem;
  color: #7c5b45;
}

.filter-row select {
  border: 1px solid #f1c9a8;
  border-radius: 0.55rem;
  background: #fff;
  color: #492819;
  padding: 0.32rem 0.42rem;
  font-size: 0.76rem;
}

.order-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(57, 33, 22, 0.3);
  z-index: 40;
  display: flex;
  align-items: flex-end;
}

.order-drawer {
  width: 100%;
  max-height: 78svh;
  border-radius: 1rem 1rem 0 0;
  border: 1px solid #f1c9a8;
  background: #fff9f4;
  padding: 0.8rem;
  display: grid;
  gap: 0.65rem;
  overflow: auto;
}

.order-drawer__head {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  align-items: center;
}

.order-drawer__head h3 {
  margin: 0;
  font-size: 1rem;
  color: #492819;
}

.order-summary {
  border: 1px solid #f1c9a8;
  border-radius: 0.75rem;
  background: #fff;
  padding: 0.55rem;
  display: grid;
  gap: 0.3rem;
  font-size: 0.75rem;
  color: #6a4b36;
}

.order-item-row {
  border: 1px solid #f1c9a8;
  border-radius: 0.75rem;
  background: #fff;
  padding: 0.55rem;
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.order-item-row__name {
  margin: 0;
  font-size: 0.78rem;
  color: #492819;
  font-weight: 700;
}

.order-item-row__meta,
.order-item-row__amount {
  margin: 0.12rem 0 0;
  font-size: 0.72rem;
  color: #7c5b45;
}

@media (min-width: 900px) {
  .sticky-filters {
    left: 50%;
    transform: translateX(-50%);
    width: min(860px, calc(100vw - 1.3rem));
  }

  .metrics-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}
</style>

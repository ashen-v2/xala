<script setup>
import { computed } from 'vue'
import { useAnalytics } from '../composables/useAnalytics'
import AuthTopNav from '../components/AuthTopNav.vue'

const {
  scope,
  year,
  month,
  selectedWeeks,
  weekOptions,
  canSelectMoreWeeks,
  orders,
  orderDetails,
  orderItems,
  selectedOrderId,
  revenueChart,
  topItemsChart,
  itemScopeChart,
  hasRevenueData,
  hasTopItemsData,
  hasItemScopeData,
  totalRevenue,
  totalOrders,
  isLoadingAnalytics,
  isLoadingOrders,
  isLoadingOrderDetails,
  isAiInsightsPanelOpen,
  aiPromptInput,
  aiPresetPrompts,
  latestAiInsight,
  analyticsError,
  ordersError,
  orderDetailsError,
  aiInsightsError,
  isLoadingAiInsights,
  toggleWeek,
  openOrder,
  closeOrder,
  openAiInsightsPanel,
  closeAiInsightsPanel,
  submitAiInsight
} = useAnalytics()

async function onAiPromptSubmit() {
  try {
    await submitAiInsight(aiPromptInput.value)
  } catch {
    // Error state is surfaced by the composable via aiInsightsError.
  }
}

async function onPresetPrompt(promptText) {
  aiPromptInput.value = promptText
  await onAiPromptSubmit()
}

const yearOptions = computed(() => {
  const start = 2024
  const end = 2030
  return Array.from({ length: end - start + 1 }, (_, index) => start + index)
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

const chartCardState = computed(() => {
  if (isLoadingAnalytics.value) {
    return 'Loading data...'
  }
  if (!hasRevenueData.value) {
    return 'No data for selected period. Showing empty baseline.'
  }
  return ''
})

const revenueOptions = computed(() => ({
  chart: {
    id: 'sales-trend',
    toolbar: { show: false },
    zoom: { enabled: false },
    foreColor: '#6a4b36'
  },
  stroke: {
    curve: 'smooth',
    width: 3
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 0.4,
      opacityFrom: 0.4,
      opacityTo: 0.08,
      stops: [0, 90, 100]
    }
  },
  colors: ['#ef4444', '#fb923c', '#f59e0b', '#f97316'],
  dataLabels: { enabled: false },
  grid: {
    borderColor: '#f4c7a7'
  },
  xaxis: {
    categories: revenueChart.value.categories,
    labels: {
      style: {
        fontSize: '11px'
      }
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => `$${Number(value).toFixed(0)}`
    }
  },
  legend: {
    show: scope.value === 'daily',
    position: 'top',
    horizontalAlign: 'left'
  },
  tooltip: {
    y: {
      formatter: (value) => `$${Number(value).toFixed(2)}`
    }
  }
}))

const topItemsOptions = computed(() => ({
  chart: {
    type: 'bar',
    toolbar: { show: false },
    foreColor: '#6a4b36'
  },
  plotOptions: {
    bar: {
      horizontal: true,
      borderRadius: 6,
      distributed: true,
      barHeight: '55%'
    }
  },
  colors: ['#fb923c', '#f97316', '#ef4444', '#fb7185', '#f59e0b'],
  dataLabels: { enabled: false },
  xaxis: {
    categories: topItemsChart.value.labels,
    labels: {
      formatter: (value) => Number(value).toFixed(0)
    }
  },
  grid: {
    borderColor: '#f4c7a7'
  }
}))

const topItemsSeries = computed(() => [
  {
    name: 'Qty',
    data: topItemsChart.value.values
  }
])

const monthlyItemOptions = computed(() => ({
  chart: {
    type: 'bar',
    toolbar: { show: false },
    foreColor: '#6a4b36'
  },
  colors: ['#9a3b18', '#c2410c', '#ea580c', '#f97316'],
  dataLabels: { enabled: false },
  plotOptions: {
    bar: {
      borderRadius: 5,
      columnWidth: '60%'
    }
  },
  xaxis: {
    categories: itemScopeChart.value.categories,
    labels: {
      style: {
        fontSize: '11px'
      }
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => Number(value).toFixed(0)
    }
  },
  legend: {
    show: false
  },
  grid: {
    borderColor: '#f4c7a7'
  }
}))

const monthlyItemSeries = computed(() => [
  ...itemScopeChart.value.series
])

const itemChartSubtitle = computed(() => {
  if (scope.value === 'daily') return 'Daily View'
  if (scope.value === 'weekly') return 'Weekly View'
  return 'Monthly View'
})

const itemChartState = computed(() => {
  if (isLoadingAnalytics.value) {
    return 'Loading data...'
  }
  if (!hasItemScopeData.value) {
    return 'No item quantity data for selected period.'
  }
  return ''
})
</script>

<template>
  <section class="analytics-screen">
    <div class="analytics-shell">
      <header class="analytics-header">
        <div>
          <p class="analytics-kicker">Performance Dashboard</p>
          <h1 class="analytics-title">Analytics</h1>
          <p class="analytics-subtitle">Get Business Insights, uncover patterns, and see your orders with more details</p>
        </div>

        <AuthTopNav />
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
          <p class="metric-card__value">Rs.{{ totalRevenue.toFixed(2) }}</p>
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
        <div class="chart-wrap">
          <apexchart type="area" height="270" :options="revenueOptions" :series="revenueChart.series" />
          <p v-if="chartCardState" class="chart-overlay-msg">{{ chartCardState }}</p>
        </div>
      </section>

      <section class="chart-card">
        <div class="chart-head">
          <h2>Top Selling Items</h2>
          <p class="chart-subtitle">Quantity sold</p>
        </div>
        <div class="chart-wrap">
          <apexchart type="bar" height="260" :options="topItemsOptions" :series="topItemsSeries" />
          <p v-if="!hasTopItemsData" class="chart-overlay-msg">No item quantity data yet.</p>
        </div>
      </section>

      <section class="chart-card">
        <div class="chart-head">
          <h2>Food Item Sales</h2>
          <p class="chart-subtitle">{{ itemChartSubtitle }}</p>
        </div>
        <div class="chart-wrap">
          <apexchart type="bar" height="260" :options="monthlyItemOptions" :series="monthlyItemSeries" />
          <p v-if="itemChartState" class="chart-overlay-msg">{{ itemChartState }}</p>
        </div>
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
              <p class="order-row__amount">Rs.{{ Number(order.total_price ?? 0).toFixed(2) }}</p>
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
          <button type="button" class="ai-insights-trigger" @click="openAiInsightsPanel">
            Get AI Insights
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
        </div>

        <div v-if="scope === 'daily'" class="week-chip-row">
          <p class="week-chip-row__label">Select up to 4 weeks:</p>
          <button
            v-for="weekValue in weekOptions"
            :key="weekValue"
            type="button"
            :class="['week-chip', { 'week-chip--active': selectedWeeks.includes(weekValue) }]"
            :disabled="!selectedWeeks.includes(weekValue) && !canSelectMoreWeeks"
            @click="toggleWeek(weekValue)"
          >
            W{{ weekValue }}
          </button>
        </div>

      </div>
    </div>

    <div v-if="selectedOrderId" class="order-drawer-backdrop" @click.self="closeOrder">
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
            <p><strong>Total:</strong> Rs.{{ Number(orderDetails.total_price ?? 0).toFixed(2) }}</p>
          </div>

          <ul v-if="orderItems.length" class="order-items-list">
            <li v-for="item in orderItems" :key="item.id" class="order-item-row">
              <div>
                <p class="order-item-row__name">{{ item.product_name }}</p>
                <p class="order-item-row__meta">Qty: {{ item.quantity }}</p>
              </div>
              <p class="order-item-row__amount">Rs.{{ Number(item.price ?? 0).toFixed(2) }}</p>
            </li>
          </ul>
          <p v-else class="status status--info">No line items found.</p>
        </template>
      </aside>
    </div>

    <div v-if="isAiInsightsPanelOpen" class="ai-panel-backdrop" @click.self="closeAiInsightsPanel">
      <aside class="ai-panel">
        <header class="ai-panel__head">
          <div>
            <h3>AI Sales Insights</h3>
            <p>Pick a quick prompt or ask your own question.</p>
          </div>
          <button type="button" class="btn-soft" @click="closeAiInsightsPanel">Close</button>
        </header>

        <div class="ai-prompt-chip-row">
          <button
            v-for="preset in aiPresetPrompts"
            :key="preset"
            type="button"
            class="ai-prompt-chip"
            :disabled="isLoadingAiInsights"
            @click="onPresetPrompt(preset)"
          >
            {{ preset }}
          </button>
        </div>

        <label class="ai-panel__label" for="ai-prompt-input">Ask for insight</label>
        <textarea
          id="ai-prompt-input"
          v-model="aiPromptInput"
          class="ai-panel__input"
          rows="4"
          maxlength="700"
          placeholder="Example: Compare this month's performance with last month and suggest 2 improvements."
        />

        <div class="ai-panel__actions">
          <button type="button" class="btn-primary" :disabled="isLoadingAiInsights" @click="onAiPromptSubmit">
            {{ isLoadingAiInsights ? 'Analyzing...' : 'Send to AI' }}
          </button>
        </div>

        <p v-if="aiInsightsError" class="status status--error">
          {{ aiInsightsError?.response?.data?.detail || 'Failed to get AI insights.' }}
        </p>

        <article v-if="latestAiInsight" class="ai-response-card">
          <p class="ai-response-card__title">Latest insight</p>
          <p class="ai-response-card__text">{{ latestAiInsight }}</p>
        </article>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.analytics-screen {
  padding: 0.65rem;
  padding-bottom: 10rem;
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

.chart-wrap {
  position: relative;
  margin-top: 0.45rem;
}

.chart-overlay-msg {
  position: absolute;
  left: 0.5rem;
  right: 0.5rem;
  bottom: 0.4rem;
  margin: 0;
  border-radius: 0.55rem;
  background: rgba(255, 250, 244, 0.92);
  border: 1px solid #f1c9a8;
  color: #7c5b45;
  font-size: 0.68rem;
  padding: 0.26rem 0.4rem;
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
  align-items: center;
  flex-wrap: wrap;
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

.week-chip-row {
  display: flex;
  align-items: center;
  gap: 0.34rem;
  flex-wrap: wrap;
}

.week-chip-row__label {
  margin: 0;
  color: #7c5b45;
  font-size: 0.68rem;
}

.week-chip {
  border: 1px solid #f1c9a8;
  background: #fff;
  color: #7b341c;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.28rem 0.55rem;
}

.week-chip--active {
  border-color: #ef4444;
  background: #ffe4cf;
}

.week-chip:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.ai-insights-trigger {
  border: 1px solid  #00F7FF;
  background:  #fdede0;
  color: #d744ff;
  border-radius: 0.82rem;
  font-size: 0.9rem;
  font-weight: 800;
  line-height: 1.15;
  padding: 0.34rem 0.55rem;
  white-space: nowrap;
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

.btn-soft {
  border: 1px solid #f1c9a8;
  border-radius: 0.65rem;
  background: #fff;
  color: #7b341c;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.36rem 0.62rem;
}

.btn-primary {
  border: 1px solid #ef4444;
  border-radius: 0.65rem;
  background: #8f2e11;
  color: #fff7ed;
  font-size: 0.76rem;
  font-weight: 700;
  padding: 0.42rem 0.75rem;
}

.btn-primary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.ai-panel-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(57, 33, 22, 0.4);
  z-index: 45;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.ai-panel {
  width: 100%;
  max-height: 72svh;
  border-radius: 1rem 1rem 0 0;
  border: 1px solid #f1c9a8;
  background: linear-gradient(180deg, #fff9f4 0%, #fffdf9 100%);
  padding: 0.8rem;
  display: grid;
  gap: 0.65rem;
  overflow: auto;
}

.ai-panel__head {
  display: flex;
  justify-content: space-between;
  gap: 0.55rem;
  align-items: flex-start;
}

.ai-panel__head h3 {
  margin: 0;
  font-size: 0.96rem;
  color: #492819;
}

.ai-panel__head p {
  margin: 0.2rem 0 0;
  font-size: 0.7rem;
  color: #7c5b45;
}

.ai-prompt-chip-row {
  display: grid;
  gap: 0.38rem;
}

.ai-prompt-chip {
  border: 1px solid #f1c9a8;
  border-radius: 0.68rem;
  background: #fff;
  color: #7b341c;
  text-align: left;
  font-size: 0.72rem;
  font-weight: 600;
  line-height: 1.3;
  padding: 0.45rem 0.55rem;
}

.ai-prompt-chip:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.ai-panel__label {
  font-size: 0.7rem;
  color: #7c5b45;
  font-weight: 700;
}

.ai-panel__input {
  width: 100%;
  resize: vertical;
  border: 1px solid #f1c9a8;
  border-radius: 0.7rem;
  background: #fff;
  color: #492819;
  padding: 0.5rem;
  font-size: 0.78rem;
  line-height: 1.4;
}

.ai-panel__actions {
  display: flex;
  justify-content: flex-end;
}

.ai-response-card {
  border: 1px solid #f1c9a8;
  border-radius: 0.8rem;
  background: #fff;
  padding: 0.6rem;
}

.ai-response-card__title {
  margin: 0;
  font-size: 0.72rem;
  color: #7c5b45;
  font-weight: 700;
}

.ai-response-card__text {
  margin: 0.3rem 0 0;
  font-size: 0.78rem;
  color: #492819;
  white-space: pre-wrap;
  line-height: 1.45;
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

  .ai-panel {
    width: min(640px, calc(100vw - 1.5rem));
    border-radius: 1rem;
    margin-bottom: 1rem;
    max-height: 70svh;
  }
}
</style>
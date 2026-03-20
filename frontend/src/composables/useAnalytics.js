import { computed, ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import api from '../api/axios'

export function useAnalytics() {
  const now = new Date()
  const scope = ref('monthly')
  const year = ref(now.getFullYear())
  const month = ref(now.getMonth() + 1)
  const week = ref(1)
  const ordersLimit = ref(50)
  const selectedOrderId = ref(null)

  const monthlySalesQuery = useQuery({
    queryKey: computed(() => ['analytics', 'monthly-sales', year.value]),
    queryFn: async () => {
      const response = await api.get(`/v1/analytics/monthly-sales/${year.value}`)
      return response.data
    }
  })

  const weeklySalesQuery = useQuery({
    queryKey: computed(() => ['analytics', 'weekly-sales', year.value, month.value]),
    queryFn: async () => {
      const response = await api.get(`/v1/analytics/weekly-sales/${year.value}/${month.value}`)
      return response.data
    },
    enabled: computed(() => scope.value === 'weekly' || scope.value === 'daily')
  })

  const dailySalesQuery = useQuery({
    queryKey: computed(() => ['analytics', 'daily-sales', year.value, month.value, week.value]),
    queryFn: async () => {
      const response = await api.get(`/v1/analytics/daily-sales/${year.value}/${month.value}/${week.value}`)
      return response.data
    },
    enabled: computed(() => scope.value === 'daily')
  })

  const topItemsQuery = useQuery({
    queryKey: ['analytics', 'top-selling-items'],
    queryFn: async () => {
      const response = await api.get('/v1/analytics/top-selling-items', {
        params: { limit: 5 }
      })
      return response.data
    }
  })

  const monthlyItemSalesQuery = useQuery({
    queryKey: computed(() => ['analytics', 'monthly-item-sales', year.value]),
    queryFn: async () => {
      const response = await api.get(`/v1/analytics/monthly-item-sales/${year.value}`)
      return response.data
    }
  })

  const ordersQuery = useQuery({
    queryKey: computed(() => ['orders', 'recent', ordersLimit.value]),
    queryFn: async () => {
      const response = await api.get('/v1/orders/', {
        params: {
          limit: ordersLimit.value,
          skip: 0
        }
      })
      return response.data
    }
  })

  const orderDetailsQuery = useQuery({
    queryKey: computed(() => ['orders', 'detail', selectedOrderId.value]),
    queryFn: async () => {
      const response = await api.get(`/v1/orders/${selectedOrderId.value}`)
      return response.data
    },
    enabled: computed(() => Boolean(selectedOrderId.value))
  })

  const orderItemsQuery = useQuery({
    queryKey: computed(() => ['orders', 'items', selectedOrderId.value]),
    queryFn: async () => {
      const response = await api.get(`/v1/orders/${selectedOrderId.value}/items`)
      return response.data
    },
    enabled: computed(() => Boolean(selectedOrderId.value))
  })

  const monthlySales = computed(() => monthlySalesQuery.data.value ?? [])
  const weeklySales = computed(() => weeklySalesQuery.data.value ?? [])
  const dailySales = computed(() => dailySalesQuery.data.value ?? [])
  const topItems = computed(() => topItemsQuery.data.value ?? [])
  const monthlyItemSales = computed(() => monthlyItemSalesQuery.data.value ?? [])
  const orders = computed(() => ordersQuery.data.value ?? [])

  const activeSalesRows = computed(() => {
    if (scope.value === 'daily') {
      return dailySales.value
    }
    if (scope.value === 'weekly') {
      return weeklySales.value
    }
    return monthlySales.value
  })

  const revenueChart = computed(() => {
    if (scope.value === 'daily') {
      return {
        labels: dailySales.value.map((row) => row.day),
        values: dailySales.value.map((row) => Number(row.total_sales ?? 0))
      }
    }

    if (scope.value === 'weekly') {
      return {
        labels: weeklySales.value.map((row, index) => `Week ${index + 1}`),
        values: weeklySales.value.map((row) => Number(row.total_sales ?? 0))
      }
    }

    return {
      labels: monthlySales.value.map((row) => row.month),
      values: monthlySales.value.map((row) => Number(row.total_sales ?? 0))
    }
  })

  const topItemsChart = computed(() => {
    return {
      labels: topItems.value.map((row) => row.item_name),
      values: topItems.value.map((row) => Number(row.total_quantity ?? 0))
    }
  })

  const monthlyQuantityChart = computed(() => {
    const monthTotals = new Map()

    for (const row of monthlyItemSales.value) {
      const current = monthTotals.get(row.month) ?? 0
      monthTotals.set(row.month, current + Number(row.total_quantity ?? 0))
    }

    const labels = Array.from(monthTotals.keys())
    const values = labels.map((monthLabel) => monthTotals.get(monthLabel))

    return { labels, values }
  })

  const totalRevenue = computed(() => {
    return activeSalesRows.value.reduce((sum, row) => sum + Number(row.total_sales ?? 0), 0)
  })

  const totalOrders = computed(() => orders.value.length)

  const weekOptions = computed(() => {
    const weeksCount = Math.max(weeklySales.value.length, 1)
    return Array.from({ length: Math.min(weeksCount, 5) }, (_, index) => index + 1)
  })

  function openOrder(orderId) {
    selectedOrderId.value = orderId
  }

  function closeOrder() {
    selectedOrderId.value = null
  }

  return {
    scope,
    year,
    month,
    week,
    weekOptions,
    ordersLimit,
    selectedOrderId,
    monthlySales,
    weeklySales,
    dailySales,
    topItems,
    monthlyItemSales,
    orders,
    orderDetails: computed(() => orderDetailsQuery.data.value ?? null),
    orderItems: computed(() => orderItemsQuery.data.value ?? []),
    revenueChart,
    topItemsChart,
    monthlyQuantityChart,
    totalRevenue,
    totalOrders,
    isLoadingAnalytics: computed(
      () =>
        monthlySalesQuery.isLoading.value ||
        weeklySalesQuery.isLoading.value ||
        dailySalesQuery.isLoading.value ||
        topItemsQuery.isLoading.value ||
        monthlyItemSalesQuery.isLoading.value
    ),
    isLoadingOrders: ordersQuery.isLoading,
    isLoadingOrderDetails: computed(
      () => orderDetailsQuery.isLoading.value || orderItemsQuery.isLoading.value
    ),
    analyticsError: computed(
      () =>
        monthlySalesQuery.error.value ||
        weeklySalesQuery.error.value ||
        dailySalesQuery.error.value ||
        topItemsQuery.error.value ||
        monthlyItemSalesQuery.error.value
    ),
    ordersError: ordersQuery.error,
    orderDetailsError: computed(() => orderDetailsQuery.error.value || orderItemsQuery.error.value),
    openOrder,
    closeOrder
  }
}

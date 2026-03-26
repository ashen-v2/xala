import { computed, ref } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'
import api from '../api/axios'

const MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const WEEK_LABELS = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
const DAY_LABELS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

export function useAnalytics() {
  const now = new Date()
  const scope = ref('monthly')
  const year = ref(now.getFullYear())
  const month = ref(now.getMonth() + 1)
  const selectedWeeks = ref([1])
  const ordersLimit = ref(50)
  const selectedOrderId = ref(null)
  const isAiInsightsPanelOpen = ref(false)
  const aiPromptInput = ref('')
  const latestAiInsight = ref('')
  const aiPresetPrompts = [
    'Summarize my sales trend for this year and highlight unusual changes.',
    'What are my top selling items recently, and what should I stock more?',
    'Give me 3 actions to improve next week revenue based on my sales pattern.'
  ]

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

  const dailySalesComparisonQuery = useQuery({
    queryKey: computed(() => [
      'analytics',
      'daily-sales-comparison',
      year.value,
      month.value,
      [...selectedWeeks.value].sort((a, b) => a - b).join('-')
    ]),
    queryFn: async () => {
      const sortedWeeks = [...selectedWeeks.value].sort((a, b) => a - b)
      const responses = await Promise.all(
        sortedWeeks.map(async (weekValue) => {
          const response = await api.get(
            `/v1/analytics/daily-sales/${year.value}/${month.value}/${weekValue}`
          )
          return {
            week: weekValue,
            rows: response.data
          }
        })
      )

      return responses
    },
    enabled: computed(() => scope.value === 'daily' && selectedWeeks.value.length > 0)
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

  const aiInsightsMutation = useMutation({
    mutationFn: async (promptText) => {
      const response = await api.post('/v1/ai/analytics', {
        data: promptText
      })
      return response.data
    }
  })

  const monthlySales = computed(() => monthlySalesQuery.data.value ?? [])
  const weeklySales = computed(() => weeklySalesQuery.data.value ?? [])
  const dailySalesByWeek = computed(() => dailySalesComparisonQuery.data.value ?? [])
  const topItems = computed(() => topItemsQuery.data.value ?? [])
  const monthlyItemSales = computed(() => monthlyItemSalesQuery.data.value ?? [])
  const orders = computed(() => ordersQuery.data.value ?? [])

  const monthlyPaddedValues = computed(() => {
    const monthTotals = new Map(MONTH_LABELS.map((label) => [label, 0]))

    for (const row of monthlySales.value) {
      const monthLabel = String(row.month ?? '').slice(0, 3)
      if (monthTotals.has(monthLabel)) {
        monthTotals.set(monthLabel, Number(row.total_sales ?? 0))
      }
    }

    return MONTH_LABELS.map((label) => monthTotals.get(label) ?? 0)
  })

  const weeklyPaddedValues = computed(() => {
    const values = [0, 0, 0, 0]

    weeklySales.value.forEach((row, index) => {
      if (index < 4) {
        values[index] = Number(row.total_sales ?? 0)
      }
    })

    return values
  })

  const dailySeriesByWeek = computed(() => {
    const weekLookup = new Map()

    dailySalesByWeek.value.forEach((group) => {
      const totals = new Map(DAY_LABELS.map((label) => [label, 0]))

      group.rows.forEach((row) => {
        const rawDay = String(row.day ?? '')
        const parts = rawDay.split('-')
        const dayLabel = parts[parts.length - 1]
        if (totals.has(dayLabel)) {
          totals.set(dayLabel, Number(row.total_sales ?? 0))
        }
      })

      weekLookup.set(group.week, DAY_LABELS.map((dayLabel) => totals.get(dayLabel) ?? 0))
    })

    return [...selectedWeeks.value].sort((a, b) => a - b).map((weekValue) => ({
      name: `Week ${weekValue}`,
      data: weekLookup.get(weekValue) ?? [0, 0, 0, 0, 0, 0, 0]
    }))
  })

  const revenueChart = computed(() => {
    if (scope.value === 'daily') {
      return {
        categories: DAY_LABELS,
        series: dailySeriesByWeek.value
      }
    }

    if (scope.value === 'weekly') {
      return {
        categories: WEEK_LABELS,
        series: [
          {
            name: 'Sales',
            data: weeklyPaddedValues.value
          }
        ]
      }
    }

    return {
      categories: MONTH_LABELS,
      series: [
        {
          name: 'Sales',
          data: monthlyPaddedValues.value
        }
      ]
    }
  })

  const topItemsChart = computed(() => {
    return {
      labels: topItems.value.map((row) => row.item_name),
      values: topItems.value.map((row) => Number(row.total_quantity ?? 0))
    }
  })

  const monthlyQuantityChart = computed(() => {
    const monthTotals = new Map(MONTH_LABELS.map((label) => [label, 0]))

    for (const row of monthlyItemSales.value) {
      const monthLabel = String(row.month ?? '').slice(0, 3)
      const current = monthTotals.get(monthLabel) ?? 0
      monthTotals.set(monthLabel, current + Number(row.total_quantity ?? 0))
    }

    const labels = MONTH_LABELS
    const values = labels.map((monthLabel) => monthTotals.get(monthLabel) ?? 0)

    return { labels, values }
  })

  const totalRevenue = computed(() => {
    return revenueChart.value.series.reduce(
      (seriesSum, series) =>
        seriesSum + series.data.reduce((sum, point) => sum + Number(point ?? 0), 0),
      0
    )
  })

  const totalOrders = computed(() => orders.value.length)

  const weekOptions = computed(() => {
    return [1, 2, 3, 4]
  })

  const canSelectMoreWeeks = computed(() => selectedWeeks.value.length < 4)

  const hasRevenueData = computed(() => {
    return revenueChart.value.series.some((series) =>
      series.data.some((point) => Number(point ?? 0) > 0)
    )
  })

  const hasTopItemsData = computed(() => topItemsChart.value.values.some((point) => point > 0))

  const hasMonthlyItemVolume = computed(() =>
    monthlyQuantityChart.value.values.some((point) => Number(point ?? 0) > 0)
  )

  function toggleWeek(weekValue) {
    if (!weekOptions.value.includes(weekValue)) return

    const hasWeek = selectedWeeks.value.includes(weekValue)

    if (hasWeek) {
      if (selectedWeeks.value.length === 1) {
        return
      }
      selectedWeeks.value = selectedWeeks.value.filter((item) => item !== weekValue)
      return
    }

    if (selectedWeeks.value.length >= 4) {
      return
    }

    selectedWeeks.value = [...selectedWeeks.value, weekValue].sort((a, b) => a - b)
  }

  function openOrder(orderId) {
    selectedOrderId.value = orderId
  }

  function closeOrder() {
    selectedOrderId.value = null
  }

  function openAiInsightsPanel() {
    isAiInsightsPanelOpen.value = true
  }

  function closeAiInsightsPanel() {
    isAiInsightsPanelOpen.value = false
  }

  async function submitAiInsight(promptText = aiPromptInput.value) {
    const nextPrompt = String(promptText ?? '').trim()
    if (!nextPrompt) {
      return
    }

    // Single-turn behavior: every new ask replaces previous output and errors.
    latestAiInsight.value = ''
    aiInsightsMutation.reset()
    aiPromptInput.value = nextPrompt

    const result = await aiInsightsMutation.mutateAsync(nextPrompt)
    latestAiInsight.value = String(result?.insights ?? '').trim()
  }

  return {
    scope,
    year,
    month,
    selectedWeeks,
    weekOptions,
    canSelectMoreWeeks,
    ordersLimit,
    selectedOrderId,
    isAiInsightsPanelOpen,
    aiPromptInput,
    aiPresetPrompts,
    latestAiInsight,
    monthlySales,
    weeklySales,
    dailySalesByWeek,
    topItems,
    monthlyItemSales,
    orders,
    orderDetails: computed(() => orderDetailsQuery.data.value ?? null),
    orderItems: computed(() => orderItemsQuery.data.value ?? []),
    revenueChart,
    topItemsChart,
    monthlyQuantityChart,
    hasRevenueData,
    hasTopItemsData,
    hasMonthlyItemVolume,
    totalRevenue,
    totalOrders,
    isLoadingAnalytics: computed(
      () =>
        monthlySalesQuery.isLoading.value ||
        weeklySalesQuery.isLoading.value ||
        dailySalesComparisonQuery.isLoading.value ||
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
        dailySalesComparisonQuery.error.value ||
        topItemsQuery.error.value ||
        monthlyItemSalesQuery.error.value
    ),
    ordersError: ordersQuery.error,
    orderDetailsError: computed(() => orderDetailsQuery.error.value || orderItemsQuery.error.value),
    aiInsightsError: aiInsightsMutation.error,
    isLoadingAiInsights: aiInsightsMutation.isPending,
    toggleWeek,
    openOrder,
    closeOrder,
    openAiInsightsPanel,
    closeAiInsightsPanel,
    submitAiInsight
  }
}

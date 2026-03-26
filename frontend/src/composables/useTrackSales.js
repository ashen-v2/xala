import { computed } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import api from '../api/axios'

const MENU_QUERY_KEY = ['menu-items']
const CART_QUERY_KEY = ['cart-items']

export function useTrackSales() {
  const queryClient = useQueryClient()

  const menuQuery = useQuery({
    queryKey: MENU_QUERY_KEY,
    queryFn: async () => {
      const response = await api.get('/v1/menu/')
      return response.data
    }
  })

  const cartQuery = useQuery({
    queryKey: CART_QUERY_KEY,
    queryFn: async () => {
      const response = await api.get('/v1/cart/')
      return response.data
    }
  })

  const addToCartMutation = useMutation({
    mutationFn: async ({ product_id, quantity = 1 }) => {
      await api.post('/v1/cart/', { product_id, quantity })
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: CART_QUERY_KEY })
    }
  })

  const updateCartItemMutation = useMutation({
    mutationFn: async ({ cartItemId, quantity }) => {
      await api.patch(`/v1/cart/${cartItemId}`, { quantity })
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: CART_QUERY_KEY })
    }
  })

  const removeCartItemMutation = useMutation({
    mutationFn: async (cartItemId) => {
      await api.delete(`/v1/cart/${cartItemId}`)
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: CART_QUERY_KEY })
    }
  })

  const createOrderMutation = useMutation({
    mutationFn: async () => {
      const response = await api.post('/v1/orders/')
      return response.data
    },
    onSuccess: async () => {
      await Promise.all([
        queryClient.invalidateQueries({ queryKey: CART_QUERY_KEY }),
        queryClient.invalidateQueries({ queryKey: ['orders'] })
      ])
    }
  })

  const menuItems = computed(() => menuQuery.data.value ?? [])
  const cartItems = computed(() => cartQuery.data.value ?? [])

  const cartByProductId = computed(() => {
    const map = new Map()
    for (const item of cartItems.value) {
      map.set(item.product_id, item)
    }
    return map
  })

  const menuById = computed(() => {
    const map = new Map()
    for (const item of menuItems.value) {
      map.set(item.id, item)
    }
    return map
  })

  const cartTotal = computed(() => {
    return cartItems.value.reduce((sum, cartItem) => {
      const menuItem = menuById.value.get(cartItem.product_id)
      const unitPrice = Number(menuItem?.price ?? 0)
      return sum + unitPrice * cartItem.quantity
    }, 0)
  })

  const cartCount = computed(() => {
    return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  return {
    menuItems,
    cartItems,
    cartByProductId,
    cartTotal,
    cartCount,
    isMenuLoading: menuQuery.isLoading,
    isCartLoading: cartQuery.isLoading,
    menuError: menuQuery.error,
    cartError: cartQuery.error,
    addToCart: addToCartMutation.mutateAsync,
    updateCartItem: updateCartItemMutation.mutateAsync,
    removeCartItem: removeCartItemMutation.mutateAsync,
    createOrder: createOrderMutation.mutateAsync,
    isAddingToCart: addToCartMutation.isPending,
    isUpdatingCart: updateCartItemMutation.isPending,
    isRemovingCartItem: removeCartItemMutation.isPending,
    isCreatingOrder: createOrderMutation.isPending,
    createdOrder: createOrderMutation.data,
    refetchCart: cartQuery.refetch
  }
}

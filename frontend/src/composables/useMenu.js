import { computed } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import api from '../api/axios'

const MENU_QUERY_KEY = ['menu-items']

export function useMenu() {
  const queryClient = useQueryClient()

  const menuQuery = useQuery({
    queryKey: MENU_QUERY_KEY,
    queryFn: async () => {
      const response = await api.get('/v1/menu/')
      return response.data
    }
  })

  const createItemMutation = useMutation({
    mutationFn: async (payload) => {
      const response = await api.post('/v1/menu/', payload)
      return response.data
    },
    onSuccess: (createdItem) => {
      queryClient.setQueryData(MENU_QUERY_KEY, (current = []) => [createdItem, ...current])
    }
  })

  const updateItemMutation = useMutation({
    mutationFn: async ({ itemId, payload }) => {
      const response = await api.patch(`/v1/menu/${itemId}`, payload)
      return response.data
    },
    onSuccess: (updatedItem) => {
      queryClient.setQueryData(MENU_QUERY_KEY, (current = []) =>
        current.map((item) => (item.id === updatedItem.id ? updatedItem : item))
      )
    }
  })

  const deleteItemMutation = useMutation({
    mutationFn: async (itemId) => {
      await api.delete(`/v1/menu/${itemId}`)
      return itemId
    },
    onSuccess: (deletedId) => {
      queryClient.setQueryData(MENU_QUERY_KEY, (current = []) =>
        current.filter((item) => item.id !== deletedId)
      )
    }
  })

  return {
    items: computed(() => menuQuery.data.value ?? []),
    isLoading: menuQuery.isLoading,
    isError: menuQuery.isError,
    error: menuQuery.error,
    refetch: menuQuery.refetch,
    createItem: createItemMutation.mutateAsync,
    updateItem: updateItemMutation.mutateAsync,
    deleteItem: deleteItemMutation.mutateAsync,
    isCreating: createItemMutation.isPending,
    isUpdating: updateItemMutation.isPending,
    isDeleting: deleteItemMutation.isPending
  }
}

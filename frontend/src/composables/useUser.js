import { computed } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import api from '../api/axios'

const USER_QUERY_KEY = ['current-user']

export function useUser() {
  const queryClient = useQueryClient()

  const userQuery = useQuery({
    queryKey: USER_QUERY_KEY,
    queryFn: async () => {
      const response = await api.get('/v1/users/me')
      return response.data
    }
  })

  const updateUserMutation = useMutation({
    mutationFn: async (payload) => {
      const response = await api.patch('/v1/users/me', payload)
      return response.data
    },
    onSuccess: (updatedUser) => {
      queryClient.setQueryData(USER_QUERY_KEY, updatedUser)
    }
  })

  return {
    user: computed(() => userQuery.data.value ?? null),
    isLoading: userQuery.isLoading,
    isError: userQuery.isError,
    error: userQuery.error,
    refetch: userQuery.refetch,
    updateUser: updateUserMutation.mutateAsync,
    isUpdating: updateUserMutation.isPending,
    updateError: updateUserMutation.error,
    isUpdateError: updateUserMutation.isError,
    isUpdateSuccess: updateUserMutation.isSuccess
  }
}

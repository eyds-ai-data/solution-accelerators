import { ref } from 'vue'
import type { GL } from '@/components/gl/data/schema'

interface ApiResponse<T> {
  status: string
  message: string
  data: T
}

interface PaginatedGLResponse {
  items: GL[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export const useGLTransactions = () => {
  const config = useRuntimeConfig()
  const glTransactions = ref<GL[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const pagination = ref({
    total: 0,
    page: 1,
    pageSize: 10,
    totalPages: 0
  })

  const fetchGLTransactions = async (urn?: string, page: number = 1, pageSize: number = 10) => {
    loading.value = true
    error.value = null
    
    try {
      const baseUrl = config.public.apiBase
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: pageSize.toString()
      })
      if (urn) {
        params.append('urn', urn)
      }
      const url = `${baseUrl}/api/v1/tax/gl-transactions?${params.toString()}`
      
      const response = await $fetch<ApiResponse<PaginatedGLResponse>>(url)
      
      if (response.status === 'Success') {
        glTransactions.value = response.data.items
        pagination.value = {
          total: response.data.total,
          page: response.data.page,
          pageSize: response.data.pageSize,
          totalPages: response.data.totalPages
        }
      } else {
        throw new Error(response.message || 'Failed to fetch GL transactions')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load GL transactions'
      console.error('Error fetching GL transactions:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    glTransactions,
    loading,
    error,
    pagination,
    fetchGLTransactions
  }
}

export const useGLTransactionDetail = () => {
  const config = useRuntimeConfig()
  const glTransaction = ref<GL | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchGLTransactionByUrn = async (urn: string) => {
    loading.value = true
    error.value = null
    
    try {
      const baseUrl = config.public.apiBase
      const url = `${baseUrl}/api/v1/tax/gl-transactions/${encodeURIComponent(urn)}`
      
      const response = await $fetch<ApiResponse<GL>>(url)
      
      if (response.status === 'Success') {
        glTransaction.value = response.data
      } else {
        throw new Error(response.message || 'Failed to fetch GL transaction')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load GL transaction'
      console.error('Error fetching GL transaction:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    glTransaction,
    loading,
    error,
    fetchGLTransactionByUrn
  }
}

export const useTaxInvoices = () => {
  const config = useRuntimeConfig()
  const taxInvoices = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchTaxInvoices = async (urn?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const baseUrl = config.public.apiBase
      const params = urn ? `?urn=${encodeURIComponent(urn)}` : ''
      const url = `${baseUrl}/api/v1/tax/tax-invoices${params}`
      
      const response = await $fetch<ApiResponse<any[]>>(url)
      
      if (response.status === 'Success') {
        taxInvoices.value = response.data
      } else {
        throw new Error(response.message || 'Failed to fetch tax invoices')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load tax invoices'
      console.error('Error fetching tax invoices:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    taxInvoices,
    loading,
    error,
    fetchTaxInvoices
  }
}

export const useInvoices = () => {
  const config = useRuntimeConfig()
  const invoices = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchInvoices = async (urn?: string) => {
    loading.value = true
    error.value = null
    
    try {
      const baseUrl = config.public.apiBase
      const params = urn ? `?urn=${encodeURIComponent(urn)}` : ''
      const url = `${baseUrl}/api/v1/tax/invoices${params}`
      
      const response = await $fetch<ApiResponse<any[]>>(url)
      
      if (response.status === 'Success') {
        invoices.value = response.data
      } else {
        throw new Error(response.message || 'Failed to fetch invoices')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load invoices'
      console.error('Error fetching invoices:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    invoices,
    loading,
    error,
    fetchInvoices
  }
}

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Invoice } from '@/components/invoice/data/schema'
import DataTableInvoices from '@/components/invoice/components/DataTableInvoices.vue'
import { invoiceDetailColumns } from '@/components/invoice/components/columns'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ArrowLeft } from 'lucide-vue-next'
import { Skeleton } from '@/components/ui/skeleton'
import { useInvoices } from '@/composables/useTaxApi'
import { formatNumber } from '@/components/gl/components/numbering'

const route = useRoute()
const router = useRouter()
const invoiceId = route.params.id as string

const { invoices, loading, error, fetchInvoices } = useInvoices()

// Fetch invoices on mount
onMounted(async () => {
  await fetchInvoices()
})

const invoice = computed(() => invoices.value.find(inv => inv.invoiceId === invoiceId) || null)

const goBack = () => {
  router.push('/mdm')
}
</script>

<template>
  <div v-if="loading" class="min-h-screen bg-muted/40">
    <div class="max-w-7xl mx-auto p-6 space-y-6">
      <!-- Header Skeleton -->
      <div class="flex items-start gap-4">
        <Skeleton class="h-10 w-10 rounded-md" />
        <Skeleton class="h-8 w-64" />
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Skeleton class="h-[500px]" />
        <div class="lg:col-span-2 space-y-4">
          <Skeleton class="h-32" />
          <Skeleton class="h-64" />
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="error" class="flex items-center justify-center min-h-screen">
    <div class="text-center max-w-md">
      <p class="text-destructive font-medium mb-2">Error loading invoice</p>
      <p class="text-sm text-muted-foreground mb-4">{{ error }}</p>
      <Button @click="goBack">Go Back to MDM</Button>
    </div>
  </div>

  <div v-else-if="invoice" class="min-h-screen bg-muted/40">
    <div class="max-w-7xl mx-auto p-6 space-y-6">
      <!-- Header -->
      <div class="flex items-start gap-4">
        <Button variant="ghost" size="icon" @click="goBack" class="mt-1">
          <ArrowLeft class="h-5 w-5" />
        </Button>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-foreground">
            Invoice: {{ invoice.invoiceNumber }}
          </h1>
          <p class="text-sm text-muted-foreground mt-1">URN: {{ invoice.urn }}</p>
        </div>
      </div>

      <!-- Invoice Detail -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- PDF Preview -->
        <Card class="h-[600px]">
          <CardHeader>
            <CardTitle class="text-lg">Document Preview</CardTitle>
          </CardHeader>
          <CardContent class="p-0">
            <div class="border-t h-[520px]">
              <iframe
                :src="invoice.documentUrl"
                class="w-full h-full"
                frameborder="0"
              ></iframe>
            </div>
          </CardContent>
        </Card>

        <!-- Invoice Info + Items -->
        <div class="space-y-6 lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Invoice Information</CardTitle>
              <CardDescription>Details about this invoice</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="grid grid-cols-2 gap-6">
                <div class="space-y-4">
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Invoice Number</label>
                    <p class="text-sm font-mono mt-1">{{ invoice.invoiceNumber }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">URN</label>
                    <p class="text-sm font-mono mt-1">{{ invoice.urn }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Project Number</label>
                    <p class="text-sm mt-1">{{ invoice.projectNumber }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Currency</label>
                    <div class="mt-1">
                      <Badge variant="outline">{{ invoice.currency }}</Badge>
                    </div>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Created At</label>
                    <p class="text-sm mt-1">{{ new Date(invoice.createdAt).toLocaleString() }}</p>
                  </div>
                </div>

                <div class="space-y-4">
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Subtotal Amount</label>
                    <p class="text-sm mt-1">{{ formatNumber(invoice.subTotalAmount) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">VAT ({{ invoice.vatPercentage }}%)</label>
                    <p class="text-sm mt-1">{{ formatNumber(invoice.vatAmount) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Discount Amount</label>
                    <p class="text-sm mt-1">{{ formatNumber(invoice.discountAmount) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">WHT ({{ invoice.whtPercentage }}%)</label>
                    <p class="text-sm mt-1">{{ formatNumber(invoice.whtAmount) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Total Amount</label>
                    <p class="text-sm font-semibold mt-1">{{ formatNumber(invoice.totalAmount) }}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Invoice Line Items</CardTitle>
              <CardDescription>Detailed breakdown of invoice items</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTableInvoices 
                :data="invoice.invoiceDetail ?? []" 
                :columns="invoiceDetailColumns" 
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="min-h-screen flex items-center justify-center bg-muted/40">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-foreground">Invoice Not Found</h2>
      <p class="text-muted-foreground mt-2">The invoice you are looking for does not exist.</p>
      <Button class="mt-4" @click="goBack">Go Back to MDM</Button>
    </div>
  </div>
</template>

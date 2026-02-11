<script setup lang="ts">
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Receipt, FileText } from 'lucide-vue-next'

// Import invoice components
import { invoiceMasterColumns } from '@/components/invoice/components/masterColumns'
import DataTableMasterInvoice from '@/components/invoice/components/DataTableMaster.vue'
import { useInvoices } from '@/composables/useTaxApi'

// Import tax invoice components
import { taxInvoiceMasterColumns } from '@/components/taxinvoice/components/masterColumns'
import DataTableMasterTaxInvoice from '@/components/taxinvoice/components/DataTableMaster.vue'
import { useTaxInvoices } from '@/composables/useTaxApi'

// Fetch invoices
const { invoices, loading: invoicesLoading, error: invoicesError, fetchInvoices } = useInvoices()

// Fetch tax invoices
const { taxInvoices, loading: taxInvoicesLoading, error: taxInvoicesError, fetchTaxInvoices } = useTaxInvoices()

// Fetch data on mount
onMounted(async () => {
  await Promise.all([
    fetchInvoices(),
    fetchTaxInvoices()
  ])
})

const activeTab = ref('invoices')
</script>

<template>
  <div class="w-full flex flex-col items-stretch gap-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">
          Master Data Management
        </h2>
        <p class="text-muted-foreground mt-1">
          View and manage all invoices and tax invoices
        </p>
      </div>
    </div>

    <!-- Tabs Content -->
    <Tabs v-model="activeTab" default-value="invoices" class="w-full">
      <TabsList class="grid w-full grid-cols-2 max-w-[400px]">
        <TabsTrigger value="invoices" class="flex items-center gap-2">
          <FileText class="size-4" />
          Invoices
        </TabsTrigger>
        <TabsTrigger value="tax-invoices" class="flex items-center gap-2">
          <Receipt class="size-4" />
          Tax Invoices
        </TabsTrigger>
      </TabsList>

      <!-- Invoices Tab -->
      <TabsContent value="invoices" class="mt-6">
        <Card>
          <CardHeader>
            <CardTitle>Invoices</CardTitle>
            <CardDescription>
              List of all invoices in the system
            </CardDescription>
          </CardHeader>
          <CardContent>
            <!-- Error Message -->
            <div v-if="invoicesError" class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-lg mb-4">
              <p class="font-medium">Error loading invoices</p>
              <p class="text-sm mt-1">{{ invoicesError }}</p>
            </div>

            <!-- Loading State -->
            <div v-if="invoicesLoading" class="space-y-4">
              <div class="space-y-4">
                <div v-for="i in 5" :key="i" class="flex items-center space-x-4">
                  <Skeleton class="h-12 w-full" />
                </div>
              </div>
            </div>

            <!-- Invoices Table -->
            <div v-else-if="invoices.length > 0">
              <DataTableMasterInvoice :data="invoices" :columns="invoiceMasterColumns" />
            </div>

            <!-- Empty State -->
            <div v-else class="flex flex-col items-center justify-center py-12">
              <FileText class="size-12 text-muted-foreground mb-4" />
              <p class="text-lg font-medium">No invoices found</p>
              <p class="text-sm text-muted-foreground">Upload invoices to see them here</p>
            </div>
          </CardContent>
        </Card>
      </TabsContent>

      <!-- Tax Invoices Tab -->
      <TabsContent value="tax-invoices" class="mt-6">
        <Card>
          <CardHeader>
            <CardTitle>Tax Invoices</CardTitle>
            <CardDescription>
              List of all tax invoices in the system
            </CardDescription>
          </CardHeader>
          <CardContent>
            <!-- Error Message -->
            <div v-if="taxInvoicesError" class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-lg mb-4">
              <p class="font-medium">Error loading tax invoices</p>
              <p class="text-sm mt-1">{{ taxInvoicesError }}</p>
            </div>

            <!-- Loading State -->
            <div v-if="taxInvoicesLoading" class="space-y-4">
              <div class="space-y-4">
                <div v-for="i in 5" :key="i" class="flex items-center space-x-4">
                  <Skeleton class="h-12 w-full" />
                </div>
              </div>
            </div>

            <!-- Tax Invoices Table -->
            <div v-else-if="taxInvoices.length > 0">
              <DataTableMasterTaxInvoice :data="taxInvoices" :columns="taxInvoiceMasterColumns" />
            </div>

            <!-- Empty State -->
            <div v-else class="flex flex-col items-center justify-center py-12">
              <Receipt class="size-12 text-muted-foreground mb-4" />
              <p class="text-lg font-medium">No tax invoices found</p>
              <p class="text-sm text-muted-foreground">Upload tax invoices to see them here</p>
            </div>
          </CardContent>
        </Card>
      </TabsContent>
    </Tabs>
  </div>
</template>

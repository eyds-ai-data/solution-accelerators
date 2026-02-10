<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { TaxInvoice } from '@/components/taxinvoice/data/schema'
import DataTableTaxInvoices from '@/components/taxinvoice/components/DataTableTaxInvoices.vue'
import { taxInvoiceDetailColumns } from '@/components/taxinvoice/components/columns'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ArrowLeft } from 'lucide-vue-next'
import { Skeleton } from '@/components/ui/skeleton'
import { useTaxInvoices } from '@/composables/useTaxApi'
import { formatNumber } from '@/components/gl/components/numbering'

const route = useRoute()
const router = useRouter()
const taxInvoiceId = route.params.id as string

const { taxInvoices, loading, error, fetchTaxInvoices } = useTaxInvoices()

// Fetch tax invoices on mount
onMounted(async () => {
  await fetchTaxInvoices()
})

const taxInvoice = computed(() => taxInvoices.value.find(inv => inv.taxInvoiceId === taxInvoiceId) || null)

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
      <p class="text-destructive font-medium mb-2">Error loading tax invoice</p>
      <p class="text-sm text-muted-foreground mb-4">{{ error }}</p>
      <Button @click="goBack">Go Back to MDM</Button>
    </div>
  </div>

  <div v-else-if="taxInvoice" class="min-h-screen bg-muted/40">
    <div class="max-w-7xl mx-auto p-6 space-y-6">
      <!-- Header -->
      <div class="flex items-start gap-4">
        <Button variant="ghost" size="icon" @click="goBack" class="mt-1">
          <ArrowLeft class="h-5 w-5" />
        </Button>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-foreground">
            Tax Invoice: {{ taxInvoice.taxInvoiceNumber }}
          </h1>
          <p class="text-sm text-muted-foreground mt-1">URN: {{ taxInvoice.urn }}</p>
        </div>
      </div>

      <!-- Tax Invoice Detail -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- PDF Preview -->
        <Card class="h-[600px]">
          <CardHeader>
            <CardTitle class="text-lg">Document Preview</CardTitle>
          </CardHeader>
          <CardContent class="p-0">
            <div class="border-t h-[520px]">
              <iframe
                :src="taxInvoice.documentUrl"
                class="w-full h-full"
                frameborder="0"
              ></iframe>
            </div>
          </CardContent>
        </Card>

        <!-- Tax Invoice Info + Items -->
        <div class="space-y-6 lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Tax Invoice Information</CardTitle>
              <CardDescription>Seller (PKP) Information</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="grid grid-cols-2 gap-6">
                <div class="space-y-4">
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Tax Invoice Number</label>
                    <p class="text-sm font-mono mt-1">{{ taxInvoice.taxInvoiceNumber }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Invoice Number</label>
                    <p class="text-sm font-mono mt-1">{{ taxInvoice.invoiceNumber }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">URN</label>
                    <p class="text-sm font-mono mt-1">{{ taxInvoice.urn }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Tax Invoice Date</label>
                    <p class="text-sm mt-1">{{ new Date(taxInvoice.taxInvoiceDate).toLocaleDateString() }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">PKP Name</label>
                    <p class="text-sm mt-1">{{ taxInvoice.namaPengusahaKenaPajak }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">PKP Address</label>
                    <p class="text-sm mt-1">{{ taxInvoice.alamatPengusahaKenaPajak }}</p>
                  </div>
                </div>

                <div class="space-y-4">
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">PKP NPWP</label>
                    <p class="text-sm font-mono mt-1">{{ taxInvoice.npwpPengusahaKenaPajak }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Buyer Name</label>
                    <p class="text-sm mt-1">{{ taxInvoice.namaPembeliKenaPajak }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Buyer Address</label>
                    <p class="text-sm mt-1">{{ taxInvoice.alamatPembeliKenaPajak }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Buyer NPWP</label>
                    <p class="text-sm font-mono mt-1">{{ taxInvoice.npwpPembeliKenaPajak }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Buyer Email</label>
                    <p class="text-sm mt-1">{{ taxInvoice.emailPembeliKenaPajak || '-' }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Created At</label>
                    <p class="text-sm mt-1">{{ new Date(taxInvoice.createdAt).toLocaleString() }}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Tax Amounts</CardTitle>
              <CardDescription>Tax calculation details</CardDescription>
            </CardHeader>
            <CardContent>
              <div class="grid grid-cols-2 gap-6">
                <div class="space-y-4">
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Total Tax Base WHT</label>
                    <p class="text-sm mt-1">{{ formatNumber(taxInvoice.totalTaxBaseWht) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Discount</label>
                    <p class="text-sm mt-1">{{ formatNumber(taxInvoice.dikurangiPotonganHarga) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Down Payment Received</label>
                    <p class="text-sm mt-1">{{ formatNumber(taxInvoice.dikurangiUangMukaYangTelahDiterima) }}</p>
                  </div>
                </div>

                <div class="space-y-4">
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">Tax Base (DPP)</label>
                    <p class="text-sm mt-1">{{ formatNumber(taxInvoice.dasarPengenaanPajak) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">PPN Amount</label>
                    <p class="text-sm font-semibold mt-1">{{ formatNumber(taxInvoice.jumlahPpn) }}</p>
                  </div>
                  <div>
                    <label class="text-sm font-medium text-muted-foreground">PPnBM Amount</label>
                    <p class="text-sm mt-1">{{ formatNumber(taxInvoice.jumlahPpnbm) }}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Tax Invoice Line Items</CardTitle>
              <CardDescription>Detailed breakdown of taxable items</CardDescription>
            </CardHeader>
            <CardContent>
              <DataTableTaxInvoices 
                :data="taxInvoice.taxInvoiceDetail ?? []" 
                :columns="taxInvoiceDetailColumns" 
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="min-h-screen flex items-center justify-center bg-muted/40">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-foreground">Tax Invoice Not Found</h2>
      <p class="text-muted-foreground mt-2">The tax invoice you are looking for does not exist.</p>
      <Button class="mt-4" @click="goBack">Go Back to MDM</Button>
    </div>
  </div>
</template>

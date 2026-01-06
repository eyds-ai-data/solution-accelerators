<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { GL } from '@/components/gl/data/schema'
import glData from '@/components/gl/data/glTable.json'
import type { Invoice } from '@/components/invoice/data/schema'
import invoiceData from '@/components/invoice/data/invoice.json'
import DataTableGLItems from '@/components/gl/components/DataTableGLItems.vue'
import DataTableInvoices from '@/components/invoice/components/DataTableInvoices.vue'
import { glReconColumns } from '@/components/gl/components/glReconItems'
import { invoiceDetailColumns } from '@/components/invoice/components/columns'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  ArrowLeft,
  MapPin,
  Clock,
  Calendar,
  Briefcase,
  Users,
  Building2,
  DollarSign,
  MoreHorizontal,
  Edit,
  Trash2,
  CheckCircle2,
  Save
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const gls = (glData as { data: GL[] }).data
const glId = route.params.urn as string
const gl = computed(() => gls.find(g => g.urn === glId))
const invoices = (invoiceData as { data: Invoice[] }).data
const invoice = computed(() => invoices.find(i => i.urn === glId))
const reconItems = computed(() => gl.value?.glReconItem ?? [])

const goBack = () => {
  router.back()
}

const formatCurrency = (amount: number, currency: string) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    maximumFractionDigits: 0
  }).format(amount)
}

const activeTab = ref<'invoice' | 'tax'>('invoice')
const invoicePdfUrl = computed(() => {
  if (!invoice.value) return ''
  return `/invoices/${invoice.value.urn}.pdf`
})
</script>

<template>
  <div v-if="gl" class="min-h-screen bg-muted/40">
    <div class="max-w-7xl mx-auto p-6 space-y-6">
      
      <!-- Header -->
      <div class="flex flex-col sm:flex-row justify-between items-start gap-4">
        <div class="flex items-start gap-4">
          <Button variant="ghost" size="icon" @click="goBack" class="mt-1">
            <ArrowLeft class="h-5 w-5" />
          </Button>
          <div>
            <div class="flex items-center gap-3 mb-1">
              <h1 class="text-2xl font-bold tracking-tight text-foreground">URN: {{ gl.urn }}</h1>
            </div>
          </div>
        </div>
        
        <div class="flex gap-2">
          <Button variant="outline">
            Cancel
          </Button>
          <Button variant="outline">
            Save
          </Button>
          <Button variant="outline">
            Export
          </Button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- GL Detail -->
        <div class="lg:col-span-2 space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

            <!-- LEFT COLUMN -->
            <div class="space-y-3">
              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Vendor Name</strong></span>
                <span class="font-medium">{{ gl.vendorId }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Reference</strong></span>
                <span class="font-medium">{{ gl.referenceNumber }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Document No</strong></span>
                <span class="font-medium">{{ gl.documentNumber }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>PO Number</strong></span>
                <span class="font-medium">{{ gl.poNumber }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Document Date</strong></span>
                <span class="font-medium">{{ gl.documentDate }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>WHT Review</strong></span>
                <span class="font-medium">Transaction</span>
              </div>
            </div>

            <!-- RIGHT COLUMN -->
            <div class="space-y-3">
              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Diff Normal</strong></span>
                <span class="font-medium">{{ gl.diffNormal }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Ref</strong></span>
                <span class="font-medium">{{ gl.ref }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>1st Vouching</strong></span>
                <span class="font-medium">{{ gl.firstVouching }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>2nd Reviewer</strong></span>
                <span class="font-medium">{{ gl.secondReviewer }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>WHT Slip Number</strong></span>
                <span class="font-medium">{{ gl.whtSlipNumber }}</span>
              </div>

              <div class="flex justify-between items-center text-sm min-h-[36px]">
                <span class="text-muted-foreground"><strong>Document Type</strong></span>
                <input
                  type="text"
                  class="w-48 rounded-md border px-2 py-1 text-sm"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- GL vs Recon -->
        <div class="lg:col-span-2 space-y-6">
          <Card>
            <CardContent>
              <div class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- GL -->
                  <div class="space-y-3">
                    <h1 class="text-2xl font-bold tracking-tight text-foreground text-center">G/L</h1>
                  
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Tax Based</strong></span>
                      <span class="font-medium">{{ gl.taxBased }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT</strong></span>
                      <span class="font-medium">{{ gl.wht }}</span>
                    </div>
                  </div>

                  <!-- RECON -->
                  <div class="space-y-3">
                    <h1 class="text-2xl font-bold tracking-tight text-foreground text-center">Recon</h1>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Tax Base WHT (Normal)</strong></span>
                      <input
                        type="text"
                        class="w-48 rounded-md border px-2 py-1 text-sm"
                      />
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT (Normal)</strong></span>
                      <input
                        type="text"
                        class="w-48 rounded-md border px-2 py-1 text-sm"
                      />
                    </div>
                  </div>
                </div>
                
                <div>
                  <!-- GL Table -->
                  <DataTableGLItems :data="gl?.glReconItem ?? []" :columns="glReconColumns" />
                </div>

                <!-- GL Details -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- Left -->
                  <div class="space-y-3">
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>CoCd</strong></span>
                      <span class="font-medium">{{ gl.cocd }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>G/L</strong></span>
                      <span class="font-medium">{{ gl.gl }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Year/Month</strong></span>
                      <span class="font-medium">{{ gl.yearMonth }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Type</strong></span>
                      <span class="font-medium">{{ gl.type }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>User Name</strong></span>
                      <span class="font-medium">{{ gl.username }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Text</strong></span>
                      <span class="font-medium">{{ gl.text }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Clearing Document</strong></span>
                      <span class="font-medium">{{ gl.clearingDocument }}</span>
                    </div>
                  </div>

                  <!-- Right -->
                  <div class="space-y-3">
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Document Currency</strong></span>
                      <span class="font-medium">{{ gl.documentCurrency }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Amount in Document Currency</strong></span>
                      <span class="font-medium">{{ gl.amountInDocumentCurrency }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Local Currency</strong></span>
                      <span class="font-medium">{{ gl.localCurrency }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Amount in Local Currency</strong></span>
                      <span class="font-medium">{{ gl.amountInLocalCurrency }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Tax Based</strong></span>
                      <span class="font-medium">{{ gl.taxBased }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Tax Rate</strong></span>
                      <span class="font-medium">{{ gl.taxRate }}</span>
                    </div>

                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT</strong></span>
                      <span class="font-medium">{{ gl.wht }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
        <!-- GL Detail -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Tabs -->
          <div class="flex border-b border-gray-200 mb-4">
            <button
              class="px-4 py-2 font-medium"
              :class="activeTab === 'invoice' ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'"
              @click="activeTab = 'invoice'"
            >
              Invoice Detail
            </button>
            <button
              class="px-4 py-2 font-medium"
              :class="activeTab === 'tax' ? 'border-b-2 border-blue-500 text-blue-500' : 'text-gray-500'"
              @click="activeTab = 'tax'"
            >
              Tax Invoice Detail
            </button>
          </div>

          <!-- Tab Panels -->
          <div>
            <!-- Invoice Detail Tab -->
            <div v-if="activeTab === 'invoice'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <!-- PDF preview -->
              <div class="border rounded-md overflow-hidden h-[500px]">
                <iframe
                  :src="invoicePdfUrl"
                  class="w-full h-full"
                  frameborder="0"
                ></iframe>
              </div>

              <!-- Invoice Info + Items -->
              <div class="space-y-4 lg:col-span-2">
                <!-- Fields -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Invoice Number</strong></span>
                      <span class="font-medium">{{ invoice?.invoiceNumber }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Invoice Date</strong></span>
                      <span class="font-medium">{{ invoice?.createdAt }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Project Number</strong></span>
                      <span class="font-medium">{{ invoice?.projectNumber }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Currency</strong></span>
                      <span class="font-medium">{{ invoice?.currency }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Sub Total Amount</strong></span>
                      <span class="font-medium">{{ invoice?.subTotalAmount }}</span>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>VAT %</strong></span>
                      <span class="font-medium">{{ invoice?.vatPercentage }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>VAT Amount</strong></span>
                      <span class="font-medium">{{ invoice?.vatAmount }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT %</strong></span>
                      <span class="font-medium">{{ invoice?.whtPercentage }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT Amount</strong></span>
                      <span class="font-medium">{{ invoice?.whtAmount }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Total Amount</strong></span>
                      <span class="font-medium">{{ invoice?.totalAmount }}</span>
                    </div>
                  </div>
                </div>
                
                  <!-- Invoice Detail Table -->
                <div>
                  <DataTableInvoices :data="invoice?.invoiceDetail ?? []" :columns="invoiceDetailColumns" />
                </div>
              </div>
            </div>

            <!-- Tax Invoice Tab -->
            <div v-if="activeTab === 'tax'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <!-- PDF preview -->
              <div class="border rounded-md overflow-hidden h-[500px]">
                <iframe
                  :src="invoicePdfUrl"
                  class="w-full h-full"
                  frameborder="0"
                ></iframe>
              </div>

              <!-- Tax Invoice Info + Table -->
              <div class="space-y-4 lg:col-span-2">
                <!-- Fields -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Invoice Number</strong></span>
                      <span class="font-medium">{{ invoice?.invoiceNumber }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Invoice Date</strong></span>
                      <span class="font-medium">{{ invoice?.createdAt }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Project Number</strong></span>
                      <span class="font-medium">{{ invoice?.projectNumber }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Currency</strong></span>
                      <span class="font-medium">{{ invoice?.currency }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Sub Total Amount</strong></span>
                      <span class="font-medium">{{ invoice?.subTotalAmount }}</span>
                    </div>
                  </div>
                  <div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>VAT %</strong></span>
                      <span class="font-medium">{{ invoice?.vatPercentage }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>VAT Amount</strong></span>
                      <span class="font-medium">{{ invoice?.vatAmount }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT %</strong></span>
                      <span class="font-medium">{{ invoice?.whtPercentage }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>WHT Amount</strong></span>
                      <span class="font-medium">{{ invoice?.whtAmount }}</span>
                    </div>
                    <div class="flex justify-between items-center text-sm min-h-[36px]">
                      <span class="text-muted-foreground"><strong>Total Amount</strong></span>
                      <span class="font-medium">{{ invoice?.totalAmount }}</span>
                    </div>
                  </div>
                </div>
                
                  <!-- Invoice Detail Table -->
                <div>
                  <!-- <DataTableInvoices :data="invoice?.invoiceDetail ?? []" :columns="invoiceDetailColumns" /> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="min-h-screen flex items-center justify-center bg-muted/40">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-foreground">Job Not Found</h2>
      <p class="text-muted-foreground mt-2">The job you are looking for does not exist.</p>
      <Button class="mt-4" @click="goBack">Go Back</Button>
    </div>
  </div>
</template>

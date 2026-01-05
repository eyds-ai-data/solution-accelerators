<script setup lang="ts">
import { ArrowLeft, UploadCloud, Loader2, RefreshCw } from 'lucide-vue-next'
import { toast } from 'vue-sonner'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

const router = useRouter()
const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)

interface UploadedFile {
  id: string
  originalFilename: string
  created_at: string
  status: string
  urn?: string
}

const page = ref(1)
const pageSize = ref(5)

const { data, status, error, refresh } = await useFetch('http://localhost:8000/api/v1/upload/list', {
  query: computed(() => ({
    page: page.value,
    page_size: pageSize.value,
  })),
})

const uploadedFiles = computed<UploadedFile[]>(() => {
  const responseData = data.value as any
  return responseData?.data?.items || []
})

const total = computed(() => {
  const responseData = data.value as any
  return responseData?.data?.total || 0
})

const goBack = () => {
  router.back()
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  const file = input.files[0]
  if (!file) return
  await uploadFile(file)
}

const handleDrop = async (event: DragEvent) => {
  event.preventDefault()
  if (!event.dataTransfer?.files || event.dataTransfer.files.length === 0) return

  const file = event.dataTransfer.files[0]
  if (!file) return
  await uploadFile(file)
}

const uploadFile = async (file: File) => {
  isUploading.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    // Using the generic file upload endpoint for invoices (PDFs)
    const { data, error } = await useFetch('http://localhost:8000/api/v1/upload/file', {
      method: 'POST',
      body: formData,
    })

    if (error.value) {
      throw new Error(error.value.message)
    }

    toast.success('File uploaded successfully')
    await refresh()
  }
  catch (err: any) {
    toast.error(`Upload failed: ${err.message}`)
  }
  finally {
    isUploading.value = false
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}
</script>

<template>
  <div class="w-full flex flex-col items-stretch gap-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <Button variant="ghost" size="icon" @click="goBack">
        <ArrowLeft class="h-4 w-4" />
      </Button>
      <div>
        <h2 class="text-2xl font-bold tracking-tight">
          Upload Tax Invoices/Invoices
        </h2>
        <p class="text-muted-foreground mt-1">
          Upload your Tax Invoices or Invoices for processing
        </p>
      </div>
    </div>

    <!-- Upload Area -->
    <div
      class="border-2 border-dashed rounded-lg p-12 flex flex-col items-center justify-center text-center transition-colors hover:bg-muted/50 cursor-pointer"
      :class="{ 'opacity-50 pointer-events-none': isUploading }"
      @click="triggerFileInput"
      @dragover.prevent
      @drop.prevent="handleDrop"
    >
      <input
        ref="fileInput"
        type="file"
        accept=".pdf"
        class="hidden"
        @change="handleFileSelect"
      >
      <div class="p-4 rounded-full bg-muted mb-4">
        <Loader2 v-if="isUploading" class="h-8 w-8 animate-spin text-muted-foreground" />
        <UploadCloud v-else class="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 class="text-lg font-semibold">
        {{ isUploading ? 'Uploading...' : 'Click to upload or drag and drop' }}
      </h3>
      <p class="text-sm text-muted-foreground mt-1">
        PDF (MAX. 10MB)
      </p>
      <Button class="mt-4" :disabled="isUploading">
        {{ isUploading ? 'Uploading...' : 'Select File' }}
      </Button>
    </div>

    <!-- Uploaded Files List -->
    <div class="mt-8 space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-xl font-semibold">
            Uploaded Documents
          </h3>
          <p class="text-sm text-muted-foreground">
            Refresh the list to see the latest status updates.
          </p>
        </div>
        <Button variant="outline" size="sm" :disabled="status === 'pending'" @click="refresh">
          <RefreshCw class="h-4 w-4 mr-2" :class="{ 'animate-spin': status === 'pending' }" />
          Refresh
        </Button>
      </div>
      <div class="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Filename</TableHead>
              <TableHead>Uploaded At</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>URN</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="file in uploadedFiles" :key="file.id">
              <TableCell>{{ file.originalFilename }}</TableCell>
              <TableCell>{{ file.created_at ? new Date(file.created_at).toLocaleString() : '-' }}</TableCell>
              <TableCell>
                <Badge
                  variant="outline"
                  :class="{
                    'bg-yellow-100 text-yellow-800 border-yellow-200': file.status === 'processing',
                    'bg-green-100 text-green-800 border-green-200': file.status === 'done',
                    'bg-gray-100 text-gray-800 border-gray-200': !['processing', 'done'].includes(file.status),
                  }"
                >
                  {{ file.status || 'Uploaded' }}
                </Badge>
              </TableCell>
              <TableCell>
                <span v-if="file.urn" class="font-mono text-sm">{{ file.urn }}</span>
                <span v-else class="text-muted-foreground">-</span>
              </TableCell>
            </TableRow>
            <TableRow v-if="uploadedFiles.length === 0">
              <TableCell colspan="4" class="text-center text-muted-foreground h-24">
                No documents uploaded yet.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>

      <div class="mt-4 flex justify-end">
        <Pagination v-if="total > 0" v-model:page="page" :total="total" :items-per-page="pageSize" :sibling-count="1" show-edges>
          <PaginationContent v-slot="{ items }">
            <PaginationItem class="w-auto h-auto p-0 bg-transparent border-none hover:bg-transparent">
              <PaginationPrevious />
            </PaginationItem>

            <template v-for="(item, index) in items">
              <PaginationItem v-if="item.type === 'page'" :key="index" :value="item.value" :is-active="item.value === page">
                {{ item.value }}
              </PaginationItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <PaginationItem class="w-auto h-auto p-0 bg-transparent border-none hover:bg-transparent">
              <PaginationNext />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  </div>
</template>

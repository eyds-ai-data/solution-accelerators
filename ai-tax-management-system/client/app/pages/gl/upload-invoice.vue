<script setup lang="ts">
import { ArrowLeft, UploadCloud, Loader2, RefreshCw, CheckCircle2, XCircle, Upload } from 'lucide-vue-next'
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
import { Progress } from '@/components/ui/progress'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'
import { Skeleton } from '@/components/ui/skeleton'

const router = useRouter()
const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)

interface UploadedFile {
  id: string
  originalFilename: string
  created_at: string
  status: string
  urn?: string
  completed_at?: string
}

interface FileUploadProgress {
  file: File
  status: 'pending' | 'uploading' | 'success' | 'error'
  progress: number
  error?: string
}

const uploadQueue = ref<FileUploadProgress[]>([])
const page = ref(1)
const pageSize = ref(5)
const MAX_CONCURRENT_UPLOADS = 3 // Limit concurrent uploads to avoid overwhelming the server

const config = useRuntimeConfig()
const { data, status, error, refresh } = await useFetch(`${config.public.apiBase}/api/v1/upload/list`, {
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

const uploadProgress = computed(() => {
  const total = uploadQueue.value.length
  if (total === 0) return 0
  const completed = uploadQueue.value.filter(f => f.status === 'success' || f.status === 'error').length
  return Number((completed / total * 100).toFixed(2))
})

const successCount = computed(() => uploadQueue.value.filter(f => f.status === 'success').length)
const failCount = computed(() => uploadQueue.value.filter(f => f.status === 'error').length)

const goBack = () => {
  router.back()
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files || input.files.length === 0) return

  const files = Array.from(input.files)
  await uploadFiles(files)
}

const handleDrop = async (event: DragEvent) => {
  event.preventDefault()
  if (!event.dataTransfer?.files || event.dataTransfer.files.length === 0) return

  const files = Array.from(event.dataTransfer.files)
  await uploadFiles(files)
}

const uploadSingleFile = async (fileProgress: FileUploadProgress): Promise<void> => {
  const formData = new FormData()
  formData.append('file', fileProgress.file)

  try {
    const config = useRuntimeConfig()
    const { data, error } = await useFetch(`${config.public.apiBase}/api/v1/upload/file`, {
      method: 'POST',
      body: formData,
    })

    if (error.value) {
      throw new Error(error.value.message || 'Upload failed')
    }

    fileProgress.status = 'success'
    fileProgress.progress = 100
  }
  catch (err: any) {
    fileProgress.status = 'error'
    fileProgress.error = err.message || 'Upload failed'
    console.error(`Failed to upload ${fileProgress.file.name}:`, err)
  }
}

const processUploadQueue = async (): Promise<void> => {
  const pendingFiles = uploadQueue.value.filter(f => f.status === 'pending')
  const activeUploads: Promise<void>[] = []

  for (const fileProgress of pendingFiles) {
    // Wait until we have available slots
    while (activeUploads.length >= MAX_CONCURRENT_UPLOADS) {
      await Promise.race(activeUploads)
      // Remove completed uploads from active list
      const completedIndex = activeUploads.findIndex(
        p => uploadQueue.value.find(f => f.file === (p as any)?.file)?.status !== 'uploading'
      )
      if (completedIndex !== -1) {
        activeUploads.splice(completedIndex, 1)
      }
    }

    fileProgress.status = 'uploading'
    fileProgress.progress = 0

    // Simulate progress (since we don't have actual upload progress from the API)
    const progressInterval = setInterval(() => {
      if (fileProgress.progress < 90) {
        fileProgress.progress = Number((fileProgress.progress + Math.random() * 20).toFixed(2))
      }
    }, 200)

    const uploadPromise = uploadSingleFile(fileProgress)
    activeUploads.push(uploadPromise)

    uploadPromise.finally(() => {
      clearInterval(progressInterval)
    })
  }

  // Wait for all remaining uploads to complete
  await Promise.all(activeUploads)
}

const uploadFiles = async (files: File[]) => {
  if (files.length === 0) return

  isUploading.value = true

  // Initialize upload queue
  uploadQueue.value = files.map(file => ({
    file,
    status: 'pending' as const,
    progress: 0,
  }))

  try {
    // Process uploads with concurrency limit
    await processUploadQueue()

    // Show summary toast
    if (successCount.value > 0 && failCount.value === 0) {
      toast.success(`${successCount.value} file${successCount.value > 1 ? 's' : ''} uploaded successfully`)
    } else if (successCount.value > 0 && failCount.value > 0) {
      toast.warning(`${successCount.value} succeeded, ${failCount.value} failed`)
    } else if (failCount.value > 0) {
      toast.error(`Failed to upload ${failCount.value} file${failCount.value > 1 ? 's' : ''}`)
    }

    // Clear queue after a delay
    setTimeout(() => {
      uploadQueue.value = []
    }, 3000)

    await refresh()
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
        <h2 class="text-xl font-bold tracking-tight">
          Upload Invoices
        </h2>
        <p class="text-muted-foreground mt-1">
          Please upload your <span class="font-bold">commercial invoices</span> or <span class="font-bold">tax invoices</span> for processing
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
        multiple
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
        PDF files (MAX. 10MB each) • Multiple files supported
      </p>
      <Button class="mt-4" :disabled="isUploading">
        {{ isUploading ? 'Uploading...' : 'Select File' }}
      </Button>
    </div>

    <!-- Upload Progress Section -->
    <div v-if="uploadQueue.length > 0" class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold">
            Upload Progress
          </h3>
          <p class="text-sm text-muted-foreground">
            {{ successCount }} succeeded, {{ failCount }} failed, {{ uploadQueue.length - successCount - failCount }} remaining
          </p>
        </div>
        <Badge variant="outline">
          {{ uploadProgress }}%
        </Badge>
      </div>

      <!-- Overall Progress Bar -->
      <div class="space-y-2">
        <Progress :value="uploadProgress" class="h-2" />
      </div>

      <!-- Individual File Progress -->
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div
          v-for="item in uploadQueue"
          :key="item.file.name"
          class="flex items-center gap-3 p-3 rounded-lg border bg-card"
        >
          <div class="flex-shrink-0">
            <Loader2 v-if="item.status === 'uploading'" class="h-5 w-5 animate-spin text-blue-500" />
            <CheckCircle2 v-else-if="item.status === 'success'" class="h-5 w-5 text-green-500" />
            <XCircle v-else-if="item.status === 'error'" class="h-5 w-5 text-red-500" />
            <Upload v-else class="h-5 w-5 text-muted-foreground" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2">
              <p class="text-sm font-medium truncate">
                {{ item.file.name }}
              </p>
              <span class="text-xs text-muted-foreground flex-shrink-0">
                {{ item.progress }}%
              </span>
            </div>
            <div v-if="item.status === 'uploading'" class="mt-1">
              <Progress :value="item.progress" class="h-1" />
            </div>
            <p v-if="item.status === 'error'" class="text-xs text-red-500 mt-1">
              {{ item.error }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Uploaded Files List -->
    <div class="space-y-4">
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
          <RefreshCw class="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>
      <div class="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Filename</TableHead>
              <TableHead>Uploaded At</TableHead>
              <TableHead>Completed At</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>URN</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <template v-if="status === 'pending'">
              <TableRow v-for="i in 5" :key="i">
                <TableCell><Skeleton class="h-4 w-[250px]" /></TableCell>
                <TableCell><Skeleton class="h-4 w-[150px]" /></TableCell>
                <TableCell><Skeleton class="h-4 w-[150px]" /></TableCell>
                <TableCell><Skeleton class="h-4 w-[100px]" /></TableCell>
                <TableCell><Skeleton class="h-4 w-[100px]" /></TableCell>
              </TableRow>
            </template>
            <template v-else>
              <TableRow v-for="file in uploadedFiles" :key="file.id">
                <TableCell>{{ file.originalFilename }}</TableCell>
                <TableCell>
                  {{ file.created_at ? new Date(file.created_at.endsWith('Z') ? file.created_at : file.created_at + 'Z').toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    timeZone: 'Asia/Jakarta'
                  }) : '-' }}
                </TableCell>
                <TableCell>
                  {{ file.completed_at ? new Date(file.completed_at.endsWith('Z') ? file.completed_at : file.completed_at + 'Z').toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    timeZone: 'Asia/Jakarta'
                  }) : '-' }}
                </TableCell>
                <TableCell>
                  <Badge
                    variant="outline"
                    :class="{
                      'bg-yellow-100 text-yellow-800 border-yellow-200': file.status === 'processing',
                      'bg-green-100 text-green-800 border-green-200': file.status === 'done',
                      'bg-gray-100 text-gray-800 border-gray-200': !['processing', 'done'].includes(file.status),
                    }"
                  >
                    <Loader2 v-if="file.status === 'processing'" class="mr-1 h-3 w-3 animate-spin" />
                    {{ file.status || 'Uploaded' }}
                  </Badge>
                </TableCell>
                <TableCell>
                  <NuxtLink 
                    v-if="file.urn" 
                    :to="`/gl/${file.urn}`"
                    class="font-mono text-sm text-blue-600 hover:underline"
                  >
                    {{ file.urn }}
                  </NuxtLink>
                  <span v-else class="text-muted-foreground">-</span>
                </TableCell>
              </TableRow>
              <TableRow v-if="uploadedFiles.length === 0">
                <TableCell colspan="5" class="text-center text-muted-foreground h-24">
                  No documents uploaded yet.
                </TableCell>
              </TableRow>
            </template>
          </TableBody>
        </Table>
      </div>

      <div class="mt-4 flex justify-end">
        <Pagination v-if="total > 0" v-model:page="page" :total="total" :items-per-page="pageSize" :sibling-count="1" show-edges>
          <PaginationContent v-slot="{ items }">
            <li class="flex items-center list-none">
              <PaginationPrevious />
            </li>

            <template v-for="(item, index) in items">
              <PaginationItem v-if="item.type === 'page'" :key="index" :value="item.value" :is-active="item.value === page">
                {{ item.value }}
              </PaginationItem>
              <PaginationEllipsis v-else :key="item.type" :index="index" />
            </template>

            <li class="flex items-center list-none">
              <PaginationNext />
            </li>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft, UploadCloud, Loader2, Info, Download } from 'lucide-vue-next'
import { toast } from 'vue-sonner'

const router = useRouter()
const fileInput = ref<HTMLInputElement | null>(null)
const isUploading = ref(false)

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
    const config = useRuntimeConfig()
    const { data, error } = await useFetch(`${config.public.apiBase}/api/v1/upload/file/gl`, {
      method: 'POST',
      body: formData,
    })

    if (error.value) {
      throw new Error(error.value.message)
    }

    toast.success('File uploaded successfully', {
      description: 'Redirecting to GL page...',
    })
    setTimeout(() => {
      router.push('/gl')
    }, 2000)
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

const downloadTemplate = () => {
  // Create a link element and trigger download
  const link = document.createElement('a')
  link.href = '/templates/gl-template.xlsx'
  link.download = 'GL-Template.xlsx'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  toast.success('Template download started', {
    description: 'Check your downloads folder',
  })
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
          Upload General Ledger (GL) File
        </h2>
        <p class="text-muted-foreground mt-1">
          Please upload your <span class="font-bold">general ledger</span> file for processing
        </p>
      </div>
    </div>

    <!-- Info Alert -->
    <Alert variant="default" class="border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800 relative pr-44">
      <Info class="h-4 w-4 text-blue-600 dark:text-blue-400" />
      <AlertTitle class="text-blue-900 dark:text-blue-100">Supported File Format</AlertTitle>
      <AlertDescription class="text-blue-800 dark:text-blue-200">
        For now, we only support XLSX files. Please ensure your general ledger data is in Excel format (.xlsx).
      </AlertDescription>
      <Button 
        variant="outline" 
        size="sm" 
        class="absolute top-3 right-4 shadow-sm border-blue-300 text-blue-700 hover:bg-blue-100 dark:border-blue-700 dark:text-blue-300 dark:hover:bg-blue-900"
        @click.stop="downloadTemplate"
      >
        <Download class="h-3.5 w-3.5 mr-1.5" />
        Download Template
      </Button>
    </Alert>

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
        accept=".xlsx"
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
        XLSX (MAX. 10MB)
      </p>
      <Button class="mt-4" :disabled="isUploading">
        {{ isUploading ? 'Uploading...' : 'Select File' }}
      </Button>
    </div>
  </div>
</template>

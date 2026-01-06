<script setup lang="ts">
import { columns } from '@/components/gl/components/columns'
import DataTable from '@/components/gl/components/DataTable.vue'
import glData from '@/components/gl/data/glTable.json'
import type { GL } from '@/components/gl/data/schema'
</script>

<template>
  <div class="w-full flex flex-col items-stretch gap-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold tracking-tight">
          GL
        </h2>
        <p class="text-muted-foreground mt-1">
          Uploaded GL transactions for review and processing
        </p>
      </div>
      <div class="flex items-center gap-2">
        <Button @click="navigateTo('/gl/upload')">
          Upload GL
        </Button>
        <Button variant="outline" @click="navigateTo('/gl/upload-invoice')">
          Upload Tax Invoices/Invoices
        </Button>
      </div>
    </div>

    <!-- GL Table -->
    <DataTable :data="(glData as { data: GL[] }).data" :columns="columns" />
  </div>
</template>
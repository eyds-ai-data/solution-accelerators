<script setup lang="ts">
import { columns } from '@/components/candidates/components/columns'
import DataTable from '@/components/candidates/components/DataTable.vue'
import type { Candidate } from '@/components/candidates/data/schema'

const { data: candidates, pending: loading, error } = await useFetch<Candidate[]>('/api/candidates')

console.log('Candidates data:', candidates)
</script>

<template>
  <div class="w-full flex flex-col items-stretch gap-6">
    <!-- Header -->
    <div>
      <h2 class="text-3xl font-bold tracking-tight">
        Candidates
      </h2>
      <p class="text-muted-foreground mt-1">
        Manage and review candidate applications and profiles
      </p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">
      {{ error }}
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
    </div>

    <!-- Candidates Table -->
    <DataTable v-if="!loading && !error && candidates" :data="candidates" :columns="columns" />
  </div>
</template>
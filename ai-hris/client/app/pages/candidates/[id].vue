<script setup lang="ts">
import { ref } from 'vue'
import type { Candidate } from '@/components/candidates/data/schema'
import candidatesData from '@/components/candidates/data/candidates.json'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { Textarea } from '@/components/ui/textarea'
import { statuses, positions } from '@/components/candidates/data/data'
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  SendIcon,
  MoveRightIcon,
  DownloadIcon,
  AlertCircleIcon,
  MapPinIcon,
  CalendarIcon,
  FileTextIcon,
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const candidates = (candidatesData as { data: Candidate[] }).data
const candidateId = route.params.id as string
const currentIndex = ref(candidates.findIndex(c => c.id === candidateId))
const candidate = computed(() => candidates[currentIndex.value])

if (currentIndex.value === -1) {
  navigateTo('/candidates')
}

const statusInfo = computed(() => {
  return statuses.find(s => s.value === candidate.value?.status)
})

const positionInfo = computed(() => {
  return positions.find(p => p.value === candidate.value?.position)
})

const goToCandidate = (index: number) => {
  if (index >= 0 && index < candidates.length) {
    currentIndex.value = index
    navigateTo(`/candidates/${candidates[index].id}`)
  }
}

const getStatusColor = (status: string) => {
  const colorMap: Record<string, string> = {
    applied: 'bg-blue-100 text-blue-800',
    reviewing: 'bg-yellow-100 text-yellow-800',
    shortlisted: 'bg-purple-100 text-purple-800',
    rejected: 'bg-red-100 text-red-800',
    hired: 'bg-green-100 text-green-800',
  }
  return colorMap[status] || 'bg-gray-100 text-gray-800'
}

// Generate mock AI interview data
const aiInterviewScores = computed(() => ({
  overall: candidate.value?.rating || 0,
  assessment: Math.round((candidate.value?.rating || 0) * 10) / 10,
  resume: Math.round((candidate.value?.rating || 0) * 10 - 2) / 10,
  visualDesign: Math.round((candidate.value?.rating || 0) * 10 - 1) / 10,
}))

const signals = [
  { label: 'Short Tenure', color: 'bg-yellow-100 text-yellow-800' },
  { label: 'Proctoring Incident', color: 'bg-red-100 text-red-800' },
  { label: 'Quick Joiner', color: 'bg-blue-100 text-blue-800' },
]

const downloadCV = () => {
  if (candidate.value?.cv_url) {
    window.open(candidate.value.cv_url, '_blank')
  }
}
</script>

<template>
  <div v-if="candidate" class="min-h-screen bg-slate-50">
    <!-- Header Navigation -->
    <div class="border-b bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2 text-sm text-muted-foreground">
          <span class="ml-4 text-xs font-medium">{{ currentIndex + 1 }} of {{ candidates.length }}</span>
        </div>
        <div class="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            :disabled="currentIndex === 0"
            @click="goToCandidate(currentIndex - 1)"
          >
            <ChevronLeftIcon class="h-4 w-4" />
            Prev
          </Button>
          <Button
            variant="outline"
            size="sm"
            :disabled="currentIndex === candidates.length - 1"
            @click="goToCandidate(currentIndex + 1)"
          >
            Next
            <ChevronRightIcon class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Header Section with Avatar -->
          <Card class="bg-white">
            <CardContent class="pt-6">
              <div class="flex items-start gap-6 mb-6">
                <div class="flex-shrink-0 relative">
                  <div class="w-20 h-20 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-2xl font-bold">
                    {{ candidate.name.charAt(0) }}
                  </div>
                  <Badge class="absolute -bottom-2 -right-2 rounded-full bg-green-500 text-white border-2 border-white">
                    {{ candidate.rating }}/10
                  </Badge>
                </div>
                <div class="flex-1">
                  <div class="flex items-baseline gap-3 mb-2">
                    <h1 class="text-3xl font-bold">{{ candidate.name }}</h1>
                    <Badge :class="getStatusColor(candidate.status)" class="text-sm">
                      {{ statusInfo?.label }}
                    </Badge>
                  </div>
                  <p class="text-lg text-muted-foreground mb-4">for {{ positionInfo?.label }}</p>
                  <div class="flex flex-wrap gap-2 text-sm text-muted-foreground">
                    <div class="flex items-center gap-1">
                      <MapPinIcon class="h-4 w-4" />
                      <span>{{ candidate.experience }} years experience</span>
                    </div>
                    <span>•</span>
                    <div class="flex items-center gap-1">
                      <CalendarIcon class="h-4 w-4" />
                      <span>Applied {{ new Date(candidate.appliedDate).toLocaleDateString() }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-2 flex-wrap">
                <Button class="gap-2">
                  <SendIcon class="h-4 w-4" />
                  Send Mail
                </Button>
                <Button variant="outline" class="gap-2">
                  <MoveRightIcon class="h-4 w-4" />
                  Move to stage
                </Button>
                <Button variant="outline" class="gap-2">
                  <DownloadIcon class="h-4 w-4" />
                  Download Candidate Report
                </Button>
                <Button variant="ghost" size="sm">
                  <AlertCircleIcon class="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          <!-- Status Note -->
          <Card class="bg-blue-50 border-blue-200">
            <CardContent class="pt-6">
              <p class="text-sm text-blue-900">
                {{ candidate.name }} is interviewing for {{ candidate.skills.length }} more role{{ candidate.skills.length > 1 ? 's' : '' }}
              </p>
            </CardContent>
          </Card>

          <!-- Signals -->
          <div>
            <h3 class="font-semibold mb-3">Signals</h3>
            <div class="flex flex-wrap gap-2">
              <Badge v-for="(signal, index) in signals" :key="index" :class="signal.color" class="px-3 py-1">
                <span v-if="index === 0" class="mr-1">📊</span>
                <span v-else-if="index === 1" class="mr-1">⚠️</span>
                <span v-else class="mr-1">⚡</span>
                {{ signal.label }}
              </Badge>
            </div>
          </div>

          <!-- Scores Section -->
          <div>
            <h3 class="font-semibold mb-4">Score</h3>
            <div class="grid grid-cols-3 gap-4">
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold text-blue-600 mb-2">{{ aiInterviewScores.overall.toFixed(1) }}</div>
                  <p class="text-sm text-muted-foreground">AI Interview</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold text-red-600 mb-2">{{ aiInterviewScores.assessment.toFixed(1) }}</div>
                  <p class="text-sm text-muted-foreground">Assessments</p>
                </CardContent>
              </Card>
              <Card>
                <CardContent class="pt-6 text-center">
                  <div class="text-3xl font-bold text-green-600 mb-2">{{ aiInterviewScores.resume.toFixed(1) }}</div>
                  <p class="text-sm text-muted-foreground">Resume</p>
                </CardContent>
              </Card>
            </div>
          </div>

          <!-- AI Interview Summary -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">AI Interview Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p class="text-sm text-muted-foreground leading-relaxed">
                {{ candidate.notes || 'No summary available. ' }}Lorem ipsum dolor sit amet consectetur. Nulla risus nisl magna platea in convallis. Vitae elementum pellentesque elit augue massa. Lectus sit nisl vitae a. Massa felis aliquot amet habitasse. Scelerisque ut proin nescitur non. Ut amet mauris nulla cursus cum mauris ac tempor. In sed condimentum nullam sed in. Nibh dui mattis ornare bibendum nullam risus ut pharetra. Sed ultrices tempus amet egestas hac arcu.
              </p>
            </CardContent>
          </Card>

          <!-- AI Interview Scores Detail -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg">AI Interview Score</CardTitle>
            </CardHeader>
            <CardContent class="space-y-6">
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Visual Design</span>
                  <span class="text-sm font-semibold">{{ aiInterviewScores.visualDesign.toFixed(1) }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-green-500 h-2 rounded-full"
                    :style="{ width: `${(aiInterviewScores.visualDesign / 10) * 100}%` }"
                  />
                </div>
              </div>
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Communication</span>
                  <span class="text-sm font-semibold">{{ (aiInterviewScores.overall * 0.9).toFixed(1) }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-blue-500 h-2 rounded-full"
                    :style="{ width: `${(aiInterviewScores.overall * 0.9 / 10) * 100}%` }"
                  />
                </div>
              </div>
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Technical Knowledge</span>
                  <span class="text-sm font-semibold">{{ (aiInterviewScores.overall * 0.95).toFixed(1) }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="bg-purple-500 h-2 rounded-full"
                    :style="{ width: `${(aiInterviewScores.overall * 0.95 / 10) * 100}%` }"
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Contact Info -->
          <Card>
            <CardHeader>
              <CardTitle class="text-sm">Contact Info</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <div>
                <p class="text-xs text-muted-foreground mb-1">Name</p>
                <p class="font-medium">{{ candidate.name }}</p>
              </div>
              <Separator />
              <div>
                <p class="text-xs text-muted-foreground mb-1">Location</p>
                <p class="font-medium">New York, NY</p>
              </div>
              <Separator />
              <div>
                <p class="text-xs text-muted-foreground mb-1">Email</p>
                <a href="#" class="text-blue-600 hover:underline text-sm">{{ candidate.email }}</a>
              </div>
              <Separator />
              <div>
                <p class="text-xs text-muted-foreground mb-1">Phone</p>
                <p class="font-medium">{{ candidate.phone }}</p>
              </div>
            </CardContent>
          </Card>

          <!-- Experience -->
          <Card>
            <CardHeader>
              <CardTitle class="text-sm">Experience</CardTitle>
            </CardHeader>
            <CardContent class="space-y-3">
              <div v-for="skill in candidate.skills" :key="skill" class="pb-3 border-b last:border-b-0 last:pb-0">
                <p class="font-medium text-sm">{{ skill }}</p>
                <p class="text-xs text-muted-foreground">2024 - present</p>
              </div>
            </CardContent>
          </Card>

          <!-- Education -->
          <Card>
            <CardHeader>
              <CardTitle class="text-sm">Education</CardTitle>
            </CardHeader>
            <CardContent class="space-y-3">
              <div>
                <p class="font-medium text-sm">Technical Skills</p>
                <p class="text-xs text-muted-foreground">2015-2019</p>
              </div>
              <Separator />
              <div>
                <p class="font-medium text-sm">Professional Training</p>
                <p class="text-xs text-muted-foreground">2012-2015</p>
              </div>
            </CardContent>
          </Card>

          <!-- Resume -->
          <Card>
            <CardHeader>
              <CardTitle class="text-sm">Résumé</CardTitle>
            </CardHeader>
            <CardContent>
              <Button v-if="candidate.cv_url" variant="outline" class="w-full gap-2 justify-start" @click="downloadCV">
                <FileTextIcon class="h-4 w-4" />
                <span class="text-xs">resume_{{ candidate.name.toLowerCase().replace(' ', '_') }}.pdf</span>
              </Button>
            </CardContent>
          </Card>

          <!-- Skills -->
          <Card>
            <CardHeader>
              <CardTitle class="text-sm">Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="flex flex-wrap gap-2">
                <Badge v-for="skill in candidate.skills" :key="skill" variant="secondary" class="text-xs">
                  {{ skill }}
                </Badge>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

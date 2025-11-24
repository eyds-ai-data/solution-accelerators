<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Candidate } from '@/components/candidates/data/schema'
import candidatesData from '@/components/candidates/data/candidates.json'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ArrowLeft, Save } from 'lucide-vue-next'
import { Badge } from '@/components/ui/badge'

const route = useRoute()
const router = useRouter()
const candidateId = route.params.id as string

// Form state
const form = ref<Partial<Candidate>>({
  name: '',
  email: '',
  phone: '',
  position: '',
  status: 'applied',
  experience: 0,
  skills: [],
  notes: ''
})

const newSkill = ref('')

// Load data
onMounted(() => {
  const candidates = (candidatesData as { data: Candidate[] }).data
  const candidate = candidates.find(c => c.id === candidateId)
  
  if (candidate) {
    form.value = { ...candidate }
  } else {
    // Handle not found
    router.push('/candidates')
  }
})

const goBack = () => {
  router.back()
}

const addSkill = () => {
  if (newSkill.value.trim() && form.value.skills) {
    if (!form.value.skills.includes(newSkill.value.trim())) {
      form.value.skills.push(newSkill.value.trim())
    }
    newSkill.value = ''
  }
}

const removeSkill = (skill: string) => {
  if (form.value.skills) {
    form.value.skills = form.value.skills.filter(s => s !== skill)
  }
}

const saveCandidate = () => {
  // Here you would typically make an API call to save the data
  console.log('Saving candidate:', form.value)
  
  // For now, just navigate back
  router.push(`/candidates/${candidateId}`)
}
</script>

<template>
  <div class="min-h-screen bg-muted/40 p-6">
    <div class="max-w-3xl mx-auto space-y-6">
      
      <!-- Header -->
      <div class="flex items-center gap-4">
        <Button variant="ghost" size="icon" @click="goBack">
          <ArrowLeft class="h-5 w-5" />
        </Button>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-foreground">Edit Candidate</h1>
          <p class="text-muted-foreground">Update candidate information</p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Personal Information</CardTitle>
          <CardDescription>Basic details about the candidate.</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="name">Full Name</Label>
              <Input id="name" v-model="form.name" placeholder="John Doe" />
            </div>
            <div class="space-y-2">
              <Label for="email">Email</Label>
              <Input id="email" type="email" v-model="form.email" placeholder="john@example.com" />
            </div>
            <div class="space-y-2">
              <Label for="phone">Phone</Label>
              <Input id="phone" v-model="form.phone" placeholder="+1 234 567 890" />
            </div>
            <div class="space-y-2">
              <Label for="experience">Experience (Years)</Label>
              <Input id="experience" type="number" v-model="form.experience" min="0" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Professional Details</CardTitle>
          <CardDescription>Role, status, and skills.</CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-2">
              <Label for="position">Position</Label>
              <Select v-model="form.position">
                <SelectTrigger>
                  <SelectValue placeholder="Select a position" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="frontend-developer">Frontend Developer</SelectItem>
                  <SelectItem value="backend-developer">Backend Developer</SelectItem>
                  <SelectItem value="product-designer">Product Designer</SelectItem>
                  <SelectItem value="product-manager">Product Manager</SelectItem>
                  <SelectItem value="data-scientist">Data Scientist</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div class="space-y-2">
              <Label for="status">Status</Label>
              <Select v-model="form.status">
                <SelectTrigger>
                  <SelectValue placeholder="Select status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="applied">Applied</SelectItem>
                  <SelectItem value="screening">Screening</SelectItem>
                  <SelectItem value="shortlisted">Shortlisted</SelectItem>
                  <SelectItem value="interviewing">Interviewing</SelectItem>
                  <SelectItem value="offered">Offered</SelectItem>
                  <SelectItem value="hired">Hired</SelectItem>
                  <SelectItem value="rejected">Rejected</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div class="space-y-2">
            <Label>Skills</Label>
            <div class="flex flex-wrap gap-2 mb-2">
              <Badge v-for="skill in form.skills" :key="skill" variant="secondary" class="gap-1 pr-1">
                {{ skill }}
                <button @click="removeSkill(skill)" class="hover:bg-muted rounded-full p-0.5">
                  <span class="sr-only">Remove</span>
                  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                </button>
              </Badge>
            </div>
            <div class="flex gap-2">
              <Input v-model="newSkill" placeholder="Add a skill (e.g. React)" @keydown.enter.prevent="addSkill" />
              <Button type="button" variant="outline" @click="addSkill">Add</Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Notes</CardTitle>
          <CardDescription>Additional information or internal notes.</CardDescription>
        </CardHeader>
        <CardContent>
          <Textarea v-model="form.notes" placeholder="Enter notes here..." class="min-h-[100px]" />
        </CardContent>
      </Card>

      <div class="flex justify-end gap-4">
        <Button variant="outline" @click="goBack">Cancel</Button>
        <Button @click="saveCandidate">
          <Save class="mr-2 h-4 w-4" />
          Save Changes
        </Button>
      </div>

    </div>
  </div>
</template>

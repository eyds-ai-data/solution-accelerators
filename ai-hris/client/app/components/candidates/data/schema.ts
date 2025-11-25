import { z } from 'zod'

export const candidateSchema = z.object({
  id: z.string(),
  candidate_id: z.string(),
  name: z.string(),
  email: z.string(),
  phone: z.string(),
  position: z.string(),
  status: z.enum(['applied', 'reviewing', 'shortlisted', 'rejected', 'hired']),
  applied_date: z.string(),
  experience: z.number(),
  skills: z.array(z.string()),
  rating: z.number().min(0).max(5).optional(),
  notes: z.string().optional(),
  cv_url: z.string().optional(),
  gender: z.string().optional(),
  date_of_birth: z.string().optional(),
  education: z.array(z.object({
    institution: z.string(),
    degree: z.string(),
    field_of_study: z.string(),
    graduation_year: z.number(),
    gpa: z.number(),
  })).optional(),
  work_experiences: z.array(z.object({
    company: z.string(),
    position: z.string(),
    start_date: z.string(),
    end_date: z.string().nullable().optional(),
    is_current: z.boolean(),
    description: z.string(),
  })).optional(),
  documents: z.array(z.object({
    type: z.string(),
    name: z.string(),
    url: z.string(),
    last_updated: z.string(),
    extracted_content: z.object({
      text: z.string(),
      tables: z.array(z.any()).optional(),
      bounding_boxes: z.array(z.any()).optional(),
    }).optional(),
  })).optional(),
})

export type Candidate = z.infer<typeof candidateSchema>

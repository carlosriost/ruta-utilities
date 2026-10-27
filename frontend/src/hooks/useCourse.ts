import { useContext } from 'react'
import { CourseContext } from '@/context/CourseContext'

export function useCourse() {
  const context = useContext(CourseContext)
  if (!context) {
    throw new Error('useCourse debe usarse dentro de <CourseProvider>')
  }
  return context
}

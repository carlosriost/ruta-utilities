import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { courseApi } from '@/services/courseApi'
import { progressApi } from '@/services/progressApi'
import { ApiError } from '@/services/apiClient'
import type { Badge, CourseResponse, NodeState, StateChange } from '@/types/api'

export interface UnlockEvent {
  phaseId: number
  phaseName: string
  previousPhaseName: string | null
  courseCompliant: boolean
}

interface CourseContextValue {
  course: CourseResponse | null
  loading: boolean
  refreshing: boolean
  error: string | null
  refresh: () => Promise<void>
  /**
   * Aplica el resultado devuelto tras marcar un tema: refresca el mapa y
   * encola las celebraciones (nuevo nivel, insignias).
   */
  applyStateChange: (change: StateChange) => Promise<void>
  resetProgress: () => Promise<void>
  unlockEvent: UnlockEvent | null
  dismissUnlock: () => void
  celebratedBadges: Badge[]
  dismissBadges: () => void
  findNode: (nodeId: number) => NodeState | undefined
}

export const CourseContext = createContext<CourseContextValue | null>(null)

export function CourseProvider({ children }: { children: ReactNode }) {
  const [course, setCourse] = useState<CourseResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [unlockEvent, setUnlockEvent] = useState<UnlockEvent | null>(null)
  const [celebratedBadges, setCelebratedBadges] = useState<Badge[]>([])
  const firstLoad = useRef(true)

  const load = useCallback(async (signal?: AbortSignal) => {
    if (firstLoad.current) setLoading(true)
    else setRefreshing(true)
    try {
      const data = await courseApi.getCourse(signal)
      setCourse(data)
      setError(null)
    } catch (err) {
      if ((err as Error).name === 'AbortError') return
      setError(
        err instanceof ApiError
          ? err.message
          : 'No pudimos cargar tu recorrido.',
      )
    } finally {
      firstLoad.current = false
      setLoading(false)
      setRefreshing(false)
    }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    void load(controller.signal)
    return () => controller.abort()
  }, [load])

  const refresh = useCallback(() => load(), [load])

  const applyStateChange = useCallback(
    async (change: StateChange) => {
      // El mapa siempre se vuelve a leer del backend: es la fuente de verdad.
      await load()
      if (change.new_badges.length > 0) setCelebratedBadges(change.new_badges)
      if (change.new_phase_unlocked && change.unlocked_phase_id) {
        setUnlockEvent({
          phaseId: change.unlocked_phase_id,
          phaseName: change.unlocked_phase_name ?? 'Nueva zona',
          previousPhaseName: change.previous_phase_name,
          courseCompliant: change.course_compliant,
        })
      }
    },
    [load],
  )

  const resetProgress = useCallback(async () => {
    await progressApi.resetProgress()
    setUnlockEvent(null)
    setCelebratedBadges([])
    await load()
  }, [load])

  const findNode = useCallback(
    (nodeId: number) =>
      course?.phases.flatMap((phase) => phase.nodes).find((n) => n.id === nodeId),
    [course],
  )

  const value = useMemo<CourseContextValue>(
    () => ({
      course,
      loading,
      refreshing,
      error,
      refresh,
      applyStateChange,
      resetProgress,
      unlockEvent,
      dismissUnlock: () => setUnlockEvent(null),
      celebratedBadges,
      dismissBadges: () => setCelebratedBadges([]),
      findNode,
    }),
    [
      course,
      loading,
      refreshing,
      error,
      refresh,
      applyStateChange,
      resetProgress,
      unlockEvent,
      celebratedBadges,
      findNode,
    ],
  )

  return <CourseContext.Provider value={value}>{children}</CourseContext.Provider>
}

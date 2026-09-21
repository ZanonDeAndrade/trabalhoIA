import { useEffect, useState } from 'react'
import { getTeams } from '../services/api'
import type { Team } from '../types/api'
import { getReadableError } from '../utils/format'

export function useTeams() {
  const [teams, setTeams] = useState<Team[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [source, setSource] = useState<'api' | 'mock'>('api')

  async function load() {
    setLoading(true)
    setError('')

    try {
      const result = await getTeams()
      setTeams(result.teams)
      setSource(result.source)
    } catch (err) {
      setError(getReadableError(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void load()
  }, [])

  return { teams, loading, error, source, retry: load }
}

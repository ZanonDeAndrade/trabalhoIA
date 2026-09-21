import { useState } from 'react'
import { predictMatch } from '../services/api'
import type { PredictionResponse, Team } from '../types/api'
import { getReadableError } from '../utils/format'

export function usePrediction() {
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [source, setSource] = useState<'api' | 'mock'>('api')

  async function submit(homeTeam: Team, awayTeam: Team) {
    setLoading(true)
    setError('')

    try {
      const result = await predictMatch(homeTeam, awayTeam)
      setPrediction(result.prediction)
      setSource(result.source)
    } catch (err) {
      setError(getReadableError(err))
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  return { prediction, loading, error, source, submit }
}

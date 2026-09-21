import { useCallback, useEffect, useRef, useState } from 'react'
import { predictMatch } from '../services/api'
import type { PredictionRequest, PredictionResponse } from '../types/api'
import { getReadableError } from '../utils/format'

type PredictionResult = { request: PredictionRequest; prediction: PredictionResponse }

export function usePrediction() {
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const controllerRef = useRef<AbortController | null>(null)

  useEffect(() => () => controllerRef.current?.abort(), [])

  const reset = useCallback(() => {
    controllerRef.current?.abort()
    setResult(null)
    setError('')
    setLoading(false)
  }, [])

  const submit = useCallback(async (request: PredictionRequest) => {
    controllerRef.current?.abort()
    const controller = new AbortController()
    controllerRef.current = controller
    setLoading(true)
    setError('')

    try {
      const prediction = await predictMatch(request, controller.signal)
      if (controller.signal.aborted) return
      setResult({ request, prediction })
    } catch (err) {
      if (controller.signal.aborted) return
      setError(getReadableError(err))
      setResult(null)
    } finally {
      if (!controller.signal.aborted) setLoading(false)
    }
  }, [])

  return { result, loading, error, submit, reset }
}

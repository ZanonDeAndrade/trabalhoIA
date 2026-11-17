import { useCallback, useEffect, useRef, useState } from 'react'
import { getReadableError } from '../utils/format'

type Settled<T> = { key: string; data?: T; error?: string }

/**
 * Busca dados na API sempre que `key` mudar, cancelando a requisição anterior.
 * `loading` é derivado da chave (sem setState síncrono no efeito) e o último dado válido
 * é mantido enquanto uma nova consulta está em andamento.
 */
export function useAsyncData<T>(fetcher: (signal: AbortSignal) => Promise<T>, key: string) {
  const [attempt, setAttempt] = useState(0)
  const fullKey = `${key}#${attempt}`
  const [settled, setSettled] = useState<Settled<T>>({ key: '' })
  const fetcherRef = useRef(fetcher)

  useEffect(() => {
    fetcherRef.current = fetcher
  })

  useEffect(() => {
    const controller = new AbortController()
    fetcherRef
      .current(controller.signal)
      .then((data) => setSettled({ key: fullKey, data }))
      .catch((err: unknown) => {
        if (controller.signal.aborted) return
        setSettled((previous) => ({ key: fullKey, data: previous.data, error: getReadableError(err) }))
      })
    return () => controller.abort()
  }, [fullKey])

  const retry = useCallback(() => setAttempt((value) => value + 1), [])
  const finished = settled.key === fullKey

  return {
    data: settled.data,
    loading: !finished,
    error: finished ? settled.error : undefined,
    retry,
  }
}

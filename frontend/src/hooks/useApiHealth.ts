import { useEffect, useState } from 'react'
import { checkApiHealth } from '../services/api'

export function useApiHealth() {
  const [online, setOnline] = useState<boolean | null>(null)

  useEffect(() => {
    let active = true

    async function check() {
      const res = await checkApiHealth()
      if (active) {
        setOnline(res.online)
      }
    }

    void check()

    // Verifica a cada 10 segundos
    const interval = setInterval(() => {
      void check()
    }, 10000)

    return () => {
      active = false
      clearInterval(interval)
    }
  }, [])

  return { online }
}

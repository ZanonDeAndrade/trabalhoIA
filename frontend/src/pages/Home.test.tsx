import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Home } from './Home'
import { healthResponse, mockApi, modelResponse } from '../test/fixtures'

afterEach(() => vi.unstubAllGlobals())

describe('Página inicial', () => {
  it('mostra indicadores e métricas reais da API', async () => {
    mockApi({ '/health': healthResponse, '/model': modelResponse })
    render(<Home onNavigate={() => {}} />)
    const indicadores = await screen.findByText('1.520')
    expect(indicadores).toBeInTheDocument()
    expect(screen.getByText('26')).toBeInTheDocument()
    expect(screen.getByText('2,39')).toBeInTheDocument()
    expect(await screen.findByText('44,5%')).toBeInTheDocument()
    expect(screen.getByText('MODELO v1.0.0 ONLINE')).toBeInTheDocument()
  })

  it('sinaliza API offline sem exibir números inventados', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    render(<Home onNavigate={() => {}} />)
    expect((await screen.findAllByRole('alert'))[0]).toHaveTextContent(/conectar à API/)
    expect(screen.getByText('API OFFLINE')).toBeInTheDocument()
    expect(screen.queryByText('1.520')).not.toBeInTheDocument()
  })
})

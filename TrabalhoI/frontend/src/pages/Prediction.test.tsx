import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Prediction } from './Prediction'
import { mockApi, predictionResponse, teamsResponse } from '../test/fixtures'

afterEach(() => vi.unstubAllGlobals())

async function escolher(mandante: string, visitante: string) {
  const user = userEvent.setup()
  await user.selectOptions(await screen.findByLabelText('Time mandante'), mandante)
  await user.selectOptions(screen.getByLabelText('Time visitante'), visitante)
  return user
}

describe('Página de previsão', () => {
  it('carrega as equipes da API e mostra o estado de carregamento', async () => {
    mockApi({ '/teams': teamsResponse })
    render(<Prediction />)
    expect(screen.getByText('Carregando equipes...')).toBeInTheDocument()
    const mandante = await screen.findByLabelText('Time mandante')
    expect(mandante).toHaveTextContent('Flamengo')
    expect(mandante).toHaveTextContent('Palmeiras')
  })

  it('impede equipes iguais e desabilita o envio', async () => {
    mockApi({ '/teams': teamsResponse })
    render(<Prediction />)
    await escolher('flamengo', 'palmeiras')
    expect(screen.getByRole('button', { name: 'Calcular previsão' })).toBeEnabled()

    const option = screen.getByRole('option', { name: 'Flamengo', selected: false })
    expect(option).toBeDisabled() // já escolhido como mandante
  })

  it('desabilita equipes sem histórico recente na data padrão', async () => {
    mockApi({ '/teams': teamsResponse })
    render(<Prediction />)
    const sport = await screen.findAllByRole('option', { name: /Sport — sem histórico recente/ })
    expect(sport[0]).toBeDisabled()
  })

  it('exibe as três probabilidades, o resultado mais provável e o confronto direto', async () => {
    const fetchSpy = mockApi({ '/teams': teamsResponse, '/predict': predictionResponse })
    render(<Prediction />)
    const user = await escolher('flamengo', 'palmeiras')
    await user.click(screen.getByRole('button', { name: 'Calcular previsão' }))

    expect(await screen.findByRole('heading', { name: 'Vitória do Flamengo' })).toBeInTheDocument()
    const grafico = screen.getByLabelText('Probabilidades da previsão')
    expect(grafico).toHaveTextContent('50%')
    expect(grafico).toHaveTextContent('20%')
    expect(grafico).toHaveTextContent('30%')
    expect(screen.getByText('Confronto direto na base')).toBeInTheDocument()
    expect(screen.getByText(/Confronto hipotético/)).toBeInTheDocument()

    const chamadaPrever = fetchSpy.mock.calls.filter(([url]) => String(url).endsWith('/predict'))
    expect(chamadaPrever).toHaveLength(1)
    expect(JSON.parse(String(chamadaPrever[0][1]?.body))).toEqual({ home_team: 'flamengo', away_team: 'palmeiras' })
  })

  it('mostra o erro devolvido quando o modelo está ausente, sem inventar previsão', async () => {
    mockApi({
      '/teams': teamsResponse,
      '/predict': () => ({ status: 503, body: { error: 'Modelo não encontrado. Execute `python src/modeling.py`.' } }),
    })
    render(<Prediction />)
    const user = await escolher('flamengo', 'palmeiras')
    await user.click(screen.getByRole('button', { name: 'Calcular previsão' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Modelo não encontrado')
    expect(screen.queryByLabelText('Probabilidades da previsão')).not.toBeInTheDocument()
  })

  it('mostra erro com nova tentativa quando a lista de equipes falha', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    render(<Prediction />)
    expect(await screen.findByRole('alert')).toHaveTextContent(/conectar à API/)
    expect(screen.getByRole('button', { name: 'Tentar novamente' })).toBeInTheDocument()
    await waitFor(() => expect(screen.queryByText('Carregando equipes...')).not.toBeInTheDocument())
  })
})

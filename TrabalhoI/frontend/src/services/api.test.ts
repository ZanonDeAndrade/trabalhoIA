import { afterEach, describe, expect, it, vi } from 'vitest'
import { ApiError, getMatches, predictMatch, validatePrediction } from './api'
import { mockApi, predictionResponse, teamsResponse } from '../test/fixtures'

afterEach(() => vi.unstubAllGlobals())

describe('validatePrediction', () => {
  it('aceita probabilidades válidas que somam 1', () => {
    expect(validatePrediction(predictionResponse).label).toBe('Vitória do Flamengo')
  })

  it('rejeita probabilidades fora de [0, 1] ou que não somam 1', () => {
    const invalida = { ...predictionResponse, probabilities: { home_win: 1.4, draw: -0.2, away_win: -0.2 } }
    expect(() => validatePrediction(invalida)).toThrow(ApiError)
    const naoSoma = { ...predictionResponse, probabilities: { home_win: 0.5, draw: 0.5, away_win: 0.5 } }
    expect(() => validatePrediction(naoSoma)).toThrow(ApiError)
  })
})

describe('predictMatch', () => {
  it('não chama a API quando mandante e visitante são iguais', async () => {
    const fetchSpy = mockApi({})
    const [flamengo] = teamsResponse.teams
    await expect(predictMatch({ homeTeam: flamengo, awayTeam: flamengo })).rejects.toThrow(/equipes diferentes/)
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('envia identificadores e a data escolhida', async () => {
    const fetchSpy = mockApi({ '/predict': predictionResponse })
    const [flamengo, palmeiras] = teamsResponse.teams
    await predictMatch({ homeTeam: flamengo, awayTeam: palmeiras, date: '2022-05-01' })
    const body = JSON.parse(String(fetchSpy.mock.calls[0][1]?.body))
    expect(body).toEqual({ home_team: 'flamengo', away_team: 'palmeiras', date: '2022-05-01' })
  })

  it('propaga a mensagem de erro devolvida pela API', async () => {
    mockApi({ '/predict': () => ({ status: 503, body: { error: 'Modelo não encontrado.', code: 'modelo_indisponivel' } }) })
    const [flamengo, palmeiras] = teamsResponse.teams
    await expect(predictMatch({ homeTeam: flamengo, awayTeam: palmeiras })).rejects.toMatchObject({
      message: 'Modelo não encontrado.',
      status: 503,
      code: 'modelo_indisponivel',
    })
  })

  it('traduz falha de rede em mensagem clara, sem dados simulados', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')))
    const [flamengo, palmeiras] = teamsResponse.teams
    await expect(predictMatch({ homeTeam: flamengo, awayTeam: palmeiras })).rejects.toThrow(/conectar à API/)
  })
})

describe('getMatches', () => {
  it('só envia o mando quando há equipe selecionada', async () => {
    const fetchSpy = mockApi({ '/matches': { matches: [], total: 0, page: 1, pages: 1 } })
    await getMatches({ season: '2023', team: 'all', venue: 'home' }, 2)
    const url = new URL(String(fetchSpy.mock.calls[0][0]))
    expect(url.searchParams.get('season')).toBe('2023')
    expect(url.searchParams.get('page')).toBe('2')
    expect(url.searchParams.has('venue')).toBe(false)
    expect(url.searchParams.has('team')).toBe(false)
  })
})

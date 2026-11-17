import type {
  ChartsData,
  HealthResponse,
  MatchesResponse,
  ModelInfo,
  OverviewStats,
  PredictionRequest,
  PredictionResponse,
  StatsFilters,
  TeamsResponse,
} from '../types/api'

export const API_URL = (import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api').replace(/\/$/, '')

const NETWORK_MESSAGE =
  'Não foi possível conectar à API. Verifique se o back-end está em execução (python src/api.py).'

export class ApiError extends Error {
  status: number
  code: string

  constructor(message: string, status = 0, code = 'erro') {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
    })
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') throw error
    throw new ApiError(NETWORK_MESSAGE, 0, 'rede')
  }

  let body: unknown = null
  try {
    body = await response.json()
  } catch {
    body = null
  }

  if (!response.ok) {
    const payload = (body ?? {}) as { error?: string; code?: string }
    throw new ApiError(
      payload.error ?? 'A API respondeu com um erro inesperado.',
      response.status,
      payload.code ?? 'erro_http',
    )
  }
  if (body === null) throw new ApiError('A API respondeu com um formato inválido.', response.status, 'formato')
  return body as T
}

function isProbability(value: unknown): value is number {
  return typeof value === 'number' && value >= 0 && value <= 1
}

export function validatePrediction(value: unknown): PredictionResponse {
  const p = value as PredictionResponse
  const probs = p?.probabilities
  if (
    p &&
    typeof p.label === 'string' &&
    isProbability(p.confidence) &&
    probs &&
    isProbability(probs.home_win) &&
    isProbability(probs.draw) &&
    isProbability(probs.away_win) &&
    Math.abs(probs.home_win + probs.draw + probs.away_win - 1) < 0.01
  ) {
    return p
  }
  throw new ApiError('A resposta da previsão está em formato inválido.', 200, 'formato')
}

export function validateTeams(value: unknown): TeamsResponse {
  const data = value as TeamsResponse
  if (
    data &&
    Array.isArray(data.teams) &&
    data.teams.every((t) => typeof t.id === 'string' && typeof t.name === 'string') &&
    data.reference
  ) {
    return data
  }
  throw new ApiError('A resposta de equipes está em formato inválido.', 200, 'formato')
}

function filterParams(filters: StatsFilters): URLSearchParams {
  const params = new URLSearchParams()
  if (filters.season !== 'all') params.set('season', filters.season)
  if (filters.team !== 'all') {
    params.set('team', filters.team)
    if (filters.venue !== 'all') params.set('venue', filters.venue)
  }
  return params
}

export function getHealth(signal?: AbortSignal) {
  return request<HealthResponse>('/health', { signal })
}

export async function getTeams(signal?: AbortSignal): Promise<TeamsResponse> {
  return validateTeams(await request<unknown>('/teams', { signal }))
}

export async function predictMatch({ homeTeam, awayTeam, date }: PredictionRequest, signal?: AbortSignal) {
  if (homeTeam.id === awayTeam.id) {
    throw new ApiError('Selecione equipes diferentes para mandante e visitante.', 422, 'equipes_iguais')
  }
  const data = await request<unknown>('/predict', {
    method: 'POST',
    signal,
    body: JSON.stringify({ home_team: homeTeam.id, away_team: awayTeam.id, ...(date ? { date } : {}) }),
  })
  return validatePrediction(data)
}

export function getOverview(filters: StatsFilters, signal?: AbortSignal) {
  return request<OverviewStats>(`/stats/overview?${filterParams(filters)}`, { signal })
}

export function getCharts(filters: StatsFilters, signal?: AbortSignal) {
  return request<ChartsData>(`/stats/charts?${filterParams(filters)}`, { signal })
}

export function getMatches(filters: StatsFilters, page: number, signal?: AbortSignal) {
  const params = filterParams(filters)
  params.set('page', String(page))
  params.set('page_size', '8')
  return request<MatchesResponse>(`/matches?${params}`, { signal })
}

export function getModelInfo(signal?: AbortSignal) {
  return request<ModelInfo>('/model', { signal })
}

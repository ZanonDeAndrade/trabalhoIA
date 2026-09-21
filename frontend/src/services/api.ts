import {
  createMockPrediction,
  getMockMatches,
  getMockOverview,
  mockTeams,
} from './mockData'
import type {
  MatchesResponse,
  OverviewStats,
  PredictionResponse,
  StatsFilters,
  Team,
} from '../types/api'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    throw new Error('A API não respondeu como esperado.')
  }

  return response.json() as Promise<T>
}

function validateTeams(value: unknown): Team[] {
  if (
    typeof value === 'object' &&
    value !== null &&
    'teams' in value &&
    Array.isArray((value as { teams: unknown }).teams)
  ) {
    return (value as { teams: Team[] }).teams.filter(
      (team) => typeof team.id === 'string' && typeof team.name === 'string',
    )
  }

  throw new Error('Resposta de equipes em formato inválido.')
}

function validatePrediction(value: unknown): PredictionResponse {
  const prediction = value as PredictionResponse

  if (
    prediction &&
    typeof prediction.label === 'string' &&
    typeof prediction.confidence === 'number' &&
    prediction.probabilities &&
    typeof prediction.probabilities.home_win === 'number' &&
    typeof prediction.probabilities.draw === 'number' &&
    typeof prediction.probabilities.away_win === 'number'
  ) {
    return prediction
  }

  throw new Error('Resposta da previsão em formato inválido.')
}

export async function checkApiHealth(): Promise<{ online: boolean; details?: unknown }> {
  try {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 2000)
    const res = await fetch(`${API_URL}/health`, { signal: controller.signal })
    clearTimeout(timeoutId)
    if (!res.ok) return { online: false }
    const details = await res.json()
    return { online: true, details }
  } catch {
    return { online: false }
  }
}

export async function getTeams(): Promise<{ teams: Team[]; source: 'api' | 'mock' }> {
  try {
    const data = await request<unknown>('/teams')
    return { teams: validateTeams(data), source: 'api' }
  } catch {
    return { teams: mockTeams, source: 'mock' }
  }
}

export async function predictMatch(
  homeTeam: Team,
  awayTeam: Team,
  matchId?: string,
): Promise<{ prediction: PredictionResponse; source: 'api' | 'mock' }> {
  if (homeTeam.id === awayTeam.id) {
    throw new Error('Selecione equipes diferentes para mandante e visitante.')
  }

  try {
    const data = await request<unknown>('/predict', {
      method: 'POST',
      body: JSON.stringify({
        home_team: homeTeam.id,
        away_team: awayTeam.id,
        match_id: matchId,
      }),
    })

    return { prediction: validatePrediction(data), source: 'api' }
  } catch (error) {
    if (error instanceof Error && error.message.includes('equipes diferentes')) {
      throw error
    }

    return {
      prediction: createMockPrediction(homeTeam, awayTeam, matchId),
      source: 'mock',
    }
  }
}

export async function getOverview(
  filters: StatsFilters,
): Promise<{ overview: OverviewStats; source: 'api' | 'mock' }> {
  const params = new URLSearchParams()

  if (filters.season !== 'all') params.set('season', filters.season)
  if (filters.team !== 'all') params.set('team', filters.team)
  if (filters.venue !== 'all') params.set('venue', filters.venue)

  try {
    const overview = await request<OverviewStats>(`/stats/overview?${params.toString()}`)
    return { overview, source: 'api' }
  } catch {
    return { overview: getMockOverview(filters), source: 'mock' }
  }
}

export async function getMatches(
  filters: StatsFilters,
  page: number,
): Promise<{ matches: MatchesResponse; source: 'api' | 'mock' }> {
  const params = new URLSearchParams({
    page: String(page),
    page_size: '5',
  })

  if (filters.season !== 'all') params.set('season', filters.season)
  if (filters.team !== 'all') params.set('team', filters.team)
  if (filters.venue !== 'all') params.set('venue', filters.venue)

  try {
    const matches = await request<MatchesResponse>(`/matches?${params.toString()}`)
    return { matches, source: 'api' }
  } catch {
    return {
      matches: getMockMatches({
        season: filters.season,
        team: filters.team,
        page,
        pageSize: 5,
      }),
      source: 'mock',
    }
  }
}

// Dados de teste com o formato exato da API. Usados apenas nos testes automatizados.
import { vi } from 'vitest'
import type {
  ChartsData,
  HealthResponse,
  MatchesResponse,
  ModelInfo,
  OverviewStats,
  PredictionResponse,
  TeamsResponse,
} from '../types/api'

export const teamsResponse: TeamsResponse = {
  teams: [
    { id: 'flamengo', name: 'Flamengo', official_name: 'CR Flamengo', eligible: true, matches_before: 152, reason: null },
    { id: 'palmeiras', name: 'Palmeiras', official_name: 'SE Palmeiras', eligible: true, matches_before: 152, reason: null },
    { id: 'sport', name: 'Sport', official_name: 'SC do Recife', eligible: false, matches_before: 76, reason: 'A equipe não disputou a temporada 2023' },
  ],
  reference: {
    default_date: '2023-12-07',
    default_hour: 16,
    min_date: '2020-08-08',
    max_date: '2024-02-04',
    last_match_date: '2023-12-06',
  },
}

const form = {
  last_five: ['V', 'E', 'D', 'V', 'V'] as Array<'V' | 'E' | 'D'>,
  points_average: 1.8,
  goals_scored_average: 1.4,
  goals_conceded_average: 0.8,
  yellow_cards_average: 2.2,
  red_cards_average: 0.2,
  matches_considered: 5,
}

export const predictionResponse: PredictionResponse = {
  prediction: 'home_win',
  label: 'Vitória do Flamengo',
  confidence: 0.5,
  probabilities: { home_win: 0.5, draw: 0.2, away_win: 0.3 },
  home_team_form: form,
  away_team_form: { ...form, last_five: ['D', 'D', 'E', 'V', 'D'], points_average: 0.8 },
  head_to_head: {
    matches: 2,
    home_team_wins: 1,
    draws: 1,
    away_team_wins: 0,
    last_matches: [{ date: '2023-11-08', home_team: 'Flamengo', away_team: 'Palmeiras', score: '3 x 0' }],
  },
  factors: [],
  explanations: ['equipe mandante: Flamengo pesa a favor de: vitória do mandante.'],
  reference: { date: '2023-12-07', hour: 16, weekday: 'quinta-feira', source: 'padrao', history_until: '2023-12-06', hypothetical: true },
  model: { algorithm: 'Regressão Logística', version: '1.0.0', trained_at: '2026-09-21T11:50:29-03:00' },
}

export const healthResponse: HealthResponse = {
  status: 'ok',
  api_version: '1.0.0',
  model_loaded: true,
  model: { algorithm: 'Regressão Logística', version: '1.0.0', trained_at: '2026-09-21T11:50:29-03:00' },
  dataset: { matches: 1520, seasons: [2020, 2021, 2022, 2023], teams: 26, goals: 3637, goals_average: 2.39, first_date: '2020-08-08', last_date: '2023-12-06' },
  warnings: [],
}

export const overviewResponse: OverviewStats = {
  total_matches: 380,
  seasons: [2023],
  teams: 20,
  first_date: '2023-04-15',
  last_date: '2023-12-06',
  total_goals: 946,
  goals_average: 2.49,
  total_yellow_cards: 2079,
  yellow_cards_average: 5.47,
  total_red_cards: 122,
  red_cards_average: 0.32,
  home_win_percentage: 0.4684,
  draw_percentage: 0.2579,
  away_win_percentage: 0.2737,
  attendance_average: 27755,
  matches_with_attendance: 367,
  matches_without_attendance: 13,
}

export const chartsResponse: ChartsData = {
  result_distribution: [
    { name: 'Mandante', value: 46.8, count: 178 },
    { name: 'Empate', value: 25.8, count: 98 },
    { name: 'Visitante', value: 27.4, count: 104 },
  ],
  results_by_season: [{ season: '2023', home_win: 178, draw: 98, away_win: 104 }],
  goals_by_season: [{ season: '2023', goals_average: 2.49, matches: 380 }],
  cards_by_season: [{ season: '2023', yellow: 5.47, red: 0.32 }],
  attendance_by_season: [{ season: '2023', attendance_average: 27755, matches_with_attendance: 367, matches: 380 }],
  top_winners: [{ team: 'Grêmio', wins: 21 }],
  top_goals: [{ team: 'Palmeiras', goals_average: 1.9 }],
  top_cards: [{ team: 'Bahia', cards: 3.1 }],
  rankings_available: true,
}

export const matchesResponse: MatchesResponse = {
  matches: [
    { id: '1', date: '2023-12-06', season: '2023', home_team: 'Flamengo', away_team: 'Palmeiras', score: '2 x 1', yellow_cards: 4, red_cards: 0, stadium: 'Maracanã', attendance: 55000 },
    { id: '2', date: '2020-09-01', season: '2020', home_team: 'Santos', away_team: 'Sport', score: '0 x 0', yellow_cards: 3, red_cards: 1, stadium: 'Vila Belmiro', attendance: null },
  ],
  total: 17,
  page: 1,
  pages: 3,
}

const metrics = (acc: number) => ({
  n: 362,
  acuracia: acc,
  acuracia_balanceada: 0.37,
  precisao_macro: 0.39,
  recall_macro: 0.37,
  f1_macro: 0.36,
  log_loss: 1.089,
  brier: 0.652,
  roc_auc_ovr_macro: 0.56,
  por_classe: {
    home_win: { precisao: 0.5, recall: 0.72, f1: 0.59, suporte: 170 },
    draw: { precisao: 0.36, recall: 0.16, f1: 0.22, suporte: 94 },
    away_win: { precisao: 0.3, recall: 0.23, f1: 0.26, suporte: 98 },
  },
  matriz_confusao: [[123, 16, 31], [57, 15, 22], [64, 11, 23]],
  distribuicao_previsoes: { home_win: 244, draw: 42, away_win: 76 },
  distribuicao_real: { home_win: 170, draw: 94, away_win: 98 },
})

export const modelResponse: ModelInfo = {
  algorithm: 'Regressão Logística',
  version: '1.0.0',
  trained_at: '2026-09-21T11:50:29-03:00',
  trained_with: 'temporadas 2020 a 2022 (treino + validação)',
  hyperparameters: { C: 0.5 },
  random_state: 42,
  classes: ['home_win', 'draw', 'away_win'],
  class_labels: { home_win: 'Vitória do mandante', draw: 'Empate', away_win: 'Vitória do visitante' },
  features: { numeric: ['a', 'b'], categorical: ['home_team', 'away_team', 'dia_semana'] },
  data_period: { inicio: '2020-08-08', fim: '2023-12-06', temporadas: [2020, 2021, 2022, 2023] },
  splits: {
    treino: { temporadas: [2020, 2021], n: 689, classes: { home_win: 314, draw: 199, away_win: 176 } },
    validacao: { temporadas: [2022], n: 363, classes: { home_win: 161, draw: 102, away_win: 100 } },
    teste: { temporadas: [2023], n: 362, classes: { home_win: 170, draw: 94, away_win: 98 } },
  },
  metrics: {
    test: metrics(0.4448),
    validation: metrics(0.416),
    train_final: metrics(0.534),
    baseline_majority_test: { ...metrics(0.4696), f1_macro: 0.213, log_loss: null },
    baseline_frequency_test: { ...metrics(0.4696), f1_macro: 0.213, log_loss: 1.061 },
  },
  dependencies: { python: '3.14.4' },
  limitations: ['Somente quatro temporadas de uma competição.'],
  permutation_importance: [{ atributo: 'dif_aproveitamento_mando', rotulo: 'diferença de aproveitamento por mando', aumento_log_loss: 0.0231, desvio_padrao: 0.0075 }],
  selection_criterion: 'maior Macro F1 na validação',
}

type Handler = unknown | ((url: URL, init?: RequestInit) => { status?: number; body: unknown } | Promise<never>)

/** Substitui `fetch` por rotas simuladas (somente em testes) e devolve o espião para inspeção. */
export function mockApi(routes: Record<string, Handler>) {
  const spy = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = new URL(String(input))
    const key = Object.keys(routes).find((path) => url.pathname.endsWith(path))
    if (!key) return new Response(JSON.stringify({ error: 'Rota não encontrada' }), { status: 404 })
    const handler = routes[key]
    const result = typeof handler === 'function' ? await handler(url, init) : { body: handler }
    return new Response(JSON.stringify(result.body), {
      status: result.status ?? 200,
      headers: { 'Content-Type': 'application/json' },
    })
  })
  vi.stubGlobal('fetch', spy)
  return spy
}

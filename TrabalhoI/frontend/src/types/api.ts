export type ResultClass = 'home_win' | 'draw' | 'away_win'

export type Team = {
  id: string
  name: string
  official_name: string
  eligible: boolean
  matches_before: number
  reason: string | null
}

export type ReferenceBounds = {
  default_date: string
  default_hour: number
  min_date: string
  max_date: string
  last_match_date: string
}

export type TeamsResponse = {
  teams: Team[]
  reference: ReferenceBounds
}

export type HealthResponse = {
  status: 'ok' | 'degraded'
  api_version: string
  model_loaded: boolean
  model: { algorithm: string; version: string; trained_at: string } | null
  dataset: {
    matches: number
    seasons: number[]
    teams: number
    goals: number
    goals_average: number
    first_date: string
    last_date: string
  }
  warnings: string[]
}

export type TeamForm = {
  last_five: Array<'V' | 'E' | 'D'>
  points_average: number
  goals_scored_average: number
  goals_conceded_average: number
  yellow_cards_average: number
  red_cards_average: number
  matches_considered: number
}

export type HeadToHead = {
  matches: number
  home_team_wins: number
  draws: number
  away_team_wins: number
  last_matches: Array<{ date: string; home_team: string; away_team: string; score: string }>
}

export type Factor = {
  feature: string
  label: string
  value: string | number
  description: string
  favors: ResultClass
  weight: number
}

export type PredictionResponse = {
  prediction: ResultClass
  label: string
  confidence: number
  probabilities: Record<ResultClass, number>
  home_team_form: TeamForm
  away_team_form: TeamForm
  head_to_head: HeadToHead
  factors: Factor[]
  explanations: string[]
  reference: {
    date: string
    hour: number
    weekday: string
    source: 'padrao' | 'usuario' | 'partida'
    history_until: string
    hypothetical: boolean
  }
  model: { algorithm: string; version: string; trained_at: string }
  actual?: { result: ResultClass; label: string; score: string; used_in_training: boolean }
}

export type PredictionRequest = {
  homeTeam: Team
  awayTeam: Team
  date?: string
}

export type OverviewStats = {
  total_matches: number
  seasons: number[]
  teams: number
  first_date: string | null
  last_date: string | null
  total_goals: number
  goals_average: number
  total_yellow_cards: number
  yellow_cards_average: number
  total_red_cards: number
  red_cards_average: number
  home_win_percentage: number
  draw_percentage: number
  away_win_percentage: number
  attendance_average: number | null
  matches_with_attendance: number
  matches_without_attendance: number
}

export type ChartsData = {
  result_distribution: Array<{ name: string; value: number; count: number }>
  results_by_season: Array<{ season: string; home_win: number; draw: number; away_win: number }>
  goals_by_season: Array<{ season: string; goals_average: number; matches: number }>
  cards_by_season: Array<{ season: string; yellow: number; red: number }>
  attendance_by_season: Array<{
    season: string
    attendance_average: number | null
    matches_with_attendance: number
    matches: number
  }>
  top_winners: Array<{ team: string; wins: number }>
  top_goals: Array<{ team: string; goals_average: number }>
  top_cards: Array<{ team: string; cards: number }>
  rankings_available: boolean
}

export type Match = {
  id: string
  date: string
  season: string
  home_team: string
  away_team: string
  score: string
  yellow_cards: number
  red_cards: number
  stadium: string
  attendance: number | null
}

export type MatchesResponse = {
  matches: Match[]
  total: number
  page: number
  pages: number
}

export type StatsFilters = {
  season: string
  team: string
  venue: string
}

export type ClassMetrics = { precisao: number; recall: number; f1: number; suporte: number }

export type EvaluationMetrics = {
  n: number
  acuracia: number
  acuracia_balanceada: number
  precisao_macro: number
  recall_macro: number
  f1_macro: number
  log_loss: number | null
  brier: number | null
  roc_auc_ovr_macro: number | null
  por_classe: Record<ResultClass, ClassMetrics>
  matriz_confusao: number[][]
  distribuicao_previsoes: Record<ResultClass, number>
  distribuicao_real: Record<ResultClass, number>
}

export type ModelInfo = {
  algorithm: string
  version: string
  trained_at: string
  trained_with: string
  hyperparameters: Record<string, string | number | boolean>
  random_state: number
  classes: ResultClass[]
  class_labels: Record<ResultClass, string>
  features: { numeric: string[]; categorical: string[] }
  data_period: { inicio: string; fim: string; temporadas: number[] }
  splits: Record<string, { temporadas: number[]; n: number; classes: Record<ResultClass, number> }>
  metrics: {
    test: EvaluationMetrics
    validation: EvaluationMetrics
    train_final: EvaluationMetrics
    baseline_majority_test: EvaluationMetrics
    baseline_frequency_test: EvaluationMetrics
  }
  dependencies: Record<string, string>
  limitations: string[]
  permutation_importance?: Array<{ atributo: string; rotulo: string; aumento_log_loss: number; desvio_padrao: number }>
  selection_criterion?: string
}

export type ResultClass = 'home_win' | 'draw' | 'away_win'

export type Team = {
  id: string
  name: string
}

export type TeamForm = {
  last_five: Array<'V' | 'E' | 'D'>
  points_average: number
  goals_scored_average: number
  goals_conceded_average: number
  yellow_cards_average: number
  red_cards_average: number
}

export type PredictionResponse = {
  prediction: ResultClass
  label: string
  confidence: number
  probabilities: Record<ResultClass, number>
  home_team_form: TeamForm
  away_team_form: TeamForm
  explanations: string[]
}

export type OverviewStats = {
  total_matches: number
  total_goals: number
  goals_average: number
  total_yellow_cards: number
  yellow_cards_average: number
  total_red_cards: number
  red_cards_average: number
  home_win_percentage: number
  draw_percentage: number
  away_win_percentage: number
  result_distribution: Array<{ name: string; value: number }>
  goals_by_season: Array<{ season: string; goals_average: number }>
  cards_by_season: Array<{ season: string; yellow: number; red: number }>
  top_winners: Array<{ team: string; wins: number }>
  top_goals: Array<{ team: string; goals_average: number }>
  top_cards: Array<{ team: string; cards: number }>
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

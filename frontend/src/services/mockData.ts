import type {
  Match,
  MatchesResponse,
  OverviewStats,
  PredictionResponse,
  ResultClass,
  Team,
} from '../types/api'

export const mockTeams: Team[] = [
  'América-MG',
  'Athletico-PR',
  'Atlético-GO',
  'Atlético-MG',
  'Bahia',
  'Botafogo',
  'Bragantino',
  'Ceará',
  'Chapecoense',
  'Corinthians',
  'Coritiba',
  'Cuiabá',
  'Flamengo',
  'Fluminense',
  'Fortaleza',
  'Goiás',
  'Grêmio',
  'Internacional',
  'Palmeiras',
  'Santos',
  'São Paulo',
  'Sport',
  'Vasco',
]
  .sort((a, b) => a.localeCompare(b, 'pt-BR'))
  .map((name) => ({
    id: name
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, ''),
    name,
  }))

const baseMatches: Match[] = [
  {
    id: '1',
    date: '2023-11-26',
    season: '2023',
    home_team: 'Flamengo',
    away_team: 'Atlético-MG',
    score: '0 x 3',
    yellow_cards: 7,
    red_cards: 0,
    stadium: 'Maracanã',
  },
  {
    id: '2',
    date: '2023-11-12',
    season: '2023',
    home_team: 'Palmeiras',
    away_team: 'Internacional',
    score: '3 x 0',
    yellow_cards: 3,
    red_cards: 0,
    stadium: 'Allianz Parque',
  },
  {
    id: '3',
    date: '2022-10-22',
    season: '2022',
    home_team: 'Santos',
    away_team: 'Corinthians',
    score: '0 x 1',
    yellow_cards: 6,
    red_cards: 1,
    stadium: 'Vila Belmiro',
  },
  {
    id: '4',
    date: '2021-08-15',
    season: '2021',
    home_team: 'Fortaleza',
    away_team: 'Santos',
    score: '1 x 1',
    yellow_cards: 4,
    red_cards: 0,
    stadium: 'Castelão',
  },
  {
    id: '5',
    date: '2020-09-10',
    season: '2020',
    home_team: 'Bahia',
    away_team: 'Grêmio',
    score: '0 x 2',
    yellow_cards: 5,
    red_cards: 0,
    stadium: 'Pituaçu',
  },
]

export const mockOverview: OverviewStats = {
  total_matches: 1520,
  total_goals: 3668,
  goals_average: 2.41,
  total_yellow_cards: 7480,
  yellow_cards_average: 4.92,
  total_red_cards: 386,
  red_cards_average: 0.25,
  home_win_percentage: 0.44,
  draw_percentage: 0.27,
  away_win_percentage: 0.29,
  result_distribution: [
    { name: 'Mandante', value: 44 },
    { name: 'Empate', value: 27 },
    { name: 'Visitante', value: 29 },
  ],
  goals_by_season: [
    { season: '2020', goals_average: 2.36 },
    { season: '2021', goals_average: 2.28 },
    { season: '2022', goals_average: 2.37 },
    { season: '2023', goals_average: 2.62 },
  ],
  cards_by_season: [
    { season: '2020', yellow: 4.7, red: 0.22 },
    { season: '2021', yellow: 4.9, red: 0.24 },
    { season: '2022', yellow: 5.0, red: 0.28 },
    { season: '2023', yellow: 5.1, red: 0.27 },
  ],
  top_winners: [
    { team: 'Palmeiras', wins: 76 },
    { team: 'Flamengo', wins: 72 },
    { team: 'Atlético-MG', wins: 70 },
    { team: 'Internacional', wins: 63 },
    { team: 'Fluminense', wins: 62 },
  ],
  top_goals: [
    { team: 'Flamengo', goals_average: 1.72 },
    { team: 'Palmeiras', goals_average: 1.69 },
    { team: 'Atlético-MG', goals_average: 1.58 },
    { team: 'Bragantino', goals_average: 1.43 },
    { team: 'Fluminense', goals_average: 1.41 },
  ],
  top_cards: [
    { team: 'Goiás', cards: 5.6 },
    { team: 'Ceará', cards: 5.4 },
    { team: 'Coritiba', cards: 5.2 },
    { team: 'Santos', cards: 5.1 },
    { team: 'Atlético-GO', cards: 5.0 },
  ],
}

export function createMockPrediction(homeTeam: Team, awayTeam: Team): PredictionResponse {
  const seed = (homeTeam.id.length + awayTeam.id.length) % 10
  const home = 0.42 + seed / 100
  const draw = 0.25
  const away = Math.max(0.1, 1 - home - draw)
  const probabilities = {
    home_win: home,
    draw,
    away_win: away,
  }
  const prediction = Object.entries(probabilities).sort((a, b) => b[1] - a[1])[0][0] as ResultClass

  return {
    prediction,
    label:
      prediction === 'home_win'
        ? `Vitória do ${homeTeam.name}`
        : prediction === 'away_win'
          ? `Vitória do ${awayTeam.name}`
          : 'Empate',
    confidence: probabilities[prediction],
    probabilities,
    home_team_form: {
      last_five: ['V', 'V', 'E', 'D', 'V'],
      points_average: 2,
      goals_scored_average: 1.8,
      goals_conceded_average: 0.8,
      yellow_cards_average: 2.3,
      red_cards_average: 0.1,
    },
    away_team_form: {
      last_five: ['D', 'V', 'E', 'E', 'D'],
      points_average: 1,
      goals_scored_average: 1,
      goals_conceded_average: 1.6,
      yellow_cards_average: 2.5,
      red_cards_average: 0.2,
    },
    explanations: [
      'O mandante possui melhor aproveitamento recente.',
      'O visitante sofreu mais gols nos últimos cinco jogos.',
      'O desempenho como mandante favoreceu a previsão.',
    ],
  }
}

export function getMockMatches(params: {
  season?: string
  team?: string
  page?: number
  pageSize?: number
}): MatchesResponse {
  const page = params.page ?? 1
  const pageSize = params.pageSize ?? 5
  const filtered = baseMatches.filter((match) => {
    const seasonMatches = !params.season || params.season === 'all' || match.season === params.season
    const teamMatches =
      !params.team ||
      params.team === 'all' ||
      match.home_team.toLowerCase().includes(params.team.toLowerCase()) ||
      match.away_team.toLowerCase().includes(params.team.toLowerCase())

    return seasonMatches && teamMatches
  })

  return {
    matches: filtered.slice((page - 1) * pageSize, page * pageSize),
    total: filtered.length,
    page,
    pages: Math.max(1, Math.ceil(filtered.length / pageSize)),
  }
}

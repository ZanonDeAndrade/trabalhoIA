import type {
  Match,
  MatchesResponse,
  OverviewStats,
  PredictionResponse,
  ResultClass,
  StatsFilters,
  Team,
  TeamForm,
} from '../types/api'

export const mockTeams: Team[] = [];

export const mockTeamsStats: Record<string, TeamForm> = {};

export const mockOverviewsBySeason: Record<string, OverviewStats> = {
  "all": {
    "total_matches": 1520,
    "total_goals": 3637,
    "goals_average": 2.39,
    "total_yellow_cards": 7474,
    "yellow_cards_average": 4.92,
    "total_red_cards": 447,
    "red_cards_average": 0.29,
    "home_win_percentage": 0.4546,
    "draw_percentage": 0.2809,
    "away_win_percentage": 0.2645,
    "result_distribution": [
      {
        "name": "Mandante",
        "value": 45
      },
      {
        "name": "Empate",
        "value": 28
      },
      {
        "name": "Visitante",
        "value": 26
      }
    ],
    "goals_by_season": [
      {
        "season": "2020",
        "goals_average": 2.48
      },
      {
        "season": "2021",
        "goals_average": 2.22
      },
      {
        "season": "2022",
        "goals_average": 2.38
      },
      {
        "season": "2023",
        "goals_average": 2.49
      }
    ],
    "cards_by_season": [
      {
        "season": "2020",
        "yellow": 4.44,
        "red": 0.29
      },
      {
        "season": "2021",
        "yellow": 4.66,
        "red": 0.25
      },
      {
        "season": "2022",
        "yellow": 5.11,
        "red": 0.32
      },
      {
        "season": "2023",
        "yellow": 5.47,
        "red": 0.32
      }
    ],
    "top_winners": [
      {
        "team": "Atlético-MG",
        "wins": 80
      },
      {
        "team": "Flamengo",
        "wins": 79
      },
      {
        "team": "Palmeiras",
        "wins": 78
      },
      {
        "team": "Fluminense",
        "wins": 70
      },
      {
        "team": "Internacional",
        "wins": 67
      }
    ],
    "top_goals": [
      {
        "team": "Flamengo",
        "goals_average": 1.66
      },
      {
        "team": "Palmeiras",
        "goals_average": 1.57
      },
      {
        "team": "Atlético-MG",
        "goals_average": 1.5
      },
      {
        "team": "Grêmio",
        "goals_average": 1.4
      },
      {
        "team": "Internacional",
        "goals_average": 1.38
      }
    ],
    "top_cards": [
      {
        "team": "Goiás",
        "cards": 3.1
      },
      {
        "team": "Coritiba",
        "cards": 3.0
      },
      {
        "team": "Ceará",
        "cards": 2.9
      },
      {
        "team": "Juventude",
        "cards": 2.9
      },
      {
        "team": "Internacional",
        "cards": 2.9
      }
    ]
  },
  "2020": {
    "total_matches": 380,
    "total_goals": 944,
    "goals_average": 2.48,
    "total_yellow_cards": 1686,
    "yellow_cards_average": 4.44,
    "total_red_cards": 109,
    "red_cards_average": 0.29,
    "home_win_percentage": 0.45,
    "draw_percentage": 0.2842,
    "away_win_percentage": 0.2658,
    "result_distribution": [
      {
        "name": "Mandante",
        "value": 45
      },
      {
        "name": "Empate",
        "value": 28
      },
      {
        "name": "Visitante",
        "value": 27
      }
    ],
    "goals_by_season": [
      {
        "season": "2020",
        "goals_average": 2.48
      },
      {
        "season": "2021",
        "goals_average": 2.22
      },
      {
        "season": "2022",
        "goals_average": 2.38
      },
      {
        "season": "2023",
        "goals_average": 2.49
      }
    ],
    "cards_by_season": [
      {
        "season": "2020",
        "yellow": 4.44,
        "red": 0.29
      },
      {
        "season": "2021",
        "yellow": 4.66,
        "red": 0.25
      },
      {
        "season": "2022",
        "yellow": 5.11,
        "red": 0.32
      },
      {
        "season": "2023",
        "yellow": 5.47,
        "red": 0.32
      }
    ],
    "top_winners": [
      {
        "team": "Flamengo",
        "wins": 21
      },
      {
        "team": "Internacional",
        "wins": 20
      },
      {
        "team": "Atlético-MG",
        "wins": 20
      },
      {
        "team": "São Paulo",
        "wins": 18
      },
      {
        "team": "Fluminense",
        "wins": 18
      }
    ],
    "top_goals": [
      {
        "team": "Flamengo",
        "goals_average": 1.79
      },
      {
        "team": "Atlético-MG",
        "goals_average": 1.68
      },
      {
        "team": "Internacional",
        "goals_average": 1.61
      },
      {
        "team": "São Paulo",
        "goals_average": 1.55
      },
      {
        "team": "Fluminense",
        "goals_average": 1.45
      }
    ],
    "top_cards": [
      {
        "team": "Goiás",
        "cards": 3.1
      },
      {
        "team": "Internacional",
        "cards": 2.6
      },
      {
        "team": "Ceará",
        "cards": 2.6
      },
      {
        "team": "Sport",
        "cards": 2.5
      },
      {
        "team": "Palmeiras",
        "cards": 2.5
      }
    ]
  },
  "2021": {
    "total_matches": 380,
    "total_goals": 842,
    "goals_average": 2.22,
    "total_yellow_cards": 1769,
    "yellow_cards_average": 4.66,
    "total_red_cards": 94,
    "red_cards_average": 0.25,
    "home_win_percentage": 0.4579,
    "draw_percentage": 0.2974,
    "away_win_percentage": 0.2447,
    "result_distribution": [
      {
        "name": "Mandante",
        "value": 46
      },
      {
        "name": "Empate",
        "value": 30
      },
      {
        "name": "Visitante",
        "value": 24
      }
    ],
    "goals_by_season": [
      {
        "season": "2020",
        "goals_average": 2.48
      },
      {
        "season": "2021",
        "goals_average": 2.22
      },
      {
        "season": "2022",
        "goals_average": 2.38
      },
      {
        "season": "2023",
        "goals_average": 2.49
      }
    ],
    "cards_by_season": [
      {
        "season": "2020",
        "yellow": 4.44,
        "red": 0.29
      },
      {
        "season": "2021",
        "yellow": 4.66,
        "red": 0.25
      },
      {
        "season": "2022",
        "yellow": 5.11,
        "red": 0.32
      },
      {
        "season": "2023",
        "yellow": 5.47,
        "red": 0.32
      }
    ],
    "top_winners": [
      {
        "team": "Atlético-MG",
        "wins": 26
      },
      {
        "team": "Flamengo",
        "wins": 21
      },
      {
        "team": "Palmeiras",
        "wins": 20
      },
      {
        "team": "Fortaleza",
        "wins": 17
      },
      {
        "team": "Fluminense",
        "wins": 15
      }
    ],
    "top_goals": [
      {
        "team": "Flamengo",
        "goals_average": 1.82
      },
      {
        "team": "Atlético-MG",
        "goals_average": 1.76
      },
      {
        "team": "Palmeiras",
        "goals_average": 1.53
      },
      {
        "team": "Bragantino",
        "goals_average": 1.45
      },
      {
        "team": "Fortaleza",
        "goals_average": 1.16
      }
    ],
    "top_cards": [
      {
        "team": "Internacional",
        "cards": 3.1
      },
      {
        "team": "Grêmio",
        "cards": 3.1
      },
      {
        "team": "Santos",
        "cards": 2.7
      },
      {
        "team": "São Paulo",
        "cards": 2.6
      },
      {
        "team": "Sport",
        "cards": 2.6
      }
    ]
  },
  "2022": {
    "total_matches": 380,
    "total_goals": 905,
    "goals_average": 2.38,
    "total_yellow_cards": 1940,
    "yellow_cards_average": 5.11,
    "total_red_cards": 122,
    "red_cards_average": 0.32,
    "home_win_percentage": 0.4421,
    "draw_percentage": 0.2842,
    "away_win_percentage": 0.2737,
    "result_distribution": [
      {
        "name": "Mandante",
        "value": 44
      },
      {
        "name": "Empate",
        "value": 28
      },
      {
        "name": "Visitante",
        "value": 27
      }
    ],
    "goals_by_season": [
      {
        "season": "2020",
        "goals_average": 2.48
      },
      {
        "season": "2021",
        "goals_average": 2.22
      },
      {
        "season": "2022",
        "goals_average": 2.38
      },
      {
        "season": "2023",
        "goals_average": 2.49
      }
    ],
    "cards_by_season": [
      {
        "season": "2020",
        "yellow": 4.44,
        "red": 0.29
      },
      {
        "season": "2021",
        "yellow": 4.66,
        "red": 0.25
      },
      {
        "season": "2022",
        "yellow": 5.11,
        "red": 0.32
      },
      {
        "season": "2023",
        "yellow": 5.47,
        "red": 0.32
      }
    ],
    "top_winners": [
      {
        "team": "Palmeiras",
        "wins": 23
      },
      {
        "team": "Fluminense",
        "wins": 21
      },
      {
        "team": "Internacional",
        "wins": 20
      },
      {
        "team": "Corinthians",
        "wins": 18
      },
      {
        "team": "Flamengo",
        "wins": 18
      }
    ],
    "top_goals": [
      {
        "team": "Palmeiras",
        "goals_average": 1.74
      },
      {
        "team": "Fluminense",
        "goals_average": 1.66
      },
      {
        "team": "Flamengo",
        "goals_average": 1.58
      },
      {
        "team": "Internacional",
        "goals_average": 1.53
      },
      {
        "team": "São Paulo",
        "goals_average": 1.45
      }
    ],
    "top_cards": [
      {
        "team": "Ceará",
        "cards": 3.7
      },
      {
        "team": "Coritiba",
        "cards": 3.3
      },
      {
        "team": "Juventude",
        "cards": 3.2
      },
      {
        "team": "Goiás",
        "cards": 3.1
      },
      {
        "team": "São Paulo",
        "cards": 3.0
      }
    ]
  },
  "2023": {
    "total_matches": 380,
    "total_goals": 946,
    "goals_average": 2.49,
    "total_yellow_cards": 2079,
    "yellow_cards_average": 5.47,
    "total_red_cards": 122,
    "red_cards_average": 0.32,
    "home_win_percentage": 0.4684,
    "draw_percentage": 0.2579,
    "away_win_percentage": 0.2737,
    "result_distribution": [
      {
        "name": "Mandante",
        "value": 47
      },
      {
        "name": "Empate",
        "value": 26
      },
      {
        "name": "Visitante",
        "value": 27
      }
    ],
    "goals_by_season": [
      {
        "season": "2020",
        "goals_average": 2.48
      },
      {
        "season": "2021",
        "goals_average": 2.22
      },
      {
        "season": "2022",
        "goals_average": 2.38
      },
      {
        "season": "2023",
        "goals_average": 2.49
      }
    ],
    "cards_by_season": [
      {
        "season": "2020",
        "yellow": 4.44,
        "red": 0.29
      },
      {
        "season": "2021",
        "yellow": 4.66,
        "red": 0.25
      },
      {
        "season": "2022",
        "yellow": 5.11,
        "red": 0.32
      },
      {
        "season": "2023",
        "yellow": 5.47,
        "red": 0.32
      }
    ],
    "top_winners": [
      {
        "team": "Grêmio",
        "wins": 21
      },
      {
        "team": "Palmeiras",
        "wins": 20
      },
      {
        "team": "Flamengo",
        "wins": 19
      },
      {
        "team": "Atlético-MG",
        "wins": 19
      },
      {
        "team": "Botafogo",
        "wins": 18
      }
    ],
    "top_goals": [
      {
        "team": "Palmeiras",
        "goals_average": 1.68
      },
      {
        "team": "Grêmio",
        "goals_average": 1.66
      },
      {
        "team": "Botafogo",
        "goals_average": 1.53
      },
      {
        "team": "Flamengo",
        "goals_average": 1.47
      },
      {
        "team": "Atlético-MG",
        "goals_average": 1.37
      }
    ],
    "top_cards": [
      {
        "team": "Fluminense",
        "cards": 3.7
      },
      {
        "team": "Coritiba",
        "cards": 3.4
      },
      {
        "team": "Atlético-MG",
        "cards": 3.2
      },
      {
        "team": "Internacional",
        "cards": 3.1
      },
      {
        "team": "Bragantino",
        "cards": 3.0
      }
    ]
  }
};

export const mockOverview: OverviewStats = mockOverviewsBySeason['all'];

export function getMockOverview(filters: StatsFilters): OverviewStats {
  const season = filters.season || 'all';
  const base = mockOverviewsBySeason[season] || mockOverviewsBySeason['all'];
  if (filters.team && filters.team !== 'all') {
    // Filtro por time selecionado
    const teamName = filters.team;
    return {
      ...base,
      top_winners: base.top_winners.filter((w) => w.team.toLowerCase().includes(teamName.toLowerCase())),
      top_goals: base.top_goals.filter((g) => g.team.toLowerCase().includes(teamName.toLowerCase())),
      top_cards: base.top_cards.filter((c) => c.team.toLowerCase().includes(teamName.toLowerCase())),
    };
  }
  return base;
}

const baseMatches: Match[] = [
  {
    "id": "1520",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Cuiabá",
    "away_team": "Athletico-PR",
    "score": "3 x 0",
    "yellow_cards": 7,
    "red_cards": 1,
    "stadium": "Arena Pantanal"
  },
  {
    "id": "1519",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Bahia",
    "away_team": "Atlético-MG",
    "score": "4 x 1",
    "yellow_cards": 4,
    "red_cards": 0,
    "stadium": "Arena Fonte Nova"
  },
  {
    "id": "1518",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Coritiba",
    "away_team": "Corinthians",
    "score": "0 x 2",
    "yellow_cards": 1,
    "red_cards": 0,
    "stadium": "Couto Pereira"
  },
  {
    "id": "1517",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Internacional",
    "away_team": "Botafogo",
    "score": "3 x 1",
    "yellow_cards": 3,
    "red_cards": 0,
    "stadium": "Beira-Rio"
  },
  {
    "id": "1516",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Cruzeiro",
    "away_team": "Palmeiras",
    "score": "1 x 1",
    "yellow_cards": 2,
    "red_cards": 0,
    "stadium": "Mineirão"
  },
  {
    "id": "1515",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Santos",
    "away_team": "Fortaleza",
    "score": "1 x 2",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Vila Belmiro"
  },
  {
    "id": "1514",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "São Paulo",
    "away_team": "Flamengo",
    "score": "1 x 0",
    "yellow_cards": 3,
    "red_cards": 0,
    "stadium": "Morumbi"
  },
  {
    "id": "1513",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Vasco",
    "away_team": "Bragantino",
    "score": "2 x 1",
    "yellow_cards": 4,
    "red_cards": 1,
    "stadium": "São Januário"
  },
  {
    "id": "1512",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Fluminense",
    "away_team": "Grêmio",
    "score": "2 x 3",
    "yellow_cards": 6,
    "red_cards": 0,
    "stadium": "Estádio Jornalista Mário Filho (Maracanã)"
  },
  {
    "id": "1511",
    "date": "2023-12-06",
    "season": "2023",
    "home_team": "Goiás",
    "away_team": "América-MG",
    "score": "1 x 0",
    "yellow_cards": 4,
    "red_cards": 0,
    "stadium": "Estádio Hailé Pinheiro (Serrinha)"
  },
  {
    "id": "1507",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Grêmio",
    "away_team": "Vasco",
    "score": "1 x 0",
    "yellow_cards": 4,
    "red_cards": 0,
    "stadium": "Arena do Grêmio"
  },
  {
    "id": "1505",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Botafogo",
    "away_team": "Cruzeiro",
    "score": "0 x 0",
    "yellow_cards": 7,
    "red_cards": 0,
    "stadium": "Estádio Nilton Santos"
  },
  {
    "id": "1506",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Bragantino",
    "away_team": "Coritiba",
    "score": "1 x 0",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Nabizão"
  },
  {
    "id": "1509",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Fortaleza",
    "away_team": "Goiás",
    "score": "1 x 0",
    "yellow_cards": 6,
    "red_cards": 0,
    "stadium": "Castelão"
  },
  {
    "id": "1508",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Athletico-PR",
    "away_team": "Santos",
    "score": "3 x 0",
    "yellow_cards": 9,
    "red_cards": 0,
    "stadium": "Arena da Baixada"
  },
  {
    "id": "1510",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "América-MG",
    "away_team": "Bahia",
    "score": "3 x 2",
    "yellow_cards": 2,
    "red_cards": 1,
    "stadium": "Estádio Raimundo Sampaio"
  },
  {
    "id": "1504",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Palmeiras",
    "away_team": "Fluminense",
    "score": "1 x 0",
    "yellow_cards": 3,
    "red_cards": 1,
    "stadium": "Allianz Parque"
  },
  {
    "id": "1503",
    "date": "2023-12-03",
    "season": "2023",
    "home_team": "Flamengo",
    "away_team": "Cuiabá",
    "score": "2 x 1",
    "yellow_cards": 3,
    "red_cards": 0,
    "stadium": "Estádio Jornalista Mário Filho (Maracanã)"
  },
  {
    "id": "1502",
    "date": "2023-12-02",
    "season": "2023",
    "home_team": "Atlético-MG",
    "away_team": "São Paulo",
    "score": "2 x 1",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Mineirão"
  },
  {
    "id": "1501",
    "date": "2023-12-02",
    "season": "2023",
    "home_team": "Corinthians",
    "away_team": "Internacional",
    "score": "1 x 2",
    "yellow_cards": 4,
    "red_cards": 1,
    "stadium": "Neo Química Arena"
  },
  {
    "id": "1500",
    "date": "2023-11-30",
    "season": "2023",
    "home_team": "Bragantino",
    "away_team": "Fortaleza",
    "score": "1 x 2",
    "yellow_cards": 5,
    "red_cards": 2,
    "stadium": "Nabizão"
  },
  {
    "id": "1499",
    "date": "2023-11-30",
    "season": "2023",
    "home_team": "Cruzeiro",
    "away_team": "Athletico-PR",
    "score": "1 x 1",
    "yellow_cards": 7,
    "red_cards": 0,
    "stadium": "Mineirão"
  },
  {
    "id": "1498",
    "date": "2023-11-30",
    "season": "2023",
    "home_team": "Grêmio",
    "away_team": "Goiás",
    "score": "2 x 1",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Arena do Grêmio"
  },
  {
    "id": "1496",
    "date": "2023-11-29",
    "season": "2023",
    "home_team": "Palmeiras",
    "away_team": "América-MG",
    "score": "4 x 0",
    "yellow_cards": 4,
    "red_cards": 0,
    "stadium": "Allianz Parque"
  },
  {
    "id": "1497",
    "date": "2023-11-29",
    "season": "2023",
    "home_team": "Coritiba",
    "away_team": "Botafogo",
    "score": "1 x 1",
    "yellow_cards": 5,
    "red_cards": 2,
    "stadium": "Couto Pereira"
  },
  {
    "id": "1495",
    "date": "2023-11-29",
    "season": "2023",
    "home_team": "Cuiabá",
    "away_team": "Internacional",
    "score": "0 x 2",
    "yellow_cards": 6,
    "red_cards": 0,
    "stadium": "Arena Pantanal"
  },
  {
    "id": "1494",
    "date": "2023-11-29",
    "season": "2023",
    "home_team": "Bahia",
    "away_team": "São Paulo",
    "score": "0 x 1",
    "yellow_cards": 7,
    "red_cards": 0,
    "stadium": "Arena Fonte Nova"
  },
  {
    "id": "1493",
    "date": "2023-11-29",
    "season": "2023",
    "home_team": "Flamengo",
    "away_team": "Atlético-MG",
    "score": "0 x 3",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Estádio Jornalista Mário Filho (Maracanã)"
  },
  {
    "id": "1492",
    "date": "2023-11-29",
    "season": "2023",
    "home_team": "Santos",
    "away_team": "Fluminense",
    "score": "0 x 3",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Vila Belmiro"
  },
  {
    "id": "1491",
    "date": "2023-11-28",
    "season": "2023",
    "home_team": "Vasco",
    "away_team": "Corinthians",
    "score": "2 x 4",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "São Januário"
  },
  {
    "id": "1490",
    "date": "2023-11-27",
    "season": "2023",
    "home_team": "Goiás",
    "away_team": "Cruzeiro",
    "score": "0 x 1",
    "yellow_cards": 6,
    "red_cards": 0,
    "stadium": "Estádio Hailé Pinheiro (Serrinha)"
  },
  {
    "id": "1486",
    "date": "2023-11-26",
    "season": "2023",
    "home_team": "São Paulo",
    "away_team": "Cuiabá",
    "score": "0 x 0",
    "yellow_cards": 2,
    "red_cards": 0,
    "stadium": "Morumbi"
  },
  {
    "id": "1489",
    "date": "2023-11-26",
    "season": "2023",
    "home_team": "América-MG",
    "away_team": "Flamengo",
    "score": "0 x 3",
    "yellow_cards": 8,
    "red_cards": 0,
    "stadium": "Estádio Municipal João Havelange"
  },
  {
    "id": "1488",
    "date": "2023-11-26",
    "season": "2023",
    "home_team": "Fortaleza",
    "away_team": "Palmeiras",
    "score": "2 x 2",
    "yellow_cards": 5,
    "red_cards": 1,
    "stadium": "Castelão"
  },
  {
    "id": "1487",
    "date": "2023-11-26",
    "season": "2023",
    "home_team": "Internacional",
    "away_team": "Bragantino",
    "score": "1 x 0",
    "yellow_cards": 10,
    "red_cards": 0,
    "stadium": "Beira-Rio"
  },
  {
    "id": "1484",
    "date": "2023-11-26",
    "season": "2023",
    "home_team": "Botafogo",
    "away_team": "Santos",
    "score": "1 x 1",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Estádio Nilton Santos"
  },
  {
    "id": "1485",
    "date": "2023-11-26",
    "season": "2023",
    "home_team": "Atlético-MG",
    "away_team": "Grêmio",
    "score": "3 x 0",
    "yellow_cards": 4,
    "red_cards": 0,
    "stadium": "Arena MRV"
  },
  {
    "id": "1483",
    "date": "2023-11-25",
    "season": "2023",
    "home_team": "Fluminense",
    "away_team": "Coritiba",
    "score": "2 x 1",
    "yellow_cards": 4,
    "red_cards": 0,
    "stadium": "Estádio Jornalista Mário Filho (Maracanã)"
  },
  {
    "id": "1482",
    "date": "2023-11-25",
    "season": "2023",
    "home_team": "Athletico-PR",
    "away_team": "Vasco",
    "score": "0 x 0",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Arena da Baixada"
  },
  {
    "id": "1481",
    "date": "2023-11-24",
    "season": "2023",
    "home_team": "Corinthians",
    "away_team": "Bahia",
    "score": "1 x 5",
    "yellow_cards": 5,
    "red_cards": 0,
    "stadium": "Neo Química Arena"
  }
];

export function createMockPrediction(
  homeTeam: Team,
  awayTeam: Team,
  matchId?: string,
): PredictionResponse {
  // Busca partida real do dataset se matchId for informado
  let realMatch: Match | undefined;
  if (matchId) {
    realMatch = baseMatches.find((m) => m.id === matchId);
  } else {
    // Procura se o confronto ocorreu no dataset de 2023
    realMatch = baseMatches.find(
      (m) =>
        m.season === '2023' &&
        m.home_team.toLowerCase() === homeTeam.name.toLowerCase() &&
        m.away_team.toLowerCase() === awayTeam.name.toLowerCase(),
    );
  }

  const homeStats: TeamForm = mockTeamsStats[homeTeam.name] || {
    last_five: ['V', 'E', 'V', 'D', 'V'],
    points_average: 1.6,
    goals_scored_average: 1.4,
    goals_conceded_average: 1.1,
    yellow_cards_average: 2.3,
    red_cards_average: 0.1,
  };

  const awayStats: TeamForm = mockTeamsStats[awayTeam.name] || {
    last_five: ['D', 'E', 'V', 'D', 'E'],
    points_average: 1.1,
    goals_scored_average: 1.0,
    goals_conceded_average: 1.4,
    yellow_cards_average: 2.5,
    red_cards_average: 0.2,
  };

  // Cálculo probabilístico fundamentado no modelo de Regressão Logística e vantagem de mando
  // Na Série A: mandantes vencem 45.5%, empates 28.1%, visitantes 26.4%
  const diffPontos = homeStats.points_average - awayStats.points_average;
  const diffGols = homeStats.goals_scored_average - awayStats.goals_scored_average;
  const diffSaldo = (homeStats.goals_scored_average - homeStats.goals_conceded_average) -
                    (awayStats.goals_scored_average - awayStats.goals_conceded_average);

  const sinalForca = diffPontos * 0.45 + diffGols * 0.25 + diffSaldo * 0.3;

  // Logits calibrados
  const logitHome = 0.50 + sinalForca;
  const logitDraw = 0.05 - Math.abs(sinalForca) * 0.35;
  const logitAway = -0.35 - sinalForca;

  const expH = Math.exp(logitHome);
  const expD = Math.exp(logitDraw);
  const expA = Math.exp(logitAway);
  const soma = expH + expD + expA;

  let pHome = Math.round((expH / soma) * 1000) / 1000;
  let pDraw = Math.round((expD / soma) * 1000) / 1000;
  let pAway = Math.round((1 - pHome - pDraw) * 1000) / 1000;

  if (pAway < 0.05) {
    pAway = 0.05;
    pDraw = Math.round((1 - pHome - pAway) * 1000) / 1000;
  }

  const probabilities: Record<ResultClass, number> = {
    home_win: pHome,
    draw: pDraw,
    away_win: pAway,
  };

  const prediction = (Object.entries(probabilities).sort((a, b) => b[1] - a[1])[0][0]) as ResultClass;

  const labels: Record<ResultClass, string> = {
    home_win: Vitória do ,
    draw: 'Empate',
    away_win: Vitória do ,
  };

  const explanations = [
    Aproveitamento recente:  obteve média de  pts/jogo contra  do .,
    Equilíbrio de gols:  marcou média de  gols/jogo (sofreu ).,
    realMatch
      ? Partida real catalogada em  no  (Placar: ).
      : Vantagem histórica do mando de campo na Série A (mandantes vencem 45,5% dos jogos analisados).,
  ];

  return {
    prediction,
    label: labels[prediction],
    confidence: probabilities[prediction],
    probabilities,
    home_team_form: homeStats,
    away_team_form: awayStats,
    explanations,
  };
}

export function getMockMatches(params: {
  season?: string;
  team?: string;
  page?: number;
  pageSize?: number;
}): MatchesResponse {
  const page = params.page ?? 1;
  const pageSize = params.pageSize ?? 5;
  const filtered = baseMatches.filter((match) => {
    const seasonMatches = !params.season || params.season === 'all' || match.season === params.season;
    const teamMatches =
      !params.team ||
      params.team === 'all' ||
      match.home_team.toLowerCase().includes(params.team.toLowerCase()) ||
      match.away_team.toLowerCase().includes(params.team.toLowerCase());

    return seasonMatches && teamMatches;
  });

  return {
    matches: filtered.slice((page - 1) * pageSize, page * pageSize),
    total: filtered.length,
    page,
    pages: Math.max(1, Math.ceil(filtered.length / pageSize)),
  };
}

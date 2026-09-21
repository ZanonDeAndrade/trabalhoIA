import { useEffect, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { ErrorState } from '../components/feedback/ErrorState'
import { LoadingState } from '../components/feedback/LoadingState'
import { MetricCard } from '../components/MetricCard'
import { ChartCard } from '../components/statistics/ChartCard'
import { MatchesTable } from '../components/statistics/MatchesTable'
import { getMatches, getOverview } from '../services/api'
import type { MatchesResponse, OverviewStats, StatsFilters } from '../types/api'
import { formatNumber, formatPercent, getReadableError } from '../utils/format'

const initialFilters: StatsFilters = {
  season: 'all',
  team: 'all',
  venue: 'all',
}

export function Statistics() {
  const [filters, setFilters] = useState<StatsFilters>(initialFilters)
  const [overview, setOverview] = useState<OverviewStats | null>(null)
  const [matches, setMatches] = useState<MatchesResponse | null>(null)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [source, setSource] = useState<'api' | 'mock'>('api')

  async function load() {
    setLoading(true)
    setError('')

    try {
      const [overviewResult, matchesResult] = await Promise.all([
        getOverview(filters),
        getMatches(filters, page),
      ])
      setOverview(overviewResult.overview)
      setMatches(matchesResult.matches)
      setSource(overviewResult.source === 'mock' || matchesResult.source === 'mock' ? 'mock' : 'api')
    } catch (err) {
      setError(getReadableError(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void load()
  }, [filters, page])

  function updateFilter(key: keyof StatsFilters, value: string) {
    setPage(1)
    setFilters((current) => ({ ...current, [key]: value }))
  }

  return (
    <div className="page-stack">
      <section className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Estatísticas</p>
          <h1>Análise exploratória do dataset</h1>
          <p>Use filtros para apoiar a demonstração dos dados processados e agregados pela API.</p>
        </div>

        <div className="filters-grid">
          <label className="field" htmlFor="season-filter">
            <span>Temporada</span>
            <select
              id="season-filter"
              value={filters.season}
              onChange={(event) => updateFilter('season', event.target.value)}
            >
              <option value="all">Todas</option>
              <option value="2020">2020</option>
              <option value="2021">2021</option>
              <option value="2022">2022</option>
              <option value="2023">2023</option>
            </select>
          </label>
          <label className="field" htmlFor="team-filter">
            <span>Equipe</span>
            <input
              id="team-filter"
              value={filters.team === 'all' ? '' : filters.team}
              placeholder="Buscar equipe"
              onChange={(event) => updateFilter('team', event.target.value || 'all')}
            />
          </label>
          <label className="field" htmlFor="venue-filter">
            <span>Mando de campo</span>
            <select
              id="venue-filter"
              value={filters.venue}
              onChange={(event) => updateFilter('venue', event.target.value)}
            >
              <option value="all">Todos</option>
              <option value="home">Mandante</option>
              <option value="away">Visitante</option>
            </select>
          </label>
          <button className="button secondary" type="button" onClick={() => setFilters(initialFilters)}>
            Limpar filtros
          </button>
        </div>
      </section>

      {source === 'mock' && (
        <div className="notice" role="status">
          API de estatísticas indisponível. Exibindo dados simulados para demonstração.
        </div>
      )}

      {loading && <LoadingState message="Carregando estatísticas..." />}
      {error && <ErrorState message={error} onRetry={load} />}

      {!loading && overview && matches && (
        <>
          <section className="metrics-grid" aria-label="Indicadores do dataset">
            <MetricCard label="Partidas" value={formatNumber(overview.total_matches)} />
            <MetricCard
              label="Gols"
              value={formatNumber(overview.total_goals)}
              helper={`média ${formatNumber(overview.goals_average, 2)}`}
            />
            <MetricCard
              label="Cartões amarelos"
              value={formatNumber(overview.total_yellow_cards)}
              helper={`média ${formatNumber(overview.yellow_cards_average, 2)}`}
            />
            <MetricCard
              label="Cartões vermelhos"
              value={formatNumber(overview.total_red_cards)}
              helper={`média ${formatNumber(overview.red_cards_average, 2)}`}
            />
            <MetricCard label="Vitórias mandante" value={formatPercent(overview.home_win_percentage)} />
            <MetricCard label="Empates" value={formatPercent(overview.draw_percentage)} />
            <MetricCard label="Vitórias visitante" value={formatPercent(overview.away_win_percentage)} />
          </section>

          <section className="charts-grid">
            <ChartCard title="Resultados por classe" summary="Distribuição entre mandante, empate e visitante.">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={overview.result_distribution}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" name="Percentual" fill="#22c55e" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Média de gols por temporada" summary="Evolução anual da média de gols.">
              <ResponsiveContainer width="100%" height={260}>
                <LineChart data={overview.goals_by_season}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line dataKey="goals_average" name="Média de gols" stroke="#22c55e" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Cartões por temporada" summary="Médias de amarelos e vermelhos por jogo.">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={overview.cards_by_season}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="yellow" name="Amarelos" fill="#f59e0b" />
                  <Bar dataKey="red" name="Vermelhos" fill="#ef4444" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Equipes com mais vitórias" summary="Ranking agregado do período analisado.">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={overview.top_winners} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="team" type="category" width={96} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="wins" name="Vitórias" fill="#86efac" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
          </section>

          <section className="section-block">
            <div className="section-heading compact">
              <h2>Tabela de partidas</h2>
              <p>Busca, ordenação temporal e paginação para consulta durante a apresentação.</p>
            </div>
            <MatchesTable data={matches} onPageChange={setPage} />
          </section>
        </>
      )}
    </div>
  )
}

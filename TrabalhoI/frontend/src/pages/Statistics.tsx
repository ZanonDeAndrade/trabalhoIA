import { useState } from 'react'
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
import { EmptyState } from '../components/feedback/EmptyState'
import { ErrorState } from '../components/feedback/ErrorState'
import { LoadingState } from '../components/feedback/LoadingState'
import { MetricCard } from '../components/MetricCard'
import { ChartCard } from '../components/statistics/ChartCard'
import { MatchesTable } from '../components/statistics/MatchesTable'
import { useAsyncData } from '../hooks/useAsyncData'
import { getCharts, getMatches, getOverview, getTeams } from '../services/api'
import type { StatsFilters } from '../types/api'
import { formatNumber, formatPercent } from '../utils/format'

const initialFilters: StatsFilters = { season: 'all', team: 'all', venue: 'all' }
const SEASONS = ['2020', '2021', '2022', '2023']

export function Statistics() {
  const [filters, setFilters] = useState<StatsFilters>(initialFilters)
  const [page, setPage] = useState(1)
  const filterKey = `${filters.season}|${filters.team}|${filters.venue}`

  const teams = useAsyncData(getTeams, 'teams')
  const overview = useAsyncData((signal) => getOverview(filters, signal), `overview|${filterKey}`)
  const charts = useAsyncData((signal) => getCharts(filters, signal), `charts|${filterKey}`)
  const matches = useAsyncData((signal) => getMatches(filters, page, signal), `matches|${filterKey}|${page}`)

  const error = overview.error || charts.error || matches.error
  const loading = overview.loading || charts.loading || matches.loading
  const hasData = Boolean(overview.data && charts.data && matches.data)

  function updateFilter(key: keyof StatsFilters, value: string) {
    setPage(1)
    setFilters((current) => ({
      ...current,
      [key]: value,
      ...(key === 'team' && value === 'all' ? { venue: 'all' } : {}),
    }))
  }

  function retry() {
    overview.retry()
    charts.retry()
    matches.retry()
  }

  const o = overview.data
  const c = charts.data
  const noMatches = o?.total_matches === 0

  return (
    <div className="page-stack">
      <section className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Estatísticas</p>
          <h1>Análise exploratória do dataset</h1>
          <p>Indicadores, gráficos e partidas calculados pela API a partir da base processada de 2020 a 2023.</p>
        </div>

        <div className="filters-grid">
          <label className="field" htmlFor="season-filter">
            <span>Temporada</span>
            <select id="season-filter" value={filters.season} onChange={(e) => updateFilter('season', e.target.value)}>
              <option value="all">Todas</option>
              {SEASONS.map((season) => (
                <option key={season} value={season}>{season}</option>
              ))}
            </select>
          </label>
          <label className="field" htmlFor="team-filter">
            <span>Equipe</span>
            <select
              id="team-filter"
              value={filters.team}
              disabled={!teams.data}
              onChange={(e) => updateFilter('team', e.target.value)}
            >
              <option value="all">Todas</option>
              {teams.data?.teams.map((team) => (
                <option key={team.id} value={team.id}>{team.name}</option>
              ))}
            </select>
          </label>
          <label className="field" htmlFor="venue-filter">
            <span>Mando de campo</span>
            <select
              id="venue-filter"
              value={filters.venue}
              disabled={filters.team === 'all'}
              aria-describedby="venue-hint"
              onChange={(e) => updateFilter('venue', e.target.value)}
            >
              <option value="all">Todos</option>
              <option value="home">Como mandante</option>
              <option value="away">Como visitante</option>
            </select>
            <small id="venue-hint" className="field-hint">Disponível ao escolher uma equipe.</small>
          </label>
          <button
            className="button secondary"
            type="button"
            onClick={() => {
              setPage(1)
              setFilters(initialFilters)
            }}
          >
            Limpar filtros
          </button>
        </div>
      </section>

      {teams.error && <div className="notice warning" role="alert">Lista de equipes indisponível: {teams.error}</div>}
      {error && <ErrorState message={error} onRetry={retry} />}
      {loading && !hasData && !error && <LoadingState message="Carregando estatísticas..." />}

      {noMatches && (
        <EmptyState title="Nenhuma partida encontrada" message="Não há jogos para essa combinação de filtros. Ajuste a temporada, a equipe ou o mando." />
      )}

      {hasData && !noMatches && o && c && (
        <div className="page-stack" aria-busy={loading}>
          <section className="metrics-grid" aria-label="Indicadores do recorte selecionado">
            <MetricCard label="Partidas" value={formatNumber(o.total_matches)} />
            <MetricCard label="Gols" value={formatNumber(o.total_goals)} helper={`média ${formatNumber(o.goals_average, 2)} por jogo`} />
            <MetricCard label="Cartões amarelos" value={formatNumber(o.total_yellow_cards)} helper={`média ${formatNumber(o.yellow_cards_average, 2)}`} />
            <MetricCard label="Expulsões" value={formatNumber(o.total_red_cards)} helper={`média ${formatNumber(o.red_cards_average, 2)}`} />
            <MetricCard label="Vitórias mandante" value={formatPercent(o.home_win_percentage, 1)} />
            <MetricCard label="Empates" value={formatPercent(o.draw_percentage, 1)} />
            <MetricCard label="Vitórias visitante" value={formatPercent(o.away_win_percentage, 1)} />
            <MetricCard
              label="Público médio"
              value={o.attendance_average === null ? 'Sem dados' : formatNumber(o.attendance_average)}
              helper={o.matches_without_attendance > 0 ? `${formatNumber(o.matches_without_attendance)} partidas sem público informado` : undefined}
            />
          </section>

          <section className="charts-grid">
            <ChartCard title="Resultados por classe" summary="Percentual de vitórias do mandante, empates e vitórias do visitante.">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={c.result_distribution}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis unit="%" />
                  <Tooltip />
                  <Bar dataKey="value" name="Percentual" fill="#22c55e" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Média de gols por temporada" summary="Gols por partida em cada temporada do recorte.">
              <ResponsiveContainer width="100%" height={260}>
                <LineChart data={c.goals_by_season}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis domain={['auto', 'auto']} />
                  <Tooltip />
                  <Line dataKey="goals_average" name="Média de gols" stroke="#22c55e" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Cartões por temporada" summary="Médias de amarelos e expulsões por jogo.">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={c.cards_by_season}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="yellow" name="Amarelos" fill="#f59e0b" />
                  <Bar dataKey="red" name="Expulsões" fill="#ef4444" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Público médio por temporada" summary="Considera apenas partidas com público informado.">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={c.attendance_by_season}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="season" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="attendance_average" name="Público médio" fill="#3d8bff" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>
            <ChartCard title="Equipes com mais vitórias" summary="Ranking do recorte, disponível sem filtro de equipe.">
              {c.rankings_available ? (
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={c.top_winners} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="team" type="category" width={96} />
                    <Tooltip />
                    <Bar dataKey="wins" name="Vitórias" fill="#86efac" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <EmptyState title="Ranking indisponível" message="Remova o filtro de equipe para comparar as equipes." />
              )}
            </ChartCard>
            <ChartCard title="Equipes com mais cartões por jogo" summary="Amarelos mais expulsões por partida, disponível sem filtro de equipe.">
              {c.rankings_available ? (
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={c.top_cards} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="team" type="category" width={96} />
                    <Tooltip />
                    <Bar dataKey="cards" name="Cartões por jogo" fill="#f59e0b" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <EmptyState title="Ranking indisponível" message="Remova o filtro de equipe para comparar as equipes." />
              )}
            </ChartCard>
          </section>

          <section className="section-block">
            <div className="section-heading compact">
              <h2>Tabela de partidas</h2>
              <p>Partidas mais recentes primeiro, com paginação. Público ausente aparece como “—”.</p>
            </div>
            {matches.data && <MatchesTable data={matches.data} onPageChange={setPage} />}
          </section>
        </div>
      )}
    </div>
  )
}

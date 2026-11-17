import type { PredictionResponse, Team } from '../../types/api'
import { formatPercent } from '../../utils/format'

type ProbabilityChartProps = { prediction: PredictionResponse; homeTeam: Team; awayTeam: Team }

export function ProbabilityChart({ prediction, homeTeam, awayTeam }: ProbabilityChartProps) {
  const rows = [
    { label: homeTeam.name, short: 'Mandante', value: prediction.probabilities.home_win, tone: 'home' },
    { label: 'Empate', short: 'Empate', value: prediction.probabilities.draw, tone: 'draw' },
    { label: awayTeam.name, short: 'Visitante', value: prediction.probabilities.away_win, tone: 'away' },
  ]
  return (
    <figure className="probability-list" aria-label="Probabilidades da previsão">
      <div className="probability-track" aria-hidden="true">{rows.map((row) => <span key={row.tone} className={row.tone} style={{ width: `${row.value * 100}%` }} />)}</div>
      <div className="probability-legend">
        {rows.map((row) => <div key={row.tone}><span><i className={row.tone} />{row.short}</span><strong>{formatPercent(row.value)}</strong><small>{row.label}</small></div>)}
      </div>
    </figure>
  )
}

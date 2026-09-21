import type { PredictionResponse, Team } from '../../types/api'
import { formatPercent } from '../../utils/format'

type ProbabilityChartProps = {
  prediction: PredictionResponse
  homeTeam: Team
  awayTeam: Team
}

export function ProbabilityChart({ prediction, homeTeam, awayTeam }: ProbabilityChartProps) {
  const rows = [
    { label: `Vitória do ${homeTeam.name}`, value: prediction.probabilities.home_win },
    { label: 'Empate', value: prediction.probabilities.draw },
    { label: `Vitória do ${awayTeam.name}`, value: prediction.probabilities.away_win },
  ]

  return (
    <div className="probability-list" aria-label="Probabilidades da previsão">
      {rows.map((row) => (
        <div className="probability-row" key={row.label}>
          <div>
            <span>{row.label}</span>
            <strong>{formatPercent(row.value)}</strong>
          </div>
          <div className="progress-track" aria-hidden="true">
            <span style={{ width: `${Math.round(row.value * 100)}%` }} />
          </div>
        </div>
      ))}
    </div>
  )
}

import type { Team, TeamForm } from '../../types/api'
import { formatNumber } from '../../utils/format'
import { RecentForm } from './RecentForm'

type TeamComparisonProps = {
  homeTeam: Team
  awayTeam: Team
  homeForm: TeamForm
  awayForm: TeamForm
}

const rows: Array<{ key: keyof TeamForm; label: string }> = [
  { key: 'points_average', label: 'Aproveitamento em pontos' },
  { key: 'goals_scored_average', label: 'Média de gols marcados' },
  { key: 'goals_conceded_average', label: 'Média de gols sofridos' },
  { key: 'yellow_cards_average', label: 'Média de cartões amarelos' },
  { key: 'red_cards_average', label: 'Média de cartões vermelhos' },
]

export function TeamComparison({ homeTeam, awayTeam, homeForm, awayForm }: TeamComparisonProps) {
  return (
    <section className="comparison-grid" aria-labelledby="comparison-title">
      <h3 id="comparison-title">Indicadores históricos usados pelo modelo</h3>
      {[{ team: homeTeam, form: homeForm }, { team: awayTeam, form: awayForm }].map(({ team, form }) => (
        <article className="panel" key={team.id}>
          <div className="panel-heading">
            <h4>{team.name}</h4>
            <RecentForm form={form} />
          </div>
          <dl className="stats-list">
            {rows.map((row) => (
              <div key={row.key}>
                <dt>{row.label}</dt>
                <dd>{formatNumber(form[row.key] as number, 1)}</dd>
              </div>
            ))}
          </dl>
        </article>
      ))}
    </section>
  )
}

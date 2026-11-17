import type { HeadToHead as HeadToHeadData, Team } from '../../types/api'
import { formatDate } from '../../utils/format'

type HeadToHeadProps = { homeTeam: Team; awayTeam: Team; data: HeadToHeadData }

export function HeadToHead({ homeTeam, awayTeam, data }: HeadToHeadProps) {
  return (
    <section className="panel" aria-labelledby="h2h-title">
      <h3 id="h2h-title">Confronto direto na base</h3>
      {data.matches === 0 ? (
        <p>Não há jogos anteriores entre as duas equipes na base (2020–2023).</p>
      ) : (
        <>
          <dl className="stats-list">
            <div><dt>Jogos anteriores</dt><dd>{data.matches}</dd></div>
            <div><dt>Vitórias do {homeTeam.name}</dt><dd>{data.home_team_wins}</dd></div>
            <div><dt>Empates</dt><dd>{data.draws}</dd></div>
            <div><dt>Vitórias do {awayTeam.name}</dt><dd>{data.away_team_wins}</dd></div>
          </dl>
          <ul className="plain-list">
            {data.last_matches.map((m) => (
              <li key={`${m.date}-${m.home_team}`}>
                {formatDate(m.date)}: {m.home_team} {m.score} {m.away_team}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  )
}

import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { ErrorState } from '../components/feedback/ErrorState'
import { LoadingState } from '../components/feedback/LoadingState'
import { HeadToHead } from '../components/prediction/HeadToHead'
import { ProbabilityChart } from '../components/prediction/ProbabilityChart'
import { TeamComparison } from '../components/prediction/TeamComparison'
import { TeamSelect } from '../components/prediction/TeamSelect'
import { useAsyncData } from '../hooks/useAsyncData'
import { usePrediction } from '../hooks/usePrediction'
import { getTeams } from '../services/api'
import { formatDate, formatPercent } from '../utils/format'

export function Prediction() {
  const teamsQuery = useAsyncData(getTeams, 'teams')
  const { result, loading, error, submit } = usePrediction()
  const [homeTeamId, setHomeTeamId] = useState('')
  const [awayTeamId, setAwayTeamId] = useState('')
  const [customDate, setCustomDate] = useState('')

  const teams = useMemo(() => teamsQuery.data?.teams ?? [], [teamsQuery.data])
  const reference = teamsQuery.data?.reference
  const date = customDate || reference?.default_date || ''
  const usingDefaultDate = !customDate || customDate === reference?.default_date
  const unavailableIds = useMemo(
    () => new Set(usingDefaultDate ? teams.filter((team) => !team.eligible).map((team) => team.id) : []),
    [teams, usingDefaultDate],
  )

  const homeTeam = teams.find((team) => team.id === homeTeamId)
  const awayTeam = teams.find((team) => team.id === awayTeamId)
  const sameTeam = Boolean(homeTeamId && awayTeamId && homeTeamId === awayTeamId)
  const canSubmit = Boolean(homeTeam && awayTeam && !sameTeam && !loading)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (!homeTeam || !awayTeam || sameTeam) return
    await submit({ homeTeam, awayTeam, date: usingDefaultDate ? undefined : customDate })
  }

  const prediction = result?.prediction
  const shown = result?.request

  return (
    <div className="page-stack">
      <section className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Previsão</p>
          <h1>Calcule uma previsão de resultado</h1>
          <p>
            Selecione as equipes para consultar as probabilidades do modelo e os indicadores históricos
            calculados só com jogos anteriores à data de referência.
          </p>
        </div>

        {teamsQuery.loading && !teamsQuery.data && <LoadingState message="Carregando equipes..." />}
        {teamsQuery.error && <ErrorState message={teamsQuery.error} onRetry={teamsQuery.retry} />}

        {teamsQuery.data && (
          <form className="prediction-form" onSubmit={handleSubmit}>
            <TeamSelect
              id="home-team"
              label="Time mandante"
              value={homeTeamId}
              teams={teams}
              disabledTeamId={awayTeamId}
              unavailableIds={unavailableIds}
              onChange={setHomeTeamId}
            />
            <TeamSelect
              id="away-team"
              label="Time visitante"
              value={awayTeamId}
              teams={teams}
              disabledTeamId={homeTeamId}
              unavailableIds={unavailableIds}
              error={sameTeam ? 'O visitante deve ser diferente do mandante.' : undefined}
              onChange={setAwayTeamId}
            />
            <label className="field" htmlFor="reference-date">
              <span>Data de referência</span>
              <input
                id="reference-date"
                type="date"
                value={date}
                min={reference?.min_date}
                max={reference?.max_date}
                onChange={(event) => setCustomDate(event.target.value)}
              />
            </label>
            <button className="button primary" type="submit" disabled={!canSubmit}>
              {loading ? 'Analisando...' : 'Calcular previsão'}
            </button>
            <p className="field-hint form-hint">
              A previsão usa jogos até o dia anterior à data de referência. Padrão: dia seguinte ao último jogo da
              base ({reference ? formatDate(reference.last_match_date) : '—'}).
            </p>
          </form>
        )}
      </section>

      {!prediction && !loading && !error && teamsQuery.data && (
        <div className="state-box" role="status">
          <strong>Selecione as equipes para gerar a previsão.</strong>
        </div>
      )}

      {loading && <LoadingState message="Analisando o histórico das equipes..." />}
      {error && <ErrorState title="Não foi possível gerar a previsão" message={error} />}

      {prediction && shown && (
        <section className="section-block" aria-live="polite">
          <div className="result-header">
            <div>
              <p className="eyebrow">
                {shown.homeTeam.name} x {shown.awayTeam.name}
              </p>
              <h2>{prediction.label}</h2>
              <p>Resultado mais provável, com probabilidade de {formatPercent(prediction.confidence)}.</p>
              <p className="field-hint">
                Referência: {formatDate(prediction.reference.date)}, {prediction.reference.hour}h (
                {prediction.reference.weekday}); histórico até {formatDate(prediction.reference.history_until)}.
                Confronto hipotético: não é uma partida do calendário.
              </p>
            </div>
            <span className="badge">
              {prediction.model.algorithm} v{prediction.model.version}
            </span>
          </div>

          <ProbabilityChart prediction={prediction} homeTeam={shown.homeTeam} awayTeam={shown.awayTeam} />

          <TeamComparison
            homeTeam={shown.homeTeam}
            awayTeam={shown.awayTeam}
            homeForm={prediction.home_team_form}
            awayForm={prediction.away_team_form}
          />

          <HeadToHead homeTeam={shown.homeTeam} awayTeam={shown.awayTeam} data={prediction.head_to_head} />

          {prediction.explanations.length > 0 && (
            <section className="panel">
              <h3>Fatores que mais pesam na diferença entre as duas classes mais prováveis</h3>
              <ul className="plain-list">
                {prediction.explanations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              <p className="field-hint">
                Contribuição = coeficiente da Regressão Logística × valor padronizado. Indica associação
                aprendida pelo modelo, não causa.
              </p>
            </section>
          )}

          <div className="notice warning" role="note">
            A previsão é uma estimativa estatística baseada em dados históricos de 2020 a 2023. O resultado
            real depende de fatores que não estão no dataset (escalações, lesões, clima, entre outros).
          </div>
        </section>
      )}
    </div>
  )
}

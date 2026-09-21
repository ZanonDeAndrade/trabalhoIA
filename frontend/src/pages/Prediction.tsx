import { useMemo, useState } from 'react'
import type { FormEvent } from 'react'
import { ErrorState } from '../components/feedback/ErrorState'
import { LoadingState } from '../components/feedback/LoadingState'
import { ProbabilityChart } from '../components/prediction/ProbabilityChart'
import { TeamComparison } from '../components/prediction/TeamComparison'
import { TeamSelect } from '../components/prediction/TeamSelect'
import { usePrediction } from '../hooks/usePrediction'
import { useTeams } from '../hooks/useTeams'
import { formatPercent } from '../utils/format'

export function Prediction() {
  const { teams, loading: loadingTeams, error: teamsError, source: teamsSource, retry } = useTeams()
  const { prediction, loading, error, source, submit } = usePrediction()
  const [homeTeamId, setHomeTeamId] = useState('')
  const [awayTeamId, setAwayTeamId] = useState('')

  const homeTeam = useMemo(() => teams.find((team) => team.id === homeTeamId), [homeTeamId, teams])
  const awayTeam = useMemo(() => teams.find((team) => team.id === awayTeamId), [awayTeamId, teams])
  const sameTeam = Boolean(homeTeamId && awayTeamId && homeTeamId === awayTeamId)
  const canSubmit = Boolean(homeTeam && awayTeam && !sameTeam && !loading)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()

    if (!homeTeam || !awayTeam || sameTeam) return

    await submit(homeTeam, awayTeam)
  }

  return (
    <div className="page-stack">
      <section className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Previsão</p>
          <h1>Calcule uma previsão de resultado</h1>
          <p>
            Selecione as equipes para consultar probabilidades e indicadores históricos usados pelo
            modelo.
          </p>
        </div>

        {teamsSource === 'mock' && (
          <div className="notice" role="status">
            API de equipes indisponível. Exibindo dados simulados para demonstração.
          </div>
        )}

        {loadingTeams && <LoadingState message="Carregando equipes..." />}
        {teamsError && <ErrorState message={teamsError} onRetry={retry} />}

        {!loadingTeams && !teamsError && (
          <form className="prediction-form" onSubmit={handleSubmit}>
            <TeamSelect
              id="home-team"
              label="Time mandante"
              value={homeTeamId}
              teams={teams}
              disabledTeamId={awayTeamId}
              onChange={setHomeTeamId}
            />
            <TeamSelect
              id="away-team"
              label="Time visitante"
              value={awayTeamId}
              teams={teams}
              disabledTeamId={homeTeamId}
              error={sameTeam ? 'O visitante deve ser diferente do mandante.' : undefined}
              onChange={setAwayTeamId}
            />
            <button className="button primary" type="submit" disabled={!canSubmit}>
              {loading ? 'Analisando...' : 'Calcular previsão'}
            </button>
          </form>
        )}
      </section>

      {!prediction && !loading && !error && (
        <div className="state-box" role="status">
          <strong>Selecione as equipes para gerar a previsão.</strong>
        </div>
      )}

      {loading && <LoadingState message="Analisando o histórico das equipes..." />}
      {error && <ErrorState message={error} />}

      {prediction && homeTeam && awayTeam && (
        <section className="section-block">
          <div className="result-header">
            <div>
              <p className="eyebrow">
                {homeTeam.name} x {awayTeam.name}
              </p>
              <h2>{prediction.label}</h2>
              <p>Resultado mais provável com confiança de {formatPercent(prediction.confidence)}.</p>
            </div>
            {source === 'mock' && <span className="badge">Dados simulados</span>}
          </div>

          <ProbabilityChart prediction={prediction} homeTeam={homeTeam} awayTeam={awayTeam} />

          <TeamComparison
            homeTeam={homeTeam}
            awayTeam={awayTeam}
            homeForm={prediction.home_team_form}
            awayForm={prediction.away_team_form}
          />

          <section className="panel">
            <h3>Fatores relevantes</h3>
            <ul className="plain-list">
              {prediction.explanations.slice(0, 3).map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>

          <div className="notice warning" role="note">
            A previsão representa uma estimativa estatística baseada em dados históricos. O resultado
            real de uma partida depende de fatores que podem não estar presentes no dataset.
          </div>
        </section>
      )}
    </div>
  )
}

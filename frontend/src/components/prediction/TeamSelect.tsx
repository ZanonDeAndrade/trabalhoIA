import type { Team } from '../../types/api'

type TeamSelectProps = {
  id: string
  label: string
  value: string
  teams: Team[]
  disabledTeamId?: string
  unavailableIds?: ReadonlySet<string>
  error?: string
  onChange: (teamId: string) => void
}

export function TeamSelect({
  id,
  label,
  value,
  teams,
  disabledTeamId,
  unavailableIds,
  error,
  onChange,
}: TeamSelectProps) {
  return (
    <label className="field" htmlFor={id}>
      <span>{label}</span>
      <select
        id={id}
        value={value}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? `${id}-error` : undefined}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="">Selecionar equipe</option>
        {teams.map((team) => {
          const unavailable = unavailableIds?.has(team.id) ?? false
          return (
            <option
              key={team.id}
              value={team.id}
              disabled={team.id === disabledTeamId || unavailable}
              title={unavailable ? (team.reason ?? undefined) : undefined}
            >
              {team.name}
              {unavailable ? ' — sem histórico recente' : ''}
            </option>
          )
        })}
      </select>
      {error && (
        <small id={`${id}-error`} className="field-error">
          {error}
        </small>
      )}
    </label>
  )
}

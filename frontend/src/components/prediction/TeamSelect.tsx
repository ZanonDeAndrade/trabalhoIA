import type { Team } from '../../types/api'

type TeamSelectProps = {
  id: string
  label: string
  value: string
  teams: Team[]
  disabledTeamId?: string
  error?: string
  onChange: (teamId: string) => void
}

export function TeamSelect({
  id,
  label,
  value,
  teams,
  disabledTeamId,
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
        <option value="">Buscar ou selecionar equipe</option>
        {teams.map((team) => (
          <option key={team.id} value={team.id} disabled={team.id === disabledTeamId}>
            {team.name}
          </option>
        ))}
      </select>
      {error && (
        <small id={`${id}-error`} className="field-error">
          {error}
        </small>
      )}
    </label>
  )
}

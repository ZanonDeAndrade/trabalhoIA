import type { TeamForm } from '../../types/api'

type RecentFormProps = {
  form: TeamForm
}

export function RecentForm({ form }: RecentFormProps) {
  return (
    <div className="recent-form" aria-label="Forma recente">
      {form.last_five.map((result, index) => (
        <span key={`${result}-${index}`} className={`form-pill result-${result.toLowerCase()}`}>
          <span className="sr-only">Resultado {index + 1}: </span>
          {result}
        </span>
      ))}
    </div>
  )
}

type MetricCardProps = {
  label: string
  value: string
  helper?: string
}

export function MetricCard({ label, value, helper }: MetricCardProps) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {helper && <small>{helper}</small>}
    </article>
  )
}

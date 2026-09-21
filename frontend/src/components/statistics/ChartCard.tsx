import type { ReactNode } from 'react'

type ChartCardProps = {
  title: string
  summary: string
  children: ReactNode
}

export function ChartCard({ title, summary, children }: ChartCardProps) {
  return (
    <section className="chart-card" aria-label={title}>
      <div className="section-heading compact">
        <h3>{title}</h3>
        <p>{summary}</p>
      </div>
      <div className="chart-area">{children}</div>
    </section>
  )
}

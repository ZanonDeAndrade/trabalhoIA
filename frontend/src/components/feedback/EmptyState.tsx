type EmptyStateProps = {
  title: string
  message: string
}

export function EmptyState({ title, message }: EmptyStateProps) {
  return (
    <div className="state-box" role="status">
      <strong>{title}</strong>
      <p>{message}</p>
    </div>
  )
}

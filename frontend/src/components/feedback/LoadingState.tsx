type LoadingStateProps = {
  message: string
}

export function LoadingState({ message }: LoadingStateProps) {
  return (
    <div className="state-box" role="status" aria-live="polite">
      <span className="loader" aria-hidden="true" />
      <strong>{message}</strong>
    </div>
  )
}

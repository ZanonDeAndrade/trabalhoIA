export function formatPercent(value: number, decimals = 0) {
  return `${new Intl.NumberFormat('pt-BR', {
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals,
  }).format(value * 100)}%`
}

export function formatNumber(value: number, decimals = 0) {
  return new Intl.NumberFormat('pt-BR', {
    maximumFractionDigits: decimals,
    minimumFractionDigits: decimals,
  }).format(value)
}

export function formatDate(iso: string) {
  const [year, month, day] = iso.slice(0, 10).split('-')
  return `${day}/${month}/${year}`
}

export function getReadableError(error: unknown) {
  if (error instanceof Error && error.message) {
    return error.message
  }

  return 'Não foi possível concluir a solicitação.'
}

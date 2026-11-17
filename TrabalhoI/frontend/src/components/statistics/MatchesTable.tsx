import type { MatchesResponse } from '../../types/api'
import { formatDate, formatNumber } from '../../utils/format'
import { EmptyState } from '../feedback/EmptyState'

type MatchesTableProps = {
  data: MatchesResponse
  onPageChange: (page: number) => void
}

export function MatchesTable({ data, onPageChange }: MatchesTableProps) {
  if (data.matches.length === 0) {
    return (
      <EmptyState
        title="Nenhuma partida encontrada"
        message="Ajuste os filtros para encontrar jogos no dataset."
      />
    )
  }

  return (
    <section className="table-section" aria-label="Tabela de partidas">
      <div className="table-wrap">
        <table>
          <caption className="sr-only">Partidas do recorte selecionado</caption>
          <thead>
            <tr>
              <th scope="col">Data</th>
              <th scope="col">Mandante</th>
              <th scope="col">Placar</th>
              <th scope="col">Visitante</th>
              <th scope="col">Amarelos</th>
              <th scope="col">Expulsões</th>
              <th scope="col">Público</th>
              <th scope="col">Estádio</th>
            </tr>
          </thead>
          <tbody>
            {data.matches.map((match) => (
              <tr key={match.id}>
                <td>{formatDate(match.date)}</td>
                <td>{match.home_team}</td>
                <td>{match.score}</td>
                <td>{match.away_team}</td>
                <td>{match.yellow_cards}</td>
                <td>{match.red_cards}</td>
                <td>{match.attendance === null ? '—' : formatNumber(match.attendance)}</td>
                <td>{match.stadium}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <nav className="pagination" aria-label="Paginação">
        <button
          className="button secondary"
          type="button"
          disabled={data.page <= 1}
          onClick={() => onPageChange(data.page - 1)}
        >
          Anterior
        </button>
        <span>
          Página {data.page} de {data.pages} · {formatNumber(data.total)} partidas
        </span>
        <button
          className="button secondary"
          type="button"
          disabled={data.page >= data.pages}
          onClick={() => onPageChange(data.page + 1)}
        >
          Próxima
        </button>
      </nav>
    </section>
  )
}

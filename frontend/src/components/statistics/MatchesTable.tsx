import type { MatchesResponse } from '../../types/api'
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
          <thead>
            <tr>
              <th>Data</th>
              <th>Mandante</th>
              <th>Placar</th>
              <th>Visitante</th>
              <th>Amarelos</th>
              <th>Vermelhos</th>
              <th>Estádio</th>
            </tr>
          </thead>
          <tbody>
            {data.matches.map((match) => (
              <tr key={match.id}>
                <td>{new Date(`${match.date}T00:00:00`).toLocaleDateString('pt-BR')}</td>
                <td>{match.home_team}</td>
                <td>{match.score}</td>
                <td>{match.away_team}</td>
                <td>{match.yellow_cards}</td>
                <td>{match.red_cards}</td>
                <td>{match.stadium}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="pagination" aria-label="Paginação">
        <button
          className="button secondary"
          type="button"
          disabled={data.page <= 1}
          onClick={() => onPageChange(data.page - 1)}
        >
          Anterior
        </button>
        <span>
          Página {data.page} de {data.pages}
        </span>
        <button
          className="button secondary"
          type="button"
          disabled={data.page >= data.pages}
          onClick={() => onPageChange(data.page + 1)}
        >
          Próxima
        </button>
      </div>
    </section>
  )
}

import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { Statistics } from './Statistics'
import { chartsResponse, matchesResponse, mockApi, overviewResponse, teamsResponse } from '../test/fixtures'

afterEach(() => vi.unstubAllGlobals())

const rotas = {
  '/teams': teamsResponse,
  '/stats/overview': overviewResponse,
  '/stats/charts': chartsResponse,
  '/matches': matchesResponse,
}

function chamadas(spy: ReturnType<typeof mockApi>, sufixo: string) {
  return spy.mock.calls.map(([url]) => new URL(String(url))).filter((u) => u.pathname.endsWith(sufixo))
}

describe('Página de estatísticas', () => {
  it('mostra indicadores e tabela com dados da API', async () => {
    mockApi(rotas)
    render(<Statistics />)
    expect(screen.getByText('Carregando estatísticas...')).toBeInTheDocument()

    const indicadores = await screen.findByLabelText('Indicadores do recorte selecionado')
    expect(within(indicadores).getByText('380')).toBeInTheDocument()
    expect(within(indicadores).getByText('946')).toBeInTheDocument()
    expect(within(indicadores).getByText(/13 partidas sem público informado/)).toBeInTheDocument()
    expect(screen.getByRole('table', { name: 'Partidas do recorte selecionado' })).toBeInTheDocument()
  })

  it('exibe traço quando o público está ausente', async () => {
    mockApi(rotas)
    render(<Statistics />)
    const linhaSantos = (await screen.findByText('Santos')).closest('tr')!
    expect(within(linhaSantos).getByText('—')).toBeInTheDocument()
  })

  it('aplica o filtro de temporada e refaz as três consultas', async () => {
    const spy = mockApi(rotas)
    render(<Statistics />)
    const user = userEvent.setup()
    await screen.findByLabelText('Indicadores do recorte selecionado')
    await user.selectOptions(screen.getByLabelText('Temporada'), '2023')

    await screen.findByLabelText('Indicadores do recorte selecionado')
    for (const rota of ['/stats/overview', '/stats/charts', '/matches']) {
      const ultima = chamadas(spy, rota).at(-1)!
      expect(ultima.searchParams.get('season')).toBe('2023')
    }
  })

  it('habilita o mando só depois de escolher uma equipe', async () => {
    const spy = mockApi(rotas)
    render(<Statistics />)
    const user = userEvent.setup()
    await screen.findByLabelText('Indicadores do recorte selecionado')
    expect(screen.getByLabelText(/Mando de campo/)).toBeDisabled()

    await user.selectOptions(screen.getByLabelText('Equipe'), 'flamengo')
    expect(screen.getByLabelText(/Mando de campo/)).toBeEnabled()
    await user.selectOptions(screen.getByLabelText(/Mando de campo/), 'home')
    await screen.findByLabelText('Indicadores do recorte selecionado')
    const ultima = chamadas(spy, '/matches').at(-1)!
    expect(ultima.searchParams.get('team')).toBe('flamengo')
    expect(ultima.searchParams.get('venue')).toBe('home')
  })

  it('pagina a tabela de partidas', async () => {
    const spy = mockApi(rotas)
    render(<Statistics />)
    const user = userEvent.setup()
    await user.click(await screen.findByRole('button', { name: 'Próxima' }))
    await screen.findByLabelText('Indicadores do recorte selecionado')
    expect(chamadas(spy, '/matches').at(-1)!.searchParams.get('page')).toBe('2')
    expect(screen.getByRole('button', { name: 'Anterior' })).toBeDisabled()
  })

  it('mostra estado vazio quando os filtros não retornam partidas', async () => {
    mockApi({ ...rotas, '/stats/overview': { ...overviewResponse, total_matches: 0 }, '/matches': { matches: [], total: 0, page: 1, pages: 1 } })
    render(<Statistics />)
    expect(await screen.findByText('Nenhuma partida encontrada')).toBeInTheDocument()
  })

  it('mostra erro com nova tentativa quando a API falha, sem dados simulados', async () => {
    mockApi({ ...rotas, '/stats/overview': () => ({ status: 500, body: { error: 'Erro interno ao processar a solicitação.' } }) })
    render(<Statistics />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Erro interno')
    expect(screen.getByRole('button', { name: 'Tentar novamente' })).toBeInTheDocument()
    expect(screen.queryByLabelText('Indicadores do recorte selecionado')).not.toBeInTheDocument()
  })

  it('não repete consultas ao carregar a página', async () => {
    const spy = mockApi(rotas)
    render(<Statistics />)
    await screen.findByLabelText('Indicadores do recorte selecionado')
    expect(chamadas(spy, '/stats/overview')).toHaveLength(1)
    expect(chamadas(spy, '/stats/charts')).toHaveLength(1)
    expect(chamadas(spy, '/matches')).toHaveLength(1)
  })
})

import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { About } from './About'
import { mockApi, modelResponse } from '../test/fixtures'

afterEach(() => vi.unstubAllGlobals())

describe('Página sobre o modelo', () => {
  it('apresenta algoritmo, versão, divisão temporal e métricas vindos da API', async () => {
    mockApi({ '/model': modelResponse })
    render(<About />)
    expect(await screen.findByText('Treinamento')).toBeInTheDocument()
    expect(screen.getAllByText('Regressão Logística').length).toBeGreaterThan(0)
    expect(screen.getByText('1.0.0')).toBeInTheDocument()
    expect(screen.getByText(/2020–2021 · 689 jogos/)).toBeInTheDocument()
    expect(screen.getByText('44,48%')).toBeInTheDocument()
    expect(screen.getByText('Somente quatro temporadas de uma competição.')).toBeInTheDocument()
    expect(screen.queryByText(/A preencher/)).not.toBeInTheDocument()
  })

  it('exibe a matriz de confusão real', async () => {
    mockApi({ '/model': modelResponse })
    render(<About />)
    const tabela = await screen.findByRole('table', { name: /Matriz de confusão/ })
    expect(tabela).toHaveTextContent('123')
    expect(tabela).toHaveTextContent('64')
  })

  it('mostra erro quando o modelo não está disponível', async () => {
    mockApi({ '/model': () => ({ status: 503, body: { error: 'Modelo não encontrado.' } }) })
    render(<About />)
    expect(await screen.findByRole('alert')).toHaveTextContent('Modelo não encontrado.')
  })
})

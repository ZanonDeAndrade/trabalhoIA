import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { Header } from './layout/Header'

describe('Cabeçalho', () => {
  it('abre e fecha o menu no celular e informa o estado por aria-expanded', async () => {
    render(<Header currentPage="home" onNavigate={() => {}} />)
    const user = userEvent.setup()
    const botao = screen.getByRole('button', { name: 'Abrir menu' })
    expect(botao).toHaveAttribute('aria-expanded', 'false')
    await user.click(botao)
    expect(screen.getByRole('button', { name: 'Fechar menu' })).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('navigation', { name: 'Menu principal' })).toHaveClass('is-open')
  })

  it('marca a página atual e navega ao clicar', async () => {
    const onNavigate = vi.fn()
    render(<Header currentPage="statistics" onNavigate={onNavigate} />)
    expect(screen.getByRole('button', { name: 'Estatísticas' })).toHaveAttribute('aria-current', 'page')
    await userEvent.setup().click(screen.getByRole('button', { name: 'Sobre o modelo' }))
    expect(onNavigate).toHaveBeenCalledWith('about')
  })
})

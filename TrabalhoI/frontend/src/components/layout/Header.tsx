import { useState } from 'react'
import type { Page } from '../../App'

type HeaderProps = { currentPage: Page; onNavigate: (page: Page) => void }

const items: Array<{ page: Page; label: string }> = [
  { page: 'home', label: 'Início' },
  { page: 'prediction', label: 'Previsão' },
  { page: 'statistics', label: 'Estatísticas' },
  { page: 'about', label: 'Sobre o modelo' },
]

export function Header({ currentPage, onNavigate }: HeaderProps) {
  const [open, setOpen] = useState(false)
  function navigate(page: Page) { onNavigate(page); setOpen(false) }

  return (
    <header className="site-header">
      <div className="header-inner">
        <button className="brand" type="button" onClick={() => navigate('home')}>PLACAR</button>
        <nav id="main-menu" className={open ? 'main-nav is-open' : 'main-nav'} aria-label="Menu principal">
          {items.map((item) => (
            <button key={item.page} type="button" aria-current={currentPage === item.page ? 'page' : undefined} onClick={() => navigate(item.page)}>
              {item.label}
            </button>
          ))}
        </nav>
        {currentPage !== 'prediction' && <button className="button primary header-cta" type="button" onClick={() => navigate('prediction')}>Fazer previsão</button>}
        <button className="menu-button" type="button" aria-label={open ? 'Fechar menu' : 'Abrir menu'} aria-expanded={open} aria-controls="main-menu" onClick={() => setOpen((value) => !value)}>
          {open ? '×' : '≡'}
        </button>
      </div>
    </header>
  )
}

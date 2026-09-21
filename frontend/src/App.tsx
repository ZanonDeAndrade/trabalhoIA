import { useState } from 'react'
import './App.css'
import { Header } from './components/layout/Header'
import { About } from './pages/About'
import { Home } from './pages/Home'
import { Prediction } from './pages/Prediction'
import { Statistics } from './pages/Statistics'

export type Page = 'home' | 'prediction' | 'statistics' | 'about'

const pageTitles: Record<Page, string> = {
  home: 'Início',
  prediction: 'Previsão',
  statistics: 'Estatísticas',
  about: 'Sobre o modelo',
}

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home')

  function navigate(page: Page) {
    setCurrentPage(page)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app-shell">
      <Header currentPage={currentPage} onNavigate={navigate} />
      <main className="page" aria-label={pageTitles[currentPage]}>
        {currentPage === 'home' && <Home onNavigate={navigate} />}
        {currentPage === 'prediction' && <Prediction />}
        {currentPage === 'statistics' && <Statistics />}
        {currentPage === 'about' && <About />}
      </main>
    </div>
  )
}

export default App

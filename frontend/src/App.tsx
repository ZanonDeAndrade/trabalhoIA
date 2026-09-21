import { lazy, Suspense, useState } from 'react'
import './App.css'
import { Header } from './components/layout/Header'
import { LoadingState } from './components/feedback/LoadingState'
import { Home } from './pages/Home'

// Páginas com gráficos ou tabelas carregam sob demanda (reduz o pacote inicial).
const About = lazy(() => import('./pages/About').then((m) => ({ default: m.About })))
const Prediction = lazy(() => import('./pages/Prediction').then((m) => ({ default: m.Prediction })))
const Statistics = lazy(() => import('./pages/Statistics').then((m) => ({ default: m.Statistics })))

export type Page = 'home' | 'prediction' | 'statistics' | 'about'

const pageTitles: Record<Page, string> = {
  home: 'Início', prediction: 'Previsão', statistics: 'Estatísticas', about: 'Sobre o modelo',
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
      <main className={currentPage === 'home' ? 'page page-home' : 'page'} aria-label={pageTitles[currentPage]}>
        <Suspense fallback={<LoadingState message="Carregando página..." />}>
          {currentPage === 'home' && <Home onNavigate={navigate} />}
          {currentPage === 'prediction' && <Prediction />}
          {currentPage === 'statistics' && <Statistics />}
          {currentPage === 'about' && <About />}
        </Suspense>
      </main>
      <footer className="site-footer">
        <strong>PLACAR</strong>
        <span>Trabalho 1 · Inteligência Artificial II · dataset partidas_20_23.csv</span>
      </footer>
    </div>
  )
}

export default App

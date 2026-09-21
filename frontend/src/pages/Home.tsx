import type { Page } from '../App'
import { MetricCard } from '../components/MetricCard'

type HomeProps = { onNavigate: (page: Page) => void }

export function Home({ onNavigate }: HomeProps) {
  return (
    <div className="home-stack">
      <section className="hero-section" aria-labelledby="hero-title">
        <div className="hero-background" aria-hidden="true" />
        <div className="hero-inner">
          <div className="hero-copy glass-panel">
            <div className="hero-meta">
              <span className="season-badge">SÉRIE A · 2020 A 2023</span>
              <span className="model-status"><i aria-hidden="true" /> MODELO v1.0.0 ONLINE</span>
            </div>
            <h1 id="hero-title">Preditor do<br />Brasileirão</h1>
            <p>Escolha dois times, defina quem joga em casa e veja as probabilidades calculadas a partir de 1.520 partidas da Série A.</p>
            <div className="actions">
              <button className="button primary large" type="button" onClick={() => onNavigate('prediction')}>Fazer previsão</button>
              <button className="button secondary large" type="button" onClick={() => onNavigate('statistics')}>Ver estatísticas</button>
            </div>
            <small>Leva menos de um minuto — e você pode voltar e trocar os times a qualquer momento.</small>
          </div>
          <div className="hero-preview glass-panel">
            <div className="preview-heading"><span className="eyebrow">PRÉVIA DE UM CONFRONTO</span><span className="badge">EXEMPLO</span></div>
            <div className="preview-match"><span>FLAMENGO × GRÊMIO</span><strong>VITÓRIA DO FLAMENGO <em>54%</em></strong></div>
            <div className="preview-bar" role="img" aria-label="Vitória do Flamengo 54%, empate 27%, vitória do Grêmio 19%"><span className="home" /><span className="draw" /><span className="away" /></div>
            <div className="preview-legend">
              <div><span><i className="home" />Mandante</span><strong>54%</strong></div>
              <div><span><i className="draw" />Empate</span><strong>27%</strong></div>
              <div><span><i className="away" />Visitante</span><strong>19%</strong></div>
            </div>
            <p>Resumo: Vitória do Flamengo 54% · Empate 27% · Vitória do Grêmio 19%. As três somam 100%.</p>
          </div>
        </div>
      </section>
      <div className="home-content">
        <section className="metrics-grid" aria-label="Indicadores gerais">
          <MetricCard label="Partidas analisadas" value="1.520" />
          <MetricCard label="Temporadas" value="4" />
          <MetricCard label="Equipes no dataset" value="26" />
        </section>
        <section className="how-section">
          <h2>Como funciona</h2>
          <div className="steps-grid">
            <article><span>01</span><h3>Escolha os times</h3><p>Selecione mandante e visitante nas listas pesquisáveis alimentadas pela API.</p></article>
            <article><span>02</span><h3>O sistema olha para trás</h3><p>O back-end calcula aproveitamento, gols e cartões usando só partidas anteriores.</p></article>
            <article><span>03</span><h3>O modelo calcula</h3><p>Saem três probabilidades — mandante, empate e visitante — e os fatores que pesaram.</p></article>
          </div>
        </section>
      </div>
    </div>
  )
}

import type { Page } from '../App'
import { MetricCard } from '../components/MetricCard'

type HomeProps = {
  onNavigate: (page: Page) => void
}

export function Home({ onNavigate }: HomeProps) {
  return (
    <div className="page-stack">
      <section className="hero-section">
        <div className="hero-copy">
          <p className="eyebrow">Brasileirão Série A 2020-2023</p>
          <h1>Preditor do Brasileirão</h1>
          <p>
            Previsões baseadas no histórico da Série A entre 2020 e 2023, com indicadores
            calculados antes das partidas para apoiar a demonstração do modelo de Machine Learning.
          </p>
          <div className="actions">
            <button className="button primary" type="button" onClick={() => onNavigate('prediction')}>
              Fazer previsão
            </button>
            <button className="button secondary" type="button" onClick={() => onNavigate('statistics')}>
              Ver estatísticas
            </button>
          </div>
        </div>
        <div className="hero-board" aria-hidden="true">
          <span>Mandante</span>
          <strong>54%</strong>
          <span>Empate</span>
          <strong>27%</strong>
          <span>Visitante</span>
          <strong>19%</strong>
        </div>
      </section>

      <section className="metrics-grid" aria-label="Indicadores gerais">
        <MetricCard label="Partidas analisadas" value="1.520" />
        <MetricCard label="Temporadas" value="4" helper="2020 a 2023" />
        <MetricCard label="Equipes no dataset" value="26" />
      </section>

      <section className="section-block">
        <div className="section-heading">
          <h2>Como funciona</h2>
          <p>O fluxo principal segue três etapas simples para a apresentação.</p>
        </div>
        <div className="steps-grid">
          <article>
            <span>1</span>
            <h3>Escolha os times</h3>
            <p>Selecione mandante e visitante usando a lista fornecida pela API.</p>
          </article>
          <article>
            <span>2</span>
            <h3>Consulte o histórico</h3>
            <p>O sistema usa apenas dados anteriores: forma recente, gols, cartões e desempenho.</p>
          </article>
          <article>
            <span>3</span>
            <h3>Veja as probabilidades</h3>
            <p>O modelo retorna vitória do mandante, empate e vitória do visitante.</p>
          </article>
        </div>
      </section>
    </div>
  )
}

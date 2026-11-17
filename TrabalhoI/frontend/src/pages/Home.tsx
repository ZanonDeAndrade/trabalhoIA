import type { Page } from '../App'
import { MetricCard } from '../components/MetricCard'
import { useAsyncData } from '../hooks/useAsyncData'
import { getHealth, getModelInfo } from '../services/api'
import { formatNumber, formatPercent } from '../utils/format'

type HomeProps = { onNavigate: (page: Page) => void }

export function Home({ onNavigate }: HomeProps) {
  const health = useAsyncData(getHealth, 'health')
  const model = useAsyncData(getModelInfo, 'model')
  const dataset = health.data?.dataset
  const test = model.data?.metrics.test
  const baseline = model.data?.metrics.baseline_majority_test

  let status = 'VERIFICANDO API'
  if (health.error) status = 'API OFFLINE'
  else if (health.data) status = health.data.model_loaded ? `MODELO v${health.data.model?.version} ONLINE` : 'MODELO INDISPONÍVEL'

  const dash = '—'

  return (
    <div className="home-stack">
      <section className="hero-section" aria-labelledby="hero-title">
        <div className="hero-background" aria-hidden="true" />
        <div className="hero-inner">
          <div className="hero-copy glass-panel">
            <div className="hero-meta">
              <span className="season-badge">
                SÉRIE A · {dataset ? `${dataset.seasons[0]} A ${dataset.seasons[dataset.seasons.length - 1]}` : '2020 A 2023'}
              </span>
              <span className="model-status" role="status"><i aria-hidden="true" /> {status}</span>
            </div>
            <h1 id="hero-title">Preditor do<br />Brasileirão</h1>
            <p>
              Escolha dois times, defina quem joga em casa e veja as probabilidades calculadas pelo
              modelo{dataset ? `, treinado com o histórico de ${formatNumber(dataset.matches)} partidas da Série A` : ''}.
            </p>
            <div className="actions">
              <button className="button primary large" type="button" onClick={() => onNavigate('prediction')}>Fazer previsão</button>
              <button className="button secondary large" type="button" onClick={() => onNavigate('statistics')}>Ver estatísticas</button>
            </div>
            <small>Leva menos de um minuto — e você pode voltar e trocar os times a qualquer momento.</small>
          </div>
          <div className="hero-preview glass-panel">
            <div className="preview-heading">
              <span className="eyebrow">DESEMPENHO NO TESTE (TEMPORADA 2023)</span>
            </div>
            <div className="preview-match">
              <span>{model.data ? `${model.data.algorithm.toUpperCase()} · ${model.data.splits.teste.n} PARTIDAS` : 'MODELO'}</span>
            </div>
            {model.error && <p role="alert">Métricas indisponíveis: {model.error}</p>}
            <div className="preview-legend">
              <div><span>Acurácia</span><strong>{test ? formatPercent(test.acuracia, 1) : dash}</strong></div>
              <div><span>Macro F1</span><strong>{test ? formatNumber(test.f1_macro, 3) : dash}</strong></div>
              <div><span>Log-Loss</span><strong>{test?.log_loss != null ? formatNumber(test.log_loss, 3) : dash}</strong></div>
            </div>
            <p>
              {baseline && test
                ? `Referência "sempre mandante": acurácia ${formatPercent(baseline.acuracia, 1)} e Macro F1 ${formatNumber(baseline.f1_macro, 3)}. O modelo reconhece mais classes, mas não é melhor em todas as métricas.`
                : 'Métricas calculadas em partidas que o modelo não viu no treinamento.'}
            </p>
          </div>
        </div>
      </section>
      <div className="home-content">
        {health.error && (
          <div className="notice warning" role="alert">{health.error}</div>
        )}
        <section className="metrics-grid" aria-label="Indicadores gerais">
          <MetricCard label="Partidas analisadas" value={dataset ? formatNumber(dataset.matches) : dash} />
          <MetricCard label="Temporadas" value={dataset ? formatNumber(dataset.seasons.length) : dash} />
          <MetricCard label="Equipes no dataset" value={dataset ? formatNumber(dataset.teams) : dash} />
          <MetricCard label="Média de gols por jogo" value={dataset ? formatNumber(dataset.goals_average, 2) : dash} />
        </section>
        <section className="how-section">
          <h2>Como funciona</h2>
          <div className="steps-grid">
            <article><span>01</span><h3>Escolha os times</h3><p>Selecione mandante e visitante na lista de equipes carregada da API.</p></article>
            <article><span>02</span><h3>O sistema olha para trás</h3><p>O back-end calcula aproveitamento, gols e cartões usando só partidas anteriores à data de referência.</p></article>
            <article><span>03</span><h3>O modelo calcula</h3><p>Saem três probabilidades — mandante, empate e visitante — e os fatores que mais pesaram.</p></article>
          </div>
        </section>
      </div>
    </div>
  )
}

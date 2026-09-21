import { ErrorState } from '../components/feedback/ErrorState'
import { LoadingState } from '../components/feedback/LoadingState'
import { useAsyncData } from '../hooks/useAsyncData'
import { getModelInfo } from '../services/api'
import type { ModelInfo, ResultClass } from '../types/api'
import { formatDate, formatNumber, formatPercent } from '../utils/format'

const CLASS_ORDER: ResultClass[] = ['home_win', 'draw', 'away_win']
const CLASS_SHORT: Record<ResultClass, string> = { home_win: 'Mandante', draw: 'Empate', away_win: 'Visitante' }

function formatTimestamp(value: string) {
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
}

function ModelDetails({ model }: { model: ModelInfo }) {
  const { test, validation, train_final: train, baseline_majority_test: base, baseline_frequency_test: freq } = model.metrics
  const matrix = test.matriz_confusao
  const seasons = (s: number[]) => (s.length > 1 ? `${s[0]}–${s[s.length - 1]}` : String(s[0]))

  return (
    <>
      <section className="about-grid">
        <article className="panel">
          <h2>Treinamento</h2>
          <dl className="stats-list">
            <div><dt>Algoritmo</dt><dd>{model.algorithm}</dd></div>
            <div><dt>Versão</dt><dd>{model.version}</dd></div>
            <div><dt>Data de treinamento</dt><dd>{formatTimestamp(model.trained_at)}</dd></div>
            <div><dt>Semente aleatória</dt><dd>{model.random_state}</dd></div>
            <div><dt>Treinado com</dt><dd>{model.trained_with}</dd></div>
          </dl>
        </article>

        <article className="panel">
          <h2>Divisão temporal</h2>
          <dl className="stats-list">
            <div><dt>Treino (seleção)</dt><dd>{seasons(model.splits.treino.temporadas)} · {model.splits.treino.n} jogos</dd></div>
            <div><dt>Validação</dt><dd>{seasons(model.splits.validacao.temporadas)} · {model.splits.validacao.n} jogos</dd></div>
            <div><dt>Teste final</dt><dd>{seasons(model.splits.teste.temporadas)} · {model.splits.teste.n} jogos</dd></div>
            <div><dt>Período dos dados</dt><dd>{formatDate(model.data_period.inicio)} a {formatDate(model.data_period.fim)}</dd></div>
          </dl>
          <p>{model.selection_criterion ? `Critério de seleção: ${model.selection_criterion}.` : null}</p>
        </article>

        <article className="panel">
          <h2>Variáveis utilizadas</h2>
          <p>
            {model.features.numeric.length + model.features.categorical.length} atributos de entrada:{' '}
            {model.features.numeric.length} numéricos e {model.features.categorical.length} categóricos
            ({model.features.categorical.join(', ')}). Os históricos usam os 5 jogos anteriores de cada equipe
            (pontos, gols marcados e sofridos, saldo, cartões, aproveitamento, aproveitamento em casa e fora),
            diferenças entre mandante e visitante e mês/hora da partida.
          </p>
        </article>

        <article className="panel">
          <h2>Métricas no teste (2023)</h2>
          <dl className="stats-list">
            <div><dt>Acurácia</dt><dd>{formatPercent(test.acuracia, 2)}</dd></div>
            <div><dt>Acurácia balanceada</dt><dd>{formatPercent(test.acuracia_balanceada, 2)}</dd></div>
            <div><dt>Precisão macro</dt><dd>{formatNumber(test.precisao_macro, 3)}</dd></div>
            <div><dt>Recall macro</dt><dd>{formatNumber(test.recall_macro, 3)}</dd></div>
            <div><dt>F1 macro</dt><dd>{formatNumber(test.f1_macro, 3)}</dd></div>
            <div><dt>Log-Loss</dt><dd>{test.log_loss === null ? '—' : formatNumber(test.log_loss, 3)}</dd></div>
            <div><dt>Brier</dt><dd>{test.brier === null ? '—' : formatNumber(test.brier, 3)}</dd></div>
          </dl>
        </article>

        <article className="panel">
          <h2>Comparação com as referências</h2>
          <table className="compact-table">
            <caption className="sr-only">Comparação do modelo com as referências no teste</caption>
            <thead>
              <tr><th scope="col">Modelo</th><th scope="col">Acurácia</th><th scope="col">F1 macro</th><th scope="col">Log-Loss</th></tr>
            </thead>
            <tbody>
              <tr><th scope="row">{model.algorithm}</th><td>{formatPercent(test.acuracia, 1)}</td><td>{formatNumber(test.f1_macro, 3)}</td><td>{formatNumber(test.log_loss ?? NaN, 3)}</td></tr>
              <tr><th scope="row">Sempre mandante</th><td>{formatPercent(base.acuracia, 1)}</td><td>{formatNumber(base.f1_macro, 3)}</td><td>—</td></tr>
              <tr><th scope="row">Frequências históricas</th><td>{formatPercent(freq.acuracia, 1)}</td><td>{formatNumber(freq.f1_macro, 3)}</td><td>{formatNumber(freq.log_loss ?? NaN, 3)}</td></tr>
            </tbody>
          </table>
          <p>
            Treino final: acurácia {formatPercent(train.acuracia, 1)}; validação (2022): {formatPercent(validation.acuracia, 1)}.
            A queda para o teste indica que o modelo não generaliza com folga.
          </p>
        </article>

        <article className="panel">
          <h2>Matriz de confusão (teste)</h2>
          <div className="confusion-matrix" role="table" aria-label="Matriz de confusão: linhas são a classe real e colunas a prevista">
            <span role="columnheader" />
            {CLASS_ORDER.map((c) => <b key={c} role="columnheader">Prev. {CLASS_SHORT[c]}</b>)}
            {CLASS_ORDER.map((real, i) => (
              <div className="confusion-row" role="row" key={real}>
                <b role="rowheader">Real {CLASS_SHORT[real]}</b>
                {matrix[i].map((value, j) => <span role="cell" key={CLASS_ORDER[j]}>{value}</span>)}
              </div>
            ))}
          </div>
          <dl className="stats-list">
            {CLASS_ORDER.map((c) => (
              <div key={c}><dt>Recall — {CLASS_SHORT[c]}</dt><dd>{formatPercent(test.por_classe[c].recall, 1)}</dd></div>
            ))}
          </dl>
        </article>
      </section>

      {model.permutation_importance && (
        <section className="section-block">
          <div className="section-heading compact">
            <h2>Variáveis com maior impacto (importância por permutação)</h2>
            <p>Aumento médio do log-loss no teste ao embaralhar cada variável. É uma associação do modelo, não uma relação causal.</p>
          </div>
          <ul className="plain-list">
            {model.permutation_importance.slice(0, 6).map((item) => (
              <li key={item.atributo}>{item.rotulo}: +{formatNumber(item.aumento_log_loss, 4)} ± {formatNumber(item.desvio_padrao, 4)}</li>
            ))}
          </ul>
        </section>
      )}

      <section className="section-block">
        <div className="section-heading compact">
          <h2>Regra contra vazamento de dados</h2>
          <p>
            Placar, gols, cartões e demais eventos da própria partida nunca entram como entrada do modelo. Os
            atributos históricos são calculados no back-end com <code>shift(1)</code>, usando apenas jogos anteriores
            à data de referência.
          </p>
        </div>
      </section>

      <section className="section-block">
        <div className="section-heading compact">
          <h2>Limitações</h2>
          <ul className="plain-list">
            {model.limitations.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>
    </>
  )
}

export function About() {
  const { data, loading, error, retry } = useAsyncData(getModelInfo, 'model')

  return (
    <div className="page-stack">
      <section className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Sobre o modelo</p>
          <h1>Classificação de resultados do Brasileirão</h1>
          <p>
            O projeto classifica cada partida da Série A em vitória do mandante, empate ou vitória do visitante,
            usando indicadores calculados apenas com os jogos anteriores das equipes. Todas as informações abaixo
            vêm dos metadados do modelo salvo pelo treinamento.
          </p>
        </div>
      </section>
      {loading && !data && <LoadingState message="Carregando informações do modelo..." />}
      {error && <ErrorState message={error} onRetry={retry} />}
      {data && <ModelDetails model={data} />}
    </div>
  )
}

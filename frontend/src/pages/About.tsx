export function About() {
  return (
    <div className="page-stack">
      <section className="section-block">
        <div className="section-heading">
          <p className="eyebrow">Sobre o modelo</p>
          <h1>Classificação de resultados do Brasileirão</h1>
          <p>
            O projeto utiliza dados de partidas do Campeonato Brasileiro Série A entre 2020 e 2023.
            Para cada jogo, foram calculados indicadores com base apenas nas partidas anteriores das
            equipes. O objetivo é classificar o resultado em vitória do mandante, empate ou vitória
            do visitante.
          </p>
        </div>
      </section>

      <section className="about-grid">
        <article className="panel">
          <h2>Dataset</h2>
          <dl className="stats-list">
            <div>
              <dt>Origem</dt>
              <dd>partidas_20_23.csv</dd>
            </div>
            <div>
              <dt>Período</dt>
              <dd>Brasileirão Série A de 2020 a 2023</dd>
            </div>
            <div>
              <dt>Volume</dt>
              <dd>1.520 partidas e 17 colunas</dd>
            </div>
          </dl>
        </article>

        <article className="panel">
          <h2>Variáveis utilizadas</h2>
          <ul className="plain-list">
            <li>Média de gols anteriores marcados e sofridos.</li>
            <li>Média de cartões amarelos e vermelhos anteriores.</li>
            <li>Pontos e sequência de resultados anteriores.</li>
            <li>Desempenho anterior como mandante e visitante.</li>
          </ul>
        </article>

        <article className="panel">
          <h2>Treinamento</h2>
          <dl className="stats-list">
            <div>
              <dt>Algoritmo</dt>
              <dd>A preencher com o modelo final.</dd>
            </div>
            <div>
              <dt>Divisão temporal</dt>
              <dd>Dados recentes reservados para teste.</dd>
            </div>
            <div>
              <dt>Data de treinamento</dt>
              <dd>A preencher após o treinamento final.</dd>
            </div>
            <div>
              <dt>Versão</dt>
              <dd>1.0.0</dd>
            </div>
          </dl>
        </article>

        <article className="panel">
          <h2>Métricas e matriz de confusão</h2>
          <p>
            Espaço reservado para acurácia, macro F1, recall por classe e matriz de confusão reais
            assim que o back-end exportar os resultados do treinamento.
          </p>
          <div className="confusion-matrix" aria-label="Matriz de confusão pendente">
            <span />
            <b>Mandante</b>
            <b>Empate</b>
            <b>Visitante</b>
            <b>Mandante</b>
            <span>-</span>
            <span>-</span>
            <span>-</span>
            <b>Empate</b>
            <span>-</span>
            <span>-</span>
            <span>-</span>
            <b>Visitante</b>
            <span>-</span>
            <span>-</span>
            <span>-</span>
          </div>
        </article>
      </section>

      <section className="section-block">
        <div className="section-heading compact">
          <h2>Regra contra vazamento de dados</h2>
          <p>
            Gols, placar e cartões da própria partida prevista não podem entrar no modelo, pois só
            são conhecidos depois do início do jogo.
          </p>
        </div>
        <div className="notice warning">
          O front-end envia apenas os identificadores de mandante e visitante para a API. O cálculo
          das variáveis históricas deve acontecer no back-end usando partidas anteriores.
        </div>
      </section>

      <section className="section-block">
        <div className="section-heading compact">
          <h2>Limitações</h2>
          <p>
            Lesões, escalações, clima, mudanças táticas e outros fatores externos podem afetar o
            resultado real e não estão necessariamente presentes no dataset.
          </p>
        </div>
      </section>
    </div>
  )
}

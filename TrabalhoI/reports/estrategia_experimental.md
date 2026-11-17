# Estratégia Experimental — Brasileirão Série A (2020–2023)

Disciplina de Inteligência Artificial II. Este documento formaliza a estratégia experimental adotada para a divisão dos dados, a prevenção de vazamento temporal (*lookahead bias*), os quantitativos das partições e as diretrizes de avaliação dos modelos de classificação preditiva do resultado das partidas.

---

## 1. Contexto e Formulação do Problema

O objetivo do projeto é prever o resultado de partidas do Campeonato Brasileiro Série A em três classes mutuamente exclusivas:
* `home_win` (0): Vitória do mandante
* `draw` (1): Empate
* `away_win` (2): Vitória do visitante

A inferência deve ser realizada estritamente **antes do início da partida** (*ex-ante*), utilizando apenas informações publicamente conhecidas antes do apito inicial (mando, dados do calendário, estádio, árbitro e métricas agregadas dos últimos 5 jogos anteriores de cada equipe).

---

## 2. Forma de Divisão dos Dados

Adota-se uma estratégia de **particionamento temporal estrito em três conjuntos: Treino / Validação / Teste (Hold-out Temporal)**, estruturada por temporadas completas de competição:

```
[ 2020 ] [ 2021 ] [ 2022 ] [ 2023 ]
|-----------------|        |        |
     TREINO           VAL     TESTE
     (50,0%)        (25,0%)  (25,0%)
```

### 2.1. Definição das Partições

1. **Conjunto de Treinamento (Treino Inicial):**
   * **Temporadas:** 2020 e 2021.
   * **Finalidade:** Ajuste de pesos e parâmetros dos algoritmos de aprendizado supervisionado.
2. **Conjunto de Validação (Sintonia e Seleção):**
   * **Temporada:** 2022.
   * **Finalidade:** Comparação de diferentes famílias de algoritmos (modelos lineares vs. árvores de decisão e ensambles), seleção de hiperparâmetros (regularização, profundidade máxima, taxa de aprendizado), definição de limiares de decisão e calibração de probabilidades.
3. **Conjunto de Teste (Avaliação Final / *Out-of-Sample*):**
   * **Temporada:** 2023.
   * **Finalidade:** Avaliação cega e imparcial do modelo campeão previamente selecionado, medindo a capacidade de generalização sobre um ano inteiro de partidas inéditas.

---

## 3. Quantitativos e Distribuição das Classes nas Partições

A base de dados é composta por **1.520 partidas** (380 por temporada). As partidas elegíveis para treinamento e avaliação preditiva confiável são aquelas com ao menos 5 jogos anteriores registrados para ambos os clubes (`utilizavel_ml == 1`), totalizando **1.414 partidas**.

A tabela a seguir apresenta os números exatos extraídos de `data/processed/partidas_processadas.csv`:

| Partição | Temporadas | Total de Partidas | Partidas Utilizáveis (`utilizavel_ml = 1`) | Sem Histórico (`utilizavel_ml = 0`) | Vitória Mandante (`home_win`) | Empate (`draw`) | Vitória Visitante (`away_win`) |
|---|---|---|---|---|---|---|---|
| **Treino** | 2020 e 2021 | 760 | **689** (48,7%) | 71 | 314 (45,57%) | 199 (28,88%) | 176 (25,54%) |
| **Validação** | 2022 | 380 | **363** (25,7%) | 17 | 161 (44,35%) | 102 (28,10%) | 100 (27,55%) |
| **Teste** | 2023 | 380 | **362** (25,6%) | 18 | 170 (46,96%) | 94 (25,97%) | 98 (27,07%) |
| **Total** | 2020–2023 | 1.520 | **1.414** (100,0%) | 106 | 645 (45,61%) | 395 (27,93%) | 374 (26,45%) |

### 3.1. Estabilidade Temporal das Classes

Observa-se que a distribuição das classes se mantém notavelmente estável entre as partições de Treino, Validação e Teste:
* `home_win`: varia entre 44,35% (Validação) e 46,96% (Teste), mantendo a vantagem histórica do mandante próxima de 45,6%.
* `draw`: varia entre 25,97% (Teste) e 28,88% (Treino).
* `away_win`: varia entre 25,54% (Treino) e 27,55% (Validação).

Como comprovado na análise exploratória (teste qui-quadrado $\chi^2 = 2{,}24$, $p = 0{,}897$), **não há desvio estatisticamente significativo nas proporções das classes entre as temporadas**. Consequentemente, o particionamento temporal não introduz desbalanceamento artificial nem requer técnicas de subamostragem ou sobreamostragem forçada.

---

## 4. Justificativas da Estratégia Adotada

### 4.1. Por que a divisão Temporal é mandatória (e o sorteio aleatório é proibido)?

* **Eliminação de Vazamento Temporal (*Temporal Leakage / Lookahead Bias*):**
  Em problemas preditivos sobre eventos organizados em séries temporais (como esportes ou finanças), a divisão aleatória convencional (`train_test_split` com *shuffle* ou validação cruzada $k$-fold clássica) é metodologicamente incorreta. Ela permite que partidas de rodadas futuras (ex.: novembro de 2023) sejam usadas no treino para "prever" partidas passadas (ex.: maio de 2020). Além de anacrônico, o modelo aprenderia sobre o contexto futuro das equipes e da tabela antes que ele ocorresse, inflando artificialmente as métricas de acurácia.
* **Respeito à Causalidade:**
  O cálculo das variáveis preditivas (médias móveis de saldo de gols, pontos e aproveitamento dos últimos 5 jogos) foi construído respeitando estritamente a linha do tempo (`shift(1)`). Misturar passado e futuro na partição destruiria a premissa de causalidade estabelecida na preparação dos dados.
* **Validade Ecológica da Avaliação:**
  A avaliação experimental deve simular a utilização real do sistema: o modelo é treinado com o histórico acumulado e colocado em operação para prever a próxima temporada completa (2023) à medida que os jogos acontecem.

### 4.2. Por que Treino / Validação / Teste em vez de apenas Treino / Teste?

* **Isolamento do Conjunto de Teste (*Blind Test Set*):**
  Se houvesse apenas Treino e Teste, todas as decisões de modelagem — como escolha entre Regressão Logística, Random Forest e Gradient Boosting, seleção de atributos e afinação de hiperparâmetros — seriam guiadas pelo desempenho no conjunto de teste. Isso acarretaria **vazamento de informação por otimização (*information leak through tuning*)**, onde o modelo se sobreajusta indiretamente ao teste, gerando estimativas excessivamente otimistas.
* **Papel da Validação (Temporada 2022):**
  A temporada de 2022 funciona como um ambiente de teste intermediário realista:
  1. Permite comparar múltiplos algoritmos em uma temporada inteira pós-pandemia.
  2. Possibilita selecionar os melhores hiperparâmetros de regularização e complexidade.
  3. Permite inspecionar a calibração de probabilidades (se a confiança de 60% em vitória do mandante realmente corresponde a ~60% de acertos).
* O conjunto de **Teste (Temporada 2023)** permanece completamente lacrado até que todos os modelos, transformações e hiperparâmetros tenham sido congelados.

### 4.3. Por que Divisão por Temporadas Inteiras e não por Fração de Meses?

* O Campeonato Brasileiro Série A tem ciclo anual de 38 corridas/rodadas por clube. Dividir exatamente no fechamento da temporada preserva a unidade estrutural da competição, incluindo turnos, retornos e as janelas de transferências entre os anos.
* A temporada de 2020 foi atípica (encerrada em fevereiro de 2021 em razão da pandemia). Ao agrupar 2020 e 2021 no conjunto de treino, absorve-se a totalidade das transições desse período de portões fechados, permitindo que as partições de Validação (2022) e Teste (2023) representem o futebol em regime estável com público pleno nos estádios.

---

## 5. Esquema Complementar de Validação Interna (*Walk-Forward*)

Para a etapa de busca de hiperparâmetros e validação interna dos modelos durante a fase de desenvolvimento, recomenda-se a técnica de **Janela Expansiva (*Walk-Forward / Expanding Window TimeSeriesSplit*)**:

* **Fold 1:** Treina em **2020** $\rightarrow$ Valida em **2021**.
* **Fold 2:** Treina em **2020 + 2021** $\rightarrow$ Valida em **2022**.
* **Retreinamento Final (Opcional após congelamento de hiperparâmetros):**
  Uma vez selecionada a melhor arquitetura e seus hiperparâmetros na Validação (2022), é prática consagrada em séries temporais retreinar o modelo final com todo o histórico disponível até a data (**2020 + 2021 + 2022 = 1.052 partidas utilizáveis**) antes de emitir as previsões oficiais da temporada de **Teste (2023)**.

---

## 6. Tratamento das Partidas com Histórico Insuficiente (`utilizavel_ml == 0`)

* **No Conjunto de Treino:** As 71 partidas com menos de 5 jogos prévios são descartadas do treinamento. Isso evita imputações artificiais com médias arbitrárias que poderiam introduzir viés ou ruído nos gradientes dos modelos.
* **No Conjunto de Validação e Teste:**
  * **Cenário Principal (Padrão):** Avaliação restrita às partidas utilizáveis com histórico completo (363 em 2022 e 362 em 2023), medindo o poder preditivo das variáveis históricas sem ruído de *cold start*.
  * **Cenário de Cobertura Total (380 jogos):** Se o experimento exigir previsão para 100% dos jogos da temporada, as 18 partidas iniciais sem histórico em 2023 terão as variáveis faltantes imputadas utilizando **exclusivamente as médias aprendidas no conjunto de treinamento**, jamais com estatísticas calculadas sobre a própria temporada de 2023.

---

## 7. Protocolo de Avaliação e Linha de Base (*Baseline*)

Para avaliar de forma justa o desempenho dos modelos em cada partição, adota-se o seguinte protocolo:

1. **Linha de Base Ingênua (Majority Class Classifier):**
   * Prever invariavelmente `home_win` para todas as partidas.
   * Acurácia esperada no teste: **46,96%** (170/362). Todo modelo de aprendizado de máquina precisa superar esse limiar para demonstrar ganho informativo real.
2. **Métricas Primárias:**
   * **Acurácia Global:** Proporção de acertos totais sobre as três classes.
   * **Macro F1-Score:** Média harmônica balanceada do F1 entre as três classes, penalizando modelos que ignoram empates (`draw`) ou vitórias de visitantes (`away_win`).
   * **Matriz de Confusão Normalizada:** Para análise qualitativa dos padrões de erro (em especial a distinção entre vitórias do mandante e empates).
3. **Métricas Probabilísticas:**
   * **Log-Loss (Entropia Cruzada Multiclasse)** e **Brier Score Multiclasse**, para mensurar a qualidade das probabilidades calibradas e a incerteza do modelo.
4. **Reprodutibilidade:**
   * Fixação da semente aleatória: `RANDOM_STATE = 42` para qualquer algoritmo estocástico (como inicialização de árvores e pesos lineares).

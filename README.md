# Previsão de resultados do Brasileirão Série A

Trabalho 1 de Inteligência Artificial II - AMF - 2026/02.

**Integrantes:** Marcelo da Costa Telles, Arthur Zanon e Milton Roberto.

Classificação supervisionada de partidas em vitória do mandante, empate ou vitória do visitante, com atributos construídos somente com informações anteriores ao jogo.

## Entrega

- [Relatório técnico em PDF](reports/relatorio_tecnico.pdf)
- [Versão textual do relatório](reports/relatorio_tecnico.md)
- [Captura da execução](reports/evidencias/01_execucao_modelos.png)
- [Captura das previsões](reports/evidencias/02_previsoes_partidas.png)
- [Notebook de demonstração executado](notebooks/03_demonstracao_funcionamento.ipynb)
- [Métricas reproduzidas e versões do ambiente](reports/evidencias/metricas_execucao.json)

## Dados e protocolo

O [CSV original](partidas_20_23.csv) contém 1.520 partidas, 17 colunas e quatro temporadas (2020-2023). Os links dos registros apontam para Opta Player Stats / Stats Perform; o procedimento original de coleta e a licença específica da base não estão documentados. O CSV processado contém 66 colunas; 1.414 partidas têm histórico geral suficiente para modelagem.

Treino: 2020-2021 (689 partidas). Validação: 2022 (363). Teste: 2023 (362). O modelo é escolhido pelo Macro F1 da validação e reajustado em 2020-2022 (1.052 partidas). São 34 atributos antes da codificação: 31 numéricos e 3 categóricos. Imputação e codificação são ajustadas somente no treinamento. O teste simula previsões antes de cada partida e pode usar resultados de jogos anteriores já encerrados em 2023.

## Instalação e execução

Ambiente verificado: Windows, Python 3.14.3. Execute na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/data_analysis.py
.\.venv\Scripts\python.exe src/modeling.py
.\.venv\Scripts\python.exe src/documentation_evidence.py
.\.venv\Scripts\python.exe -m jupyter lab
```

No JupyterLab, abra `notebooks/03_demonstracao_funcionamento.ipynb` e use **Run > Run All Cells**. A execução treina os modelos, calcula as métricas e apresenta oito previsões reais do teste. Os notebooks `01_eda_preparacao.ipynb` e `02_modelagem_classificacao.ipynb` documentam as etapas anteriores.

## Resultados e limites

A Regressão Logística foi selecionada por Macro F1 de 0,370 na validação. No teste: acurácia de **44,48%**, Macro F1 de **0,360**, Log-Loss de **1,089** e Brier de **0,652**. A referência que sempre prevê o mandante alcança acurácia de 46,96% e Macro F1 de 0,213. A referência de frequências históricas apresenta melhores Log-Loss (1,061) e Brier (0,640). Portanto, o modelo melhora a cobertura entre classes, mas não demonstra superioridade geral.

Não houve busca sistemática de hiperparâmetros, calibração ou avaliação em múltiplas janelas temporais. Os cartões incluem registros de comissão técnica. Os coeficientes de maior magnitude são categorias de equipes e dia da semana; o gráfico de coeficientes não demonstra causalidade. Consulte o relatório final para a análise crítica consolidada.

## Organização

```text
data/processed/        Dados processados
notebooks/             EDA, modelagem e demonstração
src/                   Preparação, partições, modelos e evidências
scripts/               Geradores de documentação
reports/               Relatório final e relatórios de apoio
reports/figures/       Figuras da EDA e dos modelos
reports/evidencias/    Screenshots e resultados reproduzíveis
```

## Regerar a documentação

```powershell
.\.venv\Scripts\python.exe -m pip install -r reports/requirements_documentacao.txt
.\.venv\Scripts\python.exe scripts/gerar_relatorio_tecnico.py
```

O gerador utiliza as evidências JSON, as figuras já produzidas e fontes Arial do Windows. As capturas são registros reais da sessão de demonstração; não são reconstruídas pelo gerador. O script `scripts/preparar_notebook_demonstracao.py` recria a estrutura do notebook e apaga suas saídas anteriores; use-o apenas para reconstrução e execute o notebook novamente depois.

Antes do envio, a equipe deve conferir a aprovação prévia da base, o registro das contribuições individuais e o envio do link do repositório no Classroom conforme o enunciado.

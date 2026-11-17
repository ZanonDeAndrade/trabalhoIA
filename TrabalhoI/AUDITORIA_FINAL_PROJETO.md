# Auditoria técnica do projeto — Previsão do Brasileirão Série A (IA II)

> Documento criado **antes** das correções. A seção "Estado final" no fim do arquivo é atualizada
> depois da implementação, apenas com resultados obtidos por execução real.

## 1. Inspeção inicial (estado do repositório em 21/09/2026)

- `git status` inicial: limpo, exceto `frontend/src/services/mockData.ts` (corrigido na sessão anterior: template strings corrompidas).
- Branch `main`; últimos commits: PR #5 (API do modelo + integração do front-end).
- Não existem `CLAUDE.md`, `AGENTS.md`, `Makefile`, `pyproject.toml`, `.env.example` na raiz, nem testes automatizados (Python ou front-end).
- Componentes: `src/` (EDA, partições, modelagem, API stdlib `http.server`), `frontend/` (React 19 + Vite + TypeScript + Recharts), `notebooks/` (3), `scripts/` (relatório PDF via ReportLab), `reports/` (Markdown, PDF, figuras, evidências), `data/processed/` (CSV processado).
- Duplicidade/abandono: `src/__pycache__/data_analysis.cpython-314.pyc` está versionado apesar do `.gitignore`; `frontend/src/assets/{hero.png,react.svg,vite.svg}` e `frontend/public/icons.svg` sem uso aparente (não removidos sem confirmação).
- Como executar (README): comandos apenas para Windows (`.\.venv\Scripts\python.exe`); ambiente local é Linux, Python 3.14.4.

## 2. Verificações executadas na auditoria inicial

| Verificação | Resultado |
|---|---|
| `python src/data_analysis.py` | Executa em ~6 s; 1.520 partidas, 66 colunas, 14/14 validações automáticas; `partidas_20_23.csv` inalterado (SHA-256 idêntico) |
| `python src/modeling.py` | Executa; Regressão Logística selecionada (Macro F1 val. 0,370); teste 2023: acurácia 44,48%, Macro F1 0,360 |
| `npm run lint` (front-end) | 0 erros, 3 avisos (`set-state-in-effect`, `exhaustive-deps`) |
| `npm run build` (front-end) | OK (após correção do `mockData.ts`); bundle 648 kB (aviso de tamanho) |
| Testes automatizados | **Inexistentes** |

## 3. Tabela de requisitos (estado inicial)

| Requisito | Status | Evidência encontrada | Problema | Correção necessária |
|---|---|---|---|---|
| 1. Dataset escolhido e validado | PARCIAL | `partidas_20_23.csv` (1.520 × 17), auditoria de qualidade em `reports/analise_exploratoria.md` | Aprovação do dataset pelo professor e licença não documentadas | Registrar em checklist manual |
| 2. Problema e objetivo | CONCLUÍDO | README, relatório | — | — |
| 3. Análise exploratória | CONCLUÍDO | `src/data_analysis.py`, 13 figuras, notebook 01 | Notebook 01 não reexecutado nesta auditoria | Reexecutar de ponta a ponta |
| 4. Preparação/transformação | CONCLUÍDO | `processar_partidas`, JSON sem `eval`, temporada via `link`, datas pt-BR, público | Sem testes automatizados | Criar testes |
| 5. Estratégia experimental | CONCLUÍDO | Split 2020-21 / 2022 / 2023, `data_split.py` | Seleção usa só Macro F1 (documentado); sem walk-forward na comparação | Manter e documentar |
| 6. Treinamento | PARCIAL | 4 algoritmos treinados em `modeling.py` | **Modelo não é salvo** (`models/` inexistente); API retreina no boot | Persistir `model.joblib` + `metadata.json` |
| 7. Avaliação | PARCIAL | Acurácia, acurácia balanceada, F1 macro/por classe, log-loss, Brier, matriz de confusão | Faltam precisão macro, recall macro, relatório de classificação, distribuição das previsões, calibração; números fixos no texto gerado (`resultados_modelagem.md` tem "15 dos 94", "1.052", "689") | Ampliar métricas e gerar texto a partir dos resultados |
| 8. Interpretação crítica | PARCIAL | Média |coef| da Regressão Logística | Sem permutation importance; sem exemplos de acertos/erros na análise | Adicionar permutation importance e análise de erros |
| 9. Demonstração | PARCIAL | Notebook 03 + 2 capturas do JupyterLab (Windows) | **Sem capturas do front-end**; notebook 03 com números fixos no `print` | Gerar screenshots reais do front-end |
| 10. Relatório PDF em `/reports` | COM ERRO | `reports/relatorio_tecnico.pdf` | Gerador exige fontes `C:/Windows/Fonts` (não roda em Linux); números escritos à mão no código; faltam seções "Problema e objetivo", "Modelagem", "Extensão opcional" separadas | Reescrever gerador multiplataforma, dirigido por JSON |
| 11. Repositório reproduzível | PARCIAL | `requirements.txt` | Sem Makefile; README só para Windows; sem testes | Makefile + README Linux/Windows |
| 12. README | PARCIAL | `README.md` | Não cobre API, front-end, testes, licença; comandos Windows | Reescrever |
| 13. Dependências | PARCIAL | `requirements.txt`, `package.json` | `joblib`/`pytest`/`reportlab` fora do `requirements.txt` principal; `.env.example` só no front-end | Atualizar |
| 14. Dados necessários | CONCLUÍDO | CSV original + processado versionados | — | — |
| 15. Screenshots/gravação | AUSENTE | Apenas capturas do JupyterLab | Nenhuma captura da aplicação | Gerar em `reports/screenshots/` |

## 4. Problemas encontrados (por área)

### 4.1 Vazamento de dados e modelo
- A construção dos históricos (`adicionar_historico`) usa `shift(1)` e `rolling`; as colunas proibidas são validadas em `validar_sem_vazamento`. **Nenhuma das 15 colunas listadas no enunciado entra como entrada** (verificado em `data_split.py`). Falta um teste que prove que a partida atual não participa das próprias variáveis.
- `data_analysis.py` já contém `testar_vazamento_temporal` (14 validações); será complementada por testes `pytest` independentes.

### 4.2 API (`src/api.py`)
| Achado | Gravidade |
|---|---|
| Retreina o modelo a cada inicialização (nada persistido) | Alta |
| Para confrontos sem jogo em 2023, monta "linha simulada" com atributos da última linha de cada equipe **defasados em uma partida** e com **valores falsos** (`0.0`, `dia_semana="domingo"`, `mes=10`, `hora=16`) | Alta |
| `obter_forma_equipe` devolve `["E","E","E","E","E"]`, `1.0` pts, `2.0` amarelos etc. quando não há histórico (dado inventado) | Alta |
| `/api/health` retorna números escritos à mão (`1520`, `3637`, `1052`, `362`) e o nome do modelo fixo | Média |
| Texto "mandantes vencem 45,5%" fixo nas explicações | Média |
| Erros 500 expõem `str(e)`; `int(params["page"])` sem validação (500 em `?page=abc`) | Média |
| CORS `*`, bind `0.0.0.0`, servidor single-thread | Média |
| Endpoints ausentes: `/api/stats/charts`, `/api/teams/{id}/summary`, `/api/teams/compare`, metadados do modelo | Média |
| Times com histórico insuficiente/inativo não são tratados | Alta |
| Cálculos agregados iteram linha a linha (`iterrows`) em cada requisição sem cache | Baixa |

### 4.3 Front-end
- `frontend/src/services/mockData.ts` (1.263 linhas): estatísticas, partidas e previsões **fabricadas**; `mockTeams` e `mockTeamsStats` vazios. `api.ts` usa o mock como *fallback* silencioso quando a API falha (esconde falhas com dados falsos).
- `Home.tsx`: "PRÉVIA DE UM CONFRONTO — EXEMPLO" com probabilidades fixas (Flamengo 54% / 27% / Grêmio 19%); indicadores "1.520", "4", "26" fixos; "MODELO v1.0.0 ONLINE" fixo.
- `About.tsx`: "A preencher com o modelo final", matriz de confusão vazia, sem métricas reais.
- `Statistics.tsx`: `useEffect` com `load` fora das dependências; gráficos não usam um endpoint dedicado; erros técnicos exibidos.
- `index.html`: `lang="en"`, título `projeto_ia`.
- Sem testes de front-end.

### 4.4 Relatório e documentação
- Gerador de PDF dependente de Windows; valores (161/362, 123/170, 0,724, 91,00%, datas) digitados no código; sem seção de demonstração do front-end; sem figuras de calibração/permutation importance.
- `reports/relatorio_tecnico.md` é derivado do mesmo script.

## 5. Plano de correção

1. Persistir o modelo (`models/model.joblib`, `models/metadata.json`) a partir de um único pipeline de treino que também grava as métricas.
2. Extrair um serviço de previsão que reaproveita `adicionar_historico` sobre os jogos anteriores à data de referência (mesma transformação do treino).
3. Reescrever a API mantendo o padrão da biblioteca padrão, com validação, erros seguros, cache, CORS configurável e os endpoints exigidos.
4. Remover mocks e *fallbacks* do front-end; consumir apenas a API; páginas Início/Previsão/Estatísticas/Sobre com dados reais.
5. Testes: `pytest` (dados, vazamento, modelo, API) e `vitest` (front-end).
6. Relatório PDF multiplataforma, dirigido por dados, com screenshots reais; inspeção visual página a página.
7. README, Makefile, `.env.example`, `.gitignore`, `CHECKLIST_ACOES_MANUAIS.md`, `STATUS_ENTREGA.md`.

---

## Estado final (após as correções; tudo abaixo foi obtido por execução real)

### Requisitos

| Requisito | Status | Evidência | Pendência |
|---|---|---|---|
| 1. Dataset escolhido e validado | DEPENDE DE AÇÃO MANUAL | CSV 1.520 × 17 preservado (SHA-256 verificado); 14 validações automáticas; testes em `tests/test_dados.py` | Aprovação do dataset pelo professor; licença/condições de uso não documentadas na origem |
| 2. Problema e objetivo | CONCLUÍDO | Seção 2 do relatório; README | — |
| 3. Análise exploratória | CONCLUÍDO | `src/data_analysis.py`, 13 figuras (150 dpi, pt-BR), `analise_exploratoria.md`, notebook 01 executado (105 células, 0 erros) | — |
| 4. Preparação e transformação | CONCLUÍDO | Datas pt-BR, temporada do link, público, JSON sem `eval`, cartões/gols contra/pênaltis; 46 testes de dados e vazamento | — |
| 5. Estratégia experimental | CONCLUÍDO | Treino 2020–21 (689) / validação 2022 (363) / teste 2023 (362); seleção só na validação; pipeline ajustado no treino (teste dedicado) | — |
| 6. Treinamento | CONCLUÍDO | 4 algoritmos; modelo salvo em `models/model.joblib` + `metadata.json` | — |
| 7. Avaliação | CONCLUÍDO | Acurácia, balanceada, precisão/recall/F1 macro, por classe, matriz de confusão, Log-Loss, Brier, AUC OvR, calibração, distribuição de previsões, treino×val×teste | — |
| 8. Interpretação crítica | CONCLUÍDO | Permutation importance (30 repetições), coeficientes, análise de erros; ressalvas de causalidade | — |
| 9. Demonstração | CONCLUÍDO | Notebook 03 executado; 8 capturas reais da aplicação | Gravação em vídeo (opcional, manual) |
| 10. Relatório PDF em `/reports` | CONCLUÍDO | `reports/relatorio_tecnico.pdf` (14 páginas), gerado por script multiplataforma e inspecionado página a página | Revisão do texto pela equipe |
| 11. Repositório reproduzível | CONCLUÍDO | Instalação limpa em cópia do repositório (venv novo): dados → treino → 117 testes → ruff → PDF; `npm ci` limpo: 28 testes e build | — |
| 12. README | CONCLUÍDO | Cobre todos os itens pedidos; comandos testados | Confirmar link/licença do dataset |
| 13. Dependências | CONCLUÍDO | `requirements.txt` (versões fixas), `requirements-dev.txt`, `reports/requirements_documentacao.txt`, `package-lock.json`, `.env.example`, `.gitignore` | — |
| 14. Dados necessários | CONCLUÍDO | CSV original e processado versionados; modelo em `models/` | — |
| 15. Screenshots/gravação | CONCLUÍDO (screenshots) | `reports/screenshots/01…08` (Chromium via Playwright, sem erros de console, sem rolagem horizontal em 390 px) | Vídeo opcional |

### Problemas encontrados e correções

| Problema inicial | Correção | Evidência |
|---|---|---|
| Modelo não persistido; API retreinava a cada boot | `models/model.joblib` e `metadata.json` (versão, data, algoritmo, hiperparâmetros, atributos, classes, métricas, período, semente, dependências) | `tests/test_modelo.py` |
| API montava confrontos com valores inventados (`0.0`, domingo, mês 10, hora 16, forma `E E E E E`), atributos defasados e números fixos em `/health` | Novo `src/predictor.py`: atributos do confronto calculados com o **mesmo código do treino** sobre jogos anteriores à data; sem histórico → HTTP 422 | Comparação nas **1.414** partidas elegíveis: diferença máxima 1,1e-16; `tests/test_previsor.py` |
| Erros 500 com `str(e)`; `?page=abc` gerava 500; CORS `*`; bind `0.0.0.0` | Validação de parâmetros (400/404/405/413/422), erro interno genérico, CORS por lista, bind `127.0.0.1`, servidor com threads | `tests/test_api.py` (inclui servidor HTTP real) |
| Endpoints ausentes | `/api/stats/charts`, `/api/teams/{id}/summary`, `/api/teams/compare`, `/api/model`, `/api/docs` | idem |
| Front-end com `mockData.ts` (1.263 linhas) e *fallback* silencioso | Mock removido; `api.ts` só consome a API e mostra erros reais | grep sem mocks em produção |
| Início com "prévia" Flamengo×Grêmio 54/27/19 fixa e indicadores fixos; Sobre com "A preencher" | Tudo lido de `/api/health` e `/api/model` (métricas, matriz de confusão, data/versão do modelo) | `Home.test.tsx`, `About.test.tsx`, capturas |
| Filtro de equipe em texto livre; gráficos ignoravam filtros; sem público; avisos de lint | Seleção por lista, séries filtradas, público ausente como “—”, hook `useAsyncData` com cancelamento (0 avisos) | `Statistics.test.tsx` |
| Resultado exibido podia divergir das equipes selecionadas depois de mudá-las | Resultado guarda a requisição que o gerou | `Prediction.test.tsx` |
| `index.html` com `lang="en"`, título `projeto_ia`; texto de apoio com contraste 4,4:1 | `pt-BR`, título real; `--text-muted` clareado | — |
| Bundle único de 648 kB | Páginas com carregamento sob demanda (maior chunk 397 kB) | `npm run build` |
| Métricas incompletas e números fixos em textos (`15 dos 94`, `19.117`, `-18.029`, `1.052`) | `src/evaluation.py`; relatórios, notebooks e PDF gerados a partir do JSON | notebooks 02/03 recalculados |
| Gerador do PDF dependia de fontes do Windows e de números digitados | Reescrito (DejaVu do Matplotlib; tudo lido de JSON/CSV); seções exigidas, capturas reais | PDF de 14 páginas revisado |
| Hash do CSV divergia entre sistemas (`edc5071c…` na evidência antiga = versão com CRLF do Windows; `f10ed252…` = arquivo LF do repositório) | Hash calculado ignorando CRLF/LF | `test_csv_original_esta_preservado_desde_o_treinamento` |
| README apenas para Windows, sem API/front/testes | README completo + `Makefile` | comandos executados |
| Sem testes automatizados | 117 testes Python + 28 do front-end | ver abaixo |

**Arquivos removidos (funções entendidas):** `frontend/src/services/mockData.ts` (dados falsos); `frontend/src/hooks/useApiHealth.ts` e `useTeams.ts` (substituídos por `useAsyncData`); `scripts/corrigir_textos_documentacao.py` (remendo único que reescrevia textos com números fixos); `reports/figures/16_importancia_features.png` (substituída por `16_importancia_permutacao.png`/`17_…`); `src/__pycache__/*.pyc` (saiu do índice do Git; continua ignorado). Nenhum arquivo do CSV original ou de outros integrantes foi alterado além do descrito; nada foi commitado nem enviado.

### Verificações finais (21/09/2026)

| Verificação | Resultado |
|---|---|
| `python src/data_analysis.py` | 1.520 partidas, 66 colunas, 14/14 validações |
| `python src/modeling.py` | Regressão Logística selecionada; modelo e metadados salvos |
| `python -m pytest tests` | **117 passed** |
| `ruff check .` | All checks passed |
| `npm test` (Vitest) | **28 passed** (6 arquivos) |
| `npm run typecheck` / `npm run lint` | sem erros / 0 avisos |
| `npm run build` | OK, sem aviso de tamanho |
| `npm audit` | 0 vulnerabilidades |
| API real (porta 8001) | todos os endpoints respondem; 400/404/405/422/503 verificados |
| Front-end real | 8 capturas sem erros de console; celular sem rolagem horizontal |
| Notebooks 01, 02, 03 | executados de ponta a ponta, 0 erros, 0 células sem executar |
| Instalação limpa (venv novo + `npm ci`) | dados → treino → testes → lint → PDF e front-end: OK |

### Métricas reais (teste 2023, 362 partidas)

Regressão Logística: acurácia 44,48%, acurácia balanceada 37,26%, precisão macro 0,388, recall macro 0,373, Macro F1 0,360, Log-Loss 1,089, Brier 0,652, AUC OvR 0,559. Referência “sempre mandante”: 46,96% e Macro F1 0,213. Referência de frequências: Log-Loss 1,061, Brier 0,640. O modelo **não supera as referências em acurácia nem em métricas probabilísticas**; isso está declarado no relatório, no README e na interface.

### Pendências e observações

- **Manuais:** ver `CHECKLIST_ACOES_MANUAIS.md`.
- A API antiga que estava em execução na porta 8000 (processo iniciado antes das correções) precisa ser reiniciada para usar o código novo; os testes usaram a porta 8001.
- Capturas do JupyterLab em `reports/evidencias/*.png` são de uma execução anterior (Windows); as métricas atuais estão no JSON e no notebook 03.
- Não implementado (fora do escopo/sem base): busca de hiperparâmetros, calibração, intervalos de confiança, múltiplas janelas temporais, CI.

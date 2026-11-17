# Status da entrega

| Item | Status | Evidência | Ação restante |
|---|---|---|---|
| Dataset escolhido e validado | Parcial | CSV íntegro (SHA-256), 14 validações, testes de dados | Aprovação do professor e licença (manual) |
| Problema e objetivo | Concluído | Relatório seção 2; README | — |
| Análise exploratória | Concluído | `src/data_analysis.py`, 13 figuras, notebook 01 executado | — |
| Preparação dos dados | Concluído | JSON seguro, temporada do link, datas pt-BR, público; `tests/test_dados.py` | — |
| Ausência de vazamento | Concluído | `tests/test_vazamento.py`; serviço de previsão idêntico ao treino em 1.414/1.414 partidas (dif. máx. 1,1e-16) | — |
| Estratégia experimental | Concluído | Split temporal 2020–21 / 2022 / 2023; seleção só na validação | — |
| Treinamento e modelo salvo | Concluído | `models/model.joblib`, `models/metadata.json` | — |
| Avaliação | Concluído | Métricas completas, matriz de confusão, calibração; treino×val×teste | — |
| Interpretação crítica | Concluído | Permutation importance, coeficientes, erros; ressalvas | — |
| API | Concluído | 10 rotas; validação, erros seguros, CORS; 117 testes Python | Reiniciar processo antigo da porta 8000 |
| Front-end sem mocks | Concluído | `mockData.ts` removido; 28 testes; lint/tipos/build OK; `npm audit` 0 | — |
| Notebooks | Concluído | 01, 02, 03 executados sem erros | — |
| Relatório PDF em `/reports` | Concluído | `reports/relatorio_tecnico.pdf`, 14 páginas, inspecionado | Revisão da equipe |
| Screenshots da solução | Concluído | `reports/screenshots/` (8 capturas reais) | Vídeo opcional |
| Reprodutibilidade | Concluído | Instalação limpa (venv + `npm ci`) executada até o PDF | — |
| README, dependências, Makefile | Concluído | `README.md`, `requirements*.txt`, `Makefile`, `.env.example` | — |
| Commits, compartilhamento (`rwfazul`), Classroom | Pendente | Nada foi commitado nem enviado | Ver `CHECKLIST_ACOES_MANUAIS.md` |

## Conclusão

**NÃO ESTÁ PRONTO PARA ENTREGA** — apenas por pendências que dependem da equipe, não do código:

1. as alterações **não estão commitadas** nem enviadas ao GitHub;
2. a **aprovação do dataset** pelo professor, o **compartilhamento com `rwfazul`** e a **postagem no Classroom** não podem ser feitos por código;
3. a revisão final do texto e a apresentação oral são da equipe.

Tecnicamente, o repositório está completo e verificado por execução: pipeline de dados, treino e modelo salvo, API, front-end sem dados simulados, 117 testes Python e 28 do front-end passando, lint e build limpos, relatório PDF revisado e instalação limpa reproduzida. Resultado a apresentar com honestidade: no teste de 2023 a Regressão Logística tem Macro F1 0,360 (referência 0,213), mas acurácia 44,48% (referência 46,96%) e Log-Loss 1,089 (frequências históricas: 1,061); o modelo **não demonstra superioridade geral**.

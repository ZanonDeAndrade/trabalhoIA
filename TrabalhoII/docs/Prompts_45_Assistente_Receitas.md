# Biblioteca de 45 prompts de implementação

**A documentação e os prompts são entregáveis de planejamento; não são código da aplicação executável.**

## Como usar
1. Anexe `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md` e o PDF da atividade a uma nova conversa.
2. Anexe os arquivos específicos que cada prompt indica. Use os prompts **01 a 45 na ordem**, com a etapa anterior terminada e testada antes de avançar.
3. Suba as alterações aprovadas ao repositório e atualize `IMPLEMENTATION_STATUS.md` a cada passo.
4. Se um prompt citar um arquivo ainda não criado, use a documentação como contrato, crie-o na etapa adequada e não declare que já existe.
5. Nunca passe a próxima etapa com falhas bloqueantes em RAG, MCP, inferência ou guardrails.

## Índice dos prompts

| # | Fase | Prompt | Arquivo |
|---|---|---|---|
| 01 | 01-planning | ANÁLISE DOS REQUISITOS | `PROMPT_01_01-planning_analise_dos_requisitos.md` |
| 02 | 01-planning | DEFINIÇÃO DA ARQUITETURA | `PROMPT_02_01-planning_definicao_da_arquitetura.md` |
| 03 | 01-planning | CRIAÇÃO DA ESTRUTURA DO REPOSITÓRIO | `PROMPT_03_01-planning_criacao_da_estrutura_do_repositorio.md` |
| 04 | 01-planning | CONFIGURAÇÃO DO AMBIENTE | `PROMPT_04_01-planning_configuracao_do_ambiente.md` |
| 05 | 01-planning | DEFINIÇÃO DOS CONTRATOS | `PROMPT_05_01-planning_definicao_dos_contratos.md` |
| 06 | 02-rag | COLETA E ORGANIZAÇÃO DAS RECEITAS | `PROMPT_06_02-rag_coleta_e_organizacao_das_receitas.md` |
| 07 | 02-rag | PROCESSAMENTO DOS DOCUMENTOS | `PROMPT_07_02-rag_processamento_dos_documentos.md` |
| 08 | 02-rag | CHUNKING | `PROMPT_08_02-rag_chunking.md` |
| 09 | 02-rag | GERAÇÃO DE EMBEDDINGS | `PROMPT_09_02-rag_geracao_de_embeddings.md` |
| 10 | 02-rag | ARMAZENAMENTO VETORIAL | `PROMPT_10_02-rag_armazenamento_vetorial.md` |
| 11 | 02-rag | RECUPERAÇÃO SEMÂNTICA | `PROMPT_11_02-rag_recuperacao_semantica.md` |
| 12 | 02-rag | VALIDAÇÃO DO RAG | `PROMPT_12_02-rag_validacao_do_rag.md` |
| 13 | 03-mcp | IMPLEMENTAÇÃO DO SERVIDOR MCP | `PROMPT_13_03-mcp_implementacao_do_servidor_mcp.md` |
| 14 | 03-mcp | TOOL SEARCH_KNOWLEDGE | `PROMPT_14_03-mcp_tool_search_knowledge.md` |
| 15 | 03-mcp | TOOL GET_DOCUMENT | `PROMPT_15_03-mcp_tool_get_document.md` |
| 16 | 03-mcp | TOOL LIST_TOPICS | `PROMPT_16_03-mcp_tool_list_topics.md` |
| 17 | 03-mcp | CLIENTE MCP | `PROMPT_17_03-mcp_cliente_mcp.md` |
| 18 | 03-mcp | TESTES DO MCP | `PROMPT_18_03-mcp_testes_do_mcp.md` |
| 19 | 04-llm | INTEGRAÇÃO COM LLM | `PROMPT_19_04-llm_integracao_com_llm.md` |
| 20 | 04-llm | SYSTEM PROMPT DO ASSISTENTE | `PROMPT_20_04-llm_system_prompt_do_assistente.md` |
| 21 | 04-llm | FUNCTION CALLING | `PROMPT_21_04-llm_function_calling.md` |
| 22 | 04-llm | ORQUESTRAÇÃO DE INFERÊNCIA | `PROMPT_22_04-llm_orquestracao_de_inferencia.md` |
| 23 | 04-llm | RESPOSTAS FUNDAMENTADAS | `PROMPT_23_04-llm_respostas_fundamentadas.md` |
| 24 | 05-security | GUARDRAILS DE ENTRADA | `PROMPT_24_05-security_guardrails_de_entrada.md` |
| 25 | 05-security | GUARDRAILS DE SAÍDA | `PROMPT_25_05-security_guardrails_de_saida.md` |
| 26 | 05-security | TESTES DE SEGURANÇA | `PROMPT_26_05-security_testes_de_seguranca.md` |
| 27 | 06-application | IMPLEMENTAÇÃO DO BACKEND | `PROMPT_27_06-application_implementacao_do_backend.md` |
| 28 | 06-application | INTEGRAÇÃO BACKEND MCP LLM | `PROMPT_28_06-application_integracao_backend_mcp_llm.md` |
| 29 | 06-application | ESTRUTURA DO FRONTEND | `PROMPT_29_06-application_estrutura_do_frontend.md` |
| 30 | 06-application | INTERFACE PRINCIPAL | `PROMPT_30_06-application_interface_principal.md` |
| 31 | 06-application | EXIBIÇÃO DAS RECEITAS | `PROMPT_31_06-application_exibicao_das_receitas.md` |
| 32 | 06-application | INTEGRAÇÃO FRONTEND BACKEND | `PROMPT_32_06-application_integracao_frontend_backend.md` |
| 33 | 06-application | TRATAMENTO DE ESTADOS E ERROS | `PROMPT_33_06-application_tratamento_de_estados_e_erros.md` |
| 34 | 07-quality | TESTES UNITÁRIOS | `PROMPT_34_07-quality_testes_unitarios.md` |
| 35 | 07-quality | TESTES DE INTEGRAÇÃO | `PROMPT_35_07-quality_testes_de_integracao.md` |
| 36 | 07-quality | TESTES END TO END | `PROMPT_36_07-quality_testes_end_to_end.md` |
| 37 | 07-quality | REVISÃO TÉCNICA | `PROMPT_37_07-quality_revisao_tecnica.md` |
| 38 | 07-quality | AUDITORIA DOS REQUISITOS | `PROMPT_38_07-quality_auditoria_dos_requisitos.md` |
| 39 | 08-delivery | README PROFISSIONAL | `PROMPT_39_08-delivery_readme_profissional.md` |
| 40 | 08-delivery | DOCUMENTAÇÃO TÉCNICA FINAL | `PROMPT_40_08-delivery_documentacao_tecnica_final.md` |
| 41 | 08-delivery | PREPARAÇÃO DO GITHUB | `PROMPT_41_08-delivery_preparacao_do_github.md` |
| 42 | 08-delivery | EVIDÊNCIAS DE FUNCIONAMENTO | `PROMPT_42_08-delivery_evidencias_de_funcionamento.md` |
| 43 | 08-delivery | ROTEIRO DE DEMONSTRAÇÃO | `PROMPT_43_08-delivery_roteiro_de_demonstracao.md` |
| 44 | 08-delivery | PERGUNTAS DO PROFESSOR | `PROMPT_44_08-delivery_perguntas_do_professor.md` |
| 45 | 08-delivery | VERIFICAÇÃO FINAL DE ENTREGA | `PROMPT_45_08-delivery_verificacao_final_de_entrega.md` |

## Dependências importantes

01–05 requisitos/contratos; 06–12 corpus, RAG e verificação; 13–18 MCP real; 19–23 LLM e tool calling; 24–26 guardrails; 27–33 HTTP e interface; 34–38 testes e auditoria; 39–45 entrega. As fases não autorizam adiar todos os testes ao final: cada prompt deve comprovar seu próprio funcionamento.


# PROMPT 01: ANÁLISE DOS REQUISITOS

**Papel da IA:** Analista de requisitos e auditor acadêmico.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Auditar o enunciado de IA II e garantir que cada obrigação tenha critério de aceitação mensurável.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/02-requirements/requirements.md`; `docs/12-delivery/delivery.md`.

**Instruções detalhadas:**
1. Ler o PDF da atividade completo antes de tomar decisões
2. Extrair cada exigência de RF01 a RF05 sem diluir itens
3. Comparar requisitos com escopo culinário e apontar lacunas
4. Montar matriz requisito→componente→teste→evidência
5. Distinguir exigências acadêmicas de decisões próprias e opcionais
6. Registrar ambiguidades com solução mínima documentada

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Comprovar cinco documentos como mínimo, três tools MCP reais, function calling e guardrails; conferir três testes obrigatórios e compartilhamento GitHub privado com rwfazul. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Analista de requisitos e auditor acadêmico** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 01, ANÁLISE DOS REQUISITOS**, cujo objetivo é: **Auditar o enunciado de IA II e garantir que cada obrigação tenha critério de aceitação mensurável**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/02-requirements/requirements.md`; `docs/12-delivery/delivery.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Ler o PDF da atividade completo antes de tomar decisões; extrair cada exigência de RF01 a RF05 sem diluir itens; comparar requisitos com escopo culinário e apontar lacunas; montar matriz requisito→componente→teste→evidência; distinguir exigências acadêmicas de decisões próprias e opcionais; registrar ambiguidades com solução mínima documentada. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Comprovar cinco documentos como mínimo, três tools MCP reais, function calling e guardrails; conferir três testes obrigatórios e compartilhamento GitHub privado com rwfazul**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 02 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 02: DEFINIÇÃO DA ARQUITETURA

**Papel da IA:** Arquiteto de software sênior.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Reconciliar stack e fronteiras de componentes com mínimo acoplamento.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/03-architecture/architecture.md`; `docs/03-architecture/adrs.md`; `docs/03-architecture/diagrams.md`.

**Instruções detalhadas:**
1. Separar ingestão offline RAG, servidor MCP stdio, cliente MCP no backend, orquestração LLM, guardrails e UI
2. Decidir comunicação com base na versão instalada do SDK
3. Registrar ADR sobre Chroma persistente, embeddings 384d, Ollama local e limites do hardware
4. Desenhar rotas de fluxo normal e de erro
5. Especificar dependências permitidas e proibidas
6. Impedir bypass das ferramentas MCP para respostas documentais

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** O diagrama deve mostrar tool calling de modelo para backend, chamada via MCP real e Chroma atrás do servidor; ausência de imports diretos rag no backend. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Arquiteto de software sênior** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 02, DEFINIÇÃO DA ARQUITETURA**, cujo objetivo é: **Reconciliar stack e fronteiras de componentes com mínimo acoplamento**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/03-architecture/architecture.md`; `docs/03-architecture/adrs.md`; `docs/03-architecture/diagrams.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Separar ingestão offline RAG, servidor MCP stdio, cliente MCP no backend, orquestração LLM, guardrails e UI; decidir comunicação com base na versão instalada do SDK; registrar ADR sobre Chroma persistente, embeddings 384d, Ollama local e limites do hardware; desenhar rotas de fluxo normal e de erro; especificar dependências permitidas e proibidas; impedir bypass das ferramentas MCP para respostas documentais. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **O diagrama deve mostrar tool calling de modelo para backend, chamada via MCP real e Chroma atrás do servidor; ausência de imports diretos rag no backend**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 03 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 03: CRIAÇÃO DA ESTRUTURA DO REPOSITÓRIO

**Papel da IA:** Engenheiro de software full stack.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Criar a estrutura inicial do monorepositório sem antecipar lógica de negócio.

**Requisitos relacionados:** RF01 RF02 RF03 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `README.md`; `PROJECT_CONTEXT.md`; `IMPLEMENTATION_STATUS.md`; `frontend/`; `backend/`; `mcp-server/`; `rag/`; `data/`; `scripts/`; `tests/`; `docs/`.

**Instruções detalhadas:**
1. Seguir a árvore de docs/03-architecture/project-structure.md
2. Inicializar diretórios fundamentais e módulos Python apenas quando importáveis
3. Criar placeholders .gitkeep nas pastas de dados
4. Separar packages, dependências e comandos de inicialização
5. Manter código da aplicação ausente de docs
6. Definir .gitignore para .env, node_modules, caches e data/chroma
7. Registrar arquivo criado no status

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Mostrar árvore resultante e imports mínimos; não gerar serviços fictícios ou endpoints com respostas mockadas como se reais. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de software full stack** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 03, CRIAÇÃO DA ESTRUTURA DO REPOSITÓRIO**, cujo objetivo é: **Criar a estrutura inicial do monorepositório sem antecipar lógica de negócio**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `README.md`; `PROJECT_CONTEXT.md`; `IMPLEMENTATION_STATUS.md`; `frontend/`; `backend/`; `mcp-server/`; `rag/`; `data/`; `scripts/`; `tests/`; `docs/`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Seguir a árvore de docs/03-architecture/project-structure.md; inicializar diretórios fundamentais e módulos Python apenas quando importáveis; criar placeholders .gitkeep nas pastas de dados; separar packages, dependências e comandos de inicialização; manter código da aplicação ausente de docs; definir .gitignore para .env, node_modules, caches e data/chroma; registrar arquivo criado no status. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Mostrar árvore resultante e imports mínimos; não gerar serviços fictícios ou endpoints com respostas mockadas como se reais**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 04 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 04: CONFIGURAÇÃO DO AMBIENTE

**Papel da IA:** DevOps e engenheiro de plataforma.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Configurar ambiente reproduzível em Ubuntu Linux.

**Requisitos relacionados:** RF01 RF02 RF03 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/pyproject.toml`; `mcp-server/pyproject.toml`; `rag/pyproject.toml`; `frontend/package.json`; `.env.example`; `scripts/verify_env.sh`; `docs/10-development/setup.md`.

**Instruções detalhadas:**
1. Fixar dependências após validar compatibilidade
2. Configurar Python venv e Node em versões suportadas
3. Verificar Ollama e disponibilidade do modelo local sem pressupor instalação
4. Testar import de sentence-transformers, chromadb, mcp e fastapi
5. Criar .env.example sem segredos
6. Documentar caminhos absolutos para Chroma/manifesto e como iniciar cliente/servidor stdio
7. Registrar comandos Linux válidos

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Confirmar imports, versão das ferramentas, health de Ollama quando instalado, e ausência de segredo no git; falha clara quando pré-requisito falta. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **DevOps e engenheiro de plataforma** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 04, CONFIGURAÇÃO DO AMBIENTE**, cujo objetivo é: **Configurar ambiente reproduzível em Ubuntu Linux**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/pyproject.toml`; `mcp-server/pyproject.toml`; `rag/pyproject.toml`; `frontend/package.json`; `.env.example`; `scripts/verify_env.sh`; `docs/10-development/setup.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Fixar dependências após validar compatibilidade; configurar Python venv e Node em versões suportadas; verificar Ollama e disponibilidade do modelo local sem pressupor instalação; testar import de sentence-transformers, chromadb, mcp e fastapi; criar .env.example sem segredos; documentar caminhos absolutos para Chroma/manifesto e como iniciar cliente/servidor stdio; registrar comandos Linux válidos. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Confirmar imports, versão das ferramentas, health de Ollama quando instalado, e ausência de segredo no git; falha clara quando pré-requisito falta**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 05 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 05: DEFINIÇÃO DOS CONTRATOS

**Papel da IA:** Arquiteto de API e modelagem de dados.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Congelar estruturas de entrada, saída e erros antes de implementar integrações.

**Requisitos relacionados:** RF02 RF03 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/08-application/contracts.md`; `backend/app/schemas/query.py`; `frontend/src/types/api.ts`; `mcp-server/tools.py`.

**Instruções detalhadas:**
1. Definir POST /api/v1/consultations e GET /healthz
2. Estabelecer status FOUND, INSUFFICIENT, BLOCKED e ERROR
3. Definir Recipe, Ingredient, Source, Evidence e Query
4. Diferenciar document_id, recipe_id, chunk_id e suas cardinalidades
5. Definir schemas Pydantic e tipos TypeScript compatíveis
6. Validar limites de texto e optionalidades
7. Especificar tool search_knowledge, get_document, list_topics com retornos JSON

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testes de serialização/desserialização, exemplo válido/parcial/ausente, campos obrigatórios, identificadores e compatibilidade TypeScript↔Python. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Arquiteto de API e modelagem de dados** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 05, DEFINIÇÃO DOS CONTRATOS**, cujo objetivo é: **Congelar estruturas de entrada, saída e erros antes de implementar integrações**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/08-application/contracts.md`; `backend/app/schemas/query.py`; `frontend/src/types/api.ts`; `mcp-server/tools.py`. Considere o PDF de IA II a referência normativa para RF02 RF03 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Definir POST /api/v1/consultations e GET /healthz; estabelecer status FOUND, INSUFFICIENT, BLOCKED e ERROR; definir Recipe, Ingredient, Source, Evidence e Query; diferenciar document_id, recipe_id, chunk_id e suas cardinalidades; definir schemas Pydantic e tipos TypeScript compatíveis; validar limites de texto e optionalidades; especificar tool search_knowledge, get_document, list_topics com retornos JSON. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testes de serialização/desserialização, exemplo válido/parcial/ausente, campos obrigatórios, identificadores e compatibilidade TypeScript↔Python**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 06 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 06: COLETA E ORGANIZAÇÃO DAS RECEITAS

**Papel da IA:** Engenheiro de dados e curador de corpus.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Coletar ao menos cinco documentos reais, distintos e rastreáveis.

**Requisitos relacionados:** RF01 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `data/sources/manifest.json`; `data/raw/`; `docs/04-rag/corpus.md`; `rag/ingest.py`.

**Instruções detalhadas:**
1. Utilizar cinco páginas do Wikilivros documentadas no corpus como candidatas, confirmar URL, licença, histórico e revisão
2. Coletar conteúdo pertinente via acesso permitido, mantendo snapshot e sha256
3. Registrar título, retrieved_at, source_url, revision_url, topic_key e autoria/atribuição
4. Observar variantes por página
5. Não alterar texto bruto
6. Garantir reexecução idempotente e falhas visíveis por origem

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Confirmar cinco manifest entries com conteúdo legível real, hash e licença; recusar documento vazio; não inventar páginas ou afirmar coleta sem download. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de dados e curador de corpus** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 06, COLETA E ORGANIZAÇÃO DAS RECEITAS**, cujo objetivo é: **Coletar ao menos cinco documentos reais, distintos e rastreáveis**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `data/sources/manifest.json`; `data/raw/`; `docs/04-rag/corpus.md`; `rag/ingest.py`. Considere o PDF de IA II a referência normativa para RF01. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Utilizar cinco páginas do Wikilivros documentadas no corpus como candidatas, confirmar URL, licença, histórico e revisão; coletar conteúdo pertinente via acesso permitido, mantendo snapshot e sha256; registrar título, retrieved_at, source_url, revision_url, topic_key e autoria/atribuição; observar variantes por página; não alterar texto bruto; garantir reexecução idempotente e falhas visíveis por origem. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Confirmar cinco manifest entries com conteúdo legível real, hash e licença; recusar documento vazio; não inventar páginas ou afirmar coleta sem download**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 07 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 07: PROCESSAMENTO DOS DOCUMENTOS

**Papel da IA:** Engenheiro de dados especialista em parsing.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Extrair receitas estruturadas do corpus sem perder a proveniência.

**Requisitos relacionados:** RF01 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/extract.py`; `rag/normalize.py`; `rag/ingredients.py`; `data/normalized/recipes.json`; `rag/tests/test_ingredients.py`.

**Instruções detalhadas:**
1. Remover navegação, rodapés e avisos irrelevantes
2. Segmentar variantes de uma mesma página sem misturar seus ingredientes
3. Preservar passos, unidades, números e medidas originais
4. Criar IDs estáveis por documento e variante
5. Normalizar ingredientes com mapa conservador de aliases
6. Não inferir tempo, porções ou temperaturas ausentes
7. Gerar JSON schema-validado com origem de cada receita

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testar que ovos e ovo normalizam corretamente, mas farinhas diferentes não; auditar variantes e contagem de ingredientes; comparar texto extraído com snapshots. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de dados especialista em parsing** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 07, PROCESSAMENTO DOS DOCUMENTOS**, cujo objetivo é: **Extrair receitas estruturadas do corpus sem perder a proveniência**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/extract.py`; `rag/normalize.py`; `rag/ingredients.py`; `data/normalized/recipes.json`; `rag/tests/test_ingredients.py`. Considere o PDF de IA II a referência normativa para RF01. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Remover navegação, rodapés e avisos irrelevantes; segmentar variantes de uma mesma página sem misturar seus ingredientes; preservar passos, unidades, números e medidas originais; criar IDs estáveis por documento e variante; normalizar ingredientes com mapa conservador de aliases; não inferir tempo, porções ou temperaturas ausentes; gerar JSON schema-validado com origem de cada receita. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testar que ovos e ovo normalizam corretamente, mas farinhas diferentes não; auditar variantes e contagem de ingredientes; comparar texto extraído com snapshots**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 08 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 08: CHUNKING

**Papel da IA:** Especialista em processamento de linguagem e RAG.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Construir chunks preservando a identidade de cada versão de receita.

**Requisitos relacionados:** RF01 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/chunk.py`; `rag/tests/test_chunk.py`; `docs/04-rag/pipeline.md`.

**Instruções detalhadas:**
1. Usar unidade lógica de receita para textos curtos
2. Gerar chunk de descoberta com título+categoria+ingredientes obrigatórios
3. Separar instruções longas apenas quando necessário
4. Estabelecer chunk_size=100 tokens e chunk_overlap=20 para trechos que precisem de divisão
5. Usar tokenizer compatível com embedding
6. Repetir recipe_id, document_id, source_url e topic_key em metadados
7. Verificar truncamento em max_seq_length do encoder

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Garantir nenhum chunk una duas variantes; zero chunks sem fonte; comprimento e overlap medidos; comparação de reconstrução de receita completa via recipe_id. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Especialista em processamento de linguagem e RAG** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 08, CHUNKING**, cujo objetivo é: **Construir chunks preservando a identidade de cada versão de receita**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/chunk.py`; `rag/tests/test_chunk.py`; `docs/04-rag/pipeline.md`. Considere o PDF de IA II a referência normativa para RF01. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Usar unidade lógica de receita para textos curtos; gerar chunk de descoberta com título+categoria+ingredientes obrigatórios; separar instruções longas apenas quando necessário; estabelecer chunk_size=100 tokens e chunk_overlap=20 para trechos que precisem de divisão; usar tokenizer compatível com embedding; repetir recipe_id, document_id, source_url e topic_key em metadados; verificar truncamento em max_seq_length do encoder. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Garantir nenhum chunk una duas variantes; zero chunks sem fonte; comprimento e overlap medidos; comparação de reconstrução de receita completa via recipe_id**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 09 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 09: GERAÇÃO DE EMBEDDINGS

**Papel da IA:** Especialista em embeddings semânticos.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Gerar vetores do texto de busca de maneira reproduzível.

**Requisitos relacionados:** RF01 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/embed.py`; `rag/tests/test_retrieval.py`; `docs/04-rag/pipeline.md`.

**Instruções detalhadas:**
1. Carregar uma vez sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
2. Usar transformação idêntica para consultas e corpus
3. Fixar dimensionalidade 384 e registrar modelo no índice
4. Tratar batches, falhas e tempo de inicialização
5. Garantir que vetores inválidos ou vazios interrompam a ingestão em vez de fabricar resultados
6. Escrever verificação de português em conjunto de consultas rotuladas

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Assert dimensão=384, finitude de valores, repetição determinística na mesma configuração e ausência de vetores para chunk vazio. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Especialista em embeddings semânticos** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 09, GERAÇÃO DE EMBEDDINGS**, cujo objetivo é: **Gerar vetores do texto de busca de maneira reproduzível**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/embed.py`; `rag/tests/test_retrieval.py`; `docs/04-rag/pipeline.md`. Considere o PDF de IA II a referência normativa para RF01. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Carregar uma vez sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2; usar transformação idêntica para consultas e corpus; fixar dimensionalidade 384 e registrar modelo no índice; tratar batches, falhas e tempo de inicialização; garantir que vetores inválidos ou vazios interrompam a ingestão em vez de fabricar resultados; escrever verificação de português em conjunto de consultas rotuladas. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Assert dimensão=384, finitude de valores, repetição determinística na mesma configuração e ausência de vetores para chunk vazio**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 10 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 10: ARMAZENAMENTO VETORIAL

**Papel da IA:** Engenheiro de armazenamento vetorial.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Persistir chunks e embeddings no ChromaDB de forma idempotente.

**Requisitos relacionados:** RF01 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/vector_store.py`; `data/chroma/`; `docs/04-rag/pipeline.md`.

**Instruções detalhadas:**
1. Inicializar PersistentClient apontando para caminho configurável
2. Criar coleção nomeada e versionada compatível com 384 dimensões
3. Usar chunk_id como chave estável e metadados escalares
4. Salvar documento textual, source_url, recipe_id e topic_key
5. Implementar upsert sem duplicação, recuperação por id, contagem e limpeza documentada
6. Nunca inserir embedding de modelo incompatível
7. Manter índice fora do Git

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Após duas ingestões idênticas contagem permanece igual; consultas devolvem metadados; reiniciar processo mantém vetores; falha em dimensão errada. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de armazenamento vetorial** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 10, ARMAZENAMENTO VETORIAL**, cujo objetivo é: **Persistir chunks e embeddings no ChromaDB de forma idempotente**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/vector_store.py`; `data/chroma/`; `docs/04-rag/pipeline.md`. Considere o PDF de IA II a referência normativa para RF01. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Inicializar PersistentClient apontando para caminho configurável; criar coleção nomeada e versionada compatível com 384 dimensões; usar chunk_id como chave estável e metadados escalares; salvar documento textual, source_url, recipe_id e topic_key; implementar upsert sem duplicação, recuperação por id, contagem e limpeza documentada; nunca inserir embedding de modelo incompatível; manter índice fora do Git. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Após duas ingestões idênticas contagem permanece igual; consultas devolvem metadados; reiniciar processo mantém vetores; falha em dimensão errada**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 11 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 11: RECUPERAÇÃO SEMÂNTICA

**Papel da IA:** Engenheiro de busca semântica.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Recuperar top-k candidatos reais e classificá-los por compatibilidade de ingredientes.

**Requisitos relacionados:** RF01 RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/retrieve.py`; `rag/ingredients.py`; `rag/tests/test_retrieval.py`.

**Instruções detalhadas:**
1. Implementar embedding de pergunta e query ao Chroma top_k=8 inicialmente
2. Validar IDs e proveniência de cada chunk
3. Deduplicar recipe_id e consultar JSON normalizado para completar preparo
4. Retornar evidências com score/distance sem assumir escala universal
5. Calcular presentes/faltantes por matching determinístico, diferenciar COMPLETE, PARTIAL e INSUFFICIENT
6. Filtrar topic_key só quando requisitado
7. Limitar sugestões e não inventar alternativas

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testar pergunta portuguesa próxima do corpus, ingredientes faltantes corretos, ausência de evidência e rejeição de item sem source_url. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de busca semântica** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 11, RECUPERAÇÃO SEMÂNTICA**, cujo objetivo é: **Recuperar top-k candidatos reais e classificá-los por compatibilidade de ingredientes**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/retrieve.py`; `rag/ingredients.py`; `rag/tests/test_retrieval.py`. Considere o PDF de IA II a referência normativa para RF01 RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Implementar embedding de pergunta e query ao Chroma top_k=8 inicialmente; validar IDs e proveniência de cada chunk; deduplicar recipe_id e consultar JSON normalizado para completar preparo; retornar evidências com score/distance sem assumir escala universal; calcular presentes/faltantes por matching determinístico, diferenciar COMPLETE, PARTIAL e INSUFFICIENT; filtrar topic_key só quando requisitado; limitar sugestões e não inventar alternativas. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testar pergunta portuguesa próxima do corpus, ingredientes faltantes corretos, ausência de evidência e rejeição de item sem source_url**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 12 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 12: VALIDAÇÃO DO RAG

**Papel da IA:** Engenheiro de avaliação de recuperação.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Avaliar recuperação e fundamentação antes de ligar um LLM.

**Requisitos relacionados:** RF01 RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/tests/test_retrieval.py`; `docs/09-testing/test-plan.md`; `tests/fixtures/`.

**Instruções detalhadas:**
1. Criar dataset com pelo menos quinze perguntas rotuladas e expected_recipe_ids
2. Testar completas, parciais, sem evidência e categorias
3. Computar Recall@8, Precision@5 em amostra, cobertura de fonte e erro na identificação de ingredientes
4. Coletar trace de chunks e documentar relevância
5. Calibrar threshold sem alegar universalidade
6. Registrar limitações do corpus

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Relatório com métricas realmente executadas, exemplos rastreáveis e zero URL inexistente; não anunciar metas como resultados. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de avaliação de recuperação** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 12, VALIDAÇÃO DO RAG**, cujo objetivo é: **Avaliar recuperação e fundamentação antes de ligar um LLM**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/tests/test_retrieval.py`; `docs/09-testing/test-plan.md`; `tests/fixtures/`. Considere o PDF de IA II a referência normativa para RF01 RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar dataset com pelo menos quinze perguntas rotuladas e expected_recipe_ids; testar completas, parciais, sem evidência e categorias; computar Recall@8, Precision@5 em amostra, cobertura de fonte e erro na identificação de ingredientes; coletar trace de chunks e documentar relevância; calibrar threshold sem alegar universalidade; registrar limitações do corpus. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Relatório com métricas realmente executadas, exemplos rastreáveis e zero URL inexistente; não anunciar metas como resultados**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 13 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 13: IMPLEMENTAÇÃO DO SERVIDOR MCP

**Papel da IA:** Desenvolvedor de protocolo MCP.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Criar processo servidor MCP real via SDK oficial Python e transporte stdio.

**Requisitos relacionados:** RF02 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `mcp-server/server.py`; `mcp-server/pyproject.toml`; `mcp-server/tests/test_tools.py`.

**Instruções detalhadas:**
1. Inspecionar versão realmente instalada e nomes corretos da API antes de codificar
2. Inicializar servidor, registrar lifecycle e disponibilizar ferramentas tipadas
3. Garantir stdout exclusivo ao protocolo e logs em stderr
4. Resolver caminhos Chroma/JSON via configuração
5. Separar entrypoint e implementations das tools
6. Proteger contra processos zumbis e falhas de inicialização

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Usar cliente SDK para initialize e list_tools por stdio, comprovando protocolo; testar desligamento, stderr e ambiente vazio. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Desenvolvedor de protocolo MCP** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 13, IMPLEMENTAÇÃO DO SERVIDOR MCP**, cujo objetivo é: **Criar processo servidor MCP real via SDK oficial Python e transporte stdio**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `mcp-server/server.py`; `mcp-server/pyproject.toml`; `mcp-server/tests/test_tools.py`. Considere o PDF de IA II a referência normativa para RF02. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Inspecionar versão realmente instalada e nomes corretos da API antes de codificar; inicializar servidor, registrar lifecycle e disponibilizar ferramentas tipadas; garantir stdout exclusivo ao protocolo e logs em stderr; resolver caminhos Chroma/JSON via configuração; separar entrypoint e implementations das tools; proteger contra processos zumbis e falhas de inicialização. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Usar cliente SDK para initialize e list_tools por stdio, comprovando protocolo; testar desligamento, stderr e ambiente vazio**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 14 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 14: TOOL SEARCH_KNOWLEDGE

**Papel da IA:** Desenvolvedor MCP e especialista RAG.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Expor busca semântica do corpus como ferramenta MCP tipada.

**Requisitos relacionados:** RF01 RF02 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `mcp-server/tools.py`; `rag/retrieve.py`; `mcp-server/tests/test_tools.py`.

**Instruções detalhadas:**
1. Criar search_knowledge(query:string, top_k:int opcional, topic_key:string opcional, available_ingredients:list opcional)
2. Descrever uso em linguagem adequada ao LLM
3. Limitar top_k a intervalo seguro
4. Delegar recuperação a rag/retrieve.py, retornar JSON com chunks, scores, IDs, sources e receita candidata
5. Não emitir instruções fictícias
6. Tratar ausência de dados como resultado vazio estruturado

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Cliente MCP real chama ferramenta e recebe top_k com metadados; consulta vazia gera erro tipado; corpus sem resultados não simula achado. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Desenvolvedor MCP e especialista RAG** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 14, TOOL SEARCH_KNOWLEDGE**, cujo objetivo é: **Expor busca semântica do corpus como ferramenta MCP tipada**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `mcp-server/tools.py`; `rag/retrieve.py`; `mcp-server/tests/test_tools.py`. Considere o PDF de IA II a referência normativa para RF01 RF02. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar search_knowledge(query:string, top_k:int opcional, topic_key:string opcional, available_ingredients:list opcional); descrever uso em linguagem adequada ao LLM; limitar top_k a intervalo seguro; delegar recuperação a rag/retrieve.py, retornar JSON com chunks, scores, IDs, sources e receita candidata; não emitir instruções fictícias; tratar ausência de dados como resultado vazio estruturado. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Cliente MCP real chama ferramenta e recebe top_k com metadados; consulta vazia gera erro tipado; corpus sem resultados não simula achado**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 15 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 15: TOOL GET_DOCUMENT

**Papel da IA:** Desenvolvedor MCP e engenheiro de dados.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Permitir recuperar integralmente uma receita/versionamento identificado.

**Requisitos relacionados:** RF02 RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `mcp-server/tools.py`; `data/normalized/recipes.json`; `mcp-server/tests/test_tools.py`.

**Instruções detalhadas:**
1. Criar get_document(document_id ou recipe_id conforme contrato congelado)
2. Aceitar apenas ID tipado e validar existência
3. Procurar JSON normalizado e retornar título, versão, ingredientes, passos, origem e campos opcionais verificados
4. Distinguir documento (página) de receita (variante), usando recipe_id para preparo
5. Tratar ID inexistente com resposta de erro estruturada

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Consulta conhecida devolve modo de preparo completo e fonte; ID inexistente não retorna outro documento; tool chamada pelo protocolo. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Desenvolvedor MCP e engenheiro de dados** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 15, TOOL GET_DOCUMENT**, cujo objetivo é: **Permitir recuperar integralmente uma receita/versionamento identificado**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `mcp-server/tools.py`; `data/normalized/recipes.json`; `mcp-server/tests/test_tools.py`. Considere o PDF de IA II a referência normativa para RF02 RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar get_document(document_id ou recipe_id conforme contrato congelado); aceitar apenas ID tipado e validar existência; procurar JSON normalizado e retornar título, versão, ingredientes, passos, origem e campos opcionais verificados; distinguir documento (página) de receita (variante), usando recipe_id para preparo; tratar ID inexistente com resposta de erro estruturada. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Consulta conhecida devolve modo de preparo completo e fonte; ID inexistente não retorna outro documento; tool chamada pelo protocolo**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 16 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 16: TOOL LIST_TOPICS

**Papel da IA:** Desenvolvedor MCP.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Expor lista de categorias realmente presentes no corpus.

**Requisitos relacionados:** RF02 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `mcp-server/tools.py`; `data/normalized/recipes.json`; `mcp-server/tests/test_tools.py`.

**Instruções detalhadas:**
1. Criar list_topics() com retorno estruturado [{topic_key,label,count}] e data_version se disponível
2. Derivar tópicos das receitas indexadas, não de lista fixa desconectada
3. Ordenar de forma estável, remover duplicatas
4. Lidar com base vazia e códigos de erro claros

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Tópicos e contagens devem coincidir com JSON normalizado; base vazia retorna lista vazia; chamada MCP real lista e executa a tool. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Desenvolvedor MCP** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 16, TOOL LIST_TOPICS**, cujo objetivo é: **Expor lista de categorias realmente presentes no corpus**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `mcp-server/tools.py`; `data/normalized/recipes.json`; `mcp-server/tests/test_tools.py`. Considere o PDF de IA II a referência normativa para RF02. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar list_topics() com retorno estruturado [{topic_key,label,count}] e data_version se disponível; derivar tópicos das receitas indexadas, não de lista fixa desconectada; ordenar de forma estável, remover duplicatas; lidar com base vazia e códigos de erro claros. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Tópicos e contagens devem coincidir com JSON normalizado; base vazia retorna lista vazia; chamada MCP real lista e executa a tool**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 17 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 17: CLIENTE MCP

**Papel da IA:** Engenheiro de integração Python.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Criar cliente de protocolo MCP no backend para a comunicação por stdio.

**Requisitos relacionados:** RF02 RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/integrations/mcp_client.py`; `backend/tests/test_mcp_integration.py`.

**Instruções detalhadas:**
1. Implementar sessão usando SDK compatível com servidor
2. Gerir caminho de inicialização e env seguros
3. Executar initialize, list_tools, call_tool
4. Converter schemas MCP em definições que o LLM entende sem substituir o canal real
5. Passar parâmetros tipados, validar JSON de retorno, tratar timeout e encerramento
6. Fechar subprocessos e sessões corretamente

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Trace de initialize/list_tools/call_tool pela sessão real; erro reproduzível quando servidor desconectado; nenhuma importação direta das tools Python no backend. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de integração Python** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 17, CLIENTE MCP**, cujo objetivo é: **Criar cliente de protocolo MCP no backend para a comunicação por stdio**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/integrations/mcp_client.py`; `backend/tests/test_mcp_integration.py`. Considere o PDF de IA II a referência normativa para RF02 RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Implementar sessão usando SDK compatível com servidor; gerir caminho de inicialização e env seguros; executar initialize, list_tools, call_tool; converter schemas MCP em definições que o LLM entende sem substituir o canal real; passar parâmetros tipados, validar JSON de retorno, tratar timeout e encerramento; fechar subprocessos e sessões corretamente. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Trace de initialize/list_tools/call_tool pela sessão real; erro reproduzível quando servidor desconectado; nenhuma importação direta das tools Python no backend**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 18 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 18: TESTES DO MCP

**Papel da IA:** Engenheiro QA de protocolo.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Provar que as três ferramentas são descobertas e executadas por MCP.

**Requisitos relacionados:** RF02 RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `mcp-server/tests/test_tools.py`; `backend/tests/test_mcp_integration.py`; `tests/evidence/`.

**Instruções detalhadas:**
1. Subir servidor em subprocesso isolado
2. Executar handshake e discovery
3. Validar schema/descrição de search_knowledge, get_document e list_topics
4. Chamar cada ferramenta com entrada válida e inválida
5. Medir startup e handling de resposta vazia
6. Capturar evidência sanitizada de execução via protocolo
7. Não trocar teste MCP por chamada direta de função

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Prova real de três tools listadas, três execuções tool_call e retorno estruturado; falhas de validação testadas. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro QA de protocolo** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 18, TESTES DO MCP**, cujo objetivo é: **Provar que as três ferramentas são descobertas e executadas por MCP**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `mcp-server/tests/test_tools.py`; `backend/tests/test_mcp_integration.py`; `tests/evidence/`. Considere o PDF de IA II a referência normativa para RF02 RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Subir servidor em subprocesso isolado; executar handshake e discovery; validar schema/descrição de search_knowledge, get_document e list_topics; chamar cada ferramenta com entrada válida e inválida; medir startup e handling de resposta vazia; capturar evidência sanitizada de execução via protocolo; não trocar teste MCP por chamada direta de função. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Prova real de três tools listadas, três execuções tool_call e retorno estruturado; falhas de validação testadas**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 19 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 19: INTEGRAÇÃO COM LLM

**Papel da IA:** Engenheiro de inferência com LLM.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Integrar Ollama e modelo capaz de function calling.

**Requisitos relacionados:** RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/integrations/ollama_client.py`; `backend/app/settings.py`; `backend/tests/test_inference.py`.

**Instruções detalhadas:**
1. Validar disponibilidade de Ollama e do modelo qwen3:4b ou registrar ajuste por ADR
2. Implementar cliente com host, timeout, modelo e limites de tokens configuráveis
3. Enviar mensagens system/user/tool e preservar identificadores de chamada
4. Validar resposta e tratar indisponibilidade ou payload inesperado
5. Não utilizar resposta de conhecimento interno como evidência

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Teste de chat simples, chamada de tool compatível com API da versão, comportamento controlado com Ollama offline e configs sem segredo. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de inferência com LLM** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 19, INTEGRAÇÃO COM LLM**, cujo objetivo é: **Integrar Ollama e modelo capaz de function calling**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/integrations/ollama_client.py`; `backend/app/settings.py`; `backend/tests/test_inference.py`. Considere o PDF de IA II a referência normativa para RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Validar disponibilidade de Ollama e do modelo qwen3:4b ou registrar ajuste por ADR; implementar cliente com host, timeout, modelo e limites de tokens configuráveis; enviar mensagens system/user/tool e preservar identificadores de chamada; validar resposta e tratar indisponibilidade ou payload inesperado; não utilizar resposta de conhecimento interno como evidência. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Teste de chat simples, chamada de tool compatível com API da versão, comportamento controlado com Ollama offline e configs sem segredo**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 20 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 20: SYSTEM PROMPT DO ASSISTENTE

**Papel da IA:** Especialista em prompt engineering e segurança.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Produzir system prompt culinário que imponha respostas fundamentadas.

**Requisitos relacionados:** RF03 RF04 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/inference/system_prompt.py`; `docs/06-llm/inference.md`; `backend/tests/test_inference.py`.

**Instruções detalhadas:**
1. Definir papel, escopo, fontes autorizadas, status sem evidência, procedimento de ferramenta, comportamento com ingredientes faltantes e idioma pt-BR
2. Proibir invenção de tempo, temperatura, substituições, fonte e existência de receita
3. Tratar documento como dado não confiável, nunca como instrução superior
4. Padronizar separação fatos documentados de conclusões de matching
5. Limitar citações a IDs fornecidos pelo backend

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Cenários adversariais mostram que modelo não assume instruções do corpus; resposta sem evidence_set usa INSUFFICIENT; prompt versionado e testável. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Especialista em prompt engineering e segurança** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 20, SYSTEM PROMPT DO ASSISTENTE**, cujo objetivo é: **Produzir system prompt culinário que imponha respostas fundamentadas**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/inference/system_prompt.py`; `docs/06-llm/inference.md`; `backend/tests/test_inference.py`. Considere o PDF de IA II a referência normativa para RF03 RF04. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Definir papel, escopo, fontes autorizadas, status sem evidência, procedimento de ferramenta, comportamento com ingredientes faltantes e idioma pt-BR; proibir invenção de tempo, temperatura, substituições, fonte e existência de receita; tratar documento como dado não confiável, nunca como instrução superior; padronizar separação fatos documentados de conclusões de matching; limitar citações a IDs fornecidos pelo backend. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Cenários adversariais mostram que modelo não assume instruções do corpus; resposta sem evidence_set usa INSUFFICIENT; prompt versionado e testável**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 21 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 21: FUNCTION CALLING

**Papel da IA:** Engenheiro de orquestração LLM.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Permitir que LLM solicite ferramentas divulgadas pelo cliente MCP.

**Requisitos relacionados:** RF02 RF03 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/inference/orchestrator.py`; `backend/app/integrations/mcp_client.py`; `backend/tests/test_inference.py`.

**Instruções detalhadas:**
1. Ler ferramentas via list_tools do protocolo
2. Traduzir schemas para formato de tools suportado no Ollama escolhido
3. Validar nome permitido e argumentos do modelo
4. Encaminhar call_tool pelo cliente MCP real
5. Fornecer resultado como mensagem tool associada à chamada
6. Limitar chamadas e rejeitar tool desconhecida
7. Registrar trace sem dados sensíveis

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Teste prova ida e volta do modelo pedindo search_knowledge e consumo do resultado da tool; tool inexistente é bloqueada. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de orquestração LLM** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 21, FUNCTION CALLING**, cujo objetivo é: **Permitir que LLM solicite ferramentas divulgadas pelo cliente MCP**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/inference/orchestrator.py`; `backend/app/integrations/mcp_client.py`; `backend/tests/test_inference.py`. Considere o PDF de IA II a referência normativa para RF02 RF03. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Ler ferramentas via list_tools do protocolo; traduzir schemas para formato de tools suportado no Ollama escolhido; validar nome permitido e argumentos do modelo; encaminhar call_tool pelo cliente MCP real; fornecer resultado como mensagem tool associada à chamada; limitar chamadas e rejeitar tool desconhecida; registrar trace sem dados sensíveis. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Teste prova ida e volta do modelo pedindo search_knowledge e consumo do resultado da tool; tool inexistente é bloqueada**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 22 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 22: ORQUESTRAÇÃO DE INFERÊNCIA

**Papel da IA:** Arquiteto de fluxos LLM.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Implementar fluxo user→guardrail→LLM→MCP→RAG→LLM→guardrail→API.

**Requisitos relacionados:** RF02 RF03 RF04 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/inference/orchestrator.py`; `backend/app/services/query_service.py`; `backend/tests/test_inference.py`.

**Instruções detalhadas:**
1. Criar state machine ou loop de inferência com limite máximo de tool calls e timeout
2. Carregar prompt system e mensagem user
3. Controlar escolha de tools sem chamadas repetidas desnecessárias
4. Chamar get_document quando o preparo completo for necessário
5. Manter evidence_set imutável dos resultados MCP
6. Montar resposta estruturada com status e fontes
7. Tratar tool errors e saída inconsistente

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Teste com fake transport de LLM e MCP para branches principais, e teste real para caminho feliz; sem loop infinito; resposta sem fonte vira INSUFFICIENT. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Arquiteto de fluxos LLM** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 22, ORQUESTRAÇÃO DE INFERÊNCIA**, cujo objetivo é: **Implementar fluxo user→guardrail→LLM→MCP→RAG→LLM→guardrail→API**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/inference/orchestrator.py`; `backend/app/services/query_service.py`; `backend/tests/test_inference.py`. Considere o PDF de IA II a referência normativa para RF02 RF03 RF04. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar state machine ou loop de inferência com limite máximo de tool calls e timeout; carregar prompt system e mensagem user; controlar escolha de tools sem chamadas repetidas desnecessárias; chamar get_document quando o preparo completo for necessário; manter evidence_set imutável dos resultados MCP; montar resposta estruturada com status e fontes; tratar tool errors e saída inconsistente. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Teste com fake transport de LLM e MCP para branches principais, e teste real para caminho feliz; sem loop infinito; resposta sem fonte vira INSUFFICIENT**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 23 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 23: RESPOSTAS FUNDAMENTADAS

**Papel da IA:** Engenheiro de qualidade de resposta RAG.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Garantir que cada afirmação operacional tenha documento recuperado como evidência.

**Requisitos relacionados:** RF03 RF04 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/inference/orchestrator.py`; `backend/app/guardrails/output_guardrail.py`; `backend/tests/test_inference.py`.

**Instruções detalhadas:**
1. Reconciliar IDs do LLM com IDs de tool realmente retornados
2. Manter passos, ingredientes e fonte extraídos do objeto canônico, não de texto livre do LLM
3. Impedir tempo, porção e temperatura sem dado documental
4. Diferenciar matching algorítmico de fato da receita
5. Gerar estado INSUFFICIENT quando há recuperação vazia ou dúvida
6. Vincular source_url e recipe_id diretamente aos objetos recuperados

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Teste com resposta maliciosa citando fonte inexistente deve ser rejeitada; testar citação e instruções completas contra JSON do corpus. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de qualidade de resposta RAG** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 23, RESPOSTAS FUNDAMENTADAS**, cujo objetivo é: **Garantir que cada afirmação operacional tenha documento recuperado como evidência**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/inference/orchestrator.py`; `backend/app/guardrails/output_guardrail.py`; `backend/tests/test_inference.py`. Considere o PDF de IA II a referência normativa para RF03 RF04. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Reconciliar IDs do LLM com IDs de tool realmente retornados; manter passos, ingredientes e fonte extraídos do objeto canônico, não de texto livre do LLM; impedir tempo, porção e temperatura sem dado documental; diferenciar matching algorítmico de fato da receita; gerar estado INSUFFICIENT quando há recuperação vazia ou dúvida; vincular source_url e recipe_id diretamente aos objetos recuperados. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Teste com resposta maliciosa citando fonte inexistente deve ser rejeitada; testar citação e instruções completas contra JSON do corpus**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 24 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 24: GUARDRAILS DE ENTRADA

**Papel da IA:** Especialista em segurança de aplicações e LLM.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Validar mensagem e proteger o escopo culinário.

**Requisitos relacionados:** RF04 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/guardrails/input_guardrail.py`; `backend/tests/test_guardrails.py`; `docs/07-security/guardrails.md`.

**Instruções detalhadas:**
1. Implementar validação de tipo e tamanho de pergunta, limites de ingredientes e caracteres, strings vazias e controle de recursos
2. Bloquear pedidos explicitamente fora de culinária
3. Detectar padrões de prompt injection sem assumir que só regex resolve
4. Preservar perguntas culinárias benignas mesmo com palavras comuns
5. Evitar que input sobrescreva system prompt
6. Fornecer BLOCKED tipado sem vazar detalhes

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testar vazio, array inesperado, prompt injection direto, pedido fora do escopo e consulta culinária válida; reportar falsos positivos. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Especialista em segurança de aplicações e LLM** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 24, GUARDRAILS DE ENTRADA**, cujo objetivo é: **Validar mensagem e proteger o escopo culinário**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/guardrails/input_guardrail.py`; `backend/tests/test_guardrails.py`; `docs/07-security/guardrails.md`. Considere o PDF de IA II a referência normativa para RF04. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Implementar validação de tipo e tamanho de pergunta, limites de ingredientes e caracteres, strings vazias e controle de recursos; bloquear pedidos explicitamente fora de culinária; detectar padrões de prompt injection sem assumir que só regex resolve; preservar perguntas culinárias benignas mesmo com palavras comuns; evitar que input sobrescreva system prompt; fornecer BLOCKED tipado sem vazar detalhes. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testar vazio, array inesperado, prompt injection direto, pedido fora do escopo e consulta culinária válida; reportar falsos positivos**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 25 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 25: GUARDRAILS DE SAÍDA

**Papel da IA:** Engenheiro de segurança e QA.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Verificar que cards e narrativa correspondem a evidências recuperadas.

**Requisitos relacionados:** RF03 RF04 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/guardrails/output_guardrail.py`; `backend/tests/test_guardrails.py`; `docs/07-security/guardrails.md`.

**Instruções detalhadas:**
1. Construir allowlist de IDs e source_url do conjunto MCP
2. Verificar recipe_id citado, ingredientes e passos contra receita normalizada
3. Rejeitar dados nutricionais, temperaturas e substituições não documentadas
4. Impedir vazamento de prompt interno e chaves
5. Definir fallback INSUFFICIENT ou ERROR quando resposta é inconsistente
6. Manter tratamento proporcional ao MVP

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Rejeitar source_url inventada, ingrediente inventado e preparo não documentado; aceitar resposta corretamente citada; fazer testes de regressão. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de segurança e QA** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 25, GUARDRAILS DE SAÍDA**, cujo objetivo é: **Verificar que cards e narrativa correspondem a evidências recuperadas**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/guardrails/output_guardrail.py`; `backend/tests/test_guardrails.py`; `docs/07-security/guardrails.md`. Considere o PDF de IA II a referência normativa para RF03 RF04. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Construir allowlist de IDs e source_url do conjunto MCP; verificar recipe_id citado, ingredientes e passos contra receita normalizada; rejeitar dados nutricionais, temperaturas e substituições não documentadas; impedir vazamento de prompt interno e chaves; definir fallback INSUFFICIENT ou ERROR quando resposta é inconsistente; manter tratamento proporcional ao MVP. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Rejeitar source_url inventada, ingrediente inventado e preparo não documentado; aceitar resposta corretamente citada; fazer testes de regressão**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 26 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 26: TESTES DE SEGURANÇA

**Papel da IA:** Engenheiro QA de segurança.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Avaliar entradas adversariais e falhas de fundamentação.

**Requisitos relacionados:** RF04 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/tests/test_guardrails.py`; `tests/evidence/`; `docs/09-testing/test-plan.md`.

**Instruções detalhadas:**
1. Criar suíte com prompt injections em pergunta e texto de documento, payload longo, consulta fora de domínio, tag HTML e fonte falsa
2. Testar execução de tools não autorizadas
3. Validar logs sem segredo e CORS
4. Examinar respostas de segurança alimentar não fundamentadas
5. Registrar amostras e resultados reais com indicação de falsos negativos

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Evidências de BLOCKED, INSUFFICIENT e mensagens de erro seguras; nenhuma chave em resposta/log; rastrear testes ao RF04. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro QA de segurança** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 26, TESTES DE SEGURANÇA**, cujo objetivo é: **Avaliar entradas adversariais e falhas de fundamentação**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/tests/test_guardrails.py`; `tests/evidence/`; `docs/09-testing/test-plan.md`. Considere o PDF de IA II a referência normativa para RF04. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar suíte com prompt injections em pergunta e texto de documento, payload longo, consulta fora de domínio, tag HTML e fonte falsa; testar execução de tools não autorizadas; validar logs sem segredo e CORS; examinar respostas de segurança alimentar não fundamentadas; registrar amostras e resultados reais com indicação de falsos negativos. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Evidências de BLOCKED, INSUFFICIENT e mensagens de erro seguras; nenhuma chave em resposta/log; rastrear testes ao RF04**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 27 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 27: IMPLEMENTAÇÃO DO BACKEND

**Papel da IA:** Desenvolvedor backend FastAPI.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Oferecer API HTTP enxuta e tipada para consultas culinárias.

**Requisitos relacionados:** RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/main.py`; `backend/app/api/routes.py`; `backend/app/schemas/query.py`; `backend/app/services/query_service.py`; `backend/app/settings.py`.

**Instruções detalhadas:**
1. Definir POST /api/v1/consultations e GET /healthz
2. Construir validação Pydantic e schemas do contrato
3. Orquestrar guardrail de entrada, inferência e saída com services
4. Configurar CORS limitado, timeout e erros HTTP apropriados
5. Fornecer request_id e logs mínimos
6. Não acoplar framework ao módulo RAG
7. Utilizar MCP client como única fonte de evidência documental

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testes com TestClient para 200 FOUND/INSUFFICIENT, 4xx BLOCKED/entrada inválida e 5xx/503 de dependência; json snake_case conforme contrato. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Desenvolvedor backend FastAPI** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 27, IMPLEMENTAÇÃO DO BACKEND**, cujo objetivo é: **Oferecer API HTTP enxuta e tipada para consultas culinárias**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/main.py`; `backend/app/api/routes.py`; `backend/app/schemas/query.py`; `backend/app/services/query_service.py`; `backend/app/settings.py`. Considere o PDF de IA II a referência normativa para RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Definir POST /api/v1/consultations e GET /healthz; construir validação Pydantic e schemas do contrato; orquestrar guardrail de entrada, inferência e saída com services; configurar CORS limitado, timeout e erros HTTP apropriados; fornecer request_id e logs mínimos; não acoplar framework ao módulo RAG; utilizar MCP client como única fonte de evidência documental. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testes com TestClient para 200 FOUND/INSUFFICIENT, 4xx BLOCKED/entrada inválida e 5xx/503 de dependência; json snake_case conforme contrato**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 28 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 28: INTEGRAÇÃO BACKEND MCP LLM

**Papel da IA:** Engenheiro de integração de sistemas de IA.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Integrar a aplicação HTTP com execução real do protocolo e modelo.

**Requisitos relacionados:** RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/app/services/query_service.py`; `backend/app/inference/orchestrator.py`; `backend/app/integrations/mcp_client.py`; `backend/tests/test_mcp_integration.py`.

**Instruções detalhadas:**
1. Inicializar cliente MCP stdio de modo seguro, obter catálogo de tools e convertê-lo ao modelo
2. Enviar pergunta validada, processar chamada MCP, buscar documentos e produzir answer/status/sources
3. Fechar recursos e lidar com dependências offline
4. Coletar trace de uma pergunta sobre ingredientes presentes no corpus
5. Corrigir divergências de serialização sem bypass de MCP

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Demonstrar HTTP→Ollama→cliente MCP→servidor→Chroma→Ollama→HTTP com três fontes rastreáveis; simular falhas MCP e Ollama. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro de integração de sistemas de IA** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 28, INTEGRAÇÃO BACKEND MCP LLM**, cujo objetivo é: **Integrar a aplicação HTTP com execução real do protocolo e modelo**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/app/services/query_service.py`; `backend/app/inference/orchestrator.py`; `backend/app/integrations/mcp_client.py`; `backend/tests/test_mcp_integration.py`. Considere o PDF de IA II a referência normativa para RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Inicializar cliente MCP stdio de modo seguro, obter catálogo de tools e convertê-lo ao modelo; enviar pergunta validada, processar chamada MCP, buscar documentos e produzir answer/status/sources; fechar recursos e lidar com dependências offline; coletar trace de uma pergunta sobre ingredientes presentes no corpus; corrigir divergências de serialização sem bypass de MCP. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Demonstrar HTTP→Ollama→cliente MCP→servidor→Chroma→Ollama→HTTP com três fontes rastreáveis; simular falhas MCP e Ollama**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 29 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 29: ESTRUTURA DO FRONTEND

**Papel da IA:** Desenvolvedor frontend React e TypeScript.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Inicializar app React funcional com estrutura de arquivos pactuada.

**Requisitos relacionados:** RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `frontend/package.json`; `frontend/index.html`; `frontend/src/main.tsx`; `frontend/src/App.tsx`; `frontend/src/types/api.ts`; `frontend/src/services/api.ts`.

**Instruções detalhadas:**
1. Configurar Vite, TypeScript estrito e estilos base
2. Criar App e types espelhando contrato HTTP
3. Criar camada de API central com URL base parametrizada e erros tipados
4. Preparar estrutura de components e tests sem funcionalidades falsas
5. Documentar scripts de dev/build/test
6. Evitar biblioteca pesada de gerenciamento de estado

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Npm run build sem erro TS; teste smoke renderiza App e comunicação é isolada em service. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Desenvolvedor frontend React e TypeScript** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 29, ESTRUTURA DO FRONTEND**, cujo objetivo é: **Inicializar app React funcional com estrutura de arquivos pactuada**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `frontend/package.json`; `frontend/index.html`; `frontend/src/main.tsx`; `frontend/src/App.tsx`; `frontend/src/types/api.ts`; `frontend/src/services/api.ts`. Considere o PDF de IA II a referência normativa para RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Configurar Vite, TypeScript estrito e estilos base; criar App e types espelhando contrato HTTP; criar camada de API central com URL base parametrizada e erros tipados; preparar estrutura de components e tests sem funcionalidades falsas; documentar scripts de dev/build/test; evitar biblioteca pesada de gerenciamento de estado. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **npm run build sem erro TS; teste smoke renderiza App e comunicação é isolada em service**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 30 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 30: INTERFACE PRINCIPAL

**Papel da IA:** Designer UX e desenvolvedor React.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Criar tela de consulta culinária responsiva sem distrações.

**Requisitos relacionados:** RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `frontend/src/App.tsx`; `frontend/src/components/QueryForm.tsx`; `frontend/src/styles.css`.

**Instruções detalhadas:**
1. Construir cabeçalho, explicação, campo para ingredientes e pergunta livre, CTA de envio
2. Estados empty/submitting/response
3. Validar front apenas para feedback, mantendo servidor como validador
4. Usar HTML semântico, labels, foco e teclado
5. CSS simples desktop/mobile
6. Separar apresentação e lógica sem animações desnecessárias

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Usuário consegue enviar ingredientes com teclado e mouse; layout responsivo sem cortes; nenhuma chamada HTTP é disparada com campo vazio. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Designer UX e desenvolvedor React** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 30, INTERFACE PRINCIPAL**, cujo objetivo é: **Criar tela de consulta culinária responsiva sem distrações**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `frontend/src/App.tsx`; `frontend/src/components/QueryForm.tsx`; `frontend/src/styles.css`. Considere o PDF de IA II a referência normativa para RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Construir cabeçalho, explicação, campo para ingredientes e pergunta livre, CTA de envio; estados empty/submitting/response; validar front apenas para feedback, mantendo servidor como validador; usar HTML semântico, labels, foco e teclado; CSS simples desktop/mobile; separar apresentação e lógica sem animações desnecessárias. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Usuário consegue enviar ingredientes com teclado e mouse; layout responsivo sem cortes; nenhuma chamada HTTP é disparada com campo vazio**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 31 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 31: EXIBIÇÃO DAS RECEITAS

**Papel da IA:** Designer de dados e desenvolvedor React.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Apresentar recomendações e documentação de forma auditável.

**Requisitos relacionados:** RF03 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `frontend/src/components/RecipeCard.tsx`; `frontend/src/components/SourceList.tsx`; `frontend/src/components/ResultState.tsx`.

**Instruções detalhadas:**
1. Exibir nome, categoria, ingredients disponíveis/faltantes, passos, status COMPLETE/PARTIAL, source_url e document_id
2. Não mostrar informação opcional inexistente
3. Distinguir mensagens sem evidência, bloqueio e erro
4. Renderizar URLs seguras em links externos com rel adequado
5. Mostrar texto livre do modelo como complemento, não verdade canônica

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Teste com payloads de receitas completas e parciais mostra ingrediente ausente; fonte clicável confere com resposta; sem inventar campo ausente. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Designer de dados e desenvolvedor React** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 31, EXIBIÇÃO DAS RECEITAS**, cujo objetivo é: **Apresentar recomendações e documentação de forma auditável**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `frontend/src/components/RecipeCard.tsx`; `frontend/src/components/SourceList.tsx`; `frontend/src/components/ResultState.tsx`. Considere o PDF de IA II a referência normativa para RF03 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Exibir nome, categoria, ingredients disponíveis/faltantes, passos, status COMPLETE/PARTIAL, source_url e document_id; não mostrar informação opcional inexistente; distinguir mensagens sem evidência, bloqueio e erro; renderizar URLs seguras em links externos com rel adequado; mostrar texto livre do modelo como complemento, não verdade canônica. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Teste com payloads de receitas completas e parciais mostra ingrediente ausente; fonte clicável confere com resposta; sem inventar campo ausente**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 32 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 32: INTEGRAÇÃO FRONTEND BACKEND

**Papel da IA:** Engenheiro frontend de integração.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Conectar formulário React à API de consulta.

**Requisitos relacionados:** RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `frontend/src/services/api.ts`; `frontend/src/App.tsx`; `frontend/src/types/api.ts`; `frontend/src/__tests__/App.test.tsx`.

**Instruções detalhadas:**
1. Enviar POST JSON ao endpoint padronizado
2. Analisar status de resposta e erros
3. Cancelar requisições obsoletas com AbortController se necessário
4. Evitar corridas de respostas
5. Preencher cards e fontes somente com payload retornado
6. Configurar Vite dev/proxy ou CORS coerente
7. Registrar URL backend apenas por variável de ambiente pública

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Mock HTTP valida request correto; teste real de navegador exibe respostas e fontes; falha de rede não vira card falso. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro frontend de integração** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 32, INTEGRAÇÃO FRONTEND BACKEND**, cujo objetivo é: **Conectar formulário React à API de consulta**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `frontend/src/services/api.ts`; `frontend/src/App.tsx`; `frontend/src/types/api.ts`; `frontend/src/__tests__/App.test.tsx`. Considere o PDF de IA II a referência normativa para RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Enviar POST JSON ao endpoint padronizado; analisar status de resposta e erros; cancelar requisições obsoletas com AbortController se necessário; evitar corridas de respostas; preencher cards e fontes somente com payload retornado; configurar Vite dev/proxy ou CORS coerente; registrar URL backend apenas por variável de ambiente pública. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Mock HTTP valida request correto; teste real de navegador exibe respostas e fontes; falha de rede não vira card falso**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 33 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 33: TRATAMENTO DE ESTADOS E ERROS

**Papel da IA:** QA UX e desenvolvedor React.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Garantir comportamento previsível em estados de interface.

**Requisitos relacionados:** RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `frontend/src/components/ResultState.tsx`; `frontend/src/App.tsx`; `frontend/src/__tests__/App.test.tsx`.

**Instruções detalhadas:**
1. Cobrir inicial, campo inválido, consulta em andamento, resultado FOUND, INSUFFICIENT, BLOCKED, ERROR, timeout e conexão perdida
2. Mostrar loading acessível e botão desabilitado durante request
3. Preservar pergunta para edição
4. Mapear erro HTTP sem expor stacktrace
5. Validar links/fontes ausentes

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testes componentes para todos estados e tentativa dupla de clique; nenhuma tela trava após erro e usuário pode tentar novamente. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **QA UX e desenvolvedor React** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 33, TRATAMENTO DE ESTADOS E ERROS**, cujo objetivo é: **Garantir comportamento previsível em estados de interface**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `frontend/src/components/ResultState.tsx`; `frontend/src/App.tsx`; `frontend/src/__tests__/App.test.tsx`. Considere o PDF de IA II a referência normativa para RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Cobrir inicial, campo inválido, consulta em andamento, resultado FOUND, INSUFFICIENT, BLOCKED, ERROR, timeout e conexão perdida; mostrar loading acessível e botão desabilitado durante request; preservar pergunta para edição; mapear erro HTTP sem expor stacktrace; validar links/fontes ausentes. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testes componentes para todos estados e tentativa dupla de clique; nenhuma tela trava após erro e usuário pode tentar novamente**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 34 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 34: TESTES UNITÁRIOS

**Papel da IA:** Engenheiro QA de testes unitários.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Adicionar cobertura de regras puras e contratos estáveis.

**Requisitos relacionados:** RF01 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `rag/tests/`; `backend/tests/`; `frontend/src/__tests__/`.

**Instruções detalhadas:**
1. Testar parser e segmentação com snapshots pequenos, normalização de ingrediente, matching COMPLETE/PARTIAL, validação de IDs, guardrails, schemas e UI components
2. Usar fixtures determinísticas e mocks só nas dependências externas
3. Não supor disponibilidade de Ollama para teste unitário
4. Estruturar comandos Pytest/Vitest e relatório

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Testes executados com contagem real, zero falhas não justificadas; casos extremos e regressões registrados no status. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro QA de testes unitários** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 34, TESTES UNITÁRIOS**, cujo objetivo é: **Adicionar cobertura de regras puras e contratos estáveis**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `rag/tests/`; `backend/tests/`; `frontend/src/__tests__/`. Considere o PDF de IA II a referência normativa para RF01 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Testar parser e segmentação com snapshots pequenos, normalização de ingrediente, matching COMPLETE/PARTIAL, validação de IDs, guardrails, schemas e UI components; usar fixtures determinísticas e mocks só nas dependências externas; não supor disponibilidade de Ollama para teste unitário; estruturar comandos Pytest/Vitest e relatório. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Testes executados com contagem real, zero falhas não justificadas; casos extremos e regressões registrados no status**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 35 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 35: TESTES DE INTEGRAÇÃO

**Papel da IA:** Engenheiro QA de sistemas distribuídos.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Verificar fronteiras RAG/Chroma, MCP, backend, LLM e frontend.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `backend/tests/test_mcp_integration.py`; `mcp-server/tests/test_tools.py`; `tests/fixtures/`.

**Instruções detalhadas:**
1. Iniciar Chroma local com corpus de teste e confirmar query
2. Usar cliente MCP real via stdio para listar e executar tools
3. Integrar Ollama quando disponível, registrando skip se não
4. Exercitar contrato HTTP e front
5. Isolar path do índice para não poluir corpus principal
6. Testar servidor indisponível, retorno inválido e timeout

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Registrar comandos, serviços usados, trace MCP e pass/fail; não chamar diretamente função Python em lugar de protocolo. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro QA de sistemas distribuídos** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 35, TESTES DE INTEGRAÇÃO**, cujo objetivo é: **Verificar fronteiras RAG/Chroma, MCP, backend, LLM e frontend**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `backend/tests/test_mcp_integration.py`; `mcp-server/tests/test_tools.py`; `tests/fixtures/`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Iniciar Chroma local com corpus de teste e confirmar query; usar cliente MCP real via stdio para listar e executar tools; integrar Ollama quando disponível, registrando skip se não; exercitar contrato HTTP e front; isolar path do índice para não poluir corpus principal; testar servidor indisponível, retorno inválido e timeout. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Registrar comandos, serviços usados, trace MCP e pass/fail; não chamar diretamente função Python em lugar de protocolo**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 36 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 36: TESTES END TO END

**Papel da IA:** Engenheiro QA E2E e automação.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Executar caminho completo com a UI real e corpus indexado.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `tests/e2e/`; `tests/evidence/`; `docs/09-testing/test-plan.md`.

**Instruções detalhadas:**
1. Preparar serviços, indexar cinco documentos, abrir interface, consultar ingredientes de receita confirmada, validar cards e fonte
2. Repetir com ingrediente ausente e pedido sem evidência
3. Testar prompt injection com status esperado
4. Capturar screenshot e trace por cenário, sem dados fabricados
5. Isolar dependências e registrar hardware/modelo usados

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Obter evidência de consulta válida, consulta sem documentos relevantes e entrada inadequada, com logs de tool calling MCP reais. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro QA E2E e automação** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 36, TESTES END TO END**, cujo objetivo é: **Executar caminho completo com a UI real e corpus indexado**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `tests/e2e/`; `tests/evidence/`; `docs/09-testing/test-plan.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Preparar serviços, indexar cinco documentos, abrir interface, consultar ingredientes de receita confirmada, validar cards e fonte; repetir com ingrediente ausente e pedido sem evidência; testar prompt injection com status esperado; capturar screenshot e trace por cenário, sem dados fabricados; isolar dependências e registrar hardware/modelo usados. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Obter evidência de consulta válida, consulta sem documentos relevantes e entrada inadequada, com logs de tool calling MCP reais**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 37 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 37: REVISÃO TÉCNICA

**Papel da IA:** Revisor de arquitetura e qualidade.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Auditar clareza, dependências e integridade do código construído.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/03-architecture/`; `backend/`; `mcp-server/`; `rag/`; `frontend/`.

**Instruções detalhadas:**
1. Checar import graph, funções pequenas, tipos e contracts
2. Identificar duplicações e fluxo alternativo que burla MCP
3. Revisar env/secrets, tratamento de erro, arquivos não utilizados e versões
4. Conferir documentação contra implementação sem refatorações desnecessárias
5. Registrar problemas, severidade e correções mínimas

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Linter/typecheck/testes e relatório de inconsistências; mudanças devem preservar funcionalidade previamente validada. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Revisor de arquitetura e qualidade** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 37, REVISÃO TÉCNICA**, cujo objetivo é: **Auditar clareza, dependências e integridade do código construído**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/03-architecture/`; `backend/`; `mcp-server/`; `rag/`; `frontend/`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Checar import graph, funções pequenas, tipos e contracts; identificar duplicações e fluxo alternativo que burla MCP; revisar env/secrets, tratamento de erro, arquivos não utilizados e versões; conferir documentação contra implementação sem refatorações desnecessárias; registrar problemas, severidade e correções mínimas. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Linter/typecheck/testes e relatório de inconsistências; mudanças devem preservar funcionalidade previamente validada**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 38 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 38: AUDITORIA DOS REQUISITOS

**Papel da IA:** Auditor de conformidade acadêmica.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Confrontar implementação final com exigências do professor.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/02-requirements/requirements.md`; `docs/12-delivery/delivery.md`; `IMPLEMENTATION_STATUS.md`.

**Instruções detalhadas:**
1. Ler PDF integral e todos RF
2. Verificar 5 documentos com evidências, chunks justificados, embeddings e top-k
3. Examinar três tools por MCP, function calling real, fontes e guardrails
4. Abrir interface e executar três testes obrigatórios
5. Apontar não conformidades com prioridade e instrução de correção
6. Não marcar ok por documentação teórica

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Checklist completo com link para arquivo, comando e captura de evidência; status CONFORME só após teste real. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Auditor de conformidade acadêmica** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 38, AUDITORIA DOS REQUISITOS**, cujo objetivo é: **Confrontar implementação final com exigências do professor**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/02-requirements/requirements.md`; `docs/12-delivery/delivery.md`; `IMPLEMENTATION_STATUS.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Ler PDF integral e todos RF; verificar 5 documentos com evidências, chunks justificados, embeddings e top-k; examinar três tools por MCP, function calling real, fontes e guardrails; abrir interface e executar três testes obrigatórios; apontar não conformidades com prioridade e instrução de correção; não marcar ok por documentação teórica. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Checklist completo com link para arquivo, comando e captura de evidência; status CONFORME só após teste real**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 39 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 39: README PROFISSIONAL

**Papel da IA:** Technical writer e DevEx.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Escrever instruções reproduzíveis para avaliação acadêmica.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `README.md`; `docs/10-development/setup.md`.

**Instruções detalhadas:**
1. Incluir domínio, objetivos, screenshots reais se existentes, stack, estrutura, pré-requisitos, instalação Ubuntu, configuração do modelo/Chroma, ingestão, inicialização servidor MCP/backend/front, endpoint de exemplo, testes e troubleshooting
2. Destacar CC BY-SA e documentação de fontes
3. Não afirmar deploy ou teste não executado

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Um colega reproduz setup apenas lendo README, com comandos verificados; nenhuma credencial hardcoded. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Technical writer e DevEx** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 39, README PROFISSIONAL**, cujo objetivo é: **Escrever instruções reproduzíveis para avaliação acadêmica**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `README.md`; `docs/10-development/setup.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Incluir domínio, objetivos, screenshots reais se existentes, stack, estrutura, pré-requisitos, instalação Ubuntu, configuração do modelo/Chroma, ingestão, inicialização servidor MCP/backend/front, endpoint de exemplo, testes e troubleshooting; destacar CC BY-SA e documentação de fontes; não afirmar deploy ou teste não executado. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Um colega reproduz setup apenas lendo README, com comandos verificados; nenhuma credencial hardcoded**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 40 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 40: DOCUMENTAÇÃO TÉCNICA FINAL

**Papel da IA:** Technical writer e arquiteto de soluções.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Atualizar documentos planejados com detalhes observados no software implementado.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/`; `PROJECT_CONTEXT.md`; `IMPLEMENTATION_STATUS.md`.

**Instruções detalhadas:**
1. Reconciliar paths, versões, endpoints, schema das tools, opções de modelo, diagramas, erros, limites e cobertura
2. Substituir decisões provisórias com ADR motivado
3. Atualizar exemplos JSON com dados reais e remover afirmações não comprovadas
4. Documentar como reinstalar e recuperar Chroma
5. Manter histórico breve de mudanças

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Documentos descrevem mesmos nomes e fluxos do código; links de cada arquivo relevantes e nenhum status falso. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Technical writer e arquiteto de soluções** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 40, DOCUMENTAÇÃO TÉCNICA FINAL**, cujo objetivo é: **Atualizar documentos planejados com detalhes observados no software implementado**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/`; `PROJECT_CONTEXT.md`; `IMPLEMENTATION_STATUS.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Reconciliar paths, versões, endpoints, schema das tools, opções de modelo, diagramas, erros, limites e cobertura; substituir decisões provisórias com ADR motivado; atualizar exemplos JSON com dados reais e remover afirmações não comprovadas; documentar como reinstalar e recuperar Chroma; manter histórico breve de mudanças. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Documentos descrevem mesmos nomes e fluxos do código; links de cada arquivo relevantes e nenhum status falso**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 41 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 41: PREPARAÇÃO DO GITHUB

**Papel da IA:** DevOps e mantenedor do repositório.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Preparar repositório limpo e acessível ao avaliador.

**Requisitos relacionados:** RF01 RF02 RF03 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `.gitignore`; `README.md`; `.env.example`; `docs/12-delivery/delivery.md`.

**Instruções detalhadas:**
1. Verificar Git status, remover arquivos temporários, tokens e bancos pesados
2. Revisar licença e atribuições
3. Conferir branch/tag de entrega, comandos de instalação e artefatos obrigatórios
4. Subir código com frontend, backend, MCP e RAG
5. Se privado, adicionar rwfazul com permissão exigida
6. Não publicar chaves, dados pessoais ou arquivos sem direitos

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Conferir clone limpo, execução básica, GitHub com árvore completa e acesso do avaliador; registrar URL real. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **DevOps e mantenedor do repositório** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 41, PREPARAÇÃO DO GITHUB**, cujo objetivo é: **Preparar repositório limpo e acessível ao avaliador**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `.gitignore`; `README.md`; `.env.example`; `docs/12-delivery/delivery.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Verificar Git status, remover arquivos temporários, tokens e bancos pesados; revisar licença e atribuições; conferir branch/tag de entrega, comandos de instalação e artefatos obrigatórios; subir código com frontend, backend, MCP e RAG; se privado, adicionar rwfazul com permissão exigida; não publicar chaves, dados pessoais ou arquivos sem direitos. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Conferir clone limpo, execução básica, GitHub com árvore completa e acesso do avaliador; registrar URL real**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 42 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 42: EVIDÊNCIAS DE FUNCIONAMENTO

**Papel da IA:** Engenheiro QA e documentação acadêmica.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Coletar provas verificáveis do funcionamento de cada requisito.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `tests/evidence/`; `docs/12-delivery/delivery.md`; `IMPLEMENTATION_STATUS.md`.

**Instruções detalhadas:**
1. Capturar ingestão dos cinco documentos e hashes, total de chunks e vetores
2. Salvar print/trace list_tools, call_tool das três ferramentas e function calling
3. Registrar resposta válida com fonte, consulta sem informação e tentativa bloqueada
4. Registrar comandos e versão de serviços sem expor credenciais
5. Produzir índice de evidências

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Todo RF tem pelo menos uma evidência que o avaliador possa localizar e executar; não fabricar imagens ou logs. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Engenheiro QA e documentação acadêmica** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 42, EVIDÊNCIAS DE FUNCIONAMENTO**, cujo objetivo é: **Coletar provas verificáveis do funcionamento de cada requisito**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `tests/evidence/`; `docs/12-delivery/delivery.md`; `IMPLEMENTATION_STATUS.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Capturar ingestão dos cinco documentos e hashes, total de chunks e vetores; salvar print/trace list_tools, call_tool das três ferramentas e function calling; registrar resposta válida com fonte, consulta sem informação e tentativa bloqueada; registrar comandos e versão de serviços sem expor credenciais; produzir índice de evidências. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Todo RF tem pelo menos uma evidência que o avaliador possa localizar e executar; não fabricar imagens ou logs**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 43 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 43: ROTEIRO DE DEMONSTRAÇÃO

**Papel da IA:** Especialista em apresentação técnica.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Preparar apresentação curta, técnica e executável.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/12-delivery/demonstration.md`; `tests/evidence/`.

**Instruções detalhadas:**
1. Ordenar demonstração: problema e cinco documentos, pipeline, embeddings, Chroma, ferramentas MCP reais, trace LLM, interface, consulta válida, ausência de dados e injection
2. Explicar origem dos ingredientes faltantes e limites do modelo
3. Definir comandos e estado inicial para replicar
4. Fornecer plano B em caso de Ollama indisponível sem fingir funcionamento

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Roteiro demonstra cada RF no tempo definido e aponta evidências correspondentes; linguagem adequada à banca. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Especialista em apresentação técnica** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 43, ROTEIRO DE DEMONSTRAÇÃO**, cujo objetivo é: **Preparar apresentação curta, técnica e executável**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/12-delivery/demonstration.md`; `tests/evidence/`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Ordenar demonstração: problema e cinco documentos, pipeline, embeddings, Chroma, ferramentas MCP reais, trace LLM, interface, consulta válida, ausência de dados e injection; explicar origem dos ingredientes faltantes e limites do modelo; definir comandos e estado inicial para replicar; fornecer plano B em caso de Ollama indisponível sem fingir funcionamento. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Roteiro demonstra cada RF no tempo definido e aponta evidências correspondentes; linguagem adequada à banca**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 44 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 44: PERGUNTAS DO PROFESSOR

**Papel da IA:** Professor orientador técnico e arquiteto.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Preparar respostas fundamentadas a questionamentos sobre tecnologias e decisões.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `docs/12-delivery/defense-qa.md`; `PROJECT_CONTEXT.md`.

**Instruções detalhadas:**
1. Criar Q&A sobre RAG versus MCP, embeddings, chunk_size/overlap, top-k, Chroma, evidências, cliente-servidor MCP, tool calling, guardrails, falsos positivos, casamento de ingredientes, licenças e limitações
2. Usar nomes do código real
3. Incluir armadilhas como similaridade≠disponibilidade, ausência de fontes e interface não comprova backend

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Cada resposta aponta arquivo ou log comprobatório; não alegar métrica, teste ou desempenho inexistente. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Professor orientador técnico e arquiteto** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 44, PERGUNTAS DO PROFESSOR**, cujo objetivo é: **Preparar respostas fundamentadas a questionamentos sobre tecnologias e decisões**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `docs/12-delivery/defense-qa.md`; `PROJECT_CONTEXT.md`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Criar Q&A sobre RAG versus MCP, embeddings, chunk_size/overlap, top-k, Chroma, evidências, cliente-servidor MCP, tool calling, guardrails, falsos positivos, casamento de ingredientes, licenças e limitações; usar nomes do código real; incluir armadilhas como similaridade≠disponibilidade, ausência de fontes e interface não comprova backend. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Cada resposta aponta arquivo ou log comprobatório; não alegar métrica, teste ou desempenho inexistente**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 45 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


---

# PROMPT 45: VERIFICAÇÃO FINAL DE ENTREGA

**Papel da IA:** Auditor de liberação acadêmica.

**Contexto:** O projeto é o Assistente Inteligente de Receitas (ChefAI, nome provisório), atividade de Inteligência Artificial II. O fluxo obrigatório combina **frontend React/TypeScript/Vite**, **backend Python/FastAPI**, **cliente MCP real via SDK oficial Python e transporte stdio**, **servidor MCP Python separado**, **RAG com ChromaDB persistente**, **embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384 dimensões)**, **Ollama qwen3:4b ou alternativa registrada em ADR se incompatível**, e guardrails. O corpus inicial vem de cinco documentos culinários reais, cada um com licença, fonte e versão. A fonte normativa é o PDF do professor. Os contratos estão em `docs/08-application/contracts.md`, a árvore em `docs/03-architecture/project-structure.md`, as decisões em `docs/03-architecture/adrs.md`. O código do sistema ainda não deve ser presumido pronto.

**Objetivo:** Executar checklist de aceite e congelar pacote de entrega.

**Requisitos relacionados:** RF01 RF02 RF03 RF04 RF05 do enunciado da IA II.

**Tecnologias:** seguir estritamente React/TypeScript/Vite, Python/FastAPI, MCP Python via stdio, ChromaDB, Sentence Transformers e Ollama quando pertinentes à etapa. As bibliotecas e suas versões devem ser instaladas e testadas antes de usar APIs novas. Não usar frameworks ou infraestrutura além do MVP sem justificativa.

**Arquitetura:** manter ingestão RAG offline separada; servidor MCP expõe tools; cliente MCP no backend descobre e chama ferramentas; LLM realiza function calling; guardrails são responsabilidade da aplicação; frontend apenas consome HTTP. Não introduzir dependências circulares.

**Arquivos envolvidos:** `README.md`; `IMPLEMENTATION_STATUS.md`; `docs/12-delivery/delivery.md`; `tests/evidence/`.

**Instruções detalhadas:**
1. Reclonar repo para diretório novo
2. Seguir README, rodar testes e ingestão, levantar Ollama/MCP/backend/frontend
3. Executar consulta positiva, sem evidência e entrada adversarial
4. Conferir links, fontes, três tools tipadas, metadados, prompts, README, licença e acesso rwfazul se privado
5. Listar pendências bloqueantes e não bloqueantes

**Regras de implementação:** apresentar antes uma leitura dos contratos, arquivos existentes e estado atual; gerar arquivos completos, coerentes com a árvore documentada; nunca sobrescrever módulos funcionando sem diff/justificativa; validar tipos, IDs e erros; atualizar documentação da decisão quando necessário. Se esta etapa for de planejamento ou auditoria, gerar documentação e testes propostos em vez de criar serviços artificiais. Evitar alterar qualquer outra etapa não relacionada.

**Critérios de aceitação:** Registrar data e versão commit da avaliação, pass/fail com capturas, e não marcar aprovado se existir RF obrigatório sem evidência. A implementação só será considerada concluída quando seus caminhos centrais puderem ser testados e os requisitos associados tiverem evidência objetiva.

**Testes obrigatórios:** Ao encerrar, mostre os comandos reais executados, a saída resumida, os casos que passaram/falharam e quaisquer dependências que impediram execução. Distinguir claramente **planejado**, **implementado** e **testado**. Não tratar mock como evidência de MCP real. Reexecutar testes já existentes relevantes e preservar comportamento das etapas anteriores.

**Entregáveis:** código e documentação efetivamente relacionados aos arquivos listados, exemplos de entrada/saída quando pertinentes, comandos de execução/testes, resultados reais, lista de mudanças, riscos/pendências e atualização de `IMPLEMENTATION_STATUS.md`.

**Restrições incontornáveis:** não adicionar autenticação, pagamentos, histórico persistente, painel administrativo, microserviços, múltiplos bancos ou abstrações decorativas. Não inventar fontes, arquivos já existentes, métodos de biblioteca, benchmarks, logs ou testes. Não alterar a stack aprovada sem registrar ADR e atualizar os contratos. O backend não pode substituir MCP por uma chamada local direta a `rag/retrieve.py` para atender a integração de inferência. O servidor MCP pode importar a implementação RAG, mas o backend a acessa através do protocolo. Chaves e paths sensíveis ficam em ambiente; nunca em repositório. Toda resposta factual sobre receitas precisa indicar evidência documental real; se faltar, retornar `INSUFFICIENT`. Compatibilidade de ingredientes deve ser programática e distinta do score vetorial. Sempre que a etapa exigir API de biblioteca sujeita a mudanças, verificar documentação e versão efetivamente instaladas antes de escrever código.

## Prompt completo para copiar em outra conversa

Você atuará como **Auditor de liberação acadêmica** no projeto Assistente Inteligente de Receitas. Execute exclusivamente a **etapa 45, VERIFICAÇÃO FINAL DE ENTREGA**, cujo objetivo é: **Executar checklist de aceite e congelar pacote de entrega**. Antes de qualquer alteração, solicite ou leia os seguintes arquivos quando não estiverem disponíveis: `PROJECT_CONTEXT.md`, `IMPLEMENTATION_STATUS.md`, `docs/03-architecture/architecture.md`, `docs/03-architecture/project-structure.md`, `docs/08-application/contracts.md` e os arquivos específicos desta etapa: `README.md`; `IMPLEMENTATION_STATUS.md`; `docs/12-delivery/delivery.md`; `tests/evidence/`. Considere o PDF de IA II a referência normativa para RF01 RF02 RF03 RF04 RF05. Mantenha a stack React/TypeScript/Vite + Python/FastAPI + MCP Python real em stdio + ChromaDB + embeddings multilíngues 384d + Ollama com tool calling; não presuma integrações implementadas. Execute, nesta ordem, as atividades: Reclonar repo para diretório novo; seguir README, rodar testes e ingestão, levantar Ollama/MCP/backend/frontend; executar consulta positiva, sem evidência e entrada adversarial; conferir links, fontes, três tools tipadas, metadados, prompts, README, licença e acesso rwfazul se privado; listar pendências bloqueantes e não bloqueantes. Mantenha RAG e MCP separados, sem bypass do protocolo; preserve a origem das receitas e distinga evidência da inferência. Para validar, cumpra: **Registrar data e versão commit da avaliação, pass/fail com capturas, e não marcar aprovado se existir RF obrigatório sem evidência**. Entregue arquivos completos e coerentes, não apenas trechos soltos; execute testes quando houver ambiente; indique explicitamente qualquer teste não executado; documente limitações, comandos, arquivos e resultados; atualize `IMPLEMENTATION_STATUS.md`; explique a próxima etapa, que deve ser o PROMPT 46 quando aplicável. Não crie funcionalidades fora dos RF nem afirme sucesso sem evidência.


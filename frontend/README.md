# Preditor do Brasileirão (front-end)

Interface em React 19, Vite e TypeScript que consome a API do projeto (`../src/api.py`). **Não há dados simulados:** se a API estiver fora do ar ou sem modelo, a interface mostra o erro devolvido.

## Como executar

```bash
npm install
npm run dev        # http://localhost:5173 (a API deve estar em http://localhost:8000/api)
```

Para outra URL da API: `cp .env.example .env` e edite `VITE_API_URL`. A API precisa liberar a origem do front-end em `CORS_ORIGINS` (padrão: `http://localhost:5173` e `http://127.0.0.1:5173`).

## Scripts

- `npm run dev`: servidor de desenvolvimento.
- `npm run build`: verifica os tipos e gera `dist/`.
- `npm run preview`: serve a build.
- `npm run lint`: Oxlint.
- `npm run typecheck`: `tsc -b`.
- `npm test`: Vitest (28 testes de serviço, páginas e componentes; as respostas da API são simuladas apenas nos testes).

## Páginas

- **Início:** indicadores da base e desempenho do modelo lidos de `/api/health` e `/api/model`.
- **Previsão:** equipes de `/api/teams` (equipes sem histórico recente ficam desabilitadas), data de referência opcional, probabilidades, forma recente, confronto direto e fatores de `POST /api/predict`.
- **Estatísticas:** filtros de temporada, equipe e mando; indicadores, gráficos e tabela paginada de `/api/stats/*` e `/api/matches`.
- **Sobre o modelo:** algoritmo, versão, divisão temporal, métricas, matriz de confusão e limitações de `/api/model`.

# Preditor do Brasileirão

Front-end em React, Vite e TypeScript para consultar previsões de partidas do Brasileirão Série A com base no dataset de 2020 a 2023.

## Como executar

```bash
npm install
npm run dev
```

Por padrão, o front-end procura a API em `http://localhost:8000/api`. Para alterar:

```bash
cp .env.example .env
```

Edite `VITE_API_URL` no arquivo `.env`.

## Scripts

- `npm run dev`: inicia o servidor local do Vite.
- `npm run build`: valida TypeScript e gera a versão de produção.
- `npm run preview`: abre a build de produção localmente.
- `npm run lint`: executa Oxlint.

## Endpoints esperados

- `GET /api/health`
- `GET /api/teams`
- `POST /api/predict`
- `GET /api/stats/overview`
- `GET /api/matches`

Enquanto a API não estiver disponível, a interface usa dados simulados e sinaliza isso em tela. Esse fallback serve apenas para demonstração do front-end.

## Telas implementadas

- Início
- Previsão
- Estatísticas
- Sobre o modelo

## Observações

- A lista de equipes é carregada pela API quando disponível.
- O formulário impede mandante e visitante iguais.
- A previsão exibe probabilidades, resultado mais provável, confiança, indicadores históricos e fatores relevantes.
- A página de estatísticas possui filtros, indicadores, gráficos e tabela paginada.
- A página Sobre reserva espaço para métricas reais e matriz de confusão após o treinamento final.

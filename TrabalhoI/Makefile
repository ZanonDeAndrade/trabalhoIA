# Atalhos do projeto (Linux/macOS). No Windows, use os comandos equivalentes do README.
PY ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: help setup data train test test-py test-front lint front-build api front run screenshots report all clean

help:
	@echo "make setup       cria .venv e instala dependências (Python e front-end)"
	@echo "make data        processa o CSV, gera a EDA e as figuras 01-13"
	@echo "make train       treina, avalia, salva models/ e gera figuras 14-20"
	@echo "make test        testes Python (pytest) e do front-end (vitest)"
	@echo "make lint        ruff, oxlint e verificação de tipos TypeScript"
	@echo "make api         inicia a API em http://127.0.0.1:8000/api"
	@echo "make front       inicia o front-end em http://localhost:5173"
	@echo "make run         inicia API e front-end juntos"
	@echo "make screenshots capturas reais (API e front-end precisam estar rodando)"
	@echo "make report      gera reports/relatorio_tecnico.pdf"
	@echo "make all         data + train + test"

setup:
	python3 -m venv .venv
	$(PIP) install -r requirements-dev.txt -r reports/requirements_documentacao.txt
	cd frontend && npm install

data:
	$(PY) src/data_analysis.py

train:
	$(PY) src/modeling.py

test: test-py test-front

test-py:
	$(PY) -m pytest tests -q

test-front:
	cd frontend && npm test

lint:
	$(PY) -m ruff check .
	cd frontend && npm run lint && npm run typecheck

front-build:
	cd frontend && npm run build

api:
	$(PY) src/api.py

front:
	cd frontend && npm run dev

run:
	$(PY) src/api.py & API=$$!; trap "kill $$API" EXIT INT TERM; cd frontend && npm run dev

screenshots:
	$(PY) scripts/capturar_screenshots.py --front http://127.0.0.1:5173

report:
	$(PY) scripts/gerar_relatorio_tecnico.py

all: data train test

clean:
	rm -rf .pytest_cache .ruff_cache reports/.cache_relatorio frontend/dist

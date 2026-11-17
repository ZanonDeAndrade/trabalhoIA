# Ações manuais (exigem uma pessoa)

Somente tarefas que não podem ser feitas por código dentro do repositório.

- [ ] **Validar o dataset com o professor** (`partidas_20_23.csv`): a atividade exige aprovação prévia. Registrar a origem (Opta Player Stats / Stats Perform, conforme os links) e confirmar as condições de uso/licença, que não estão documentadas.
- [ ] **Conferir os nomes dos integrantes** na capa do relatório e no README (Marcelo da Costa Telles, Arthur Zanon, Milton Roberto).
- [ ] **Revisar e commitar as alterações**: nada foi commitado nem enviado. Sugestão: `git status`, revisar o diff e fazer commits separados por área (dados/modelo, API, front-end, relatório).
- [ ] **Confirmar os commits de cada integrante** no histórico do repositório (o enunciado pede contribuição individual rastreável).
- [ ] **Reiniciar a API que ficou rodando na porta 8000** (processo antigo, antes das correções): `Ctrl+C` e `python src/api.py`; reiniciar também o `npm run dev` se necessário.
- [ ] **Compartilhar o repositório privado com `rwfazul`** (GitHub > Settings > Collaborators).
- [ ] **Postar o link do repositório no Google Classroom** conforme o enunciado.
- [ ] **Revisar o texto final do relatório** (`reports/relatorio_tecnico.pdf`) e, se desejar, ajustar redação; para regerar: `python scripts/gerar_relatorio_tecnico.py`.
- [ ] **(Opcional) Gravar um vídeo de tela** da aplicação: `python src/api.py`, `cd frontend && npm run dev`, abrir http://localhost:5173 e percorrer Início → Previsão → Estatísticas → Sobre o modelo.
- [ ] **Preparar a apresentação oral**: roteiro sugerido — problema; dataset e cuidados contra vazamento; divisão temporal; comparação de modelos; resultados e limitações (o modelo não supera as referências em acurácia/Log-Loss); demonstração da aplicação.

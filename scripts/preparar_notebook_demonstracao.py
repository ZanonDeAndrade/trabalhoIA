"""Cria o notebook da demonstração. Não executa nem fabrica saídas de células."""
from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]
nb=nbf.v4.new_notebook()
nb.metadata.kernelspec={'display_name':'Python 3 (ipykernel)','language':'python','name':'python3'}
nb.cells=[
nbf.v4.new_markdown_cell('''# Demonstração de funcionamento\n## Previsão do resultado de partidas do Brasileirão\n**Inteligência Artificial II · AMF · 2026/02**\n\nExecute as células em ordem. O treinamento utiliza 2020–2021, a seleção utiliza 2022 e o teste utiliza 2023. Esta é uma **avaliação retrospectiva**, com informações disponíveis antes de cada partida. O placar real é exibido somente para conferir a previsão.'''),
nbf.v4.new_code_cell('''from pathlib import Path
import sys
raiz = Path.cwd() if (Path.cwd() / "src").exists() else Path.cwd().parent
sys.path.insert(0, str(raiz))
from src.documentation_evidence import executar_evidencias
dados = executar_evidencias()'''),
nbf.v4.new_markdown_cell('''## 1. Resultados da execução\nA comparação probabilística usa também as frequências de classes aprendidas no treinamento. Nenhum desses referenciais usa os resultados de 2023 para ajustar seus parâmetros.'''),
nbf.v4.new_code_cell('''import pandas as pd
from IPython.display import display, HTML
display(HTML("<style>.dataframe{font-size:16px!important}.dataframe th,.dataframe td{padding:10px 12px!important}</style>"))
linhas = []
for nome, r in [("Regressão logística", dados["teste"]),
                ("Sempre mandante", dados["baselines_teste"]["majoritaria"]),
                ("Frequências históricas", dados["baselines_teste"]["frequencias"])]:
    linhas.append({"Modelo":nome,"Acurácia":f'{r["acuracia"]:.2%}',
                   "Macro F1":f'{r["f1_macro"]:.3f}',"Log-Loss":f'{r["log_loss_val"]:.3f}',
                   "Brier":f'{r["brier_score"]:.3f}'})
display(pd.DataFrame(linhas).style.hide(axis="index"))
print("Execução:", dados["executado_em"])
print("Amostra de teste: 362 partidas; retreino final: 1.052 partidas.")'''),
nbf.v4.new_markdown_cell('''## 2. Previsões geradas pelo modelo\nOito primeiras partidas elegíveis do teste, em ordem cronológica; os exemplos não foram escolhidos pelo acerto. As probabilidades somam 100% antes do arredondamento.'''),
nbf.v4.new_code_cell('''from src.data_analysis import NOME_CURTO
amostra = []
for e in dados["exemplos"]:
    amostra.append({"Confronto":NOME_CURTO.get(e["mandante"],e["mandante"]) + " × " + NOME_CURTO.get(e["visitante"],e["visitante"]),
                    "P(casa)":f'{e["p_mandante"]:.1%}',"P(empate)":f'{e["p_empate"]:.1%}',
                    "P(fora)":f'{e["p_visitante"]:.1%}',"Previsão":e["previsto"],
                    "Real":e["real"],"Placar":e["placar"],"Acerto":"Sim" if e["acertou"] else "Não"})
display(pd.DataFrame(amostra).style.hide(axis="index"))
print("Partidas disputadas entre", dados["exemplos"][0]["data"][:10], "e", dados["exemplos"][-1]["data"][:10])'''),
nbf.v4.new_markdown_cell('''## 3. Leitura crítica\nO modelo melhora o Macro F1 em relação à classe majoritária, mas acerta menos partidas no total. A referência de frequências históricas tem Log-Loss e Brier menores. As evidências comprovam a execução e permitem inspecionar acertos e erros; não demonstram superioridade geral do modelo.\n\nArquivos gerados: `reports/evidencias/metricas_execucao.json` e `reports/evidencias/previsoes_exemplo.json`.''')]
destino=ROOT/'notebooks/03_demonstracao_funcionamento.ipynb'
nbf.write(nb,destino)
print(destino)

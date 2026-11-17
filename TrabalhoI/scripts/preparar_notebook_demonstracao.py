"""Cria o notebook 03 (demonstração) e atualiza as células do notebook 02 que citavam números fixos.

Este script NÃO executa nem fabrica saídas de células. Depois de rodá-lo, execute os notebooks:

    python scripts/preparar_notebook_demonstracao.py
    python -m jupyter nbconvert --to notebook --execute --inplace notebooks/02_modelagem_classificacao.ipynb
    python -m jupyter nbconvert --to notebook --execute --inplace notebooks/03_demonstracao_funcionamento.ipynb
"""
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell


def notebook_demonstracao() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata.kernelspec = {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"}
    nb.cells = [
        md("""# Demonstração de funcionamento
## Previsão do resultado de partidas do Brasileirão

**Inteligência Artificial II · AMF · 2026/02**

Execute as células em ordem (*Kernel > Restart & Run All*). O treinamento usa as temporadas 2020–2021, a seleção usa 2022 e o teste usa 2023.
Esta é uma **avaliação retrospectiva**, com informações disponíveis antes de cada partida; o placar real só aparece para conferir a previsão.
Todos os números abaixo são calculados nesta execução."""),
        code("""from pathlib import Path
import sys
raiz = Path.cwd() if (Path.cwd() / "src").exists() else Path.cwd().parent
sys.path.insert(0, str(raiz))
from src.documentation_evidence import executar_evidencias
dados = executar_evidencias()"""),
        md("""## 1. Comparação dos algoritmos na validação (2022)
Cada modelo foi ajustado em 2020–2021. A seleção usa o maior Macro F1 (a referência majoritária não participa da escolha)."""),
        code("""import pandas as pd
from IPython.display import display, HTML, Markdown
display(HTML("<style>.dataframe{font-size:15px!important}.dataframe th,.dataframe td{padding:8px 10px!important}</style>"))

def pct(v): return f"{v:.2%}"
def num(v): return "—" if v is None else f"{v:.3f}"

linhas = []
for nome, m in dados["modelos"].items():
    tr, va = m["treino"], m["validacao"]
    linhas.append({"Modelo": nome, "Acurácia treino": pct(tr["acuracia"]), "Acurácia validação": pct(va["acuracia"]),
                   "Precisão macro": num(va["precisao_macro"]), "Recall macro": num(va["recall_macro"]),
                   "Macro F1": num(va["f1_macro"]), "Log-Loss": num(va["log_loss"]), "Tempo de ajuste (s)": f'{m["tempo_treino_s"]:.2f}'})
display(pd.DataFrame(linhas).style.hide(axis="index"))
print("Modelo selecionado:", dados["modelo_selecionado"], "| critério:", dados["criterio_selecao"])"""),
        md("""## 2. Avaliação final no teste (2023)
O modelo selecionado foi reajustado com 2020–2022 e avaliado uma única vez em 2023. A referência de frequências históricas usa as proporções de classes do mesmo período de treino."""),
        code("""teste = dados["final"]["teste"]
linhas = []
for nome, r in [(dados["modelo_selecionado"], teste), ("Sempre mandante", dados["baselines_teste"]["majoritaria"]),
                ("Frequências históricas", dados["baselines_teste"]["frequencias"])]:
    linhas.append({"Modelo": nome, "Acurácia": pct(r["acuracia"]), "Acurácia balanceada": pct(r["acuracia_balanceada"]),
                   "Precisão macro": num(r["precisao_macro"]), "Recall macro": num(r["recall_macro"]),
                   "Macro F1": num(r["f1_macro"]), "Log-Loss": num(r["log_loss"]) if nome != "Sempre mandante" else "n/a",
                   "Brier": num(r["brier"]) if nome != "Sempre mandante" else "n/a", "AUC (OvR)": num(r["roc_auc_ovr_macro"])})
display(pd.DataFrame(linhas).style.hide(axis="index"))
print("Execução:", dados["executado_em"], "| partidas de teste:", teste["n"], "| retreino final:", dados["particoes"]["treino_final"]["n"], "partidas")"""),
        code("""rot = {"home_win": "Vitória do mandante", "draw": "Empate", "away_win": "Vitória do visitante"}
por_classe = pd.DataFrame([{"Classe": rot[c], "Precisão": num(v["precisao"]), "Recall": num(v["recall"]), "F1": num(v["f1"]), "Suporte": v["suporte"],
                            "Previsões do modelo": teste["distribuicao_previsoes"][c]} for c, v in teste["por_classe"].items()])
display(por_classe.style.hide(axis="index"))
matriz = pd.DataFrame(teste["matriz_confusao"], index=[f"Real: {rot[c]}" for c in rot], columns=[f"Previsto: {rot[c]}" for c in rot])
display(matriz)"""),
        md("""## 3. Treino × validação × teste (sobreajuste)"""),
        code("""nome = dados["modelo_selecionado"]
final = dados["final"]
comparacao = pd.DataFrame([
    {"Partição": "Treino (2020–2021)", "Acurácia": pct(dados["modelos"][nome]["treino"]["acuracia"]), "Macro F1": num(dados["modelos"][nome]["treino"]["f1_macro"])},
    {"Partição": "Validação (2022)", "Acurácia": pct(dados["modelos"][nome]["validacao"]["acuracia"]), "Macro F1": num(dados["modelos"][nome]["validacao"]["f1_macro"])},
    {"Partição": "Treino final (2020–2022)", "Acurácia": pct(final["treino_final"]["acuracia"]), "Macro F1": num(final["treino_final"]["f1_macro"])},
    {"Partição": "Teste (2023)", "Acurácia": pct(teste["acuracia"]), "Macro F1": num(teste["f1_macro"])},
])
display(comparacao.style.hide(axis="index"))"""),
        md("""## 4. Previsões geradas pelo modelo
Oito primeiras partidas elegíveis do teste, em ordem cronológica (não escolhidas pelo acerto). As probabilidades somam 100% antes do arredondamento."""),
        code("""from src.data_analysis import NOME_CURTO
amostra = []
for e in dados["exemplos"]:
    amostra.append({"Confronto": NOME_CURTO.get(e["mandante"], e["mandante"]) + " × " + NOME_CURTO.get(e["visitante"], e["visitante"]),
                    "P(mandante)": f'{e["p_mandante"]:.1%}', "P(empate)": f'{e["p_empate"]:.1%}', "P(visitante)": f'{e["p_visitante"]:.1%}',
                    "Previsão": e["previsto"], "Real": e["real"], "Placar": e["placar"], "Acerto": "Sim" if e["acertou"] else "Não"})
display(pd.DataFrame(amostra).style.hide(axis="index"))
print("Partidas disputadas entre", dados["exemplos"][0]["data"][:10], "e", dados["exemplos"][-1]["data"][:10])"""),
        md("""## 5. Interpretação e erros (descritivos, não causais)"""),
        code("""imp = pd.DataFrame(dados["importancia_permutacao"][:8])[["rotulo", "aumento_log_loss", "desvio_padrao"]]
imp.columns = ["Atributo embaralhado", "Aumento do log-loss", "Desvio padrão (30 repetições)"]
display(imp.style.hide(axis="index").format({"Aumento do log-loss": "{:.4f}", "Desvio padrão (30 repetições)": "{:.4f}"}))

erros = dados["analise_erros"]
tabela = pd.DataFrame([{"Data": e["data"], "Confronto": f'{e["mandante"]} × {e["visitante"]}', "Placar": e["placar"],
                        "Previsto": rot[e["previsto"]], "Real": rot[e["real"]], "Confiança": f'{e["confianca"]:.1%}'} for e in erros["erros_mais_confiantes"]])
display(Markdown("**Erros em que o modelo estava mais confiante:**"))
display(tabela.style.hide(axis="index"))"""),
        md("""## 6. Usando o modelo salvo (`models/model.joblib`)
O mesmo artefato é usado pela API. O confronto abaixo é hipotético: usa o histórico até o último jogo da base."""),
        code("""import json
from src.common import CatalogoEquipes, carregar_partidas
from src.predictor import ServicoPrevisao

partidas = carregar_partidas()
servico = ServicoPrevisao(partidas, CatalogoEquipes(partidas))
resposta = servico.prever("flamengo", "palmeiras")
print("Modelo carregado:", resposta["model"])
print("Referência:", resposta["reference"])
print("Probabilidades:", resposta["probabilities"], "->", resposta["label"])
print("Forma recente (mandante):", resposta["home_team_form"]["last_five"], "| (visitante):", resposta["away_team_form"]["last_five"])"""),
        code("""fmt = lambda v: f"{v:.2%}".replace(".", ",")
display(Markdown(f'''## 7. Leitura crítica

* **Desempenho geral:** {dados["modelo_selecionado"]} obteve acurácia de {fmt(teste["acuracia"])} e Macro F1 de {teste["f1_macro"]:.3f} no teste; a referência que sempre prevê o mandante obteve {fmt(dados["baselines_teste"]["majoritaria"]["acuracia"])} e {dados["baselines_teste"]["majoritaria"]["f1_macro"]:.3f}.
* **Classes difíceis:** o recall foi de {fmt(teste["por_classe"]["draw"]["recall"])} para empates e {fmt(teste["por_classe"]["away_win"]["recall"])} para vitórias do visitante; o modelo previu empate em apenas {teste["distribuicao_previsoes"]["draw"]} de {teste["n"]} partidas (a maior probabilidade de empate atribuída foi {erros["maior_probabilidade_de_empate"]:.1%}).
* **Probabilidades:** o Log-Loss do modelo foi {teste["log_loss"]:.3f}, contra {dados["baselines_teste"]["frequencias"]["log_loss"]:.3f} da referência de frequências históricas; o modelo não é melhor em qualidade probabilística.
* **Generalização:** acurácia de {fmt(final["treino_final"]["acuracia"])} no treino final contra {fmt(teste["acuracia"])} no teste indica sobreajuste moderado.
* **Limites:** as evidências mostram que o pipeline funciona e permitem inspecionar acertos e erros; não demonstram superioridade geral do modelo.

Arquivos gerados: `models/model.joblib`, `models/metadata.json`, `reports/evidencias/metricas_execucao.json` e `reports/evidencias/previsoes_exemplo.json`.'''))"""),
    ]
    return nb


def atualizar_notebook_modelagem() -> None:
    """Troca valores digitados à mão do notebook 02 por células calculadas na execução."""
    caminho = ROOT / "notebooks/02_modelagem_classificacao.ipynb"
    nb = nbf.read(caminho, as_version=4)
    for i, celula in enumerate(nb.cells):
        fonte = celula.source
        if celula.cell_type == "code" and "plotar_importancia_features" in fonte:
            celula.source = fonte.replace("    plotar_importancia_features,\n", "")
        if celula.cell_type == "markdown" and fonte.startswith("## 6. Retreino Expandido"):
            celula.source = (
                "## 6. Retreino Expandido e Avaliação Final no Teste (Temporada 2023)\n\n"
                "O modelo com maior Macro F1 na validação é retreinado com **todo o histórico disponível** até o final de 2022 "
                "(temporadas 2020 a 2022) e avaliado de forma cega nas partidas da temporada de 2023."
            )
        if celula.cell_type == "code" and fonte.startswith("# Retreino do modelo campeão"):
            celula.source = '''# Seleciona pelo Macro F1 da validação (a baseline não concorre) e retreina em 2020-2022
validacao = {r["Modelo"]: float(r["Macro F1"]) for r in resultados_val if "Baseline" not in r["Modelo"]}
nome_melhor = max(validacao, key=validacao.get)
print("Modelo selecionado pela validação:", nome_melhor)
melhor_modelo = modelos[nome_melhor]
melhor_modelo.fit(particoes.X_train_val, particoes.y_train_val)

dummy = modelos["Baseline (Majoritária)"]
dummy.fit(particoes.X_train_val, particoes.y_train_val)

res_teste = avaliar_modelo(melhor_modelo, particoes.X_test, particoes.y_test, nome_melhor, "Teste (2023)")
res_dummy_teste = avaliar_modelo(dummy, particoes.X_test, particoes.y_test, "Baseline", "Teste (2023)")

tabela_final = pd.DataFrame([
    {"Métrica": "Acurácia Global", "Baseline Majoritária": f"{res_dummy_teste.acuracia*100:.2f}%", nome_melhor: f"{res_teste.acuracia*100:.2f}%",
     "Diferença": f"{(res_teste.acuracia - res_dummy_teste.acuracia)*100:+.2f} p.p."},
    {"Métrica": "Acurácia Balanceada", "Baseline Majoritária": f"{res_dummy_teste.acuracia_balanceada*100:.2f}%", nome_melhor: f"{res_teste.acuracia_balanceada*100:.2f}%",
     "Diferença": f"{(res_teste.acuracia_balanceada - res_dummy_teste.acuracia_balanceada)*100:+.2f} p.p."},
    {"Métrica": "Precisão macro", "Baseline Majoritária": f"{res_dummy_teste.precisao_macro:.3f}", nome_melhor: f"{res_teste.precisao_macro:.3f}",
     "Diferença": f"{res_teste.precisao_macro - res_dummy_teste.precisao_macro:+.3f}"},
    {"Métrica": "Recall macro", "Baseline Majoritária": f"{res_dummy_teste.recall_macro:.3f}", nome_melhor: f"{res_teste.recall_macro:.3f}",
     "Diferença": f"{res_teste.recall_macro - res_dummy_teste.recall_macro:+.3f}"},
    {"Métrica": "Macro F1-Score", "Baseline Majoritária": f"{res_dummy_teste.f1_macro:.3f}", nome_melhor: f"{res_teste.f1_macro:.3f}",
     "Diferença": f"{res_teste.f1_macro - res_dummy_teste.f1_macro:+.3f}"},
    {"Métrica": "F1 Vitória Mandante", "Baseline Majoritária": f"{res_dummy_teste.f1_home_win:.3f}", nome_melhor: f"{res_teste.f1_home_win:.3f}",
     "Diferença": f"{res_teste.f1_home_win - res_dummy_teste.f1_home_win:+.3f}"},
    {"Métrica": "F1 Empate", "Baseline Majoritária": f"{res_dummy_teste.f1_draw:.3f}", nome_melhor: f"{res_teste.f1_draw:.3f}",
     "Diferença": f"{res_teste.f1_draw - res_dummy_teste.f1_draw:+.3f}"},
    {"Métrica": "F1 Vitória Visitante", "Baseline Majoritária": f"{res_dummy_teste.f1_away_win:.3f}", nome_melhor: f"{res_teste.f1_away_win:.3f}",
     "Diferença": f"{res_teste.f1_away_win - res_dummy_teste.f1_away_win:+.3f}"},
    {"Métrica": "Log-Loss (probabilidades do modelo)", "Baseline Majoritária": "n/a (probabilidades 0 ou 1)", nome_melhor: f"{res_teste.log_loss_val:.3f}", "Diferença": "—"},
])
display(tabela_final)
'''
        if celula.cell_type == "markdown" and fonte.startswith("## 7. Relevância das Features"):
            celula.source = (
                "## 7. Relevância das Features e Interpretabilidade\n\n"
                "Importância por permutação (aumento do log-loss no teste ao embaralhar cada atributo). "
                "É uma associação do modelo, não uma relação causal:"
            )
        if celula.cell_type == "code" and "16_importancia_features.png" in fonte:
            celula.source = fonte.replace("16_importancia_features.png", "16_importancia_permutacao.png")
        if celula.cell_type == "markdown" and fonte.startswith("## 8. Conclusões"):
            nb.cells[i] = code('''from IPython.display import Markdown, display
fmt = lambda v: f"{v:.2%}".replace(".", ",")
display(Markdown(f\'\'\'## 8. Conclusões e considerações metodológicas

1. **Protocolo temporal:** treino em 2020-2021, validação em 2022 e teste em 2023. Históricos anteriores ao jogo e transformações ajustadas no treino evitam incorporar a própria partida nas entradas. O teste pode usar partidas anteriores já encerradas em 2023.
2. **Desempenho:** {nome_melhor} obteve Macro F1 de {res_teste.f1_macro:.3f} e acurácia balanceada de {fmt(res_teste.acuracia_balanceada)}, contra {res_dummy_teste.f1_macro:.3f} e {fmt(res_dummy_teste.acuracia_balanceada)} da referência majoritária. A acurácia global foi {fmt(res_teste.acuracia)} (referência: {fmt(res_dummy_teste.acuracia)}). Empates reconhecidos: {res_teste.matriz_confusao[1][1]} de {res_teste.matriz_confusao[1].sum()}; vitórias de visitantes: {res_teste.matriz_confusao[2][2]} de {res_teste.matriz_confusao[2].sum()}.
3. **Interpretação:** a importância por permutação e os coeficientes são associações do modelo; não indicam causalidade.
4. **Probabilidades:** Log-Loss do modelo {res_teste.log_loss_val:.3f}. O relatório final compara também uma referência de frequências históricas; não há evidência de superioridade geral.

Consulte `reports/relatorio_tecnico.pdf` e o notebook `03_demonstracao_funcionamento.ipynb` para as evidências consolidadas.\'\'\'))
''')
    nbf.write(nb, caminho)


if __name__ == "__main__":
    destino = ROOT / "notebooks/03_demonstracao_funcionamento.ipynb"
    nbf.write(notebook_demonstracao(), destino)
    atualizar_notebook_modelagem()
    print(destino)

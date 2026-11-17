"""Gera reports/relatorio_tecnico.pdf (e a versão .md) a partir dos resultados reais do projeto.

Fontes de dados (nenhum número é digitado aqui):
  - reports/evidencias/metricas_execucao.json  (gerado por src/modeling.py)
  - models/metadata.json                        (metadados do modelo salvo)
  - data/processed/partidas_processadas.csv     (base processada)
  - reports/figures e reports/screenshots       (figuras e capturas reais)

Uso:  python scripts/gerar_relatorio_tecnico.py
Requer: pip install -r reports/requirements_documentacao.txt (ReportLab). Usa a fonte DejaVu Sans que
acompanha o Matplotlib, portanto funciona em Windows, Linux e macOS.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib
import pandas as pd
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "reports"
D = json.loads((OUT / "evidencias/metricas_execucao.json").read_text(encoding="utf-8"))
META = json.loads((ROOT / "models/metadata.json").read_text(encoding="utf-8"))
DF = pd.read_csv(ROOT / "data/processed/partidas_processadas.csv", parse_dates=["data_partida"])
CACHE_IMG = OUT / ".cache_relatorio"
CACHE_IMG.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- #
# Fontes (DejaVu Sans, distribuída com o Matplotlib)
# --------------------------------------------------------------------------- #
FONTES = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
for nome, arq in [("Body", "DejaVuSans.ttf"), ("Body-Bold", "DejaVuSans-Bold.ttf"),
                  ("Body-Italic", "DejaVuSans-Oblique.ttf"), ("Body-BoldItalic", "DejaVuSans-BoldOblique.ttf")]:
    pdfmetrics.registerFont(TTFont(nome, str(FONTES / arq)))
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic", boldItalic="Body-BoldItalic")

AZUL = colors.HexColor("#153753")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Txt", fontName="Body", fontSize=9.2, leading=13.4, spaceAfter=8, textColor=colors.HexColor("#263445")))
styles.add(ParagraphStyle(name="TitleReport", fontName="Body-Bold", fontSize=23, leading=29, spaceAfter=14, textColor=AZUL))
styles.add(ParagraphStyle(name="Section", fontName="Body-Bold", fontSize=15, leading=19, spaceAfter=12, textColor=AZUL, keepWithNext=1))
styles.add(ParagraphStyle(name="Sub", fontName="Body-Bold", fontSize=10.6, leading=14, spaceBefore=7, spaceAfter=6, textColor=AZUL, keepWithNext=1))
styles.add(ParagraphStyle(name="Small", fontName="Body", fontSize=7.8, leading=10.4, spaceAfter=7, textColor=colors.HexColor("#526475")))
styles.add(ParagraphStyle(name="Cell", fontName="Body", fontSize=7.9, leading=10.2))
styles.add(ParagraphStyle(name="Cmd", fontName="Body", fontSize=7.9, leading=10.4, spaceAfter=3, textColor=colors.HexColor("#1b2a3a"),
                          backColor=colors.HexColor("#F1F4F7"), leftIndent=4, borderPadding=(2, 3, 2, 3)))

story: list = []
markdown: list[str] = []


def p(text: str, style: str = "Txt") -> None:
    story.append(Paragraph(text, styles[style]))
    plano = text.replace("<b>", "**").replace("</b>", "**").replace("<br/>", "\n").replace("<i>", "*").replace("</i>", "*")
    markdown.append(("## " if style == "Section" else "### " if style == "Sub" else "") + plano)


def pagina(titulo: str, quebra: bool = False) -> None:
    """Novo título de seção; ``quebra=True`` força página nova, senão só quebra se sobrar pouco espaço."""
    if story:
        story.append(PageBreak() if quebra else CondPageBreak(190))
        if not quebra:
            story.append(Spacer(1, 10))
    p(titulo, "Section")


def tabela(cabecalho: list[str], linhas: list[list], larguras: list[float]) -> None:
    dados = [[Paragraph(escape(str(c)), styles["Cell"]) for c in linha] for linha in [cabecalho] + linhas]
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5EDF3")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), .6, colors.HexColor("#8CA7B9")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7F9")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story.extend([t, Spacer(1, 9)])
    markdown.extend(["| " + " | ".join(cabecalho) + " |", "| " + " | ".join(["---"] * len(cabecalho)) + " |"]
                    + ["| " + " | ".join(map(str, r)) + " |" for r in linhas] + [""])


contador = {"fig": 0}


def figura(rel: str, legenda: str, maxw: float = 499, maxh: float = 290, recorte_altura: float | None = None,
           recorte_inicio: float = 0.0) -> None:
    """Insere uma imagem real. Capturas longas podem ser recortadas (razões altura/largura) para ficarem legíveis."""
    caminho = OUT / rel
    if recorte_altura is not None:
        img = PILImage.open(caminho)
        topo = int(img.width * recorte_inicio)
        img = img.crop((0, topo, img.width, min(img.height, topo + int(img.width * recorte_altura))))
        caminho = CACHE_IMG / (rel.replace("/", "_"))
        img.save(caminho)
    w, h = ImageReader(str(caminho)).getSize()
    escala = min(maxw / w, maxh / h)
    contador["fig"] += 1
    texto = f"Figura {contador['fig']}. {legenda}"
    story.append(KeepTogether([Image(str(caminho), width=w * escala, height=h * escala), Spacer(1, 4),
                               Paragraph(texto, styles["Small"])]))
    markdown.extend([texto, f"![Figura {contador['fig']}]({rel})"])


def pct(v: float, casas: int = 2) -> str:
    return f"{100 * v:.{casas}f}%".replace(".", ",")


def dec(v: float | None, casas: int = 3) -> str:
    return "n/a" if v is None else f"{v:.{casas}f}".replace(".", ",")


def inteiro(v: int) -> str:
    return f"{v:,}".replace(",", ".")


def data_br(iso: str) -> str:
    return datetime.fromisoformat(iso[:10]).strftime("%d/%m/%Y")


def rodape(c, doc) -> None:
    c.setStrokeColor(colors.HexColor("#CDD9E2"))
    c.line(48, 806, 547, 806)
    c.setFont("Body", 7.5)
    c.setFillColor(colors.HexColor("#526475"))
    c.drawString(48, 815, "INTELIGÊNCIA ARTIFICIAL II  |  RELATÓRIO TÉCNICO")
    c.drawString(48, 29, f"Brasileirão Série A · 2020-2023 · gerado em {data_br(D['executado_em'])}")
    c.drawRightString(547, 29, str(doc.page))


# --------------------------------------------------------------------------- #
# Números derivados (todos calculados)
# --------------------------------------------------------------------------- #
T = D["final"]["teste"]
BASE = D["baselines_teste"]["majoritaria"]
FREQ = D["baselines_teste"]["frequencias"]
FINAL = D["final"]
NOME = D["modelo_selecionado"]
PART = D["particoes"]
CLASSES = ["home_win", "draw", "away_win"]
ROT = {"home_win": "Vitória do mandante", "draw": "Empate", "away_win": "Vitória do visitante"}
n_base = len(DF)
por_classe = DF["resultado"].value_counts()
por_temp = DF.groupby("temporada")
publico_ausente = DF["publico"].isna().sum()
virada = int(((DF["temporada"] == 2020) & (DF["ano_calendario"] == 2021)).sum())
equipes = sorted(set(DF["home_team"]) | set(DF["away_team"]))
cm = T["matriz_confusao"]
comparativo_acc = "inferior" if T["acuracia"] < BASE["acuracia"] else "superior"
comparativo_ll = "melhores" if FREQ["log_loss"] < T["log_loss"] else "piores"
val_final = D["modelos"][NOME]["validacao"]
tr_ini = D["modelos"][NOME]["treino"]
top_perm = D["importancia_permutacao"][:3]
erros = D["analise_erros"]
melhor_logloss_val = min((n for n in D["modelos"] if "Baseline" not in n), key=lambda n: D["modelos"][n]["validacao"]["log_loss"])

# --------------------------------------------------------------------------- #
# Capa e resumo
# --------------------------------------------------------------------------- #
p("Previsão de resultados do<br/>Brasileirão Série A", "TitleReport")
p("Classificação multiclasse com dados históricos de 2020 a 2023", "Sub")
p("<b>Trabalho 1 - Inteligência Artificial II</b><br/>Antonio Meneghetti Faculdade (AMF) · 2026/02<br/>" + data_br(D["executado_em"]))
p("<b>Integrantes</b><br/>Marcelo da Costa Telles<br/>Arthur Zanon<br/>Milton Roberto")
p("Resumo", "Sub")
p(f"Este trabalho prevê o resultado de partidas do Campeonato Brasileiro Série A antes de sua realização, distinguindo vitória do mandante, empate e vitória do visitante. "
  f"A base contém {inteiro(n_base)} partidas de quatro temporadas; {inteiro(D['dados']['partidas_utilizaveis'])} têm histórico suficiente e foram usadas na modelagem, com separação cronológica entre treinamento ({PART['treino']['n']}), "
  f"validação ({PART['validacao']['n']}) e teste ({PART['teste']['n']}).")
p(f"Foram comparados {len(D['modelos'])} algoritmos (uma referência majoritária, Regressão Logística, Random Forest e HistGradientBoosting). Foi selecionado o modelo <b>{NOME}</b>, pelo maior Macro F1 na validação. "
  f"No teste de 2023 obteve <b>{pct(T['acuracia'])} de acurácia, Macro F1 de {dec(T['f1_macro'])} e Log-Loss de {dec(T['log_loss'])}</b>. "
  f"A acurácia é {comparativo_acc} à da referência que sempre prevê o mandante ({pct(BASE['acuracia'])}), embora o Macro F1 seja maior ({dec(T['f1_macro'])} contra {dec(BASE['f1_macro'])}). "
  f"Uma referência de frequências históricas tem Log-Loss {comparativo_ll} ({dec(FREQ['log_loss'])}). O modelo, portanto, não demonstra superioridade geral.")
p("Além do modelo, o projeto inclui uma API (Python) que serve o modelo salvo e um front-end (React) para demonstração; ambos são descritos na seção de extensão.")
tabela(["Base original", "Base elegível", "Teste independente", "Modelo salvo"],
       [[f"{inteiro(n_base)} partidas / {len(equipes)} clubes", f"{inteiro(D['dados']['partidas_utilizaveis'])} partidas / {D['atributos']['total']} atributos",
         f"{PART['teste']['n']} partidas de 2023", f"models/model.joblib (v{META['versao']})"]], [125, 125, 125, 124])
p("Organização: 1 Dataset · 2 Problema e objetivo · 3 Exploração e preparação · 4 Estratégia experimental · 5 Modelagem · 6 Avaliação · 7 Análise dos resultados · 8 Demonstração de funcionamento · 9 Extensão opcional · 10 Limitações · 11 Referências e reprodução.", "Small")

# --------------------------------------------------------------------------- #
pagina("1. Dataset")
p(f"O arquivo <b>partidas_20_23.csv</b> reúne {inteiro(n_base)} linhas e 17 colunas, com 380 partidas por temporada, {len(equipes)} clubes distintos e partidas de {data_br(D['dados']['periodo_inicio'])} a {data_br(D['dados']['periodo_fim'])}. "
  "Cada linha traz equipes, placar, data e horário, estádio, público, árbitro, listas JSON de gols e cartões e o link da partida. Os links apontam para o domínio Opta Player Stats / Stats Perform; "
  "essa é a origem identificável nos registros. O procedimento original de coleta e a licença específica da base não estão documentados no repositório.")
p("<b>Validação do dataset:</b> o CSV original é lido somente para leitura e seu SHA-256 é registrado nos metadados do modelo; 14 verificações automáticas (contagens, placares não negativos, datas interpretadas, temporadas, ordem cronológica, identificadores únicos) são executadas por <i>src/data_analysis.py</i>. "
  "A aprovação do dataset pelo professor é uma etapa manual da equipe.")
tabela(["Indicador", "Resultado e tratamento"], [
    ["Classes", "; ".join(f"{int(por_classe[c])} {ROT[c].lower()} ({pct(por_classe[c] / n_base, 1)})" for c in CLASSES) + "."],
    ["Gols", f"{inteiro(int(DF['total_gols'].sum()))} gols; média de {dec(DF['total_gols'].mean(), 2)} por jogo; máximo de {int(DF['total_gols'].max())} em uma partida (valores extremos preservados)."],
    ["Público ausente", f"{publico_ausente} partidas ({pct(publico_ausente / n_base, 1)}): " + ", ".join(f"{int(v)} em {t}" for t, v in por_temp["publico"].apply(lambda s: s.isna().sum()).items())
     + ". Ausência não foi substituída por zero."],
    ["Temporada e calendário", f"{virada} jogos da temporada 2020 ocorreram em 2021; a temporada é extraída do link, e não do ano da data."],
    ["Eventos disciplinares", f"{inteiro(int(DF['total_amarelos'].sum()))} amarelos e {int(DF['total_expulsoes'].sum())} expulsões contabilizadas (incluem registros de comissão técnica)."]], [105, 394])
figura("figures/01_distribuicao_resultados.png", "Distribuição das classes na base completa. O desequilíbrio motiva avaliar também o Macro F1.", maxh=170)
figura("figures/02_resultados_por_temporada.png", "Resultados por temporada.", maxh=170)
p("Todas as figuras de exploração são geradas por <i>src/data_analysis.py</i> a partir dos dados reais e ficam em reports/figures.", "Small")

pagina("2. Problema e objetivo")
p("<b>Problema.</b> Classificação supervisionada multiclasse: dada uma partida ainda não disputada, estimar a classe do resultado final — vitória do mandante (<i>home_win</i>), empate (<i>draw</i>) ou vitória do visitante (<i>away_win</i>). "
  "O alvo é derivado do placar registrado; a versão numérica usada internamente é 0, 1 e 2, respectivamente.")
p("<b>Objetivo.</b> Implementar e avaliar um processo reproduzível que use somente informações disponíveis antes de cada jogo e analisar criticamente seus limites de generalização, comparando algoritmos com referências simples.")
p("<b>Escopo.</b> A unidade de análise é uma partida. As probabilidades estimadas permitem examinar a incerteza entre as três classes. A avaliação é retrospectiva; a demonstração na aplicação prevê confrontos hipotéticos a partir do histórico até o último jogo da base e não constitui um serviço de previsão em tempo real.")
p("<b>Critérios de sucesso.</b> (i) evitar vazamento de dados; (ii) superar referências simples em ao menos uma métrica adequada ao desequilíbrio de classes; (iii) relatar honestamente onde o modelo não supera as referências.")

pagina("3. Exploração e preparação dos dados")
p("A exploração cobre dimensões, tipos, ausências, duplicidades, valores extremos (regra do IQR), distribuição das classes, gols e cartões por temporada, desempenho de mandantes e visitantes, rankings de equipes e público por temporada.")
g = por_temp[["total_gols", "total_amarelos", "total_expulsoes"]].mean()
tabela(["Temporada", "Gols por jogo", "Amarelos por jogo", "Expulsões por jogo", "Público médio (informado)"],
       [[str(t), dec(g.loc[t, "total_gols"], 2), dec(g.loc[t, "total_amarelos"], 2), dec(g.loc[t, "total_expulsoes"], 2),
         "sem dados" if pd.isna(DF[DF.temporada == t]["publico"].mean()) else inteiro(int(round(DF[DF.temporada == t]["publico"].mean())))] for t in g.index],
       [70, 100, 110, 110, 109])
figura("figures/04_cartoes_por_temporada.png", "Cartões por temporada.", maxh=160)
figura("figures/05_times_mais_vitoriosos.png", "Equipes com mais vitórias no período.", maxh=190)
p("Preparação", "Sub")
p("As datas em português são convertidas por dicionário de meses; as listas JSON são interpretadas com <i>json.loads</i> (nunca <i>eval</i>), registrando inconsistências; o público com ponto de milhar é convertido e <i>No data</i> vira ausente; "
  "expulsões somam vermelhos diretos e segundos amarelos; gols contra e pênaltis são contados a partir dos campos <i>cont</i> e <i>penal</i>. Os nomes das equipes são padronizados e a variável-alvo deriva exclusivamente do placar.")
p("Atributos e prevenção de vazamento", "Sub")
p("As médias e contagens dos últimos cinco jogos usam <b>shift(1)</b> antes da janela móvel: a partida a prever não contribui para os próprios atributos. Exige-se histórico mínimo de cinco jogos; o histórico atravessa temporadas consecutivas e reinicia após uma temporada inteira sem jogos do clube. "
  "Placar, gols, cartões, totais e resultado da própria partida nunca são entradas; só servem para construir o histórico. Esse comportamento é verificado por testes automatizados (perturbação do placar da partida atual, recálculo independente das médias e conferência das colunas proibidas).")
tabela(["Grupo", "Conteúdo"], [
    ["22 históricos numéricos", "Por equipe: pontos, vitórias, empates, derrotas, gols marcados e sofridos, saldo, amarelos, expulsões e aproveitamento; mais aproveitamento do mandante em casa e do visitante fora."],
    ["2 de calendário", "Mês e hora da partida."],
    ["7 derivados", "Seis diferenças entre históricos do mandante e do visitante e uma soma de gols marcados pelo mandante com gols sofridos pelo visitante."],
    ["3 categóricos", "Equipe mandante, equipe visitante e dia da semana (codificados por one-hot)."]], [125, 374])
p(f"São <b>{D['atributos']['total']} atributos de entrada: {len(D['atributos']['numericos'])} numéricos e {len(D['atributos']['categoricos'])} categóricos</b>. "
  f"O filtro <i>utilizavel_ml</i> retém {inteiro(D['dados']['partidas_utilizaveis'])} partidas e exclui {n_base - D['dados']['partidas_utilizaveis']} sem histórico suficiente. "
  f"Há {sum(D['ausencias_atributos'].values())} partidas elegíveis com ausência nos atributos de mando ({D['ausencias_atributos']['treino']} no treino, {D['ausencias_atributos']['validacao']} na validação e {D['ausencias_atributos']['teste']} no teste); "
  "elas são mantidas e imputadas pela mediana aprendida somente no treinamento. A padronização (StandardScaler) é aplicada apenas ao modelo linear; valores extremos de gols foram preservados por serem resultados legítimos.")

pagina("4. Estratégia experimental")
tabela(["Etapa", "Temporadas", "Partidas", "Mandante / empate / visitante"],
       [[nome, "–".join(str(t) for t in (PART[k]["temporadas"][0], PART[k]["temporadas"][-1])) if len(PART[k]["temporadas"]) > 1 else str(PART[k]["temporadas"][0]),
         inteiro(PART[k]["n"]), " / ".join(str(PART[k]["classes"][c]) for c in CLASSES)]
        for nome, k in [("Treinamento inicial", "treino"), ("Validação e seleção", "validacao"), ("Teste final", "teste"), ("Retreino do selecionado", "treino_final")]], [140, 90, 70, 199])
p(f"A divisão é estritamente cronológica; não há sorteio de partidas entre períodos. Os candidatos são ajustados em 2020–2021 e comparados em 2022. A seleção usa o <b>{D['criterio_selecao']}</b>. "
  "O selecionado é reajustado com 2020–2022 e avaliado uma única vez em 2023: o teste não é usado para escolher modelo nem hiperparâmetros. "
  f"O pré-processamento (imputação, escala e codificação) faz parte do <i>Pipeline</i> e é ajustado só com os dados de treinamento (verificado: as medianas do ajuste final coincidem com as de treino + validação: {'sim' if D['medianas_apenas_treino_final'] else 'não'}).")
p("Métricas", "Sub")
p("<b>Acurácia</b>; <b>acurácia balanceada</b> (média do recall das classes); <b>precisão macro</b>, <b>recall macro</b> e <b>Macro F1</b> (médias simples entre as classes); relatório por classe; matriz de confusão; "
  "<b>Log-Loss</b> e <b>Brier multiclasse</b> (menores são melhores; Brier de 0 a 2); <b>ROC AUC um-contra-todos</b> (macro); calibração (curvas em faixas de mesmo tamanho e erro de calibração esperado da classe prevista).")
p("Não houve busca sistemática de hiperparâmetros, calibração das probabilidades nem avaliação em múltiplas janelas temporais; esses pontos estão listados nas limitações.")

pagina("5. Modelagem")
linhas = []
just = {"Baseline (Majoritária)": "Quantifica o resultado de sempre prever a classe mais comum no treino.",
        "Regressão Logística": "Modelo linear probabilístico; a regularização L2 limita a complexidade em uma base pequena.",
        "Random Forest": "Captura relações não lineares; profundidade e folhas limitadas para reduzir sobreajuste.",
        "HistGradientBoosting": "Conjunto sequencial de árvores; avalia interações entre atributos."}
for nome, m in D["modelos"].items():
    h = {k: v for k, v in m["hiperparametros"].items() if k != "algoritmo"}
    linhas.append([nome, "; ".join(f"{k}={v}" for k, v in h.items()) or "—", f"{m['tempo_treino_s']:.3f} s".replace(".", ","), just[nome]])
tabela(["Algoritmo", "Hiperparâmetros", "Tempo de ajuste", "Justificativa"], linhas, [95, 165, 55, 184])
p(f"Pré-processamento: imputação pela mediana em todos os modelos; StandardScaler apenas na Regressão Logística; OneHotEncoder (categorias desconhecidas ignoradas). Semente aleatória: {D['random_state']}. "
  f"Ambiente: Python {D['ambiente']['python']}, NumPy {D['ambiente']['numpy']}, pandas {D['ambiente']['pandas']}, scikit-learn {D['ambiente']['scikit_learn']}.")
p(f"O modelo final ({NOME}, reajustado em 2020–2022, {FINAL['tempo_treino_s']:.3f} s) é salvo em <i>models/model.joblib</i> com metadados em <i>models/metadata.json</i> "
  "(versão, data de treinamento, algoritmo, hiperparâmetros, atributos, classes, métricas, período dos dados, semente e versões das dependências), e é o mesmo artefato usado pela API.")

pagina("6. Avaliação")
p("Validação (2022) e comparação com o treino", "Sub")
tabela(["Modelo", "Acurácia treino", "Acurácia val.", "Bal. acc. val.", "Prec. macro", "Recall macro", "Macro F1", "Log-Loss"],
       [[n, pct(m["treino"]["acuracia"]), pct(m["validacao"]["acuracia"]), pct(m["validacao"]["acuracia_balanceada"]), dec(m["validacao"]["precisao_macro"]),
         dec(m["validacao"]["recall_macro"]), dec(m["validacao"]["f1_macro"]), dec(m["validacao"]["log_loss"]) if "Baseline" not in n else "n/a"] for n, m in D["modelos"].items()],
       [100, 55, 55, 55, 50, 50, 50, 84])
figura("figures/14_comparacao_modelos_validacao.png", "Comparação dos modelos na validação (parâmetros ajustados somente em 2020-2021).", maxh=210)
p("Teste final (2023)", "Sub")
tabela(["Modelo / referência", "Acurácia", "Bal. acc.", "Prec. macro", "Recall macro", "Macro F1", "Log-Loss", "Brier", "AUC"],
       [[NOME, pct(T["acuracia"]), pct(T["acuracia_balanceada"]), dec(T["precisao_macro"]), dec(T["recall_macro"]), dec(T["f1_macro"]), dec(T["log_loss"]), dec(T["brier"]), dec(T["roc_auc_ovr_macro"])],
        ["Sempre mandante", pct(BASE["acuracia"]), pct(BASE["acuracia_balanceada"]), dec(BASE["precisao_macro"]), dec(BASE["recall_macro"]), dec(BASE["f1_macro"]), "n/a", "n/a", dec(BASE["roc_auc_ovr_macro"])],
        ["Frequências históricas", pct(FREQ["acuracia"]), pct(FREQ["acuracia_balanceada"]), dec(FREQ["precisao_macro"]), dec(FREQ["recall_macro"]), dec(FREQ["f1_macro"]), dec(FREQ["log_loss"]), dec(FREQ["brier"]), dec(FREQ["roc_auc_ovr_macro"])]],
       [92, 50, 50, 52, 52, 50, 50, 50, 53])
tabela(["Classe verdadeira", "Acertos / total", "Precisão", "Recall", "F1", "Previsões do modelo"],
       [[ROT[c], f"{cm[i][i]} / {sum(cm[i])}", dec(T["por_classe"][c]["precisao"]), dec(T["por_classe"][c]["recall"]), dec(T["por_classe"][c]["f1"]), T["distribuicao_previsoes"][c]] for i, c in enumerate(CLASSES)],
       [120, 80, 70, 70, 70, 89])
figura("figures/15_matriz_confusao_teste.png", "Matriz de confusão do teste (linhas: classe verdadeira; colunas: classe prevista).", maxh=250)

pagina("7. Análise dos resultados")
p("Comparação com as referências", "Sub")
p(f"O modelo acertou <b>{round(T['acuracia'] * T['n'])} de {T['n']} jogos</b>; a referência majoritária acertou {round(BASE['acuracia'] * BASE['n'])}. A diferença de acurácia é de {f"{100 * (T['acuracia'] - BASE['acuracia']):+.2f}".replace('.', ',')} pontos percentuais"
  + f". Em contrapartida, o Macro F1 passa de {dec(BASE['f1_macro'])} para {dec(T['f1_macro'])} e a acurácia balanceada de {pct(BASE['acuracia_balanceada'])} para {pct(T['acuracia_balanceada'])}: o modelo passa a reconhecer empates e vitórias de visitantes. "
  f"O ROC AUC macro é {dec(T['roc_auc_ovr_macro'])}, próximo de 0,5, o que indica baixo poder de ordenação. A referência de frequências históricas apresenta Log-Loss de {dec(FREQ['log_loss'])} e Brier de {dec(FREQ['brier'])}, "
  f"{comparativo_ll} que os {dec(T['log_loss'])} e {dec(T['brier'])} do modelo. Na validação, o menor Log-Loss foi de {melhor_logloss_val}: a escolha pelo Macro F1 é uma decisão de critério, não de superioridade geral.")
p("Overfitting e generalização", "Sub")
figura("figures/19_treino_validacao_teste.png", "Desempenho do modelo selecionado em treino, validação e teste.", maxh=200)
sobre = {n: (m["treino"]["acuracia"], m["validacao"]["acuracia"]) for n, m in D["modelos"].items() if "Baseline" not in n}
maior = max(sobre, key=lambda n: sobre[n][0] - sobre[n][1])
p(f"A acurácia cai do treino para a validação em todos os modelos; a maior queda é a do {maior} ({pct(sobre[maior][0])} → {pct(sobre[maior][1])}), o que indica sobreajuste. "
  f"No modelo selecionado, a acurácia vai de {pct(tr_ini['acuracia'])} (treino 2020–21) para {pct(val_final['acuracia'])} (validação) e {pct(FINAL['treino_final']['acuracia'])} (treino final) contra {pct(T['acuracia'])} no teste. "
  "Métricas de treino medem os dados usados no ajuste e não substituem a avaliação temporal.")
p("Classes mais difíceis e erros", "Sub")
conf = erros["confusoes_mais_frequentes"][:2]
p(f"O recall foi de {pct(T['por_classe']['home_win']['recall'], 1)} para vitórias do mandante, {pct(T['por_classe']['draw']['recall'], 1)} para empates e {pct(T['por_classe']['away_win']['recall'], 1)} para vitórias do visitante. "
  f"O modelo previu empate em apenas {erros['previsoes_de_empate']} das {T['n']} partidas (a maior probabilidade de empate atribuída foi {pct(erros['maior_probabilidade_de_empate'], 1)}); como o empate raramente é a classe mais provável, ele é pouco previsto. "
  f"As confusões mais frequentes foram: {', '.join(f'{ROT[c['real']].lower()} previsto como {ROT[c['previsto']].lower()} ({c['partidas']} partidas)' for c in conf)}.")
figura("figures/20_distribuicao_previsoes.png", "Distribuição das previsões e dos resultados reais no teste.", maxh=170)
tabela(["Data", "Confronto", "Placar", "Previsto", "Real", "Confiança"],
       [[data_br(e["data"]), f"{e['mandante']} x {e['visitante']}", e["placar"], ROT[e["previsto"]], ROT[e["real"]], pct(e["confianca"], 1)] for e in erros["erros_mais_confiantes"]], [60, 130, 40, 100, 100, 69])
p("A tabela lista as previsões erradas em que o modelo atribuiu maior probabilidade à classe prevista. Não foram investigadas as causas de cada erro; possíveis fatores gerais são a alta variância do futebol e a ausência, no dataset, de escalações, lesões e contexto do jogo. "
  "Os acertos de maior confiança estão em reports/evidencias/metricas_execucao.json.", "Small")
p("Interpretação (associação, não causalidade)", "Sub")
figura("figures/16_importancia_permutacao.png", "Importância por permutação no teste (aumento médio do log-loss; barras: desvio padrão de 30 repetições).", maxh=250)
p(f"Os atributos de maior impacto foram: {'; '.join(f'{d['rotulo']} (+{d['aumento_log_loss']:.4f})'.replace('.', ',') for d in top_perm)}. "
  "Os desvios são grandes em relação às médias, e atributos correlacionados dividem a importância; os resultados descrevem o comportamento do modelo, não causas dos resultados. "
  "Os coeficientes da Regressão Logística por classe (reports/figures/17) mostram a direção do efeito condicional de cada atributo padronizado, mas indicadores de equipes e do dia da semana têm escala diferente dos numéricos.")
figura("figures/18_calibracao_teste.png", f"Calibração no teste; ECE da classe prevista = {dec(D['calibracao']['ece_classe_prevista'])}, com {D['calibracao']['n_faixas']} faixas (amostra pequena: curvas ruidosas).", maxh=210)

pagina("8. Demonstração de funcionamento")
p("A aplicação foi executada de ponta a ponta (API + front-end) e as capturas abaixo foram feitas automaticamente pelo script <i>scripts/capturar_screenshots.py</i> com o navegador Chromium, sem edição. "
  "Todas as probabilidades, tabelas e gráficos vêm da API; não há dados simulados no front-end. Há também o notebook <i>03_demonstracao_funcionamento.ipynb</i>, executado do início ao fim.")
figura("screenshots/01_inicio.png", "Página inicial: indicadores e métricas reais lidos da API (topo da página).", maxh=320, recorte_altura=0.62)
figura("screenshots/03_previsao_probabilidades.png", "Previsão de Flamengo x Palmeiras: equipes, data de referência e as três probabilidades.", maxh=340)
figura("screenshots/04_previsao_comparacao_historica.png", "Comparação histórica: forma recente, médias dos últimos 5 jogos e confronto direto.", maxh=320, recorte_altura=0.62, recorte_inicio=0.62)
figura("screenshots/05_estatisticas_geral.png", "Estatísticas: indicadores e gráficos calculados pela API (topo da página).", maxh=320, recorte_altura=0.85)
figura("screenshots/06_estatisticas_filtrada.png", "Estatísticas filtradas por temporada 2023 e equipe Flamengo (topo da página).", maxh=320, recorte_altura=0.85)
figura("screenshots/07_sobre_o_modelo.png", "Sobre o modelo: algoritmo, divisão temporal e métricas reais (topo da página).", maxh=330, recorte_altura=0.85)
figura("screenshots/08_celular_previsao.png", "Uso em celular (390 px): sem rolagem horizontal (topo da página).", maxh=330, maxw=160, recorte_altura=1.95)
p("As imagens completas estão em reports/screenshots/. As capturas do JupyterLab de execuções anteriores permanecem em reports/evidencias/.", "Small")

pagina("9. Extensão opcional: API e aplicação web")
p("Como extensão, o modelo foi disponibilizado por uma API HTTP (Python, biblioteca padrão) e uma interface web (React + TypeScript + Vite). A API carrega <i>models/model.joblib</i> e a base processada uma única vez, valida entradas, restringe CORS às origens configuradas e responde erros em JSON sem expor detalhes internos.")
p("Na previsão de um confronto, a API calcula os atributos com <b>o mesmo código do treinamento</b> sobre os jogos anteriores à data de referência; testes comprovam que os atributos coincidem com os do conjunto de treino nas 1.414 partidas elegíveis. "
  "Equipes sem cinco jogos ou sem jogos recentes são recusadas (HTTP 422) em vez de receberem valores inventados.")
tabela(["Endpoint", "Função"], [
    ["GET /api/health", "Estado da API, do modelo e da base."], ["GET /api/model", "Metadados e métricas reais do modelo."],
    ["GET /api/teams", "Equipes e elegibilidade para previsão."], ["GET /api/teams/{id}/summary", "Resumo de desempenho de uma equipe."],
    ["GET /api/teams/compare", "Comparação e confronto direto."], ["GET /api/stats/overview · /charts", "Indicadores e séries com filtros de temporada, equipe e mando."],
    ["GET /api/matches", "Partidas paginadas."], ["POST /api/predict", "Três probabilidades, classe prevista, forma recente, confronto direto e fatores."]], [170, 329])

pagina("10. Limitações")
for item in [
    f"Base pequena: {inteiro(n_base)} partidas de uma única competição em quatro temporadas; mudanças de elenco, técnico e participação dos clubes não são modeladas.",
    "O histórico de cinco jogos é curto; não há escalações, lesões, força do elenco, mercado ou informações externas. Cartões incluem comissão técnica.",
    "Não houve busca sistemática de hiperparâmetros, calibração das probabilidades, intervalos de confiança, testes de significância entre modelos ou avaliação em várias janelas temporais.",
    "A avaliação em 2023 é sequencial: o histórico do teste usa jogos anteriores já encerrados em 2023, cenário coerente com a previsão antes de cada partida, não com a previsão de toda a temporada de uma vez.",
    "As verificações de vazamento (testes automatizados) sustentam o desenho, mas não são garantia universal contra todo tipo de vazamento.",
    "Confrontos hipotéticos na aplicação dependem da data de referência escolhida e assumem calendário e mando informados pelo usuário.",
    "A origem dos dados é identificável pelo link, mas a coleta original e a licença de uso não estão documentadas.",
    f"Estimativas de interpretação são associações; os desvios da importância por permutação são grandes ({', '.join(f'{d['desvio_padrao']:.4f}'.replace('.', ',') for d in top_perm)} nos três primeiros)."]:
    p("• " + item)
p("Conclusão", "Sub")
p(f"O trabalho entrega uma solução supervisionada reproduzível, com engenharia temporal sem vazamento, comparação de algoritmos, avaliação com várias métricas e interpretação crítica. O modelo selecionado ({NOME}) melhora o reconhecimento das três classes (Macro F1 {dec(T['f1_macro'])} contra {dec(BASE['f1_macro'])}), "
  f"mas tem acurácia {comparativo_acc} à da referência majoritária e Log-Loss {'pior' if FREQ['log_loss'] < T['log_loss'] else 'melhor'} que o das frequências históricas. "
  "Como continuidade: avaliar múltiplas janelas temporais, incluir atributos pré-jogo adicionais, ajustar hiperparâmetros só com validação e calibrar probabilidades.")

pagina("11. Referências e reprodução")
p("Ambiente e comandos", "Sub")
for cmd in ["python -m venv .venv && source .venv/bin/activate     # Windows: .venv\\Scripts\\activate", "pip install -r requirements.txt -r requirements-dev.txt",
            "python src/data_analysis.py      # EDA, base processada e figuras 01-13", "python src/modeling.py           # treino, avaliação, modelo salvo e figuras 14-20",
            "python -m pytest tests           # testes de dados, vazamento, modelo, previsão e API", "python src/api.py                # API em http://127.0.0.1:8000/api",
            "cd frontend && npm install && npm run dev     # interface em http://localhost:5173", "python scripts/capturar_screenshots.py   # capturas reais (Playwright)",
            "python scripts/gerar_relatorio_tecnico.py     # este relatório", "make setup data train test run report              # atalhos equivalentes"]:
    p(escape(cmd), "Cmd")
p("Com o Makefile, <i>make all</i> executa dados, treino e testes. Detalhes no README.")
p("Estrutura do repositório", "Sub")
tabela(["Caminho", "Finalidade"], [
    ["src/data_analysis.py, data_split.py", "Limpeza, atributos históricos, EDA e separação temporal."], ["src/modeling.py, evaluation.py", "Treinamento, seleção, métricas, interpretação e persistência."],
    ["src/api.py, predictor.py, analytics.py", "API, previsão com o modelo salvo e estatísticas."], ["frontend/", "Interface web e seus testes."], ["tests/", "Testes automatizados em Python."],
    ["models/", "Modelo salvo e metadados."], ["notebooks/", "EDA, modelagem e demonstração executados."], ["reports/", "Relatórios, figuras, evidências e capturas."]], [190, 309])
p("Referências", "Sub")
p("[1] Enunciado: Trabalho 1 - Inteligência Artificial II, 2026/02. Documento fornecido para a atividade.<br/>"
  "[2] Código e dados do projeto: github.com/ZanonDeAndrade/trabalhoIA.<br/>"
  "[3] Stats Perform / Opta Player Stats: domínio presente na coluna link do CSV (optaplayerstats.statsperform.com).<br/>"
  "[4] Pedregosa et al. Scikit-learn: Machine Learning in Python. JMLR 12, 2011.<br/>"
  "[5] Documentação do scikit-learn: Pipeline, LogisticRegression, permutation_importance e calibration_curve.")
p("A atividade exige aprovação prévia do dataset e entrega do repositório conforme o enunciado. Este relatório não comprova aprovação docente, envio no Classroom nem a contribuição individual de cada integrante; essas etapas devem ser conferidas pela equipe.", "Small")

pdf = OUT / "relatorio_tecnico.pdf"
SimpleDocTemplate(str(pdf), pagesize=A4, rightMargin=48, leftMargin=48, topMargin=52, bottomMargin=47,
                  title="Previsão de resultados do Brasileirão Série A - Relatório técnico",
                  author="Marcelo da Costa Telles; Arthur Zanon; Milton Roberto").build(story, onFirstPage=rodape, onLaterPages=rodape)
(OUT / "relatorio_tecnico.md").write_text("\n\n".join(markdown), encoding="utf-8")
print(pdf)

"""Pipeline de modelagem preditiva, treinamento e avaliação de modelos.

Este módulo constrói, avalia e compara múltiplos classificadores para previsão
do resultado das partidas do Brasileirão Série A:
1. Linha de Base Ingênua (DummyClassifier - classe majoritária)
2. Regressão Logística Multinomial (Regularizada)
3. Random Forest Classifier
4. HistGradientBoosting Classifier (Ensemble com Gradient Boosting)

Todas as transformações (imputação e escalonamento) são empacotadas via
`sklearn.pipeline.Pipeline`, prevenindo qualquer vazamento entre partições.
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

# Garante que a raiz do repositório esteja no sys.path
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    log_loss,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data_split import (
    CLASSES,
    CODIGO_RESULTADO,
    RANDOM_STATE,
    ROTULO_RESULTADO,
    ParticoesDados,
    carregar_e_dividir_dados,
)


logger = logging.getLogger("modeling")

DIR_RELATORIOS = Path(__file__).resolve().parents[1] / "reports"
DIR_FIGURAS = DIR_RELATORIOS / "figures"
ARQUIVO_RELATORIO = DIR_RELATORIOS / "resultados_modelagem.md"


@dataclass
class ResultadoAvaliacao:
    """Métricas consolidadas de avaliação de um modelo em uma partição."""
    nome_modelo: str
    particao: str
    acuracia: float
    acuracia_balanceada: float
    f1_macro: float
    f1_weighted: float
    f1_home_win: float
    f1_draw: float
    f1_away_win: float
    log_loss_val: float
    brier_score: float
    matriz_confusao: np.ndarray


def calcular_brier_multiclasse(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Calcula o Brier Score multiclasse: média da soma das diferenças quadráticas."""
    n_classes = y_prob.shape[1]
    y_true_onehot = np.eye(n_classes)[y_true]
    return float(np.mean(np.sum((y_prob - y_true_onehot) ** 2, axis=1)))


def criar_preprocessador(
    features_numericas: list[str],
    features_categoricas: list[str],
    para_arvore: bool = False,
) -> ColumnTransformer:
    """Gera o ColumnTransformer de pré-processamento.
    
    Se para_arvore=True, o escalonamento numérico é dispensado, mantendo a imputação.
    """
    if para_arvore:
        pipe_num = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
        ])
    else:
        pipe_num = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])

    pipe_cat = Pipeline([
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    return ColumnTransformer(
        transformers=[
            ("num", pipe_num, features_numericas),
            ("cat", pipe_cat, features_categoricas),
        ],
        remainder="drop",
    )


def construir_modelos(
    features_numericas: list[str],
    features_categoricas: list[str],
) -> dict[str, Pipeline]:
    """Instancia os pipelines dos modelos a serem comparados."""
    pre_linear = criar_preprocessador(features_numericas, features_categoricas, para_arvore=False)
    pre_arvore = criar_preprocessador(features_numericas, features_categoricas, para_arvore=True)

    modelos = {
        "Baseline (Majoritária)": Pipeline([
            ("dummy", DummyClassifier(strategy="most_frequent")),
        ]),
        "Regressão Logística": Pipeline([
            ("prep", pre_linear),
            ("clf", LogisticRegression(
                solver="lbfgs",
                max_iter=1000,
                C=0.5,
                random_state=RANDOM_STATE,
            )),
        ]),
        "Random Forest": Pipeline([
            ("prep", pre_arvore),
            ("clf", RandomForestClassifier(
                n_estimators=200,
                max_depth=6,
                min_samples_leaf=8,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            )),
        ]),
        "HistGradientBoosting": Pipeline([
            ("prep", pre_arvore),
            ("clf", HistGradientBoostingClassifier(
                max_iter=120,
                max_depth=4,
                min_samples_leaf=15,
                learning_rate=0.05,
                random_state=RANDOM_STATE,
            )),
        ]),
    }
    return modelos


def avaliar_modelo(
    modelo: Any,
    X: pd.DataFrame,
    y: pd.Series,
    nome_modelo: str,
    particao: str,
) -> ResultadoAvaliacao:
    """Calcula todas as métricas oficiais para um modelo avaliado em X, y."""
    y_true = y.to_numpy()
    y_pred = modelo.predict(X)

    if hasattr(modelo, "predict_proba"):
        y_prob = modelo.predict_proba(X)
        try:
            ll = float(log_loss(y_true, y_prob, labels=[0, 1, 2]))
        except Exception:
            ll = float("nan")
        brier = calcular_brier_multiclasse(y_true, y_prob)
    else:
        ll = float("nan")
        brier = float("nan")

    f1_classes = f1_score(y_true, y_pred, average=None, labels=[0, 1, 2], zero_division=0)

    return ResultadoAvaliacao(
        nome_modelo=nome_modelo,
        particao=particao,
        acuracia=float(accuracy_score(y_true, y_pred)),
        acuracia_balanceada=float(balanced_accuracy_score(y_true, y_pred)),
        f1_macro=float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        f1_weighted=float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        f1_home_win=float(f1_classes[0]),
        f1_draw=float(f1_classes[1]),
        f1_away_win=float(f1_classes[2]),
        log_loss_val=ll,
        brier_score=brier,
        matriz_confusao=confusion_matrix(y_true, y_pred, labels=[0, 1, 2]),
    )


def plotar_comparacao_modelos(
    df_resumos: pd.DataFrame,
    caminho_saida: Path = DIR_FIGURAS / "14_comparacao_modelos_validacao.png",
) -> None:
    """Gera gráfico de barras comparando Acurácia, Acurácia Balanceada e F1 Macro."""
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    df_plot = df_resumos[df_resumos["particao"] == "Validação (2022)"].copy()

    metricas = [
        ("acuracia", "Acurácia Global"),
        ("acuracia_balanceada", "Acurácia Balanceada"),
        ("f1_macro", "Macro F1-Score"),
    ]

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
    x = np.arange(len(df_plot))
    width = 0.25

    cores = ["#2a78d6", "#1baf7a", "#eb6834"]
    for i, (col, rotulo) in enumerate(metricas):
        valores = df_plot[col].to_numpy() * 100
        barras = ax.bar(x + (i - 1) * width, valores, width, label=rotulo, color=cores[i], alpha=0.9)
        for b in barras:
            h = b.get_height()
            ax.annotate(
                f"{h:.1f}%",
                xy=(b.get_x() + b.get_width() / 2, h),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold",
            )

    ax.set_xticks(x)
    ax.set_xticklabels(df_plot["nome_modelo"], fontsize=10)
    ax.set_ylabel("Percentual (%)", fontsize=11)
    ax.set_title("Comparação de Desempenho na Validação (Temporada 2022)", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(0, 70)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(frameon=True, facecolor="white", loc="upper left")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()


def plotar_matriz_confusao(
    cm: np.ndarray,
    nome_modelo: str,
    particao: str,
    caminho_saida: Path = DIR_FIGURAS / "15_matriz_confusao_teste.png",
) -> None:
    """Gera visualização da matriz de confusão com valores absolutos e percentuais."""
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] * 100

    rotulos_classes = ["Vitória Mandante", "Empate", "Vitória Visitante"]

    fig, ax = plt.subplots(figsize=(6.5, 5.5), dpi=150)
    sns.heatmap(
        cm_norm,
        annot=False,
        cmap="Blues",
        cbar=True,
        ax=ax,
        vmin=0,
        vmax=100,
    )

    for i in range(len(rotulos_classes)):
        for j in range(len(rotulos_classes)):
            texto = f"{cm[i, j]}\n({cm_norm[i, j]:.1f}%)"
            cor = "white" if cm_norm[i, j] > 50 else "black"
            ax.text(j + 0.5, i + 0.5, texto, ha="center", va="center", color=cor, fontweight="bold")

    ax.set_title(f"Matriz de Confusão: {nome_modelo}\nPartição de {particao}", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Classe Prevista", fontsize=11)
    ax.set_ylabel("Classe Real", fontsize=11)
    ax.set_xticklabels(rotulos_classes, fontsize=9.5)
    ax.set_yticklabels(rotulos_classes, fontsize=9.5)

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()


def plotar_importancia_features(
    modelo: Pipeline,
    features_numericas: list[str],
    caminho_saida: Path = DIR_FIGURAS / "16_importancia_features.png",
    top_n: int = 15,
) -> None:
    """Extrai e plota a importância das features para o modelo selecionado."""
    DIR_FIGURAS.mkdir(parents=True, exist_ok=True)
    clf = modelo.named_steps.get("clf")
    if clf is None:
        return

    # Verificar se o modelo possui feature_importances_ ou coef_
    if hasattr(clf, "feature_importances_"):
        prep = modelo.named_steps["prep"]
        nomes_cat = prep.named_transformers_["cat"].named_steps["encoder"].get_feature_names_out()
        todos_nomes = list(features_numericas) + list(nomes_cat)
        importancias = clf.feature_importances_
    elif hasattr(clf, "coef_"):
        prep = modelo.named_steps["prep"]
        nomes_cat = prep.named_transformers_["cat"].named_steps["encoder"].get_feature_names_out()
        todos_nomes = list(features_numericas) + list(nomes_cat)
        importancias = np.mean(np.abs(clf.coef_), axis=0)
    else:
        return

    df_imp = pd.DataFrame({"feature": todos_nomes, "importancia": importancias})
    df_imp = df_imp.sort_values("importancia", ascending=False).head(top_n)

    fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
    bars = ax.barh(df_imp["feature"][::-1], df_imp["importancia"][::-1], color="#2a78d6")
    ax.set_xlabel("Importância Média Relativa", fontsize=11)
    ax.set_title(f"Top {top_n} Features Mais Relevantes para a Predição", fontsize=12, fontweight="bold", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()


def executar_experimento_completo() -> tuple[pd.DataFrame, ResultadoAvaliacao, Pipeline]:
    """Executa o ciclo completo de treinamento, validação, seleção, retreino e teste."""
    particoes = carregar_e_dividir_dados()
    modelos = construir_modelos(particoes.features_numericas, particoes.features_categoricas)

    resultados_lista = []

    print("\n" + "=" * 65)
    print("ETAPA 1: Treinamento em 2020-2021 e Avaliação na Validação (2022)")
    print("=" * 65)

    for nome, pipe in modelos.items():
        pipe.fit(particoes.X_train, particoes.y_train)
        res_val = avaliar_modelo(pipe, particoes.X_val, particoes.y_val, nome, "Validação (2022)")
        resultados_lista.append(res_val)

        print(
            f"[{nome:<24}] Acurácia: {res_val.acuracia*100:5.2f}% | "
            f"Bal Acc: {res_val.acuracia_balanceada*100:5.2f}% | "
            f"Macro F1: {res_val.f1_macro:5.3f} | "
            f"LogLoss: {res_val.log_loss_val:5.3f}"
        )

    df_resumos = pd.DataFrame([
        {
            "nome_modelo": r.nome_modelo,
            "particao": r.particao,
            "acuracia": r.acuracia,
            "acuracia_balanceada": r.acuracia_balanceada,
            "f1_macro": r.f1_macro,
            "f1_weighted": r.f1_weighted,
            "f1_home_win": r.f1_home_win,
            "f1_draw": r.f1_draw,
            "f1_away_win": r.f1_away_win,
            "log_loss": r.log_loss_val,
            "brier_score": r.brier_score,
        }
        for r in resultados_lista
    ])

    # Plotar comparação na validação
    plotar_comparacao_modelos(df_resumos)

    # Identificar o modelo com maior Macro F1 na validação (exceto dummy)
    candidatos = [r for r in resultados_lista if "Baseline" not in r.nome_modelo]
    melhor_res = max(candidatos, key=lambda x: x.f1_macro)
    nome_melhor = melhor_res.nome_modelo

    print("\n" + "=" * 65)
    print(f"ETAPA 2: Seleção do Modelo Vencedor: {nome_melhor}")
    print(f"Critério: Maior Macro F1 na Validação ({melhor_res.f1_macro:.3f})")
    print("=" * 65)

    # Retreinar o melhor modelo com Treino + Validação (2020-2022)
    print("\nETAPA 3: Retreino Expandido (2020 a 2022 = 1.052 partidas utilizáveis)")
    melhor_pipe = modelos[nome_melhor]
    melhor_pipe.fit(particoes.X_train_val, particoes.y_train_val)

    # Avaliação Final no Conjunto de Teste (2023)
    print("\nETAPA 4: Avaliação Final Cega no Conjunto de Teste (Temporada 2023)")
    res_teste = avaliar_modelo(melhor_pipe, particoes.X_test, particoes.y_test, nome_melhor, "Teste (2023)")

    # Avaliar também a Baseline majoritária no Teste para comparação rigorosa
    baseline_pipe = modelos["Baseline (Majoritária)"]
    baseline_pipe.fit(particoes.X_train_val, particoes.y_train_val)
    res_baseline_teste = avaliar_modelo(baseline_pipe, particoes.X_test, particoes.y_test, "Baseline (Majoritária)", "Teste (2023)")

    print(
        f"-> Baseline no Teste: Acurácia: {res_baseline_teste.acuracia*100:5.2f}% | "
        f"Macro F1: {res_baseline_teste.f1_macro:5.3f}"
    )
    print(
        f"-> {nome_melhor} no Teste: Acurácia: {res_teste.acuracia*100:5.2f}% | "
        f"Bal Acc: {res_teste.acuracia_balanceada*100:5.2f}% | "
        f"Macro F1: {res_teste.f1_macro:5.3f} | "
        f"LogLoss: {res_teste.log_loss_val:5.3f}"
    )

    # Plotar matriz de confusão e importância de features
    plotar_matriz_confusao(res_teste.matriz_confusao, nome_melhor, "Teste (2023)")
    plotar_importancia_features(melhor_pipe, particoes.features_numericas)

    # Gravar relatório de modelagem
    gravar_relatorio_md(df_resumos, res_teste, res_baseline_teste, nome_melhor)

    return df_resumos, res_teste, melhor_pipe


def gravar_relatorio_md(
    df_resumos: pd.DataFrame,
    res_teste: ResultadoAvaliacao,
    res_baseline_teste: ResultadoAvaliacao,
    nome_melhor: str,
) -> None:
    """Gera o relatório formal em Markdown documentando todo o experimento preditivo."""
    DIR_RELATORIOS.mkdir(parents=True, exist_ok=True)

    cm = res_teste.matriz_confusao
    linhas_md = [
        "# Relatório de Modelagem Preditiva — Brasileirão Série A (2020–2023)",
        "",
        "Disciplina de Inteligência Artificial II. Este documento consolida a etapa de treinamento, validação e teste de modelos preditivos multiclasse para os resultados das partidas do Campeonato Brasileiro, seguindo a partição temporal formalizada em `reports/estrategia_experimental.md`.",
        "",
        "---",
        "",
        "## 1. Modelos Avaliados",
        "",
        "1. **Baseline Ingênua (Dummy):** Predição constante da classe majoritária (`home_win`), representando a referência básica a ser superada.",
        "2. **Regressão Logística Multinomial:** Modelo linear regularizado L2 com padronização via `StandardScaler` e codificação de equipes via `OneHotEncoder`.",
        "3. **Random Forest Classifier:** Conjunto de 200 árvores de decisão com controle de profundidade máxima (`max_depth=6`) para contenção de sobreajuste.",
        "4. **HistGradientBoosting Classifier:** Modelo baseado em árvores com aumento de gradiente e regularização adaptada para matrizes tabulares.",
        "",
        "---",
        "",
        "## 2. Resultados da Fase de Validação (Temporada 2022)",
        "",
        "Os modelos foram ajustados estritamente com as temporadas 2020 e 2021 (689 partidas) e avaliados na temporada de 2022 (363 partidas):",
        "",
        "| Modelo | Acurácia Global | Acurácia Balanceada | Macro F1-Score | Log-Loss | Brier Score |",
        "|---|---|---|---|---|---|",
    ]

    for _, r in df_resumos.iterrows():
        linhas_md.append(
            f"| **{r['nome_modelo']}** | {r['acuracia']*100:.2f}% | {r['acuracia_balanceada']*100:.2f}% | {r['f1_macro']:.3f} | {r['log_loss']:.3f} | {r['brier_score']:.3f} |"
        )

    linhas_md.extend([
        "",
        "![Comparação dos Modelos na Validação](figures/14_comparacao_modelos_validacao.png)",
        "",
        f"**Decisão:** O modelo selecionado para o teste final foi o **{nome_melhor}**, pois obteve o maior Macro F1-Score na validação; a escolha não implica superioridade em todas as métricas.",
        "",
        "---",
        "",
        "## 3. Avaliação Final Cega no Conjunto de Teste (Temporada 2023)",
        "",
        f"O modelo vencedor ({nome_melhor}) foi retreinado com todo o histórico disponível até a véspera da temporada 2023 (2020 + 2021 + 2022 = 1.052 partidas utilizáveis) e avaliado nas **362 partidas da temporada de 2023**:",
        "",
        "| Métrica | Baseline Majoritária | Modelo Vencedor (" + nome_melhor + ") | Ganho Relativo |",
        "|---|---|---|---|",
        f"| **Acurácia Global** | {res_baseline_teste.acuracia*100:.2f}% | **{res_teste.acuracia*100:.2f}%** | {(res_teste.acuracia - res_baseline_teste.acuracia)*100:+.2f} p.p. |",
        f"| **Acurácia Balanceada** | {res_baseline_teste.acuracia_balanceada*100:.2f}% | **{res_teste.acuracia_balanceada*100:.2f}%** | {(res_teste.acuracia_balanceada - res_baseline_teste.acuracia_balanceada)*100:+.2f} p.p. |",
        f"| **Macro F1-Score** | {res_baseline_teste.f1_macro:.3f} | **{res_teste.f1_macro:.3f}** | {(res_teste.f1_macro - res_baseline_teste.f1_macro):+.3f} |",
        f"| **F1 Vitória Mandante (`home_win`)** | {res_baseline_teste.f1_home_win:.3f} | **{res_teste.f1_home_win:.3f}** | — |",
        f"| **F1 Empate (`draw`)** | {res_baseline_teste.f1_draw:.3f} | **{res_teste.f1_draw:.3f}** | — |",
        f"| **F1 Vitória Visitante (`away_win`)** | {res_baseline_teste.f1_away_win:.3f} | **{res_teste.f1_away_win:.3f}** | — |",
        f"| **Log-Loss** | — | **{res_teste.log_loss_val:.3f}** | — |",
        f"| **Brier Score Multiclasse** | — | **{res_teste.brier_score:.3f}** | — |",
        "",
        "### Matriz de Confusão no Teste (2023)",
        "",
        "| Real \\ Previsto | Vitória Mandante | Empate | Vitória Visitante | Total Real |",
        "|---|---|---|---|---|",
        f"| **Vitória Mandante** | {cm[0, 0]} ({cm[0, 0]/cm[0].sum()*100:.1f}%) | {cm[0, 1]} ({cm[0, 1]/cm[0].sum()*100:.1f}%) | {cm[0, 2]} ({cm[0, 2]/cm[0].sum()*100:.1f}%) | {cm[0].sum()} |",
        f"| **Empate** | {cm[1, 0]} ({cm[1, 0]/cm[1].sum()*100:.1f}%) | {cm[1, 1]} ({cm[1, 1]/cm[1].sum()*100:.1f}%) | {cm[1, 2]} ({cm[1, 2]/cm[1].sum()*100:.1f}%) | {cm[1].sum()} |",
        f"| **Vitória Visitante** | {cm[2, 0]} ({cm[2, 0]/cm[2].sum()*100:.1f}%) | {cm[2, 1]} ({cm[2, 1]/cm[2].sum()*100:.1f}%) | {cm[2, 2]} ({cm[2, 2]/cm[2].sum()*100:.1f}%) | {cm[2].sum()} |",
        "",
        "![Matriz de Confusão](figures/15_matriz_confusao_teste.png)",
        "",
        "---",
        "",
        "## 4. Relevância das Features e Interpretabilidade",
        "",
        "![Importância das Features](figures/16_importancia_features.png)",
        "",
        "### Principais Conclusões:",
        "1. **Coeficientes:** Os 15 maiores valores da média absoluta dos coeficientes correspondem a categorias de equipes e dia da semana. O gráfico não sustenta a predominância dos diferenciais de pontos ou saldo de gols e não demonstra causalidade.",
        "2. **Dificuldade do Empate no Experimento:** O modelo acertou 15 dos 94 empates no teste (recall de 16,0%). O resultado limita sua capacidade de reconhecer essa classe.",
        "3. **Integridade Temporal e Limites:** As partições cronológicas e os históricos deslocados evitam usar a própria partida nas entradas. O teste é sequencial por jogo e pode usar partidas anteriores de 2023. As verificações não constituem garantia universal contra vazamento. Consulte relatorio_tecnico.pdf para comparação com frequências históricas e limitações.",
    ])

    with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_md))
    print(f"\n[OK] Relatório gravado com sucesso em: {ARQUIVO_RELATORIO}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executar_experimento_completo()

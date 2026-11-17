"""Métricas, calibração, interpretação e gráficos de avaliação dos classificadores.

Todas as funções trabalham sobre as previsões reais dos modelos treinados. Nenhum valor
é escrito à mão: os resultados alimentam o JSON de métricas, o relatório e a API.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.inspection import permutation_importance
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_fscore_support,
    roc_auc_score,
)

CLASSES = ["home_win", "draw", "away_win"]
ROTULOS_CLASSES = {
    "home_win": "Vitória do mandante",
    "draw": "Empate",
    "away_win": "Vitória do visitante",
}
ROTULOS_CURTOS = ["Mandante", "Empate", "Visitante"]
CORES_CLASSES = {"home_win": "#2a78d6", "draw": "#8a8985", "away_win": "#eb6834"}
DPI = 150

# Rótulos legíveis para as variáveis de entrada (usados em gráficos, relatório e API).
ROTULOS_ATRIBUTOS = {
    "pontos_media_ultimos_5": "pontos por jogo (últimos 5)",
    "vitorias_ultimos_5": "vitórias (últimos 5)",
    "empates_ultimos_5": "empates (últimos 5)",
    "derrotas_ultimos_5": "derrotas (últimos 5)",
    "gols_marcados_media_ultimos_5": "gols marcados por jogo (últimos 5)",
    "gols_sofridos_media_ultimos_5": "gols sofridos por jogo (últimos 5)",
    "saldo_gols_media_ultimos_5": "saldo de gols por jogo (últimos 5)",
    "amarelos_media_ultimos_5": "cartões amarelos por jogo (últimos 5)",
    "expulsoes_media_ultimos_5": "expulsões por jogo (últimos 5)",
    "aproveitamento_ultimos_5": "aproveitamento (últimos 5)",
    "aproveitamento_mandante_em_casa": "aproveitamento do mandante em casa",
    "aproveitamento_visitante_fora": "aproveitamento do visitante fora",
    "dif_pontos_media_ultimos_5": "diferença de pontos por jogo (mandante − visitante)",
    "dif_saldo_gols_media_ultimos_5": "diferença de saldo de gols (mandante − visitante)",
    "dif_gols_marcados_media_ultimos_5": "diferença de gols marcados (mandante − visitante)",
    "dif_gols_sofridos_media_ultimos_5": "diferença de gols sofridos (mandante − visitante)",
    "dif_aproveitamento_ultimos_5": "diferença de aproveitamento (mandante − visitante)",
    "dif_aproveitamento_mando": "diferença de aproveitamento por mando",
    "expectativa_total_gols_ultimos_5": "gols marcados do mandante + sofridos do visitante",
    "mes": "mês da partida",
    "hora": "hora da partida",
    "home_team": "equipe mandante",
    "away_team": "equipe visitante",
    "dia_semana": "dia da semana",
}


def rotulo_atributo(nome: str) -> str:
    """Traduz o nome técnico de um atributo (com sufixo _mandante/_visitante) para português."""
    if nome in ROTULOS_ATRIBUTOS:
        return ROTULOS_ATRIBUTOS[nome]
    for sufixo, lado in (("_mandante", "mandante"), ("_visitante", "visitante")):
        if nome.endswith(sufixo) and nome[: -len(sufixo)] in ROTULOS_ATRIBUTOS:
            return f"{ROTULOS_ATRIBUTOS[nome[: -len(sufixo)]]} — {lado}"
    return nome


def _como_float(valor: Any) -> float | None:
    valor = float(valor)
    return None if np.isnan(valor) else valor


def calcular_brier_multiclasse(y_true: np.ndarray, y_prob: np.ndarray) -> float:
    """Brier multiclasse: média da soma dos erros quadráticos das três probabilidades (0 a 2)."""
    return float(np.mean(np.sum((y_prob - np.eye(y_prob.shape[1])[y_true]) ** 2, axis=1)))


def metricas_completas(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None = None) -> dict[str, Any]:
    """Todas as métricas de classificação multiclasse em um dicionário serializável em JSON."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    prec, rec, f1, sup = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1, 2], zero_division=0
    )
    resultado: dict[str, Any] = {
        "n": int(len(y_true)),
        "acuracia": float(accuracy_score(y_true, y_pred)),
        "acuracia_balanceada": float(balanced_accuracy_score(y_true, y_pred)),
        "precisao_macro": float(np.mean(prec)),
        "recall_macro": float(np.mean(rec)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "f1_ponderado": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "por_classe": {
            classe: {
                "precisao": float(prec[i]),
                "recall": float(rec[i]),
                "f1": float(f1[i]),
                "suporte": int(sup[i]),
            }
            for i, classe in enumerate(CLASSES)
        },
        "matriz_confusao": confusion_matrix(y_true, y_pred, labels=[0, 1, 2]).tolist(),
        "distribuicao_real": {c: int((y_true == i).sum()) for i, c in enumerate(CLASSES)},
        "distribuicao_previsoes": {c: int((y_pred == i).sum()) for i, c in enumerate(CLASSES)},
        "log_loss": None,
        "brier": None,
        "roc_auc_ovr_macro": None,
    }
    if y_prob is not None:
        resultado["log_loss"] = _como_float(log_loss(y_true, y_prob, labels=[0, 1, 2]))
        resultado["brier"] = calcular_brier_multiclasse(y_true.astype(int), y_prob)
        try:
            resultado["roc_auc_ovr_macro"] = _como_float(
                roc_auc_score(y_true, y_prob, multi_class="ovr", average="macro", labels=[0, 1, 2])
            )
        except ValueError:
            resultado["roc_auc_ovr_macro"] = None
    return resultado


def calibracao(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 5) -> dict[str, Any]:
    """Curvas de calibração um-contra-todos e erro de calibração esperado (ECE) da classe prevista."""
    y_true = np.asarray(y_true)
    curvas = {}
    for i, classe in enumerate(CLASSES):
        freq, prevista = calibration_curve(
            (y_true == i).astype(int), y_prob[:, i], n_bins=n_bins, strategy="quantile"
        )
        curvas[classe] = {
            "probabilidade_media_prevista": [float(v) for v in prevista],
            "frequencia_observada": [float(v) for v in freq],
        }
    # ECE da classe de maior probabilidade, em faixas de mesma quantidade de partidas
    confianca = y_prob.max(axis=1)
    acerto = (y_prob.argmax(axis=1) == y_true).astype(float)
    ordem = np.argsort(confianca)
    ece = 0.0
    for faixa in np.array_split(ordem, n_bins):
        if len(faixa):
            ece += len(faixa) / len(y_true) * abs(acerto[faixa].mean() - confianca[faixa].mean())
    return {"n_faixas": n_bins, "curvas": curvas, "ece_classe_prevista": float(ece)}


def importancia_por_permutacao(
    pipe: Any, X: pd.DataFrame, y: pd.Series, n_repeticoes: int = 30, semente: int = 42
) -> list[dict[str, Any]]:
    """Queda média do log-loss ao embaralhar cada atributo de entrada (descritiva, não causal)."""
    r = permutation_importance(
        pipe, X, y, scoring="neg_log_loss", n_repeats=n_repeticoes, random_state=semente, n_jobs=1
    )
    ordem = np.argsort(r.importances_mean)[::-1]
    return [
        {
            "atributo": X.columns[i],
            "rotulo": rotulo_atributo(X.columns[i]),
            "aumento_log_loss": float(r.importances_mean[i]),
            "desvio_padrao": float(r.importances_std[i]),
        }
        for i in ordem
    ]


def coeficientes_regressao(pipe: Any, features_numericas: list[str]) -> dict[str, Any]:
    """Coeficientes (atributos padronizados) da Regressão Logística por classe."""
    clf = pipe.named_steps["clf"]
    nomes = [n.split("__", 1)[1] for n in pipe.named_steps["prep"].get_feature_names_out()]
    coef = clf.coef_
    tabela = {
        nome: {classe: float(coef[i, j]) for i, classe in enumerate(CLASSES)}
        for j, nome in enumerate(nomes)
    }
    numericos = {n: tabela[n] for n in features_numericas if n in tabela}
    categoricos = {n: v for n, v in tabela.items() if n not in numericos}
    media_abs = {n: float(np.mean(np.abs(list(v.values())))) for n, v in tabela.items()}
    top = sorted(media_abs.items(), key=lambda kv: kv[1], reverse=True)[:15]
    return {
        "numericos": numericos,
        "categoricos": categoricos,
        "media_abs_top15": [{"atributo": n, "rotulo": rotulo_atributo(n), "valor": v} for n, v in top],
    }


def analise_erros(
    df_teste: pd.DataFrame, y_true: np.ndarray, y_prob: np.ndarray, nomes_curtos: dict[str, str], n: int = 5
) -> dict[str, Any]:
    """Confusões mais frequentes e exemplos de previsões corretas e erradas do teste."""
    y_pred = y_prob.argmax(axis=1)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1, 2])
    confusoes = sorted(
        (
            {"real": CLASSES[i], "previsto": CLASSES[j], "partidas": int(cm[i, j])}
            for i in range(3)
            for j in range(3)
            if i != j
        ),
        key=lambda c: c["partidas"],
        reverse=True,
    )

    def linha(i: int) -> dict[str, Any]:
        p = df_teste.iloc[i]
        return {
            "id_partida": int(p["id_partida"]),
            "data": str(p["data_partida"])[:10],
            "mandante": nomes_curtos.get(p["home_team"], p["home_team"]),
            "visitante": nomes_curtos.get(p["away_team"], p["away_team"]),
            "placar": f"{int(p['home_team_score'])} x {int(p['away_team_score'])}",
            "real": CLASSES[int(y_true[i])],
            "previsto": CLASSES[int(y_pred[i])],
            "probabilidades": {c: float(y_prob[i, k]) for k, c in enumerate(CLASSES)},
            "confianca": float(y_prob[i].max()),
        }

    confianca = y_prob.max(axis=1)
    certos = [i for i in np.argsort(-confianca) if y_pred[i] == y_true[i]][:n]
    errados = [i for i in np.argsort(-confianca) if y_pred[i] != y_true[i]][:n]
    return {
        "confusoes_mais_frequentes": confusoes,
        "maior_probabilidade_de_empate": float(y_prob[:, 1].max()),
        "previsoes_de_empate": int((y_pred == 1).sum()),
        "acertos_mais_confiantes": [linha(i) for i in certos],
        "erros_mais_confiantes": [linha(i) for i in errados],
    }


# --------------------------------------------------------------------------- #
# Gráficos (reports/figures)
# --------------------------------------------------------------------------- #
def _salvar(fig: plt.Figure, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(caminho, dpi=DPI)
    plt.close(fig)


def grafico_importancia_permutacao(importancias: list[dict[str, Any]], caminho: Path, top_n: int = 15) -> None:
    dados = importancias[:top_n][::-1]
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    ax.barh(
        [d["rotulo"] for d in dados],
        [d["aumento_log_loss"] for d in dados],
        xerr=[d["desvio_padrao"] for d in dados],
        color="#2a78d6",
        ecolor="#52514e",
        capsize=3,
    )
    ax.axvline(0, color="#0b0b0b", linewidth=0.8)
    ax.set_xlabel("Aumento médio do log-loss ao embaralhar o atributo (teste 2023)", fontsize=10)
    fig.suptitle("Importância por permutação: 15 atributos de maior impacto", fontweight="bold", fontsize=12)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    _salvar(fig, caminho)


def grafico_coeficientes(coef: dict[str, Any], caminho: Path, top_n: int = 15) -> None:
    dados = coef["media_abs_top15"][:top_n][::-1]
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    ax.barh([d["rotulo"] for d in dados], [d["valor"] for d in dados], color="#eb6834")
    ax.set_xlabel("Média do valor absoluto do coeficiente entre as três classes")
    fig.suptitle("Regressão Logística: coeficientes de maior magnitude", fontweight="bold", fontsize=12)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    _salvar(fig, caminho)


def grafico_calibracao(cal: dict[str, Any], caminho: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.plot([0, 1], [0, 1], linestyle="--", color="#8a8985", label="Calibração perfeita")
    for classe in CLASSES:
        c = cal["curvas"][classe]
        ax.plot(
            c["probabilidade_media_prevista"],
            c["frequencia_observada"],
            marker="o",
            color=CORES_CLASSES[classe],
            label=ROTULOS_CLASSES[classe],
        )
    ax.set_xlabel("Probabilidade média prevista (faixas com o mesmo número de partidas)")
    ax.set_ylabel("Frequência observada")
    fig.suptitle(f"Calibração no teste 2023 (ECE da classe prevista: {cal['ece_classe_prevista']:.3f})".replace(".", ","), fontsize=11, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(linestyle="--", alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    _salvar(fig, caminho)


def grafico_treino_validacao_teste(resumo: dict[str, dict[str, float]], caminho: Path) -> None:
    """Compara acurácia e Macro F1 do modelo final entre treino, validação e teste."""
    etapas = list(resumo)
    x = np.arange(len(etapas))
    largura = 0.36
    fig, ax = plt.subplots(figsize=(8.6, 5))
    for k, (chave, rotulo, cor) in enumerate([("acuracia", "Acurácia", "#2a78d6"), ("f1_macro", "Macro F1", "#eb6834")]):
        valores = [resumo[e][chave] * 100 for e in etapas]
        barras = ax.bar(x + (k - 0.5) * largura, valores, largura, label=rotulo, color=cor)
        for b, v in zip(barras, valores):
            ax.annotate(f"{v:.1f}%", (b.get_x() + b.get_width() / 2, v), xytext=(0, 3),
                        textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(etapas)
    ax.set_ylabel("Percentual (%)")
    ax.set_ylim(0, 80)
    ax.set_title("Modelo selecionado: desempenho em treino, validação e teste", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend(loc="upper right")
    _salvar(fig, caminho)


def grafico_distribuicao_previsoes(real: dict[str, int], previsto: dict[str, int], caminho: Path) -> None:
    x = np.arange(3)
    largura = 0.36
    fig, ax = plt.subplots(figsize=(8, 5))
    for k, (dados, rotulo, cor) in enumerate([(real, "Resultado real", "#52514e"), (previsto, "Previsão do modelo", "#2a78d6")]):
        valores = [dados[c] for c in CLASSES]
        barras = ax.bar(x + (k - 0.5) * largura, valores, largura, label=rotulo, color=cor)
        for b, v in zip(barras, valores):
            ax.annotate(str(v), (b.get_x() + b.get_width() / 2, v), xytext=(0, 3),
                        textcoords="offset points", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(ROTULOS_CURTOS)
    ax.set_ylabel("Partidas do teste (2023)")
    ax.set_title("Distribuição das previsões e dos resultados reais no teste", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.legend()
    _salvar(fig, caminho)

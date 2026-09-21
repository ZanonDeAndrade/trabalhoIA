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

import hashlib
import json
import logging
import platform
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Garante que a raiz do repositório esteja no sys.path
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.common import sha256_texto
from src.data_analysis import CSV_ORIGINAL, NOME_CURTO
from src.data_split import (
    CLASSES,
    CSV_PROCESSADO_PADRAO,
    RANDOM_STATE,
    ROTULO_RESULTADO,
    ParticoesDados,
    carregar_e_dividir_dados,
)
from src.evaluation import (
    analise_erros,
    calibracao,
    coeficientes_regressao,
    grafico_calibracao,
    grafico_coeficientes,
    grafico_distribuicao_previsoes,
    grafico_importancia_permutacao,
    grafico_treino_validacao_teste,
    importancia_por_permutacao,
    metricas_completas,
)


logger = logging.getLogger("modeling")

RAIZ = RAIZ_PROJETO
VERSAO_MODELO = "1.0.0"
DIR_RELATORIOS = RAIZ / "reports"
DIR_FIGURAS = DIR_RELATORIOS / "figures"
DIR_EVIDENCIAS = DIR_RELATORIOS / "evidencias"
DIR_MODELOS = RAIZ / "models"
ARQUIVO_MODELO = DIR_MODELOS / "model.joblib"
ARQUIVO_METADADOS = DIR_MODELOS / "metadata.json"
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
    precisao_macro: float = float("nan")
    recall_macro: float = float("nan")


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
        precisao_macro=float(precision_score(y_true, y_pred, average="macro", labels=[0, 1, 2], zero_division=0)),
        recall_macro=float(recall_score(y_true, y_pred, average="macro", labels=[0, 1, 2], zero_division=0)),
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

    fig, ax = plt.subplots(figsize=(7.6, 5.6), dpi=150)
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
    ax.set_yticklabels(rotulos_classes, fontsize=9.5, rotation=0, va="center")

    plt.tight_layout()
    plt.savefig(caminho_saida)
    plt.close()


def _hiperparametros(pipe: Pipeline) -> dict[str, Any]:
    """Hiperparâmetros configurados no estimador final (valores diferentes do padrão do scikit-learn)."""
    est = pipe.steps[-1][1]
    padrao = type(est)().get_params()
    saida: dict[str, Any] = {"algoritmo": type(est).__name__}
    for chave, valor in est.get_params().items():
        if not isinstance(valor, (bool, int, float, str)):
            continue
        if valor != padrao.get(chave) or chave in ("random_state", "solver"):
            saida[chave] = valor
    saida.pop("penalty", None)
    return saida


def _sha256(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def _distribuicao(y: pd.Series) -> dict[str, int]:
    return {c: int((y == i).sum()) for i, c in enumerate(CLASSES)}


def _prever(pipe: Pipeline, X: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    return pipe.predict(X), pipe.predict_proba(X)


def _avaliar_dict(pipe: Pipeline, X: pd.DataFrame, y: pd.Series) -> dict[str, Any]:
    pred, prob = _prever(pipe, X)
    return metricas_completas(y.to_numpy(), pred, prob)


def executar_experimento_completo(salvar: bool = True) -> dict[str, Any]:
    """Treina, valida, seleciona, reajusta, testa e (opcionalmente) persiste todos os artefatos.

    Protocolo (nada é decidido com o teste):
    1. ajuste em 2020-2021 e avaliação em 2022 para cada candidato;
    2. seleção do maior Macro F1 na validação, exceto a referência ingênua;
    3. reajuste do selecionado em 2020-2022;
    4. avaliação única no teste (2023).
    """
    particoes = carregar_e_dividir_dados()
    modelos = construir_modelos(particoes.features_numericas, particoes.features_categoricas)

    print("\n" + "=" * 65)
    print("ETAPA 1: Treinamento em 2020-2021 e avaliação na validação (2022)")
    print("=" * 65)
    por_modelo: dict[str, Any] = {}
    for nome, pipe in modelos.items():
        inicio = time.perf_counter()
        pipe.fit(particoes.X_train, particoes.y_train)
        tempo = time.perf_counter() - inicio
        por_modelo[nome] = {
            "hiperparametros": _hiperparametros(pipe),
            "tempo_treino_s": round(tempo, 3),
            "treino": _avaliar_dict(pipe, particoes.X_train, particoes.y_train),
            "validacao": _avaliar_dict(pipe, particoes.X_val, particoes.y_val),
        }
        v = por_modelo[nome]["validacao"]
        print(
            f"[{nome:<24}] Acurácia: {v['acuracia']*100:5.2f}% | Bal Acc: {v['acuracia_balanceada']*100:5.2f}% | "
            f"Macro F1: {v['f1_macro']:5.3f} | LogLoss: {v['log_loss']:5.3f}"
        )

    candidatos = {n: m for n, m in por_modelo.items() if "Baseline" not in n}
    nome_melhor = max(candidatos, key=lambda n: candidatos[n]["validacao"]["f1_macro"])
    print("\n" + "=" * 65)
    print(f"ETAPA 2: Modelo selecionado: {nome_melhor}")
    print(f"Critério: maior Macro F1 na validação ({por_modelo[nome_melhor]['validacao']['f1_macro']:.3f})")
    print("=" * 65)

    n_final = len(particoes.X_train_val)
    print(f"\nETAPA 3: Reajuste em 2020 a 2022 ({n_final} partidas utilizáveis)")
    melhor = modelos[nome_melhor]
    inicio = time.perf_counter()
    melhor.fit(particoes.X_train_val, particoes.y_train_val)
    tempo_final = time.perf_counter() - inicio

    print("\nETAPA 4: Avaliação final no teste (temporada 2023)")
    pred_teste, prob_teste = _prever(melhor, particoes.X_test)
    y_teste = particoes.y_test.to_numpy()
    teste = metricas_completas(y_teste, pred_teste, prob_teste)
    treino_final = _avaliar_dict(melhor, particoes.X_train_val, particoes.y_train_val)

    baselines = {}
    for chave, estrategia in (("majoritaria", "most_frequent"), ("frequencias", "prior")):
        dummy = DummyClassifier(strategy=estrategia).fit(particoes.X_train_val, particoes.y_train_val)
        baselines[chave] = _avaliar_dict(dummy, particoes.X_test, particoes.y_test)

    print(
        f"-> Baseline no teste: acurácia {baselines['majoritaria']['acuracia']*100:5.2f}% | "
        f"Macro F1 {baselines['majoritaria']['f1_macro']:5.3f}"
    )
    print(
        f"-> {nome_melhor} no teste: acurácia {teste['acuracia']*100:5.2f}% | "
        f"Bal Acc {teste['acuracia_balanceada']*100:5.2f}% | Macro F1 {teste['f1_macro']:5.3f} | "
        f"LogLoss {teste['log_loss']:5.3f}"
    )

    # Interpretação e diagnósticos (descritivos: não alteram o modelo escolhido)
    importancias = importancia_por_permutacao(melhor, particoes.X_test, particoes.y_test)
    coef = coeficientes_regressao(melhor, particoes.features_numericas) if hasattr(melhor.named_steps.get("clf"), "coef_") else None
    cal = calibracao(y_teste, prob_teste)
    erros = analise_erros(particoes.df_test, y_teste, prob_teste, NOME_CURTO)

    prep = melhor.named_steps["prep"]
    medianas_ok = bool(
        np.allclose(
            prep.named_transformers_["num"].named_steps["imputer"].statistics_,
            particoes.X_train_val[particoes.features_numericas].median().to_numpy(),
        )
    )

    exemplos = []
    for i in range(min(8, len(particoes.df_test))):
        p = particoes.df_test.iloc[i]
        exemplos.append({
            "id_partida": int(p["id_partida"]),
            "data": str(p["data_partida"]),
            "mandante": p["home_team"],
            "visitante": p["away_team"],
            "p_mandante": float(prob_teste[i, 0]),
            "p_empate": float(prob_teste[i, 1]),
            "p_visitante": float(prob_teste[i, 2]),
            "previsto": ROTULO_RESULTADO[CLASSES[int(pred_teste[i])]],
            "real": ROTULO_RESULTADO[CLASSES[int(y_teste[i])]],
            "placar": f"{int(p['home_team_score'])} x {int(p['away_team_score'])}",
            "acertou": bool(pred_teste[i] == y_teste[i]),
        })

    df_todas = pd.read_csv(CSV_PROCESSADO_PADRAO, usecols=["data_partida", "temporada"])
    agora = datetime.now(timezone.utc)
    resultados: dict[str, Any] = {
        "executado_em": agora.astimezone().isoformat(timespec="seconds"),
        "versao_modelo": VERSAO_MODELO,
        "random_state": RANDOM_STATE,
        "ambiente": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
            "joblib": joblib.__version__,
        },
        "sha256_csv_original": sha256_texto(CSV_ORIGINAL),
        "sha256_csv_processado": sha256_texto(CSV_PROCESSADO_PADRAO),
        "dados": {
            "partidas_base": int(len(df_todas)),
            "partidas_utilizaveis": int(len(particoes.X_train) + len(particoes.X_val) + len(particoes.X_test)),
            "periodo_inicio": str(df_todas["data_partida"].min())[:10],
            "periodo_fim": str(df_todas["data_partida"].max())[:10],
            "temporadas": sorted(int(t) for t in df_todas["temporada"].unique()),
        },
        "particoes": {
            "treino": {"temporadas": [2020, 2021], "n": len(particoes.X_train), "classes": _distribuicao(particoes.y_train)},
            "validacao": {"temporadas": [2022], "n": len(particoes.X_val), "classes": _distribuicao(particoes.y_val)},
            "teste": {"temporadas": [2023], "n": len(particoes.X_test), "classes": _distribuicao(particoes.y_test)},
            "treino_final": {"temporadas": [2020, 2021, 2022], "n": n_final, "classes": _distribuicao(particoes.y_train_val)},
        },
        "atributos": {
            "numericos": particoes.features_numericas,
            "categoricos": particoes.features_categoricas,
            "total": len(particoes.features_numericas) + len(particoes.features_categoricas),
        },
        "ausencias_atributos": {
            "treino": int(particoes.X_train.isna().any(axis=1).sum()),
            "validacao": int(particoes.X_val.isna().any(axis=1).sum()),
            "teste": int(particoes.X_test.isna().any(axis=1).sum()),
        },
        "medianas_apenas_treino_final": medianas_ok,
        "criterio_selecao": "maior Macro F1 na validação (2022), excluindo a referência majoritária",
        "modelo_selecionado": nome_melhor,
        "modelos": por_modelo,
        "final": {
            "nome": nome_melhor,
            "hiperparametros": _hiperparametros(melhor),
            "tempo_treino_s": round(tempo_final, 3),
            "treino_final": treino_final,
            "teste": teste,
        },
        "baselines_teste": baselines,
        "calibracao": cal,
        "importancia_permutacao": importancias,
        "coeficientes": coef,
        "analise_erros": erros,
        "exemplos": exemplos,
    }

    if salvar:
        salvar_artefatos(melhor, resultados, particoes)
        gerar_figuras(resultados, por_modelo, nome_melhor)
        gravar_relatorio_md(resultados)
    return resultados


def gerar_figuras(resultados: dict[str, Any], por_modelo: dict[str, Any], nome_melhor: str) -> None:
    """Grava as figuras 14 a 19 em reports/figures a partir dos resultados desta execução."""
    df_val = pd.DataFrame([
        {"nome_modelo": n, "particao": "Validação (2022)", **{k: m["validacao"][k] for k in ("acuracia", "acuracia_balanceada", "f1_macro")}}
        for n, m in por_modelo.items()
    ])
    plotar_comparacao_modelos(df_val)
    teste = resultados["final"]["teste"]
    plotar_matriz_confusao(np.array(teste["matriz_confusao"]), nome_melhor, "Teste (2023)")
    grafico_importancia_permutacao(resultados["importancia_permutacao"], DIR_FIGURAS / "16_importancia_permutacao.png")
    if resultados["coeficientes"]:
        grafico_coeficientes(resultados["coeficientes"], DIR_FIGURAS / "17_coeficientes_regressao_logistica.png")
    grafico_calibracao(resultados["calibracao"], DIR_FIGURAS / "18_calibracao_teste.png")
    grafico_treino_validacao_teste(
        {
            "Treino (2020-21)": por_modelo[nome_melhor]["treino"],
            "Validação (2022)": por_modelo[nome_melhor]["validacao"],
            "Teste (2023)": teste,
        },
        DIR_FIGURAS / "19_treino_validacao_teste.png",
    )
    grafico_distribuicao_previsoes(
        teste["distribuicao_real"], teste["distribuicao_previsoes"], DIR_FIGURAS / "20_distribuicao_previsoes.png"
    )


def salvar_artefatos(pipe: Pipeline, resultados: dict[str, Any], particoes: ParticoesDados) -> None:
    """Persiste o modelo final e seus metadados, além do JSON completo de métricas."""
    DIR_MODELOS.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, ARQUIVO_MODELO, compress=3)

    final = resultados["final"]
    metadados = {
        "versao": resultados["versao_modelo"],
        "data_treinamento": resultados["executado_em"],
        "algoritmo": final["nome"],
        "hiperparametros": final["hiperparametros"],
        "classes": CLASSES,
        "rotulos_classes": ROTULO_RESULTADO,
        "atributos_numericos": particoes.features_numericas,
        "atributos_categoricos": particoes.features_categoricas,
        "colunas_entrada": list(particoes.X_train.columns),
        "periodo_dados": {
            "inicio": resultados["dados"]["periodo_inicio"],
            "fim": resultados["dados"]["periodo_fim"],
            "temporadas": resultados["dados"]["temporadas"],
        },
        "particoes": resultados["particoes"],
        "treinado_com": "temporadas 2020 a 2022 (treino + validação)",
        "criterio_selecao": resultados["criterio_selecao"],
        "semente_aleatoria": resultados["random_state"],
        "metricas": {
            "treino_final": final["treino_final"],
            "validacao": resultados["modelos"][final["nome"]]["validacao"],
            "teste": final["teste"],
            "baselines_teste": resultados["baselines_teste"],
        },
        "calibracao_ece_classe_prevista": resultados["calibracao"]["ece_classe_prevista"],
        "tempo_treino_s": final["tempo_treino_s"],
        "dependencias": resultados["ambiente"],
        "sha256_csv_original": resultados["sha256_csv_original"],
        "sha256_csv_processado": resultados["sha256_csv_processado"],
        "arquivo_modelo": ARQUIVO_MODELO.name,
        "sha256_modelo": _sha256(ARQUIVO_MODELO),
    }
    ARQUIVO_METADADOS.write_text(json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")

    DIR_EVIDENCIAS.mkdir(parents=True, exist_ok=True)
    (DIR_EVIDENCIAS / "metricas_execucao.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (DIR_EVIDENCIAS / "previsoes_exemplo.json").write_text(
        json.dumps(resultados["exemplos"], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n[OK] Modelo salvo em {ARQUIVO_MODELO.relative_to(RAIZ)}")
    print(f"[OK] Metadados salvos em {ARQUIVO_METADADOS.relative_to(RAIZ)}")


def _pct(v: float) -> str:
    return f"{v * 100:.2f}%"


def gravar_relatorio_md(resultados: dict[str, Any]) -> None:
    """Relatório de modelagem em Markdown. Todos os números vêm de ``resultados``."""
    DIR_RELATORIOS.mkdir(parents=True, exist_ok=True)
    nome = resultados["final"]["nome"]
    teste = resultados["final"]["teste"]
    base = resultados["baselines_teste"]["majoritaria"]
    freq = resultados["baselines_teste"]["frequencias"]
    part = resultados["particoes"]
    cm = teste["matriz_confusao"]

    def total(i: int) -> int:
        return sum(cm[i])

    linhas = [
        "# Relatório de modelagem — Brasileirão Série A (2020–2023)",
        "",
        "Este arquivo é **gerado por `python src/modeling.py`**; todos os números vêm da execução registrada em "
        f"`reports/evidencias/metricas_execucao.json` (executada em {resultados['executado_em']}).",
        "",
        "## 1. Protocolo",
        "",
        f"- Treino: temporadas 2020–2021 ({part['treino']['n']} partidas).",
        f"- Validação e seleção: 2022 ({part['validacao']['n']} partidas).",
        f"- Teste: 2023 ({part['teste']['n']} partidas), usado uma única vez após a escolha.",
        f"- Reajuste do modelo selecionado: 2020–2022 ({part['treino_final']['n']} partidas).",
        f"- Critério de seleção: {resultados['criterio_selecao']}.",
        "",
        "## 2. Modelos, hiperparâmetros e tempo de treinamento",
        "",
        "| Modelo | Hiperparâmetros principais | Tempo de ajuste (2020–2021) |",
        "|---|---|---|",
    ]
    for n, m in resultados["modelos"].items():
        h = {k: v for k, v in m["hiperparametros"].items() if k in (
            "strategy", "C", "solver", "max_iter", "n_estimators", "max_depth", "min_samples_leaf",
            "learning_rate", "random_state")}
        linhas.append(f"| {n} | {', '.join(f'{k}={v}' for k, v in h.items()) or '—'} | {m['tempo_treino_s']:.3f} s |")

    linhas += [
        "",
        "## 3. Desempenho por partição",
        "",
        "| Modelo | Partição | Acurácia | Acurácia bal. | Precisão macro | Recall macro | Macro F1 | Log-Loss | Brier |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for n, m in resultados["modelos"].items():
        for rotulo, chave in (("Treino 2020–21", "treino"), ("Validação 2022", "validacao")):
            r = m[chave]
            linhas.append(
                f"| {n} | {rotulo} | {_pct(r['acuracia'])} | {_pct(r['acuracia_balanceada'])} | {r['precisao_macro']:.3f} | "
                f"{r['recall_macro']:.3f} | {r['f1_macro']:.3f} | {r['log_loss']:.3f} | {r['brier']:.3f} |"
            )
    linhas += [
        "",
        "![Comparação dos modelos na validação](figures/14_comparacao_modelos_validacao.png)",
        "",
        f"**Modelo selecionado:** {nome}. A escolha pelo Macro F1 não implica superioridade em todas as métricas.",
        "",
        "## 4. Avaliação final no teste (2023)",
        "",
        "| Métrica | Baseline majoritária | Frequências históricas | " + nome + " |",
        "|---|---|---|---|",
        f"| Acurácia | {_pct(base['acuracia'])} | {_pct(freq['acuracia'])} | **{_pct(teste['acuracia'])}** |",
        f"| Acurácia balanceada | {_pct(base['acuracia_balanceada'])} | {_pct(freq['acuracia_balanceada'])} | **{_pct(teste['acuracia_balanceada'])}** |",
        f"| Precisão macro | {base['precisao_macro']:.3f} | {freq['precisao_macro']:.3f} | **{teste['precisao_macro']:.3f}** |",
        f"| Recall macro | {base['recall_macro']:.3f} | {freq['recall_macro']:.3f} | **{teste['recall_macro']:.3f}** |",
        f"| Macro F1 | {base['f1_macro']:.3f} | {freq['f1_macro']:.3f} | **{teste['f1_macro']:.3f}** |",
        f"| Log-Loss | — | {freq['log_loss']:.3f} | **{teste['log_loss']:.3f}** |",
        f"| Brier | — | {freq['brier']:.3f} | **{teste['brier']:.3f}** |",
        f"| ROC AUC (um-contra-todos, macro) | — | {freq['roc_auc_ovr_macro']:.3f} | **{teste['roc_auc_ovr_macro']:.3f}** |",
        "",
        "Log-Loss e Brier não se aplicam à baseline majoritária (probabilidades 0 ou 1).",
        "",
        "### Métricas por classe (teste)",
        "",
        "| Classe | Precisão | Recall | F1 | Suporte |",
        "|---|---|---|---|---|",
    ]
    for c in CLASSES:
        r = teste["por_classe"][c]
        linhas.append(f"| {ROTULO_RESULTADO[c]} | {r['precisao']:.3f} | {r['recall']:.3f} | {r['f1']:.3f} | {r['suporte']} |")
    linhas += [
        "",
        "### Matriz de confusão (teste)",
        "",
        "| Real \\ Previsto | Mandante | Empate | Visitante | Total |",
        "|---|---|---|---|---|",
    ]
    for i, c in enumerate(CLASSES):
        linhas.append(
            f"| {ROTULO_RESULTADO[c]} | " + " | ".join(f"{cm[i][j]} ({cm[i][j] / total(i) * 100:.1f}%)" for j in range(3)) + f" | {total(i)} |"
        )
    linhas += [
        "",
        "![Matriz de confusão](figures/15_matriz_confusao_teste.png)",
        "![Distribuição das previsões](figures/20_distribuicao_previsoes.png)",
        "![Treino, validação e teste](figures/19_treino_validacao_teste.png)",
        "![Calibração](figures/18_calibracao_teste.png)",
        "",
        "## 5. Interpretação",
        "",
        "![Importância por permutação](figures/16_importancia_permutacao.png)",
        "",
        "Importância por permutação e coeficientes descrevem associações do modelo; **não são causalidade**.",
        "",
        "| Atributo | Aumento do log-loss ± desvio |",
        "|---|---|",
    ]
    for d in resultados["importancia_permutacao"][:10]:
        linhas.append(f"| {d['rotulo']} | {d['aumento_log_loss']:.4f} ± {d['desvio_padrao']:.4f} |")
    linhas += ["", "## 6. Erros mais confiantes no teste", "", "| Data | Confronto | Placar | Previsto | Real | Confiança |", "|---|---|---|---|---|---|"]
    for e in resultados["analise_erros"]["erros_mais_confiantes"]:
        linhas.append(
            f"| {e['data']} | {e['mandante']} x {e['visitante']} | {e['placar']} | {ROTULO_RESULTADO[e['previsto']]} | "
            f"{ROTULO_RESULTADO[e['real']]} | {e['confianca']:.1%} |"
        )
    ARQUIVO_RELATORIO.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"[OK] Relatório gravado em {ARQUIVO_RELATORIO.relative_to(RAIZ)}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executar_experimento_completo()

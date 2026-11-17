"""Treinamento, métricas, persistência e compatibilidade do artefato do modelo."""
from __future__ import annotations

import json

import joblib
import numpy as np
import pytest

from src.data_split import CLASSES, carregar_e_dividir_dados
from src.evaluation import calibracao, metricas_completas
from src.modeling import ARQUIVO_METADADOS, ARQUIVO_MODELO, construir_modelos


@pytest.fixture(scope="module")
def particoes():
    return carregar_e_dividir_dados()


@pytest.fixture(scope="module")
def metadados():
    return json.loads(ARQUIVO_METADADOS.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def modelo():
    return joblib.load(ARQUIVO_MODELO)


def test_metricas_de_exemplo_calculadas_a_mao():
    # real:     0 0 0 0 1 1 2 2   previsto: 0 0 1 2 1 0 2 2
    y = np.array([0, 0, 0, 0, 1, 1, 2, 2])
    p = np.array([0, 0, 1, 2, 1, 0, 2, 2])
    m = metricas_completas(y, p)
    assert m["acuracia"] == pytest.approx(5 / 8)
    assert m["matriz_confusao"] == [[2, 1, 1], [1, 1, 0], [0, 0, 2]]
    assert m["por_classe"]["home_win"]["precisao"] == pytest.approx(2 / 3)
    assert m["por_classe"]["home_win"]["recall"] == pytest.approx(2 / 4)
    assert m["por_classe"]["draw"]["precisao"] == pytest.approx(1 / 2)
    assert m["recall_macro"] == pytest.approx((2 / 4 + 1 / 2 + 1) / 3)
    assert m["acuracia_balanceada"] == pytest.approx(m["recall_macro"])
    assert m["distribuicao_previsoes"] == {"home_win": 3, "draw": 2, "away_win": 3}


def test_log_loss_e_brier_de_exemplo_simples():
    y = np.array([0, 1, 2])
    prob = np.array([[0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.1, 0.8]])
    m = metricas_completas(y, prob.argmax(axis=1), prob)
    assert m["log_loss"] == pytest.approx(-np.mean(np.log([0.8, 0.6, 0.8])))
    esperado = np.mean([0.2**2 + 0.1**2 + 0.1**2, 0.2**2 + 0.4**2 + 0.2**2, 0.1**2 + 0.1**2 + 0.2**2])
    assert m["brier"] == pytest.approx(esperado)


def test_calibracao_de_previsoes_perfeitas_tem_ece_pequeno():
    rng = np.random.default_rng(0)
    prob = rng.dirichlet([1, 1, 1], size=600)
    y = np.array([rng.choice(3, p=p) for p in prob])  # rótulos sorteados a partir das próprias probabilidades
    assert calibracao(y, prob)["ece_classe_prevista"] < 0.08


def test_baseline_preve_sempre_a_classe_mais_frequente_do_treino(particoes):
    dummy = construir_modelos(particoes.features_numericas, particoes.features_categoricas)["Baseline (Majoritária)"]
    dummy.fit(particoes.X_train, particoes.y_train)
    assert set(dummy.predict(particoes.X_test)) == {int(particoes.y_train.mode()[0])} == {0}


def test_treinamento_e_previsao_de_todos_os_algoritmos(particoes):
    for nome, pipe in construir_modelos(particoes.features_numericas, particoes.features_categoricas).items():
        pipe.fit(particoes.X_train, particoes.y_train)
        prob = pipe.predict_proba(particoes.X_val)
        assert prob.shape == (len(particoes.X_val), 3), nome
        assert np.allclose(prob.sum(axis=1), 1.0), nome
        assert ((prob >= 0) & (prob <= 1)).all(), nome
        assert set(pipe.predict(particoes.X_val)) <= {0, 1, 2}, nome


def test_treinamento_e_reprodutivel_com_a_mesma_semente(particoes):
    def coeficientes():
        pipe = construir_modelos(particoes.features_numericas, particoes.features_categoricas)["Regressão Logística"]
        return pipe.fit(particoes.X_train_val, particoes.y_train_val).named_steps["clf"].coef_

    np.testing.assert_array_equal(coeficientes(), coeficientes())


def test_persistencia_preserva_as_previsoes(particoes, tmp_path):
    pipe = construir_modelos(particoes.features_numericas, particoes.features_categoricas)["Regressão Logística"]
    pipe.fit(particoes.X_train, particoes.y_train)
    destino = tmp_path / "m.joblib"
    joblib.dump(pipe, destino)
    recarregado = joblib.load(destino)
    np.testing.assert_allclose(pipe.predict_proba(particoes.X_test), recarregado.predict_proba(particoes.X_test))


def test_artefatos_do_modelo_existem_e_estao_completos(metadados):
    assert ARQUIVO_MODELO.exists() and ARQUIVO_METADADOS.exists()
    for chave in ("versao", "data_treinamento", "algoritmo", "hiperparametros", "classes", "atributos_numericos",
                  "atributos_categoricos", "colunas_entrada", "periodo_dados", "semente_aleatoria", "metricas",
                  "dependencias", "sha256_modelo"):
        assert chave in metadados, chave
    assert metadados["classes"] == CLASSES
    assert metadados["semente_aleatoria"] == 42
    assert {"python", "numpy", "pandas", "scikit_learn", "joblib"} <= set(metadados["dependencias"])


def test_modelo_salvo_e_compativel_com_as_variaveis_do_projeto(modelo, metadados, particoes):
    assert metadados["colunas_entrada"] == list(particoes.X_train.columns)
    assert list(modelo.named_steps["clf"].classes_) == [0, 1, 2]
    assert modelo.feature_names_in_.tolist() == metadados["colunas_entrada"] if hasattr(modelo, "feature_names_in_") else True


def test_metricas_registradas_correspondem_ao_modelo_salvo(modelo, metadados, particoes):
    """As métricas de teste dos metadados devem ser reproduzíveis com o artefato persistido."""
    pred = modelo.predict(particoes.X_test)
    prob = modelo.predict_proba(particoes.X_test)
    m = metricas_completas(particoes.y_test.to_numpy(), pred, prob)
    reg = metadados["metricas"]["teste"]
    assert m["acuracia"] == pytest.approx(reg["acuracia"])
    assert m["f1_macro"] == pytest.approx(reg["f1_macro"])
    assert m["log_loss"] == pytest.approx(reg["log_loss"])
    assert m["matriz_confusao"] == reg["matriz_confusao"]


def test_modelo_salvo_foi_treinado_apenas_ate_2022(modelo, particoes):
    imputador = modelo.named_steps["prep"].named_transformers_["num"].named_steps["imputer"]
    np.testing.assert_allclose(imputador.statistics_, particoes.X_train_val[particoes.features_numericas].median().to_numpy())


def test_categoria_desconhecida_e_ignorada_sem_erro(modelo, particoes):
    x = particoes.X_test.head(1).copy()
    x["home_team"] = "Time Inexistente FC"
    prob = modelo.predict_proba(x)
    assert prob.shape == (1, 3) and np.isclose(prob.sum(), 1)

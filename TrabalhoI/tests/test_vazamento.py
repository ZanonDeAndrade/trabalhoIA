"""Provas de que a partida prevista não participa das próprias variáveis (sem vazamento)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src import data_analysis as da
from src.data_split import (
    COLUNAS_PROIBIDAS,
    CLASSES,
    carregar_e_dividir_dados,
    validar_sem_vazamento,
)

PROIBIDAS_DO_ENUNCIADO = [
    "home_team_score", "away_team_score", "gols_home", "gols_away", "yellow_cards_home", "yellow_cards_away",
    "red_cards_home", "red_cards_away", "sec_card_home", "sec_card_away", "total_gols", "total_amarelos",
    "total_expulsoes", "resultado", "resultado_codigo",
]


@pytest.mark.parametrize("coluna", PROIBIDAS_DO_ENUNCIADO)
def test_coluna_proibida_e_rejeitada(coluna):
    with pytest.raises(ValueError, match="Vazamento"):
        validar_sem_vazamento(["pontos_media_ultimos_5_mandante", coluna])


def test_atributos_do_modelo_nao_incluem_colunas_proibidas():
    p = carregar_e_dividir_dados()
    entradas = set(p.X_train.columns)
    assert not entradas & set(PROIBIDAS_DO_ENUNCIADO)
    assert not entradas & COLUNAS_PROIBIDAS
    assert not entradas & set(da.COLUNAS_PROIBIDAS_ADICIONAIS)
    assert len(entradas) == 34 and len(p.features_numericas) == 31 and len(p.features_categoricas) == 3


def _jogos_da_equipe(df: pd.DataFrame, equipe: str) -> pd.DataFrame:
    """Jogos da equipe em ordem cronológica com gols pró/contra e pontos, calculados de forma independente."""
    j = df[(df["home_team"] == equipe) | (df["away_team"] == equipe)].sort_values(["data_partida", "id_partida"])
    casa = j["home_team"] == equipe
    pro = np.where(casa, j["home_team_score"], j["away_team_score"])
    contra = np.where(casa, j["away_team_score"], j["home_team_score"])
    out = j[["id_partida", "temporada", "data_partida"]].copy()
    out["pro"], out["contra"] = pro, contra
    out["pontos"] = np.where(pro > contra, 3, np.where(pro == contra, 1, 0))
    return out


def test_medias_moveis_usam_apenas_os_cinco_jogos_anteriores(processado):
    df, _ = processado
    rng = np.random.default_rng(0)
    amostra = df[df["utilizavel_ml"] == 1].sample(40, random_state=3)
    for _, partida in amostra.iterrows():
        for lado, equipe in (("mandante", partida["home_team"]), ("visitante", partida["away_team"])):
            jogos = _jogos_da_equipe(df, equipe)
            anteriores = jogos[jogos["data_partida"] < partida["data_partida"]].tail(5)
            assert len(anteriores) == 5
            assert partida[f"pontos_media_ultimos_5_{lado}"] == pytest.approx(anteriores["pontos"].mean())
            assert partida[f"gols_marcados_media_ultimos_5_{lado}"] == pytest.approx(anteriores["pro"].mean())
            assert partida[f"gols_sofridos_media_ultimos_5_{lado}"] == pytest.approx(anteriores["contra"].mean())
            assert partida[f"aproveitamento_ultimos_5_{lado}"] == pytest.approx(anteriores["pontos"].sum() / 15)
    del rng


def test_alterar_a_propria_partida_nao_muda_suas_variaveis_mas_muda_as_seguintes(processado):
    """Trocar placar e cartões de um jogo não altera seus atributos; altera os do jogo seguinte da equipe."""
    df, _ = processado
    alvo = df[(df["utilizavel_ml"] == 1) & (df["temporada"] == 2022)].iloc[10]
    equipe = alvo["home_team"]
    modificado = df.copy()
    idx = modificado.index[modificado["id_partida"] == alvo["id_partida"]][0]
    modificado.loc[idx, ["home_team_score", "away_team_score"]] = [9, 0]
    modificado.loc[idx, ["amarelos_mandante", "expulsoes_mandante", "amarelos_visitante", "expulsoes_visitante"]] = [7, 3, 6, 2]

    recalculado = da.adicionar_historico(modificado)
    colunas = da.COLUNAS_HISTORICAS
    antes = df.loc[df["id_partida"] == alvo["id_partida"], colunas].iloc[0]
    depois = recalculado.loc[recalculado["id_partida"] == alvo["id_partida"], colunas].iloc[0]
    pd.testing.assert_series_equal(antes, depois, check_names=False)

    proximo = df[((df["home_team"] == equipe) | (df["away_team"] == equipe)) & (df["data_partida"] > alvo["data_partida"])].iloc[0]
    lado = "mandante" if proximo["home_team"] == equipe else "visitante"
    coluna = f"gols_marcados_media_ultimos_5_{lado}"
    valor_novo = recalculado.loc[recalculado["id_partida"] == proximo["id_partida"], coluna].iloc[0]
    assert valor_novo != proximo[coluna]


def test_primeiros_jogos_de_cada_equipe_ficam_sem_historico(processado):
    df, _ = processado
    for equipe in pd.concat([df["home_team"], df["away_team"]]).unique():
        primeiros = _jogos_da_equipe(df, equipe).head(5)["id_partida"]
        assert (df.loc[df["id_partida"].isin(primeiros), "utilizavel_ml"] == 0).all()


def test_divisao_e_estritamente_cronologica():
    p = carregar_e_dividir_dados()
    assert p.df_train["data_partida"].max() < p.df_val["data_partida"].min()
    assert p.df_val["data_partida"].max() < p.df_test["data_partida"].min()
    assert set(p.df_train["temporada"]) == {2020, 2021}
    assert set(p.df_val["temporada"]) == {2022}
    assert set(p.df_test["temporada"]) == {2023}
    assert (p.df_train_val["data_partida"].max() < p.df_test["data_partida"].min())
    assert len(p.X_train) == 689 and len(p.X_val) == 363 and len(p.X_test) == 362


def test_pre_processamento_e_ajustado_somente_no_treino():
    """Medianas de imputação vêm do treino (e não do teste), evitando vazamento no pré-processamento."""
    from src.modeling import construir_modelos

    p = carregar_e_dividir_dados()
    pipe = construir_modelos(p.features_numericas, p.features_categoricas)["Regressão Logística"].fit(p.X_train, p.y_train)
    imputador = pipe.named_steps["prep"].named_transformers_["num"].named_steps["imputer"]
    np.testing.assert_allclose(imputador.statistics_, p.X_train[p.features_numericas].median().to_numpy())
    assert not np.allclose(imputador.statistics_, p.X_test[p.features_numericas].median().to_numpy())


def test_alvo_so_tem_as_tres_classes():
    p = carregar_e_dividir_dados()
    for y in (p.y_train, p.y_val, p.y_test):
        assert set(y.unique()) <= {0, 1, 2}
    assert CLASSES == ["home_win", "draw", "away_win"]


def test_validacoes_internas_do_pipeline_de_dados_passam(processado, bruto_texto, bruto):
    df, aux = processado
    da.executar_validacoes(bruto, df, caminho_saida=da.CSV_PROCESSADO)
